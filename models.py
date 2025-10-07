from dataclasses import dataclass, field
from typing import List, Set
import uuid

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
    disponibilidade: Set[str]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Turma:
    nome: str
    serie: str
    turno: str
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

@dataclass
class Feriado:
    data: str
    motivo: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))