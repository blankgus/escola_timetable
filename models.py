"""
Modelos de dados para o sistema de grade horária
"""

import uuid
from typing import List, Set, Dict, Any

# Constantes
DIAS_SEMANA = ["seg", "ter", "qua", "qui", "sex"]

# Horários disponíveis por segmento
HORARIOS_EFII = [1, 2, 3, 4, 5, 6]  # EF II: 6 aulas + intervalo no 3º horário
HORARIOS_EM = [1, 2, 3, 4, 5, 6, 7]  # EM: 7 aulas + intervalo no 4º horário

# Horários reais formatados
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
    
    def __repr__(self):
        return f"Turma({self.nome}, {self.serie}, {self.grupo})"

class Professor:
    def __init__(self, nome: str, disciplinas: List[str], disponibilidade: Set[str], 
                 grupo: str = "AMBOS", horarios_indisponiveis: Set[str] = None):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.disciplinas = disciplinas
        self.disponibilidade = disponibilidade
        self.grupo = grupo
        self.horarios_indisponiveis = horarios_indisponiveis or set()
    
    def __repr__(self):
        return f"Professor({self.nome}, {self.disciplinas}, {self.grupo})"

class Disciplina:
    def __init__(self, nome: str, carga_semanal: int, tipo: str, turmas: List[str], 
                 grupo: str, cor_fundo: str = "#4A90E2", cor_fonte: str = "#FFFFFF"):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.carga_semanal = carga_semanal
        self.tipo = tipo  # pesada, media, leve, pratica
        self.turmas = turmas
        self.grupo = grupo
        self.cor_fundo = cor_fundo
        self.cor_fonte = cor_fonte
    
    def __repr__(self):
        return f"Disciplina({self.nome}, {self.carga_semanal}h, {self.grupo})"

class Sala:
    def __init__(self, nome: str, capacidade: int, tipo: str = "normal"):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.capacidade = capacidade
        self.tipo = tipo  # normal, laboratorio, auditorio
    
    def __repr__(self):
        return f"Sala({self.nome}, {self.capacidade}, {self.tipo})"