"""
NEURO RULES - Configurações inteligentes para horários e cargas
"""

# ================= CONFIGURAÇÕES DE HORÁRIOS =================

HORARIOS_NEURO = {
    'EF_II': {
        'inicio': '07:50',
        'fim': '12:20',
        'aulas_antes_intervalo': 2,  # 2 aulas antes do intervalo
        'aulas_depois_intervalo': 4,  # 4 aulas depois do intervalo
        'total_periodos': 6,
        'carga_maxima_semanal': 25,
        'intervalo_horario': 3  # Intervalo no 3º horário
    },
    'EM': {
        'inicio': '07:00',
        'fim': '13:10',  # ✅ CORREÇÃO: SEMPRE até 13:10
        'aulas_antes_intervalo': 3,  # 3 aulas antes do intervalo
        'aulas_depois_intervalo': 4,  # 4 aulas depois do intervalo  
        'total_periodos': 7,
        'carga_maxima_semanal': 35,  # ✅ CORREÇÃO: 35 horas
        'intervalo_horario': 4  # Intervalo no 4º horário
    }
}

# ================= CONFIGURAÇÕES DE DISCIPLINAS EM =================

DISCIPLINAS_EM = {
    '1em': {
        'Portugues': 5,
        'Matematica': 5,
        'Historia': 3,
        'Geografia': 3,
        'Biologia': 3,
        'Fisica': 3,
        'Quimica': 3,
        'Ingles': 3,
        'Arte': 2,
        'Educacao Fisica': 2,
        'Filosofia': 2,
        'Sociologia': 2,
        'Informatica': 2
    },
    '2em': {
        'Portugues': 5,
        'Matematica': 5,
        'Historia': 3,
        'Geografia': 3,
        'Biologia': 3,
        'Fisica': 3,
        'Quimica': 3,
        'Ingles': 3,
        'Arte': 2,
        'Educacao Fisica': 2,
        'Filosofia': 2,
        'Sociologia': 2,
        'Informatica': 2
    },
    '3em': {
        'Portugues': 5,
        'Matematica': 5,
        'Historia': 3,
        'Geografia': 3,
        'Biologia': 3,
        'Fisica': 3,
        'Quimica': 3,
        'Ingles': 3,
        'Arte': 2,
        'Educacao Fisica': 2,
        'Filosofia': 2,
        'Sociologia': 2,
        'Informatica': 2
    }
}

# ================= CONFIGURAÇÕES DE DISCIPLINAS EF II =================

DISCIPLINAS_EF_II = {
    '6ano': {
        'Portugues': 4,
        'Matematica': 5,
        'Historia': 3,
        'Geografia': 3,
        'Ciencias': 3,
        'Ingles': 2,
        'Arte': 2,
        'Educacao Fisica': 2,
        'Informatica': 2,
        'Dinamica': 1,
        'Vida Pratica': 1
    },
    '7ano': {
        'Portugues': 4,
        'Matematica': 5,
        'Historia': 3,
        'Geografia': 3,
        'Ciencias': 3,
        'Ingles': 2,
        'Arte': 2,
        'Educacao Fisica': 2,
        'Informatica': 2,
        'Dinamica': 1,
        'Vida Pratica': 1
    },
    '8ano': {
        'Portugues': 4,
        'Matematica': 5,
        'Historia': 3,
        'Geografia': 3,
        'Ciencias': 3,
        'Ingles': 2,
        'Arte': 2,
        'Educacao Fisica': 2,
        'Informatica': 2,
        'Dinamica': 1,
        'Vida Pratica': 1
    },
    '9ano': {
        'Portugues': 4,
        'Matematica': 5,
        'Historia': 3,
        'Geografia': 3,
        'Ciencias': 3,
        'Ingles': 2,
        'Arte': 2,
        'Educacao Fisica': 2,
        'Informatica': 2,
        'Dinamica': 1,
        'Vida Pratica': 1
    }
}

# ================= PROFESSORES REAIS =================

