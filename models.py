from dataclasses import dataclass, field
from typing import List, Set
import uuid
from neuro_rules import HORARIOS_NEURO

DIAS_SEMANA = ["seg", "ter", "qua", "qui", "sex"]

# ✅ CORREÇÃO: Horários baseados nas regras neuro
HORARIOS_EFII = list(range(1, HORARIOS_NEURO['EF_II']['total_periodos'] + 1))
HORARIOS_EM = list(range(1, HORARIOS_NEURO['EM']['total_periodos'] + 1))

# Mapeamento de horários reais
HORARIOS_REAIS = {
    # EM: 07:00-13:10 (7 períodos)
    1: "07:00-07:50",
    2: "07:50-08:40",
    3: "08:40-09:30", 
    4: "09:30-09:50",  # INTERVALO
    5: "09:50-10:40",
    6: "10:40-11:30",
    7: "11:30-12:20",
    8: "12:20-13:10",
    
    # EF II: 07:50-12:20 (6 períodos) - usando os mesmos números mas diferentes horários
    # O sistema ajusta automaticamente baseado no segmento
}

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