"""
Regras e configurações específicas para a escola Neuro - DADOS REAIS
"""

import json
import os
from models import Turma, Professor, Disciplina, Sala

# Configurações de professores neuro - DADOS REAIS
PROFESSORES_NEURO = {
    "Heliana": {
        "disciplinas": ["Português A", "Português B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Deise": {
        "disciplinas": ["Português A", "Português B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Loide": {
        "disciplinas": ["Português A", "Português B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Tatiane": {
        "disciplinas": ["Matemática A", "Matemática B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Ricardo": {
        "disciplinas": ["Matemática A", "Matemática B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Laís": {
        "disciplinas": ["História A", "História B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Waldemar": {
        "disciplinas": ["História A", "História B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Rene": {
        "disciplinas": ["Geografia A", "Geografia B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Vladmir": {
        "disciplinas": ["Química A", "Química B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Zabuor": {
        "disciplinas": ["Química A", "Química B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Gisele": {
        "disciplinas": ["Geografia A", "Geografia B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Marina": {
        "disciplinas": ["Biologia A", "Biologia B", "Ciências A", "Ciências B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "César": {
        "disciplinas": ["Informática A", "Informática B", "Física A", "Física B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Anna Maria": {
        "disciplinas": ["Filosofia A", "Filosofia B", "Sociologia A", "Sociologia B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Marcão": {
        "disciplinas": ["Educação Física A", "Educação Física B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Andréia": {
        "disciplinas": ["Educação Física A", "Educação Física B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Vanessa": {
        "disciplinas": ["Arte A", "Arte B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Maria Luiza": {
        "disciplinas": ["Inglês A", "Inglês B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Andréia Barreto": {
        "disciplinas": ["Dinâmica A", "Dinâmica B", "Vida Pratica A", "Vida Pratica B"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    }
}

# Configurações de salas neuro - DADOS REAIS
SALAS_NEURO = [
    {"nome": "Sala 1", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 2", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 3", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 4", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 5", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 6", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 7", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 8", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 9", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 10", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 11", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 12", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 13", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 14", "capacidade": 30, "tipo": "normal"},
    {"nome": "Laboratório de Ciências", "capacidade": 25, "tipo": "laboratório"},
    {"nome": "Auditório", "capacidade": 100, "tipo": "auditório"}
]

# Turmas padrão neuro - DADOS REAIS
TURMAS_NEURO = [
    {"nome": "6anoA", "serie": "6ano", "turno": "manha", "grupo": "A", "segmento": "EF_II"},
    {"nome": "7anoA", "serie": "7ano", "turno": "manha", "grupo": "A", "segmento": "EF_II"},
    {"nome": "8anoA", "serie": "8ano", "turno": "manha", "grupo": "A", "segmento": "EF_II"},
    {"nome": "9anoA", "serie": "9ano", "turno": "manha", "grupo": "A", "segmento": "EF_II"},
    {"nome": "1emA", "serie": "1em", "turno": "manha", "grupo": "A", "segmento": "EM"},
    {"nome": "2emA", "serie": "2em", "turno": "manha", "grupo": "A", "segmento": "EM"},
    {"nome": "3emA", "serie": "3em", "turno": "manha", "grupo": "A", "segmento": "EM"},
    {"nome": "6anoB", "serie": "6ano", "turno": "manha", "grupo": "B", "segmento": "EF_II"},
    {"nome": "7anoB", "serie": "7ano", "turno": "manha", "grupo": "B", "segmento": "EF_II"},
    {"nome": "8anoB", "serie": "8ano", "turno": "manha", "grupo": "B", "segmento": "EF_II"},
    {"nome": "9anoB", "serie": "9ano", "turno": "manha", "grupo": "B", "segmento": "EF_II"},
    {"nome": "1emB", "serie": "1em", "turno": "manha", "grupo": "B", "segmento": "EM"},
    {"nome": "2emB", "serie": "2em", "turno": "manha", "grupo": "B", "segmento": "EM"},
    {"nome": "3emB", "serie": "3em", "turno": "manha", "grupo": "B", "segmento": "EM"}
]

# Disciplinas por série - DADOS REAIS
def obter_disciplinas_por_serie(serie, grupo):
    """
    Retorna as disciplinas padrão para cada série com cargas horárias reais
    """
    disciplinas_base = {
        "6ano": [
            {"nome": f"Português {grupo}", "carga": 5, "tipo": "pesada"},
            {"nome": f"Matemática {grupo}", "carga": 4, "tipo": "pesada"},
            {"nome": f"História {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Geografia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Ciências {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Inglês {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Arte {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Educação Física {grupo}", "carga": 2, "tipo": "pratica"},
            {"nome": f"Informática {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Dinâmica {grupo}", "carga": 1, "tipo": "leve"},
            {"nome": f"Vida Pratica {grupo}", "carga": 1, "tipo": "leve"}
        ],
        "7ano": [
            {"nome": f"Português {grupo}", "carga": 5, "tipo": "pesada"},
            {"nome": f"Matemática {grupo}", "carga": 4, "tipo": "pesada"},
            {"nome": f"História {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Geografia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Ciências {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Inglês {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Arte {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Educação Física {grupo}", "carga": 2, "tipo": "pratica"},
            {"nome": f"Informática {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Dinâmica {grupo}", "carga": 1, "tipo": "leve"},
            {"nome": f"Vida Pratica {grupo}", "carga": 1, "tipo": "leve"}
        ],
        "8ano": [
            {"nome": f"Português {grupo}", "carga": 5, "tipo": "pesada"},
            {"nome": f"Matemática {grupo}", "carga": 4, "tipo": "pesada"},
            {"nome": f"História {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Geografia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Ciências {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Inglês {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Arte {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Educação Física {grupo}", "carga": 2, "tipo": "pratica"},
            {"nome": f"Informática {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Dinâmica {grupo}", "carga": 1, "tipo": "leve"},
            {"nome": f"Vida Pratica {grupo}", "carga": 1, "tipo": "leve"}
        ],
        "9ano": [
            {"nome": f"Português {grupo}", "carga": 5, "tipo": "pesada"},
            {"nome": f"Matemática {grupo}", "carga": 4, "tipo": "pesada"},
            {"nome": f"História {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Geografia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Ciências {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Inglês {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Arte {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Educação Física {grupo}", "carga": 2, "tipo": "pratica"},
            {"nome": f"Informática {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Dinâmica {grupo}", "carga": 1, "tipo": "leve"},
            {"nome": f"Vida Pratica {grupo}", "carga": 1, "tipo": "leve"}
        ],
        "1em": [
            {"nome": f"Português {grupo}", "carga": 5, "tipo": "pesada"},
            {"nome": f"Matemática {grupo}", "carga": 4, "tipo": "pesada"},
            {"nome": f"História {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Geografia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Biologia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Física {grupo}", "carga": 2, "tipo": "pesada"},
            {"nome": f"Química {grupo}", "carga": 2, "tipo": "pesada"},
            {"nome": f"Inglês {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Arte {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Educação Física {grupo}", "carga": 2, "tipo": "pratica"},
            {"nome": f"Filosofia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Sociologia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Informática {grupo}", "carga": 2, "tipo": "leve"}
        ],
        "2em": [
            {"nome": f"Português {grupo}", "carga": 5, "tipo": "pesada"},
            {"nome": f"Matemática {grupo}", "carga": 4, "tipo": "pesada"},
            {"nome": f"História {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Geografia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Biologia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Física {grupo}", "carga": 2, "tipo": "pesada"},
            {"nome": f"Química {grupo}", "carga": 2, "tipo": "pesada"},
            {"nome": f"Inglês {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Arte {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Educação Física {grupo}", "carga": 2, "tipo": "pratica"},
            {"nome": f"Filosofia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Sociologia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Informática {grupo}", "carga": 2, "tipo": "leve"}
        ],
        "3em": [
            {"nome": f"Português {grupo}", "carga": 5, "tipo": "pesada"},
            {"nome": f"Matemática {grupo}", "carga": 4, "tipo": "pesada"},
            {"nome": f"História {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Geografia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Biologia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Física {grupo}", "carga": 2, "tipo": "pesada"},
            {"nome": f"Química {grupo}", "carga": 2, "tipo": "pesada"},
            {"nome": f"Inglês {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Arte {grupo}", "carga": 2, "tipo": "leve"},
            {"nome": f"Educação Física {grupo}", "carga": 2, "tipo": "pratica"},
            {"nome": f"Filosofia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Sociologia {grupo}", "carga": 2, "tipo": "media"},
            {"nome": f"Informática {grupo}", "carga": 2, "tipo": "leve"}
        ]
    }
    
    return disciplinas_base.get(serie, [])

# Cores padrão para disciplinas - DADOS REAIS
CORES_DISCIPLINAS = {
    "Português A": {"fundo": "#4A90E2", "fonte": "#FFFFFF"},
    "Português B": {"fundo": "#4A90E2", "fonte": "#FFFFFF"},
    "Matemática A": {"fundo": "#50E3C2", "fonte": "#000000"},
    "Matemática B": {"fundo": "#50E3C2", "fonte": "#000000"},
    "História A": {"fundo": "#B8E986", "fonte": "#000000"},
    "História B": {"fundo": "#B8E986", "fonte": "#000000"},
    "Geografia A": {"fundo": "#7ED321", "fonte": "#000000"},
    "Geografia B": {"fundo": "#7ED321", "fonte": "#000000"},
    "Ciências A": {"fundo": "#BD10E0", "fonte": "#FFFFFF"},
    "Ciências B": {"fundo": "#BD10E0", "fonte": "#FFFFFF"},
    "Biologia A": {"fundo": "#9013FE", "fonte": "#FFFFFF"},
    "Biologia B": {"fundo": "#9013FE", "fonte": "#FFFFFF"},
    "Física A": {"fundo": "#417505", "fonte": "#FFFFFF"},
    "Física B": {"fundo": "#417505", "fonte": "#FFFFFF"},
    "Química A": {"fundo": "#F5A623", "fonte": "#000000"},
    "Química B": {"fundo": "#F5A623", "fonte": "#000000"},
    "Inglês A": {"fundo": "#F8E71C", "fonte": "#000000"},
    "Inglês B": {"fundo": "#F8E71C", "fonte": "#000000"},
    "Arte A": {"fundo": "#D0021B", "fonte": "#FFFFFF"},
    "Arte B": {"fundo": "#D0021B", "fonte": "#FFFFFF"},
    "Educação Física A": {"fundo": "#8B572A", "fonte": "#FFFFFF"},
    "Educação Física B": {"fundo": "#8B572A", "fonte": "#FFFFFF"},
    "Filosofia A": {"fundo": "#50E3C2", "fonte": "#000000"},
    "Filosofia B": {"fundo": "#50E3C2", "fonte": "#000000"},
    "Sociologia A": {"fundo": "#B8E986", "fonte": "#000000"},
    "Sociologia B": {"fundo": "#B8E986", "fonte": "#000000"},
    "Informática A": {"fundo": "#4A90E2", "fonte": "#FFFFFF"},
    "Informática B": {"fundo": "#4A90E2", "fonte": "#FFFFFF"},
    "Dinâmica A": {"fundo": "#F5A623", "fonte": "#000000"},
    "Dinâmica B": {"fundo": "#F5A623", "fonte": "#000000"},
    "Vida Pratica A": {"fundo": "#7ED321", "fonte": "#000000"},
    "Vida Pratica B": {"fundo": "#7ED321", "fonte": "#000000"}
}

def obter_cor_disciplina(nome_disciplina):
    """Retorna as cores padrão para uma disciplina"""
    return CORES_DISCIPLINAS.get(nome_disciplina, {"fundo": "#4A90E2", "fonte": "#FFFFFF"})