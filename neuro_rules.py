"""
NEURO RULES - Regras Inteligentes para Grade Horária
Configurações específicas para EM e EF II
"""

# CONFIGURAÇÕES DE HORÁRIOS POR SEGMENTO
CONFIG_HORARIOS = {
    'EF_II': {
        'nome': 'Ensino Fundamental II',
        'inicio': '07:50',
        'fim': '12:20',
        'horarios_disponiveis': [1, 2, 3, 4, 5, 6],  # 6 períodos
        'horario_intervalo': 3,  # Intervalo no 3º horário
        'carga_horaria_maxima': 25,
        'dias_semana': 5
    },
    'EM': {
        'nome': 'Ensino Médio', 
        'inicio': '07:00',
        'fim': '13:10',
        'horarios_disponiveis': [1, 2, 3, 4, 5, 6, 7],  # 7 períodos
        'horario_intervalo': 4,  # Intervalo no 4º horário
        'carga_horaria_maxima': 35,
        'dias_semana': 5
    }
}

# CARGA HORÁRIA RECOMENDADA POR DISCIPLINA - EM
CARGA_HORARIA_EM = {
    'Português': 5,
    'Matemática': 5,
    'História': 3,
    'Geografia': 3,
    'Física': 3,
    'Química': 3,
    'Biologia': 3,
    'Inglês': 3,
    'Arte': 2,
    'Educação Física': 2,
    'Filosofia': 2,
    'Sociologia': 2,
    'Informática': 2
}

# CARGA HORÁRIA RECOMENDADA POR DISCIPLINA - EF II
CARGA_HORARIA_EFII = {
    'Português': 4,
    'Matemática': 5,
    'História': 3,
    'Geografia': 3,
    'Ciências': 3,
    'Inglês': 2,
    'Arte': 2,
    'Educação Física': 2,
    'Informática': 2,
    'Dinâmica': 1,
    'Vida Prática': 1
}

# PROFESSORES REAIS COM SUAS DISCIPLINAS
PROFESSORES_CONFIG = {
    # LINGUAGENS
    'Heliana': ['Português A', 'Português B'],
    'Deise': ['Português A', 'Português B'],
    'Loide': ['Português A', 'Português B'],
    'Maria Luiza': ['Inglês A', 'Inglês B'],
    'Vanessa': ['Arte A', 'Arte B'],
    
    # MATEMÁTICA
    'Tatiane': ['Matemática A', 'Matemática B'],
    'Ricardo': ['Matemática A', 'Matemática B'],
    
    # CIÊNCIAS HUMANAS
    'Laís': ['História A', 'História B'],
    'Waldemar': ['História A', 'História B'],
    'Rene': ['Geografia A', 'Geografia B'],
    'Gisele': ['Geografia A', 'Geografia B'],
    'Anna Maria': ['Filosofia A', 'Filosofia B', 'Sociologia A', 'Sociologia B'],
    
    # CIÊNCIAS DA NATUREZA
    'Marina': ['Biologia A', 'Biologia B', 'Ciências A', 'Ciências B'],
    'Vladmir': ['Química A', 'Química B'],
    'Zabuor': ['Química A', 'Química B'],
    'César': ['Física A', 'Física B', 'Informática A', 'Informática B'],
    
    # EDUCAÇÃO FÍSICA E OUTRAS
    'Marcão': ['Educação Física A', 'Educação Física B'],
    'Andréia': ['Educação Física A', 'Educação Física B'],
    'Andréia Barreto': ['Dinâmica A', 'Dinâmica B', 'Vida Pratica A', 'Vida Pratica B']
}

# SALAS DISPONÍVEIS
SALAS_CONFIG = [
    {'nome': 'Sala 1', 'capacidade': 30, 'tipo': 'normal'},
    {'nome': 'Sala 2', 'capacidade': 30, 'tipo': 'normal'},
    {'nome': 'Sala 3', 'capacidade': 30, 'tipo': 'normal'},
    {'nome': 'Sala 4', 'capacidade': 30, 'tipo': 'normal'},
    {'nome': 'Sala 5', 'capacidade': 30, 'tipo': 'normal'},
    {'nome': 'Sala 6', 'capacidade': 30, 'tipo': 'normal'},
    {'nome': 'Sala 7', 'capacidade': 30, 'tipo': 'normal'},
    {'nome': 'Sala 8', 'capacidade': 30, 'tipo': 'normal'},
    {'nome': 'Sala 9', 'capacidade': 30, 'tipo': 'normal'},
    {'nome': 'Sala 10', 'capacidade': 30, 'tipo': 'normal'},
    {'nome': 'Laboratório de Ciências', 'capacidade': 25, 'tipo': 'laboratório'},
    {'nome': 'Laboratório de Informática', 'capacidade': 20, 'tipo': 'laboratório'},
    {'nome': 'Auditório', 'capacidade': 100, 'tipo': 'auditório'},
]

