from models import Aula, DIAS_SEMANA, HORARIOS_DISPONIVEIS
from collections import defaultdict
import random
import streamlit as st

class SimpleGradeHoraria:
    def __init__(self, turmas, professores, disciplinas):
        self.turmas = turmas
        self.professores = {p.nome: p for p in professores}
        self.disciplinas = {d.nome: d for d in disciplinas}
        self.dias = DIAS_SEMANA
        self.horarios = HORARIOS_DISPONIVEIS
        
        self.carga_turma = defaultdict(lambda: defaultdict(int))
        for turma in turmas:
            for nome_disc, disc in self.disciplinas.items():
                if turma.serie in disc.series:
                    self.carga_turma[turma.nome][nome_disc] = disc.carga_semanal

    def gerar_grade(self):
        aulas = []
        prof_aulas = defaultdict(list)
        turma_aulas = defaultdict(list)
        
        # Criar lista de aulas pendentes
        pendentes = []
        for turma_nome in self.carga_turma:
            for disc, carga in self.carga_turma[turma_nome].items():
                for _ in range(carga):
                    pendentes.append((turma_nome, disc))
        
        if not pendentes:
            st.warning("⚠️ Nenhuma aula pendente para alocar!")
            return aulas
        
        st.info(f"📋 Alocando {len(pendentes)} aulas...")
        
        # Embaralhar para tentativa mais aleatória
        random.shuffle(pendentes)
        
        aulas_alocadas = 0
        tentativas_maximas = 3
        
        for tentativa in range(tentativas_maximas):
            st.write(f"🔧 Tentativa {tentativa + 1} de {tentativas_maximas}...")
            
            for turma_nome, disc_nome in pendentes:
                if any(a.turma == turma_nome and a.disciplina == disc_nome for a in aulas):
                    continue  # Já alocada
                
                atribuido = False
                profs_possiveis = [p for p in self.professores.values() if disc_nome in p.disciplinas]
                
                if not profs_possiveis:
                    st.warning(f"⚠️ Nenhum professor disponível para {disc_nome} na turma {turma_nome}")
                    continue
                
                # Embaralhar professores e combinações
                random.shuffle(profs_possiveis)
                combinacoes = [(dia, h) for dia in self.dias for h in self.horarios]
                random.shuffle(combinacoes)
                
                for prof in profs_possiveis:
                    for dia, horario in combinacoes:
                        # Verificar disponibilidade do professor
                        if dia not in prof.disponibilidade:
                            continue
                        
                        # Verificar horário indisponível
                        if f"{dia}_{horario}" in prof.horarios_indisponiveis:
                            continue
                        
                        # Verificar conflitos
                        conflito = False
                        
                        # Conflito com outras aulas do professor
                        for a in prof_aulas[prof.nome]:
                            if a.dia == dia and a.horario == horario:
                                conflito = True
                                break
                        
                        if conflito:
                            continue
                        
                        # Conflito com outras aulas da turma
                        for a in turma_aulas[turma_nome]:
                            if a.dia == dia and a.horario == horario:
                                conflito = True
                                break
                        
                        if not conflito:
                            # Encontrar sala disponível (simplificado)
                            sala_nome = "Sala 1"
                            grupo_turma = next((t.grupo for t in self.turmas if t.nome == turma_nome), "A")
                            
                            aula = Aula(turma_nome, disc_nome, prof.nome, dia, horario, sala_nome, grupo_turma)
                            aulas.append(aula)
                            prof_aulas[prof.nome].append(aula)
                            turma_aulas[turma_nome].append(aula)
                            aulas_alocadas += 1
                            atribuido = True
                            break
                    
                    if atribuido:
                        break
            
            # Verificar se todas as aulas foram alocadas
            if len(aulas) == len(pendentes):
                st.success(f"✅ Todas as {len(aulas)} aulas alocadas com sucesso!")
                break
            else:
                st.warning(f"⚠️ Tentativa {tentativa + 1}: {len(aulas)}/{len(pendentes)} aulas alocadas")
                
                # Limpar e tentar novamente
                if tentativa < tentativas_maximas - 1:
                    aulas = []
                    prof_aulas = defaultdict(list)
                    turma_aulas = defaultdict(list)
                    aulas_alocadas = 0
        
        st.info(f"📊 Resultado final: {len(aulas)}/{len(pendentes)} aulas alocadas")
        return aulas