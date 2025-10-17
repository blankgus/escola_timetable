import streamlit as st
from models import Turma, Professor, Disciplina, Sala, DIAS_SEMANA
import database
import uuid

def init_session_state():
    database.init_db()
    
    # ✅ SEMPRE TENTA CARREGAR DO BANCO PRIMEIRO
    turmas_db = database.carregar_turmas()
    professores_db = database.carregar_professores()
    disciplinas_db = database.carregar_disciplinas()
    salas_db = database.carregar_salas()
    periodos_db = database.carregar_periodos()
    feriados_db = database.carregar_feriados()
    
    if "turmas" not in st.session_state:
        st.session_state.turmas = turmas_db or [
            # TURMAS GRUPO A
            Turma("6anoA", "6ano", "manha", "A"),
            Turma("7anoA", "7ano", "manha", "A"),
            Turma("8anoA", "8ano", "manha", "A"),
            Turma("9anoA", "9ano", "manha", "A"),
            Turma("1emA", "1em", "manha", "A"),
            Turma("2emA", "2em", "manha", "A"),
            Turma("3emA", "3em", "manha", "A"),
            # TURMAS GRUPO B
            Turma("6anoB", "6ano", "tarde", "B"),
            Turma("7anoB", "7ano", "tarde", "B"),
            Turma("8anoB", "8ano", "tarde", "B"),
            Turma("9anoB", "9ano", "tarde", "B"),
            Turma("1emB", "1em", "tarde", "B"),
            Turma("2emB", "2em", "tarde", "B"),
            Turma("3emB", "3em", "tarde", "B"),
        ]
    
    if "professores" not in st.session_state:
        st.session_state.professores = professores_db or [
            # PROFESSORES GRUPO A
            Professor("Ana", ["Matemática A"], {"seg", "ter", "qua", "qui", "sex"}, "A"),
            Professor("Bruno", ["Português A"], {"seg", "ter", "qua", "qui", "sex"}, "A"),
            Professor("Carla", ["História A", "Geografia A"], {"seg", "ter", "qua", "qui", "sex"}, "A"),
            # PROFESSORES GRUPO B
            Professor("Diego", ["Matemática B"], {"seg", "ter", "qua", "qui", "sex"}, "B"),
            Professor("Eliane", ["Português B"], {"seg", "ter", "qua", "qui", "sex"}, "B"),
            Professor("Fábio", ["História B", "Geografia B"], {"seg", "ter", "qua", "qui", "sex"}, "B"),
            # PROFESSORES AMBOS GRUPOS
            Professor("Gisele", ["Artes A", "Artes B"], {"seg", "ter", "qua", "qui", "sex"}, "AMBOS"),
            Professor("Hugo", ["Educação Física A", "Educação Física B"], {"seg", "ter", "qua", "qui", "sex"}, "AMBOS"),
        ]
    
    if "disciplinas" not in st.session_state:
        st.session_state.disciplinas = disciplinas_db or [
            # DISCIPLINAS GRUPO A
            Disciplina("Matemática A", 4, "pesada", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "A", "#4A90E2", "#FFFFFF"),
            Disciplina("Português A", 4, "pesada", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "A", "#D35400", "#FFFFFF"),
            Disciplina("História A", 3, "media", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "A", "#C0392B", "#FFFFFF"),
            Disciplina("Geografia A", 3, "media", ["6ano", "7ano", "8ano", "9ano", "1em"], "A", "#F39C12", "#000000"),
            Disciplina("Ciências A", 3, "media", ["6ano", "7ano", "8ano"], "A", "#1ABC9C", "#000000"),
            Disciplina("Biologia A", 3, "media", ["9ano", "1em", "2em", "3em"], "A", "#27AE60", "#FFFFFF"),
            Disciplina("Física A", 3, "pesada", ["2em", "3em"], "A", "#8E44AD", "#FFFFFF"),
            Disciplina("Química A", 3, "pesada", ["9ano", "1em", "2em", "3em"], "A", "#2980B9", "#FFFFFF"),
            Disciplina("Inglês A", 3, "media", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "A", "#2C3E50", "#FFFFFF"),
            Disciplina("Artes A", 1, "leve", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "A", "#E67E22", "#FFFFFF"),
            Disciplina("Educação Física A", 2, "pratica", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "A", "#2ECC71", "#000000"),
            
            # DISCIPLINAS GRUPO B
            Disciplina("Matemática B", 4, "pesada", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "B", "#4A90E2", "#FFFFFF"),
            Disciplina("Português B", 4, "pesada", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "B", "#D35400", "#FFFFFF"),
            Disciplina("História B", 3, "media", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "B", "#C0392B", "#FFFFFF"),
            Disciplina("Geografia B", 3, "media", ["6ano", "7ano", "8ano", "9ano", "1em"], "B", "#F39C12", "#000000"),
            Disciplina("Ciências B", 3, "media", ["6ano", "7ano", "8ano"], "B", "#1ABC9C", "#000000"),
            Disciplina("Biologia B", 3, "media", ["9ano", "1em", "2em", "3em"], "B", "#27AE60", "#FFFFFF"),
            Disciplina("Física B", 3, "pesada", ["2em", "3em"], "B", "#8E44AD", "#FFFFFF"),
            Disciplina("Química B", 3, "pesada", ["9ano", "1em", "2em", "3em"], "B", "#2980B9", "#FFFFFF"),
            Disciplina("Inglês B", 3, "media", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "B", "#2C3E50", "#FFFFFF"),
            Disciplina("Artes B", 1, "leve", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "B", "#E67E22", "#FFFFFF"),
            Disciplina("Educação Física B", 2, "pratica", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "B", "#2ECC71", "#000000"),
        ]
    
    if "salas" not in st.session_state:
        st.session_state.salas = salas_db or [
            Sala("Sala 1", 30, "normal"),
            Sala("Sala 2", 30, "normal"),
            Sala("Laboratório de Ciências", 25, "laboratório"),
            Sala("Auditório", 100, "auditório"),
        ]
    
    if "periodos" not in st.session_state:
        st.session_state.periodos = periodos_db or [
            {"nome": "1º Bimestre", "inicio": "2025-02-01", "fim": "2025-03-31", "id": str(uuid.uuid4())},
            {"nome": "2º Bimestre", "inicio": "2025-04-01", "fim": "2025-05-31", "id": str(uuid.uuid4())},
            {"nome": "3º Bimestre", "inicio": "2025-06-01", "fim": "2025-07-31", "id": str(uuid.uuid4())},
            {"nome": "4º Bimestre", "inicio": "2025-08-01", "fim": "2025-09-30", "id": str(uuid.uuid4())},
        ]
    
    if "feriados" not in st.session_state:
        st.session_state.feriados = feriados_db or [
            {"data": "2025-01-01", "motivo": "Ano Novo", "id": str(uuid.uuid4())},
            {"data": "2025-04-21", "motivo": "Tiradentes", "id": str(uuid.uuid4())},
            {"data": "2025-05-01", "motivo": "Dia do Trabalho", "id": str(uuid.uuid4())},
            {"data": "2025-09-07", "motivo": "Independência", "id": str(uuid.uuid4())},
            {"data": "2025-10-12", "motivo": "Nossa Sra. Aparecida", "id": str(uuid.uuid4())},
            {"data": "2025-11-02", "motivo": "Finados", "id": str(uuid.uuid4())},
            {"data": "2025-11-15", "motivo": "Proclamação da República", "id": str(uuid.uuid4())},
            {"data": "2025-12-25", "motivo": "Natal", "id": str(uuid.uuid4())},
        ]
    
    if "aulas" not in st.session_state:
        st.session_state.aulas = database.carregar_grade() or []