import random
from models import Aula
import streamlit as st

class SimpleGradeHoraria:
    def __init__(self, turmas, professores, disciplinas):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = disciplinas
        self.aulas_alocadas = []
        
    def obter_grupo_seguro(self, objeto):
        try:
            if hasattr(objeto, 'grupo'):
                grupo = objeto.grupo
                if grupo in ["A", "B", "AMBOS"]:
                    return grupo
            return "A"
        except:
            return "A"
    
    def gerar_grade(self):
        """Gera uma grade horária semanal tradicional"""
        self.aulas_alocadas = []
        
        # Dias da semana (segunda a sexta) - ✅ FORMATO COMPLETO
        dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
        # Horários disponíveis (8 horários)
        horarios = [1, 2, 3, 4, 5, 6, 7, 8]
        
        st.info(f"📋 Gerando grade semanal para {len(self.turmas)} turmas...")
        
        progress_bar = st.progress(0)
        total_aulas_alocadas = 0
        
        # Para cada turma, criar grade semanal
        for idx, turma in enumerate(self.turmas):
            grupo_turma = self.obter_grupo_seguro(turma)
            
            # CORREÇÃO: Filtrar disciplinas APENAS do MESMO GRUPO
            disciplinas_turma = []
            disciplinas_info = []  # Para debug
            
            for disc in self.disciplinas:
                disc_grupo = self.obter_grupo_seguro(disc)
                # SÓ inclui disciplinas do MESMO grupo e série correta
                if turma.serie in disc.series and disc_grupo == grupo_turma:
                    # Adiciona a disciplina repetidas vezes conforme carga semanal
                    for i in range(disc.carga_semanal):
                        disciplinas_turma.append(disc)
                        disciplinas_info.append(f"{disc.nome} ({i+1}/{disc.carga_semanal})")
            
            st.write(f"**Turma {turma.nome}**: {len(disciplinas_turma)} aulas a alocar")
            if disciplinas_info:
                st.write(f"Disciplinas: {', '.join(set([d.nome for d in disciplinas_turma]))}")
            
            if not disciplinas_turma:
                st.warning(f"⚠️ Turma {turma.nome} [{grupo_turma}] não tem disciplinas do seu grupo")
                progress_bar.progress((idx + 1) / len(self.turmas))
                continue
            
            # Embaralhar disciplinas para distribuição
            random.shuffle(disciplinas_turma)
            
            # Alocar aulas para esta turma
            aulas_turma = self._alocar_turma_semanal(turma, disciplinas_turma, dias, horarios, grupo_turma)
            self.aulas_alocadas.extend(aulas_turma)
            total_aulas_alocadas += len(aulas_turma)
            
            st.write(f"✅ {len(aulas_turma)} aulas alocadas para {turma.nome}")
            progress_bar.progress((idx + 1) / len(self.turmas))
        
        st.success(f"✅ Grade gerada com {total_aulas_alocadas} aulas no total!")
        return self.aulas_alocadas
    
    def _alocar_turma_semanal(self, turma, disciplinas_turma, dias, horarios, grupo_turma):
        """Aloca aulas para uma turma na semana toda"""
        aulas_turma = []
        disciplinas_restantes = disciplinas_turma.copy()
        
        # Criar matriz de horários ocupados
        horarios_ocupados = set()
        
        # Tentativa 1: Alocar de forma sequencial
        for dia in dias:
            for horario in horarios:
                if not disciplinas_restantes:
                    break
                
                # Verificar se este horário já está ocupado
                slot_key = f"{turma.nome}_{dia}_{horario}"
                if slot_key in horarios_ocupados:
                    continue
                
                # Pegar próxima disciplina
                disciplina = disciplinas_restantes[0]
                
                # VERIFICAÇÃO DE SEGURANÇA: garantir que é do mesmo grupo
                disc_grupo = self.obter_grupo_seguro(disciplina)
                if disc_grupo != grupo_turma:
                    st.error(f"❌ ERRO: Disciplina {disciplina.nome} [{disc_grupo}] para turma {turma.nome} [{grupo_turma}]")
                    disciplinas_restantes.pop(0)
                    continue
                
                # Encontrar professor compatível
                professor = self._encontrar_professor_compativel(disciplina.nome, dia, horario, grupo_turma)
                
                if professor:
                    sala = self._encontrar_sala_disponivel(dia, horario)
                    
                    aula = Aula(
                        turma=turma.nome,
                        disciplina=disciplina.nome,
                        professor=professor.nome,
                        dia=dia,
                        horario=horario,
                        sala=sala,
                        grupo=grupo_turma
                    )
                    
                    aulas_turma.append(aula)
                    horarios_ocupados.add(slot_key)
                    disciplinas_restantes.pop(0)
        
        # Tentativa 2: Se ainda há disciplinas restantes, tentar alocar em slots livres
        tentativas_extras = 0
        while disciplinas_restantes and tentativas_extras < 100:  # Limite de segurança
            tentativas_extras += 1
            for dia in dias:
                for horario in horarios:
                    if not disciplinas_restantes:
                        break
                    
                    slot_key = f"{turma.nome}_{dia}_{horario}"
                    if slot_key in horarios_ocupados:
                        continue
                    
                    # Tentar com a primeira disciplina disponível
                    disciplina = disciplinas_restantes[0]
                    professor = self._encontrar_professor_compativel(disciplina.nome, dia, horario, grupo_turma)
                    
                    if professor:
                        sala = self._encontrar_sala_disponivel(dia, horario)
                        
                        aula = Aula(
                            turma=turma.nome,
                            disciplina=disciplina.nome,
                            professor=professor.nome,
                            dia=dia,
                            horario=horario,
                            sala=sala,
                            grupo=grupo_turma
                        )
                        
                        aulas_turma.append(aula)
                        horarios_ocupados.add(slot_key)
                        disciplinas_restantes.pop(0)
        
        if disciplinas_restantes:
            st.warning(f"⚠️ Não foi possível alocar {len(disciplinas_restantes)} aulas para {turma.nome}")
            st.write(f"Disciplinas não alocadas: {[d.nome for d in disciplinas_restantes]}")
        
        return aulas_turma
    
    def _encontrar_professor_compativel(self, disciplina_nome, dia, horario, grupo_turma):
        """Encontra professor que atende TODOS os critérios"""
        professores_candidatos = []
        
        for professor in self.professores:
            professor_grupo = self.obter_grupo_seguro(professor)
            
            # CRITÉRIOS DE COMPATIBILIDADE:
            # 1. Professor deve ministrar a disciplina
            if disciplina_nome not in professor.disciplinas:
                continue
            
            # 2. Professor deve estar disponível no dia (formato completo)
            if dia not in professor.disponibilidade:
                continue
            
            # 3. Professor não pode ter horário indisponível
            if f"{dia}_{horario}" in professor.horarios_indisponiveis:
                continue
            
            # 4. Professor deve ser do MESMO grupo ou AMBOS
            if professor_grupo not in [grupo_turma, "AMBOS"]:
                continue
            
            professores_candidatos.append(professor)
        
        if professores_candidatos:
            # Ordenar por quantidade de aulas já atribuídas (para distribuir carga)
            professores_ordenados = sorted(professores_candidatos, 
                                         key=lambda p: len([a for a in self.aulas_alocadas if a.professor == p.nome]))
            return professores_ordenados[0]
        
        # DEBUG: Mostrar por que não encontrou professor
        st.warning(f"❌ Nenhum professor encontrado para {disciplina_nome} no {dia} {horario}º (Grupo {grupo_turma})")
        return None
    
    def _encontrar_sala_disponivel(self, dia, horario):
        """Encontra uma sala disponível (implementação simples)"""
        # Implementação básica - sempre retorna Sala 1
        # Em uma versão mais avançada, verificaria conflitos de sala
        return "Sala 1"