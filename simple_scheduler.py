import random
from models import Aula, HORARIOS_REAIS
import streamlit as st

class SimpleGradeHoraria:
    def __init__(self, turmas, professores, disciplinas, dias_em_estendido=None):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = disciplinas
        self.dias_em_estendido = dias_em_estendido or []
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
    
    def obter_segmento_turma(self, turma_nome):
        """Determina o segmento da turma baseado no nome"""
        if 'em' in turma_nome.lower():
            return "EM"
        else:
            return "EF_II"
    
    def obter_horarios_turma(self, turma_nome, dia):
        """Retorna os horários disponíveis para a turma considerando o dia"""
        segmento = self.obter_segmento_turma(turma_nome)
        
        if segmento == "EM":
            # EM: 7 períodos, mas pode variar por dia
            if dia in self.dias_em_estendido:
                return [1, 2, 3, 4, 5, 6, 7]  # Até 13:10
            else:
                return [1, 2, 3, 4, 5, 6]  # Até 12:20
        else:
            # EF II: sempre 6 períodos (07:50-12:20)
            return [1, 2, 3, 4, 5, 6]
    
    def gerar_grade(self):
        """Gera uma grade horária semanal tradicional respeitando horários reais"""
        self.aulas_alocadas = []
        
        # Dias da semana (segunda a sexta) - ✅ FORMATO COMPLETO
        dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
        
        st.info(f"📋 Gerando grade semanal para {len(self.turmas)} turmas...")
        st.info(f"📅 Dias EM estendido: {self.dias_em_estendido}")
        
        progress_bar = st.progress(0)
        total_aulas_alocadas = 0
        
        # Para cada turma, criar grade semanal
        for idx, turma in enumerate(self.turmas):
            grupo_turma = self.obter_grupo_seguro(turma)
            segmento = self.obter_segmento_turma(turma.nome)
            
            # ✅ CORREÇÃO: Filtrar disciplinas pela TURMA ESPECÍFICA
            disciplinas_turma = []
            disciplinas_info = []  # Para debug
            
            for disc in self.disciplinas:
                disc_grupo = self.obter_grupo_seguro(disc)
                # ✅ AGORA: Verifica se a disciplina está vinculada a ESTA turma específica
                if turma.nome in disc.turmas and disc_grupo == grupo_turma:
                    # Adiciona a disciplina repetidas vezes conforme carga semanal
                    for i in range(disc.carga_semanal):
                        disciplinas_turma.append(disc)
                        disciplinas_info.append(f"{disc.nome} ({i+1}/{disc.carga_semanal})")
            
            st.write(f"**Turma {turma.nome}** ({segmento}): {len(disciplinas_turma)} aulas a alocar")
            if disciplinas_info:
                disciplinas_unicas = list(set([d.nome for d in disciplinas_turma]))
                st.write(f"Disciplinas: {', '.join(disciplinas_unicas)}")
            
            if not disciplinas_turma:
                st.warning(f"⚠️ Turma {turma.nome} não tem disciplinas vinculadas")
                progress_bar.progress((idx + 1) / len(self.turmas))
                continue
            
            # Embaralhar disciplinas para distribuição
            random.shuffle(disciplinas_turma)
            
            # Alocar aulas para esta turma
            aulas_turma = self._alocar_turma_semanal(turma, disciplinas_turma, dias, grupo_turma)
            self.aulas_alocadas.extend(aulas_turma)
            total_aulas_alocadas += len(aulas_turma)
            
            st.write(f"✅ {len(aulas_turma)} aulas alocadas para {turma.nome}")
            progress_bar.progress((idx + 1) / len(self.turmas))
        
        st.success(f"✅ Grade gerada com {total_aulas_alocadas} aulas no total!")
        return self.aulas_alocadas
    
    def _alocar_turma_semanal(self, turma, disciplinas_turma, dias, grupo_turma):
        """Aloca aulas para uma turma na semana toda"""
        aulas_turma = []
        disciplinas_restantes = disciplinas_turma.copy()
        
        # Criar matriz de horários ocupados
        horarios_ocupados = set()
        
        # Tentativa 1: Alocar de forma sequencial por dia e horário
        for dia in dias:
            # Obter horários disponíveis para este dia específico
            horarios_disponiveis = self.obter_horarios_turma(turma.nome, dia)
            
            for horario in horarios_disponiveis:
                if not disciplinas_restantes:
                    break
                
                # Verificar se este horário já está ocupado
                slot_key = f"{turma.nome}_{dia}_{horario}"
                if slot_key in horarios_ocupados:
                    continue
                
                # Pular horário de intervalo
                if self._eh_horario_intervalo(turma.nome, horario):
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
                horarios_disponiveis = self.obter_horarios_turma(turma.nome, dia)
                
                for horario in horarios_disponiveis:
                    if not disciplinas_restantes:
                        break
                    
                    slot_key = f"{turma.nome}_{dia}_{horario}"
                    if slot_key in horarios_ocupados:
                        continue
                    
                    # Pular horário de intervalo
                    if self._eh_horario_intervalo(turma.nome, horario):
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
                        break  # Sair do loop interno quando alocar
        
        if disciplinas_restantes:
            st.warning(f"⚠️ Não foi possível alocar {len(disciplinas_restantes)} aulas para {turma.nome}")
            st.write(f"Disciplinas não alocadas: {[d.nome for d in disciplinas_restantes]}")
        
        return aulas_turma
    
    def _eh_horario_intervalo(self, turma_nome, horario):
        """Verifica se o horário é de intervalo"""
        segmento = self.obter_segmento_turma(turma_nome)
        
        if segmento == "EF_II":
            return horario == 3  # EF II: intervalo no 3º horário
        else:
            return horario == 4  # EM: intervalo no 4º horário
    
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
            
            # ✅ CORREÇÃO CRÍTICA: Professor deve ser do MESMO grupo ou AMBOS
            if professor_grupo not in [grupo_turma, "AMBOS"]:
                continue
            
            professores_candidatos.append(professor)
        
        if professores_candidatos:
            # Ordenar por quantidade de aulas já atribuídas (para distribuir carga)
            professores_ordenados = sorted(professores_candidatos, 
                                         key=lambda p: len([a for a in self.aulas_alocadas if a.professor == p.nome]))
            return professores_ordenados[0]
        
        # DEBUG: Mostrar por que não encontrou professor
        st.warning(f"❌ Nenhum professor encontrado para {disciplina_nome} no {dia} {horario}º")
        st.write(f"  - Grupo necessário: {grupo_turma}")
        st.write(f"  - Professores que ministram {disciplina_nome}: {[p.nome for p in self.professores if disciplina_nome in p.disciplinas]}")
        st.write(f"  - Grupos desses professores: {[self.obter_grupo_seguro(p) for p in self.professores if disciplina_nome in p.disciplinas]}")
        return None
    
    def _encontrar_sala_disponivel(self, dia, horario):
        """Encontra uma sala disponível (implementação simples)"""
        # Implementação básica - sempre retorna Sala 1
        # Em uma versão mais avançada, verificaria conflitos de sala
        return "Sala 1"