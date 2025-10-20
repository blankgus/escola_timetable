import streamlit as st
from models import Turma, Professor, Disciplina, Sala, DIAS_SEMANA
import database
import uuid
from neuro_rules import PROFESSORES_NEURO, SALAS_NEURO, obter_disciplinas_por_serie

def init_session_state():
    database.init_db()
    
    turmas_db = database.carregar_turmas()
    professores_db = database.carregar_professores()
    disciplinas_db = database.carregar_disciplinas()
    salas_db = database.carregar_salas()
    periodos_db = database.carregar_periodos()
    feriados_db = database.carregar_feriados()
    aulas_db = database.carregar_grade()
    
    if "turmas" not in st.session_state:
        st.session_state.turmas = turmas_db or criar_turmas_padrao()
    
    if "professores" not in st.session_state:
        st.session_state.professores = professores_db or criar_professores_padrao()
    
    if "disciplinas" not in st.session_state:
        st.session_state.disciplinas = disciplinas_db or criar_disciplinas_padrao()
    
    if "salas" not in st.session_state:
        st.session_state.salas = salas_db or criar_salas_padrao()
    
    if "periodos" not in st.session_state:
        st.session_state.periodos = periodos_db or criar_periodos_padrao()
    
    if "feriados" not in st.session_state:
        st.session_state.feriados = feriados_db or criar_feriados_padrao()
    
    if "aulas" not in st.session_state:
        st.session_state.aulas = aulas_db or []

def criar_turmas_padrao():
    return [
        # EF II
        Turma("6anoA", "6ano", "manha", "A", "EF_II"),
        Turma("7anoA", "7ano", "manha", "A", "EF_II"),
        Turma("8anoA", "8ano", "manha", "A", "EF_II"),
        Turma("9anoA", "9ano", "manha", "A", "EF_II"),
        Turma("6anoB", "6ano", "manha", "B", "EF_II"),
        Turma("7anoB", "7ano", "manha", "B", "EF_II"),
        Turma("8anoB", "8ano", "manha", "B", "EF_II"),
        Turma("9anoB", "9ano", "manha", "B", "EF_II"),
        
        # EM - ✅ CORREÇÃO: Segmento EM
        Turma("1emA", "1em", "manha", "A", "EM"),
        Turma("2emA", "2em", "manha", "A", "EM"),
        Turma("3emA", "3em", "manha", "A", "EM"),
        Turma("1emB", "1em", "manha", "B", "EM"),
        Turma("2emB", "2em", "manha", "B", "EM"),
        Turma("3emB", "3em", "manha", "B", "EM"),
    ]

def criar_professores_padrao():
    """Cria professores baseados nas regras neuro"""
    professores = []
    for prof_info in PROFESSORES_NEURO:
        professor = Professor(
            nome=prof_info["nome"],
            disciplinas=prof_info["disciplinas"],
            disponibilidade={"seg", "ter", "qua", "qui", "sex"},
            grupo=prof_info["grupo"]
        )
        professores.append(professor)
    return professores

def criar_disciplinas_padrao():
    """Cria disciplinas baseadas nas regras neuro"""
    disciplinas = []
    
    # Turmas do EF II
    turmas_efii = ["6anoA", "7anoA", "8anoA", "9anoA", "6anoB", "7anoB", "8anoB", "9anoB"]
    
    for turma_nome in turmas_efii:
        serie = turma_nome.replace('A', '').replace('B', '')
        grupo = 'A' if 'A' in turma_nome else 'B'
        
        disciplinas_serie = obter_disciplinas_por_serie(serie, grupo)
        
        for nome_disc, carga in disciplinas_serie.items():
            # Verificar se disciplina já existe
            disc_existente = next((d for d in disciplinas if d.nome == nome_disc), None)
            
            if disc_existente:
                if turma_nome not in disc_existente.turmas:
                    disc_existente.turmas.append(turma_nome)
            else:
                tipo = "pesada" if "Portugues" in nome_disc or "Matematica" in nome_disc else "media"
                nova_disciplina = Disciplina(
                    nome=nome_disc,
                    carga_semanal=carga,
                    tipo=tipo,
                    turmas=[turma_nome],
                    grupo=grupo
                )
                disciplinas.append(nova_disciplina)
    
    # Turmas do EM
    turmas_em = ["1emA", "2emA", "3emA", "1emB", "2emB", "3emB"]
    
    for turma_nome in turmas_em:
        serie = turma_nome.replace('A', '').replace('B', '')
        grupo = 'A' if 'A' in turma_nome else 'B'
        
        disciplinas_serie = obter_disciplinas_por_serie(serie, grupo)
        
        for nome_disc, carga in disciplinas_serie.items():
            # Verificar se disciplina já existe
            disc_existente = next((d for d in disciplinas if d.nome == nome_disc), None)
            
            if disc_existente:
                if turma_nome not in disc_existente.turmas:
                    disc_existente.turmas.append(turma_nome)
            else:
                tipo = "pesada" if "Portugues" in nome_disc or "Matematica" in nome_disc else "media"
                nova_disciplina = Disciplina(
                    nome=nome_disc,
                    carga_semanal=carga,
                    tipo=tipo,
                    turmas=[turma_nome],
                    grupo=grupo
                )
                disciplinas.append(nova_disciplina)
    
    return disciplinas

def criar_salas_padrao():
    """Cria salas baseadas nas regras neuro"""
    salas = []
    for sala_info in SALAS_NEURO:
        sala = Sala(
            nome=sala_info["nome"],
            capacidade=sala_info["capacidade"],
            tipo=sala_info["tipo"]
        )
        salas.append(sala)
    return salas

def criar_periodos_padrao():
    return [
        {"nome": "1º Bimestre", "inicio": "2025-02-01", "fim": "2025-03-31", "id": str(uuid.uuid4())},
        {"nome": "2º Bimestre", "inicio": "2025-04-01", "fim": "2025-05-31", "id": str(uuid.uuid4())},
        {"nome": "3º Bimestre", "inicio": "2025-06-01", "fim": "2025-07-31", "id": str(uuid.uuid4())},
        {"nome": "4º Bimestre", "inicio": "2025-08-01", "fim": "2025-09-30", "id": str(uuid.uuid4())},
    ]

def criar_feriados_padrao():
    return [
        {"data": "2025-01-01", "motivo": "Ano Novo", "id": str(uuid.uuid4())},
        {"data": "2025-04-21", "motivo": "Tiradentes", "id": str(uuid.uuid4())},
        {"data": "2025-05-01", "motivo": "Dia do Trabalho", "id": str(uuid.uuid4())},
        {"data": "2025-09-07", "motivo": "Independência", "id": str(uuid.uuid4())},
        {"data": "2025-10-12", "motivo": "Nossa Sra. Aparecida", "id": str(uuid.uuid4())},
        {"data": "2025-11-02", "motivo": "Finados", "id": str(uuid.uuid4())},
        {"data": "2025-11-15", "motivo": "Proclamação da República", "id": str(uuid.uuid4())},
        {"data": "2025-12-25", "motivo": "Natal", "id": str(uuid.uuid4())},
    ]