def obter_config_segmento(segmento):
    """Retorna configurações para o segmento"""
    return CONFIG_HORARIOS.get(segmento, CONFIG_HORARIOS['EF_II'])

def obter_carga_horaria_recomendada(disciplina_nome, segmento):
    """Retorna carga horária recomendada para disciplina"""
    if segmento == 'EM':
        # Remove sufixo A/B para encontrar carga base
        nome_base = disciplina_nome.replace(' A', '').replace(' B', '')
        return CARGA_HORARIA_EM.get(nome_base, 3)
    else:
        nome_base = disciplina_nome.replace(' A', '').replace(' B', '')
        return CARGA_HORARIA_EFII.get(nome_base, 2)

def validar_carga_horaria_turma(turma_nome, disciplinas_vinculadas):
    """Valida se a carga horária está dentro do limite"""
    from app import obter_segmento_turma, calcular_carga_maxima
    
    segmento = obter_segmento_turma(turma_nome)
    carga_maxima = calcular_carga_maxima(turma_nome.split('ano')[0] + 'ano' if 'ano' in turma_nome else turma_nome)
    
    carga_total = sum(disc.carga_semanal for disc in disciplinas_vinculadas)
    
    return {
        'valido': carga_total <= carga_maxima,
        'carga_atual': carga_total,
        'carga_maxima': carga_maxima,
        'diferenca': carga_maxima - carga_total
    }

def gerar_disciplinas_por_segmento():
    """Gera lista de disciplinas organizadas por segmento"""
    disciplinas_em_a = []
    disciplinas_em_b = []
    disciplinas_efii_a = []
    disciplinas_efii_b = []
    
    # Disciplinas do EM
    for disc_base, carga in CARGA_HORARIA_EM.items():
        disciplinas_em_a.append({
            'nome': f'{disc_base} A',
            'carga_semanal': carga,
            'tipo': 'pesada' if disc_base in ['Português', 'Matemática', 'Física', 'Química'] else 'media',
            'turmas': ['1emA', '2emA', '3emA'],
            'grupo': 'A'
        })
        disciplinas_em_b.append({
            'nome': f'{disc_base} B',
            'carga_semanal': carga,
            'tipo': 'pesada' if disc_base in ['Português', 'Matemática', 'Física', 'Química'] else 'media',
            'turmas': ['1emB', '2emB', '3emB'],
            'grupo': 'B'
        })
    
    # Disciplinas do EF II
    for disc_base, carga in CARGA_HORARIA_EFII.items():
        disciplinas_efii_a.append({
            'nome': f'{disc_base} A',
            'carga_semanal': carga,
            'tipo': 'pesada' if disc_base in ['Português', 'Matemática'] else 'media',
            'turmas': ['6anoA', '7anoA', '8anoA', '9anoA'],
            'grupo': 'A'
        })
        disciplinas_efii_b.append({
            'nome': f'{disc_base} B',
            'carga_semanal': carga,
            'tipo': 'pesada' if disc_base in ['Português', 'Matemática'] else 'media',
            'turmas': ['6anoB', '7anoB', '8anoB', '9anoB'],
            'grupo': 'B'
        })
    
    return {
        'EM_A': disciplinas_em_a,
        'EM_B': disciplinas_em_b,
        'EFII_A': disciplinas_efii_a,
        'EFII_B': disciplinas_efii_b
    }

def obter_professor_para_disciplina(disciplina_nome):
    """Encontra professores que podem ministrar a disciplina"""
    professores_compatíveis = []
    for professor, disciplinas in PROFESSORES_CONFIG.items():
        if disciplina_nome in disciplinas:
            professores_compatíveis.append(professor)
    return professores_compatíveis