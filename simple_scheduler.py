"""
Algoritmo simples de geração de grade horária
"""

import random
from models import DIAS_SEMANA, HORARIOS_EFII, HORARIOS_EM
import streamlit as st

class SimpleGradeHoraria:
    def __init__(self, turmas, professores, disciplinas, salas):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = disciplinas
        self.salas = salas
        self.grade = {}
        self.info_grade = {}
        
    def gerar_grade(self):
        """Gera grade horária usando algoritmo simples"""
        try:
            self._inicializar_grade()
            return self._alocar_aulas()
        except Exception as e:
            return False, f"Erro no algoritmo simples: {str(e)}"
    
    def _inicializar_grade(self):
        """Inicializa estrutura vazia da grade"""
        self.grade = {}
        for turma in self.turmas:
            self.grade[turma.nome] = {}
            for dia in DIAS_SEMANA:
                self.grade[turma.nome][dia] = {}
                # Usar os horários CORRETOS da turma
                horarios = turma.get_horarios()
                for horario in horarios:
                    self.grade[turma.nome][dia][horario] = {}
    
    def _alocar_aulas(self):
        """Aloca aulas na grade respeitando horários corretos"""
        try:
            # Para cada turma, criar uma grade básica
            for turma in self.turmas:
                turma_nome = turma.nome
                grupo_turma = turma.grupo
                
                # Obter disciplinas desta turma
                disciplinas_turma = []
                for disc in self.disciplinas:
                    if turma_nome in disc.turmas and disc.grupo == grupo_turma:
                        disciplinas_turma.extend([disc] * disc.carga_semanal)
                
                if not disciplinas_turma:
                    st.warning(f"⚠️ Nenhuma disciplina para {turma_nome} [{grupo_turma}]")
                    continue
                
                # Embaralhar disciplinas para distribuição aleatória
                random.shuffle(disciplinas_turma)
                
                # Usar horários CORRETOS da turma
                horarios = turma.get_horarios()
                dias_disponiveis = DIAS_SEMANA.copy()
                
                idx_disciplina = 0
                for dia in dias_disponiveis:
                    for horario in horarios:
                        if idx_disciplina >= len(disciplinas_turma):
                            break
                            
                        disc = disciplinas_turma[idx_disciplina]
                        
                        # Encontrar professor para esta disciplina
                        professor = self._encontrar_professor(disc.nome, grupo_turma, dia, horario)
                        sala = self._encontrar_sala(disc.tipo)
                        
                        if professor and sala:
                            aula = {
                                'disciplina': disc.nome,
                                'professor': professor,
                                'sala': sala,
                                'turma': turma_nome,
                                'dia': dia,
                                'horario': horario,
                                'cor': disc.cor_fundo,
                                'cor_fonte': disc.cor_fonte
                            }
                            
                            self.grade[turma_nome][dia][horario] = aula
                            idx_disciplina += 1
                    
                    if idx_disciplina >= len(disciplinas_turma):
                        break
            
            self.info_grade = {
                'status': 'SUCESSO',
                'mensagem': f'Grade gerada para {len(self.turmas)} turmas',
                'turmas_processadas': len(self.turmas)
            }
            
            return True, "Grade gerada com sucesso (algoritmo simples)"
            
        except Exception as e:
            return False, f"Erro ao alocar aulas: {str(e)}"
    
    def _encontrar_professor(self, disciplina_nome, grupo_turma, dia, horario):
        """Encontra professor disponível para a disciplina"""
        professores_candidatos = []
        
        for prof in self.professores:
            # Verificar se professor ministra esta disciplina
            if disciplina_nome not in prof.disciplinas:
                continue
            
            # Verificar compatibilidade de grupo
            if prof.grupo != "AMBOS" and prof.grupo != grupo_turma:
                continue
            
            # Verificar disponibilidade no dia
            dia_completo = self._converter_dia_para_completo(dia)
            if dia_completo not in prof.disponibilidade:
                continue
            
            # Verificar se horário não é indisponível
            chave_horario = f"{dia}_{horario}"
            if chave_horario in prof.horarios_indisponiveis:
                continue
            
            professores_candidatos.append(prof.nome)
        
        return random.choice(professores_candidatos) if professores_candidatos else "Professor Não Encontrado"
    
    def _encontrar_sala(self, tipo_disciplina):
        """Encontra sala disponível"""
        salas_candidatas = []
        
        for sala in self.salas:
            # Verificar compatibilidade de tipo
            if tipo_disciplina == "pratica" and sala.tipo != "laboratorio":
                continue
                
            salas_candidatas.append(sala.nome)
        
        return random.choice(salas_candidatas) if salas_candidatas else "Sala Não Encontrada"
    
    def _converter_dia_para_completo(self, dia):
        """Converte dia abreviado para completo"""
        conversao = {
            "seg": "segunda",
            "ter": "terca", 
            "qua": "quarta",
            "qui": "quinta",
            "sex": "sexta"
        }
        return conversao.get(dia, dia)
