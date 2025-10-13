# models.py
from dataclasses import dataclass, field
from typing import List, Set
import uuid

DIAS_SEMANA = ["dom", "seg", "ter", "qua", "qui", "sex", "sab"]

@dataclass
class DisciplinaTurma:
    """Representa uma disciplina alocada para uma turma específica."""
    nome: str              # Nome da disciplina
    carga_semanal: int     # Quantas aulas por semana
    professor: str         # Nome do professor responsável
    professor_fixo: bool = False  # Se o professor é fixo para esta disciplina na turma
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Disciplina:
    nome: str
    carga_semanal: int
    tipo: str
    series: List[str]
    cor_fundo: str = "#4A90E2"
    cor_fonte: str = "#FFFFFF"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Professor:
    nome: str
    disciplinas: List[str]
    disponibilidade_dias: Set[str]  # Dias disponíveis
    disponibilidade_horarios: Set[int]  # Horários disponíveis
    horarios_indisponiveis: Set[str] = field(default_factory=set)  # Ex: {"seg_1", "qua_3"}
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Turma:
    nome: str
    serie: str
    turno: str
    disciplinas_turma: List[DisciplinaTurma] = field(default_factory=list)
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
    id: str = field(default_factory=lambda: str(uuid.uuid4()))