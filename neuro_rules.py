"""
Regras e configurações específicas para a escola Neuro
"""

# Configurações de professores neuro
PROFESSORES_NEURO = {
    "Lucas": {
        "disciplinas": ["Matemática", "Física"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Ana": {
        "disciplinas": ["Português", "Literatura"],
        "grupo": "AMBOS", 
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Carlos": {
        "disciplinas": ["História", "Geografia"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Mariana": {
        "disciplinas": ["Biologia", "Química"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Pedro": {
        "disciplinas": ["Inglês"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    },
    "Julia": {
        "disciplinas": ["Artes", "Educação Física"],
        "grupo": "AMBOS",
        "disponibilidade": ["segunda", "terca", "quarta", "quinta", "sexta"],
        "horarios_indisponiveis": []
    }
}

# Configurações de salas neuro
SALAS_NEURO = [
    {"nome": "Sala 1", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 2", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 3", "capacidade": 30, "tipo": "normal"},
    {"nome": "Sala 4", "capacidade": 30, "tipo": "normal"},
    {"nome": "Laboratório de Ciências", "capacidade": 25, "tipo": "laboratório"},
    {"nome": "Sala de Artes", "capacidade": 20, "tipo": "normal"}
]

# Disciplinas por série
def obter_disciplinas_por_serie(serie):
    """
    Retorna as disciplinas padrão para cada série
    """
    disciplinas_base = {
        "6ano": [
            {"nome": "Matemática", "carga": 5, "tipo": "pesada", "grupo": "A"},
            {"nome": "Português", "carga": 5, "tipo": "pesada", "grupo": "A"},
            {"nome": "História", "carga": 2, "tipo": "media", "grupo": "A"},
            {"nome": "Geografia", "carga": 2, "tipo": "media", "grupo": "A"},
            {"nome": "Ciências", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Inglês", "carga": 2, "tipo": "leve", "grupo": "A"},
            {"nome": "Artes", "carga": 2, "tipo": "leve", "grupo": "A"},
            {"nome": "Educação Física", "carga": 2, "tipo": "pratica", "grupo": "A"}
        ],
        "7ano": [
            {"nome": "Matemática", "carga": 5, "tipo": "pesada", "grupo": "A"},
            {"nome": "Português", "carga": 5, "tipo": "pesada", "grupo": "A"},
            {"nome": "História", "carga": 2, "tipo": "media", "grupo": "A"},
            {"nome": "Geografia", "carga": 2, "tipo": "media", "grupo": "A"},
            {"nome": "Ciências", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Inglês", "carga": 2, "tipo": "leve", "grupo": "A"},
            {"nome": "Artes", "carga": 2, "tipo": "leve", "grupo": "A"},
            {"nome": "Educação Física", "carga": 2, "tipo": "pratica", "grupo": "A"}
        ],
        "8ano": [
            {"nome": "Matemática", "carga": 5, "tipo": "pesada", "grupo": "A"},
            {"nome": "Português", "carga": 5, "tipo": "pesada", "grupo": "A"},
            {"nome": "História", "carga": 2, "tipo": "media", "grupo": "A"},
            {"nome": "Geografia", "carga": 2, "tipo": "media", "grupo": "A"},
            {"nome": "Ciências", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Inglês", "carga": 2, "tipo": "leve", "grupo": "A"},
            {"nome": "Artes", "carga": 2, "tipo": "leve", "grupo": "A"},
            {"nome": "Educação Física", "carga": 2, "tipo": "pratica", "grupo": "A"}
        ],
        "9ano": [
            {"nome": "Matemática", "carga": 5, "tipo": "pesada", "grupo": "A"},
            {"nome": "Português", "carga": 5, "tipo": "pesada", "grupo": "A"},
            {"nome": "História", "carga": 2, "tipo": "media", "grupo": "A"},
            {"nome": "Geografia", "carga": 2, "tipo": "media", "grupo": "A"},
            {"nome": "Ciências", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Inglês", "carga": 2, "tipo": "leve", "grupo": "A"},
            {"nome": "Artes", "carga": 2, "tipo": "leve", "grupo": "A"},
            {"nome": "Educação Física", "carga": 2, "tipo": "pratica", "grupo": "A"}
        ],
        "1em": [
            {"nome": "Matemática", "carga": 5, "tipo": "pesada", "grupo": "A"},
            {"nome": "Português", "carga": 5, "tipo": "pesada", "grupo": "A"},
            {"nome": "História", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Geografia", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Biologia", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Física", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Química", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Inglês", "carga": 2, "tipo": "leve", "grupo": "A"},
            {"nome": "Educação Física", "carga": 2, "tipo": "pratica", "grupo": "A"}
        ],
        "2em": [
            {"nome": "Matemática", "carga": 5, "tipo": "pesada", "grupo": "A"},
            {"nome": "Português", "carga": 5, "tipo": "pesada", "grupo": "A"},
            {"nome": "História", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Geografia", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Biologia", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Física", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Química", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Inglês", "carga": 2, "tipo": "leve", "grupo": "A"},
            {"nome": "Educação Física", "carga": 2, "tipo": "pratica", "grupo": "A"}
        ],
        "3em": [
            {"nome": "Matemática", "carga": 6, "tipo": "pesada", "grupo": "A"},
            {"nome": "Português", "carga": 6, "tipo": "pesada", "grupo": "A"},
            {"nome": "História", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Geografia", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Biologia", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Física", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Química", "carga": 3, "tipo": "media", "grupo": "A"},
            {"nome": "Inglês", "carga": 2, "tipo": "leve", "grupo": "A"},
            {"nome": "Educação Física", "carga": 2, "tipo": "pratica", "grupo": "A"}
        ]
    }
    
    return disciplinas_base.get(serie, [])

# Turmas padrão neuro
TURMAS_NEURO = [
    {"nome": "6anoA", "serie": "6ano", "turno": "manha", "grupo": "A", "segmento": "EF_II"},
    {"nome": "6anoB", "serie": "6ano", "turno": "manha", "grupo": "B", "segmento": "EF_II"},
    {"nome": "7anoA", "serie": "7ano", "turno": "manha", "grupo": "A", "segmento": "EF_II"},
    {"nome": "7anoB", "serie": "7ano", "turno": "manha", "grupo": "B", "segmento": "EF_II"},
    {"nome": "8anoA", "serie": "8ano", "turno": "manha", "grupo": "A", "segmento": "EF_II"},
    {"nome": "8anoB", "serie": "8ano", "turno": "manha", "grupo": "B", "segmento": "EF_II"},
    {"nome": "9anoA", "serie": "9ano", "turno": "manha", "grupo": "A", "segmento": "EF_II"},
    {"nome": "9anoB", "serie": "9ano", "turno": "manha", "grupo": "B", "segmento": "EF_II"},
    {"nome": "1emA", "serie": "1em", "turno": "manha", "grupo": "A", "segmento": "EM"},
    {"nome": "1emB", "serie": "1em", "turno": "manha", "grupo": "B", "segmento": "EM"},
    {"nome": "2emA", "serie": "2em", "turno": "manha", "grupo": "A", "segmento": "EM"},
    {"nome": "2emB", "serie": "2em", "turno": "manha", "grupo": "B", "segmento": "EM"},
    {"nome": "3emA", "serie": "3em", "turno": "manha", "grupo": "A", "segmento": "EM"},
    {"nome": "3emB", "serie": "3em", "turno": "manha", "grupo": "B", "segmento": "EM"}
]

# Cores padrão para disciplinas
CORES_DISCIPLINAS = {
    "Matemática": {"fundo": "#4A90E2", "fonte": "#FFFFFF"},
    "Português": {"fundo": "#50E3C2", "fonte": "#000000"},
    "História": {"fundo": "#B8E986", "fonte": "#000000"},
    "Geografia": {"fundo": "#7ED321", "fonte": "#000000"},
    "Ciências": {"fundo": "#BD10E0", "fonte": "#FFFFFF"},
    "Biologia": {"fundo": "#9013FE", "fonte": "#FFFFFF"},
    "Física": {"fundo": "#417505", "fonte": "#FFFFFF"},
    "Química": {"fundo": "#F5A623", "fonte": "#000000"},
    "Inglês": {"fundo": "#F8E71C", "fonte": "#000000"},
    "Artes": {"fundo": "#D0021B", "fonte": "#FFFFFF"},
    "Educação Física": {"fundo": "#8B572A", "fonte": "#FFFFFF"},
    "Literatura": {"fundo": "#50E3C2", "fonte": "#000000"}
}

def obter_cor_disciplina(nome_disciplina):
    """Retorna as cores padrão para uma disciplina"""
    return CORES_DISCIPLINAS.get(nome_disciplina, {"fundo": "#4A90E2", "fonte": "#FFFFFF"})