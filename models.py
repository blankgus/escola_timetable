"""
Modelos de dados para o sistema de grade horária
"""

import uuid
from typing import List, Set, Dict, Any
from dataclasses import dataclass

# Constantes
DIAS_SEMANA = ["seg", "ter", "qua", "qui", "sex"]

# Horários disponíveis por segmento - CORRIGIDO
HORARIOS_EFII = [1, 2, 3, 4, 5]  # EF II: 5 aulas + intervalo (25h semanais)
HORARIOS_EM = [1, 2, 3, 4, 5, 6, 7]  # EM: 7 aulas + intervalo (35h semanais)

# Horários reais formatados - CORRIGIDO
HORARIOS_REAIS_EFII = {
    1: "07:50 - 08:40",
    2: "08:40 - 09:30", 
    3: "09:30 - 09:50 (Intervalo)",
    4: "09:50 - 10:40",
    5: "10:40 - 11:30",
    6: "11:30 - 12:20"
}

HORARIOS_REAIS_EM = {
    1: "07:00 - 07:50",
    2: "07:50 - 08:40",
    3: "08:40 - 09:30",
    4: "09:30 - 09:50 (Intervalo)",
    5: "09:50 - 10:40", 
    6: "10:40 - 11:30",
    7: "11:30 - 12:20",
    8: "12:20 - 13:10"
}

def obter_horarios_reais(segmento):
    """Retorna os horários reais baseado no segmento"""
    if segmento == "EM":
        return HORARIOS_REAIS_EM
    else:
        return HORARIOS_REAIS_EFII

def obter_horarios_disponiveis(segmento):
    """Retorna os horários disponíveis baseado no segmento"""
    if segmento == "EM":
        return HORARIOS_EM
    else:
        return HORARIOS_EFII

@dataclass
class Aula:
    """Representa uma aula alocada na grade horária"""
    disciplina: str
    professor: str
    sala: str
    turma: str
    dia: str
    horario: int
    cor_fundo: str = "#4A90E2"
    cor_fonte: str = "#FFFFFF"
    
    def to_dict(self):
        return {
            'disciplina': self.disciplina,
            'professor': self.professor,
            'sala': self.sala,
            'turma': self.turma,
            'dia': self.dia,
            'horario': self.horario,
            'cor': self.cor_fundo,
            'cor_fonte': self.cor_fonte
        }

class Turma:
    def __init__(self, nome: str, serie: str, turno: str, grupo: str, segmento: str = None):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.serie = serie
        self.turno = turno
        self.grupo = grupo
        self.segmento = segmento or self._determinar_segmento()
    
    def _determinar_segmento(self):
        """Determina o segmento baseado na série"""
        if 'em' in self.serie.lower() or 'medio' in self.serie.lower():
            return "EM"
        else:
            return "EF_II"
    
    def get_horarios(self):
        """Retorna os horários disponíveis para esta turma"""
        if self.segmento == "EM":
            return HORARIOS_EM
        else:
            return HORARIOS_EFII
    
    def get_horario_real(self, horario):
        """Retorna o horário real formatado"""
        if self.segmento == "EM":
            return HORARIOS_REAIS_EM.get(horario, f"Horário {horario}")
        else:
            return HORARIOS_REAIS_EFII.get(horario, f"Horário {horario}")
    
    def get_carga_maxima(self):
        """Retorna a carga horária máxima semanal"""
        if self.segmento == "EM":
            return 35  # 7 horas por dia × 5 dias = 35 horas
        else:
            return 25  # 5 horas por dia × 5 dias = 25 horas
    
    def __repr__(self):
        return f"Turma({self.nome}, {self.serie}, {self.grupo}, {self.segmento})"

# Restante do código permanece igual...
