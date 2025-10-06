from dataclasses import dataclass, field
from typing import List, Set
import hashlib

@dataclass
class Disciplina:
    nome: str
    carga_semanal: int
    tipo: str
    series: List[str]
    cor: str = field(init=False)
    
    def __post_init__(self):
        hash_obj = hashlib.md5(self.nome.encode())
        hex_color = hash_obj.hexdigest()[:6]
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        if (r*0.299 + g*0.587 + b*0.114) > 186:
            self.cor = f"#{max(0, r-50):02x}{max(0, g-50):02x}{max(0, b-50):02x}"
        else:
            self.cor = f"#{hex_color}"

@dataclass
class Professor:
    nome: str
    disciplinas: List[str]
    disponibilidade: Set[str]

@dataclass
class Turma:
    nome: str
    serie: str
    turno: str

@dataclass
class Sala:
    nome: str
    capacidade: int = 30
    tipo: str = "normal"

@dataclass
class Aula:
    turma: str
    disciplina: str
    professor: str
    dia: str
    horario: int
