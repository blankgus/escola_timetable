from dataclasses import dataclass, field
from typing import List, Set
import uuid

# ✅ CORREÇÃO: Horários reais por segmento
DIAS_SEMANA = ["seg", "ter", "qua", "qui", "sex"]

# Horários disponíveis por segmento
HORARIOS_EFII = [1, 2, 3, 4, 5, 6]  # 07:50-12:20 (6 períodos)
HORARIOS_EM = [1, 2, 3, 4, 5, 6, 7]  # 07:00-12:20 ou 13:10 (7 períodos)

# Mapeamento de horários reais
HORARIOS_REAIS = {
    # EF II: 07:50-12:20
    1: "07:50-08:40",
    2: "08:40-09:30", 
    3: "09:30-09:50",  # INTERVALO
    4: "09:50-10:40",
    5: "10:40-11:30",
    6: "11:30-12:20",
    
    # EM adicional: 12:20-13:10
    7: "12:20-13:10"
}

@dataclass
class Disciplina:
    nome: str
    carga_semanal: int
    tipo: str
    turmas: List[str]  # Lista de turmas específicas
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
    segmento: str = "EF_II"  # ✅ NOVO: EF_II ou EM
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

# No final do models.py, adicione:
def formatar_horario_aula(aula):
    """Formata uma aula para exibição na grade do professor"""
    return f"{aula.turma}\n{aula.disciplina}\n{aula.sala}"
