from dataclasses import dataclass, field
from typing import List, Set
import uuid

DIAS_SEMANA = ["seg", "ter", "qua", "qui", "sex"]

# ✅ CORREÇÃO: Horários separados por segmento
HORARIOS_EFII = [1, 2, 3, 4, 5, 6]  # EF II: 6 períodos (07:50-12:20)
HORARIOS_EM = [1, 2, 3, 4, 5, 6, 7, 8]  # EM: 8 períodos (07:00-13:10)

# ✅ CORREÇÃO: Horários reais separados
HORARIOS_REAIS_EFII = {
    1: "07:50-08:40",
    2: "08:40-09:30", 
    3: "09:30-09:50",  # INTERVALO
    4: "09:50-10:40",
    5: "10:40-11:30",
    6: "11:30-12:20"
}

HORARIOS_REAIS_EM = {
    1: "07:00-07:50",
    2: "07:50-08:40", 
    3: "08:40-09:30",
    4: "09:30-09:50",  # INTERVALO
    5: "09:50-10:40",
    6: "10:40-11:30",
    7: "11:30-12:20",
    8: "12:20-13:10"
}

def obter_horarios_reais(segmento):
    """Retorna horários reais baseado no segmento"""
    if segmento == "EM":
        return HORARIOS_REAIS_EM
    else:
        return HORARIOS_REAIS_EFII

@dataclass
class Disciplina:
    nome: str
    carga_semanal: int
    tipo: str
    turmas: List[str]
    grupo: str = "A"
    cor_fundo: str = "#4A90E2"
    cor_fonte: str = "#FFFFFF"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Professor:
    nome: str
    disciplinas: List[str]
    disponibilidade: Set[str]
    grupo: str = "A"
    horarios_indisponiveis: Set[str] = field(default_factory=set)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Turma:
    nome: str
    serie: str
    turno: str
    grupo: str = "A"
    segmento: str = "EF_II"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Sala:
    nome: str
    capacidade: int = 30
    tipo: str = "normal"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Aula:
    turma: str
    disciplina: str
    professor: str
    dia: str
    horario: int
    sala: str = "Sala 1"
    grupo: str = "A"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))