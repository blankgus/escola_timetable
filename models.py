from dataclasses import dataclass, field
from typing import List, Set
import uuid

DIAS_SEMANA = ["seg", "ter", "qua", "qui", "sex"]

@dataclass
class Disciplina:
    nome: str
    carga_semanal: int
    tipo: str
    series: List[str]
    grupo: str = "A"  # ✅ NOVO: "A" ou "B"
    cor_fundo: str = "#4A90E2"
    cor_fonte: str = "#FFFFFF"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Professor:
    nome: str
    disciplinas: List[str]
    disponibilidade: Set[str]  # dias da semana
    grupo: str = "A"  # ✅ NOVO: "A" ou "B" ou "AMBOS"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Turma:
    nome: str
    serie: str
    turno: str
    grupo: str = "A"  # ✅ NOVO: "A" ou "B"
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
    grupo: str = "A"  # ✅ NOVO: "A" ou "B"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Feriado:
    data: str
    motivo: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))