PROFESSORES_NEURO = [
    # Língua Portuguesa
    {"nome": "Heliana", "disciplinas": ["Portugues A", "Portugues B"], "grupo": "AMBOS"},
    {"nome": "Deise", "disciplinas": ["Portugues A", "Portugues B"], "grupo": "AMBOS"},
    {"nome": "Loide", "disciplinas": ["Portugues A", "Portugues B"], "grupo": "AMBOS"},
    
    # Matemática
    {"nome": "Tatiane", "disciplinas": ["Matematica A", "Matematica B"], "grupo": "AMBOS"},
    {"nome": "Ricardo", "disciplinas": ["Matematica A", "Matematica B"], "grupo": "AMBOS"},
    
    # História
    {"nome": "Laís", "disciplinas": ["Historia A", "Historia B"], "grupo": "AMBOS"},
    {"nome": "Waldemar", "disciplinas": ["Historia A", "Historia B"], "grupo": "AMBOS"},
    
    # Geografia
    {"nome": "Rene", "disciplinas": ["Geografia A", "Geografia B"], "grupo": "AMBOS"},
    {"nome": "Gisele", "disciplinas": ["Geografia A", "Geografia B"], "grupo": "AMBOS"},
    
    # Ciências/Biologia
    {"nome": "Marina", "disciplinas": ["Ciencias A", "Ciencias B", "Biologia A", "Biologia B"], "grupo": "AMBOS"},
    
    # Física/Química/Informática
    {"nome": "César", "disciplinas": ["Fisica A", "Fisica B", "Quimica A", "Quimica B", "Informatica A", "Informatica B"], "grupo": "AMBOS"},
    {"nome": "Vladmir", "disciplinas": ["Quimica A", "Quimica B"], "grupo": "AMBOS"},
    {"nome": "Zabuor", "disciplinas": ["Quimica A", "Quimica B"], "grupo": "AMBOS"},
    
    # Filosofia/Sociologia
    {"nome": "Anna Maria", "disciplinas": ["Filosofia A", "Filosofia B", "Sociologia A", "Sociologia B"], "grupo": "AMBOS"},
    
    # Educação Física
    {"nome": "Marcão", "disciplinas": ["Educacao Fisica A", "Educacao Fisica B"], "grupo": "AMBOS"},
    {"nome": "Andréia", "disciplinas": ["Educacao Fisica A", "Educacao Fisica B"], "grupo": "AMBOS"},
    
    # Arte
    {"nome": "Vanessa", "disciplinas": ["Arte A", "Arte B"], "grupo": "AMBOS"},
    
    # Inglês
    {"nome": "Maria Luiza", "disciplinas": ["Ingles A", "Ingles B"], "grupo": "AMBOS"},
    
    # Dinâmica/Vida Prática
    {"nome": "Andréia Barreto", "disciplinas": ["Dinamica A", "Dinamica B", "Vida Pratica A", "Vida Pratica B"], "grupo": "AMBOS"},
]

# ================= SALAS =================

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
    {"nome": "Laboratório de Ciências", "capacidade": 25, "tipo": "laboratorio"},
    {"nome": "Laboratório de Informática", "capacidade": 25, "tipo": "laboratorio"},
    {"nome": "Auditório", "capacidade": 100, "tipo": "auditorio"},
]

# ================= FUNÇÕES AUXILIARES =================

def obter_config_segmento(segmento):
    """Retorna configurações do segmento"""
    return HORARIOS_NEURO.get(segmento, HORARIOS_NEURO['EF_II'])

def obter_carga_maxima(serie):
    """Retorna carga máxima baseada na série"""
    if 'em' in serie.lower():
        return 35  # EM: 35 horas
    else:
        return 25  # EF II: 25 horas

def obter_disciplinas_por_serie(serie, grupo):
    """Retorna disciplinas e carga horária para uma série"""
    if 'em' in serie.lower():
        serie_key = '1em' if '1' in serie else '2em' if '2' in serie else '3em'
        disciplinas = DISCIPLINAS_EM.get(serie_key, {})
    else:
        serie_key = '6ano' if '6' in serie else '7ano' if '7' in serie else '8ano' if '8' in serie else '9ano'
        disciplinas = DISCIPLINAS_EF_II.get(serie_key, {})
    
    # Adicionar sufixo do grupo (A/B)
    return {f"{nome} {grupo}": carga for nome, carga in disciplinas.items()}

def validar_carga_horaria(turma_nome, serie, grupo):
    """Valida se a carga horária está dentro do limite"""
    disciplinas = obter_disciplinas_por_serie(serie, grupo)
    carga_total = sum(disciplinas.values())
    carga_maxima = obter_carga_maxima(serie)
    
    return {
        'turma': turma_nome,
        'carga_total': carga_total,
        'carga_maxima': carga_maxima,
        'dentro_limite': carga_total <= carga_maxima,
        'diferenca': carga_maxima - carga_total
    }