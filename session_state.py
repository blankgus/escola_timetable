import streamlit as st
from models import Turma, Professor, Disciplina, Sala
import database
import uuid

def init_session_state():
    database.init_db()
    
    if "turmas" not in st.session_state:
        st.session_state.turmas = database.carregar_turmas() or [
            Turma("6anoA", "6ano", "manha"),
            Turma("7anoA", "7ano", "manha"),
            Turma("8anoA", "8ano", "manha"),
            Turma("9anoA", "9ano", "manha"),
            Turma("1emA", "1em", "manha"),
            Turma("2emA", "2em", "manha"),
            Turma("3emA", "3em", "manha"),
        ]
    
    if "professores" not in st.session_state:
        st.session_state.professores = database.carregar_professores() or [
            Professor("Ana", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Bruno", ["Português"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Carla", ["História", "Geografia"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Diego", ["Ciências", "Biologia"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Eliane", ["Inglês"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Fábio", ["Educação Física"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Gisele", ["Artes"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Hugo", ["Física", "Matemática"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Isabel", ["Química"], {"seg", "ter", "qua", "qui", "sex"}),
            Professor("Jorge", ["Filosofia", "Sociologia"], {"seg", "ter", "qua", "qui", "sex"}),
        ]
    
    if "disciplinas" not in st.session_state:
        st.session_state.disciplinas = database.carregar_disciplinas() or [
            Disciplina("Matemática", 4, "pesada", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "#4A90E2", "#FFFFFF"),
            Disciplina("Português", 4, "pesada", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "#D35400", "#FFFFFF"),
            Disciplina("Ciências", 3, "media", ["6ano", "7ano", "8ano"], "#1ABC9C", "#000000"),
            Disciplina("Biologia", 3, "media", ["9ano", "1em", "2em", "3em"], "#27AE60", "#FFFFFF"),
            Disciplina("Física", 3, "pesada", ["2em", "3em"], "#8E44AD", "#FFFFFF"),
            Disciplina("Química", 3, "pesada", ["9ano", "1em", "2em", "3em"], "#2980B9", "#FFFFFF"),
            Disciplina("História", 3, "media", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "#C0392B", "#FFFFFF"),
            Disciplina("Geografia", 3, "media", ["6ano", "7ano", "8ano", "9ano", "1em"], "#F39C12", "#000000"),
            Disciplina("Inglês", 3, "media", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "#2C3E50", "#FFFFFF"),
            Disciplina("Artes", 1, "leve", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "#E67E22", "#FFFFFF"),
            Disciplina("Educação Física", 2, "pratica", ["6ano", "7ano", "8ano", "9ano", "1em", "2em", "3em"], "#2ECC71", "#000000"),
            Disciplina("Filosofia", 2, "leve", ["1em", "2em", "3em"], "#9B59B6", "#FFFFFF"),
            Disciplina("Sociologia", 2, "leve", ["2em", "3em"], "#16A085", "#FFFFFF"),
        ]
    
    if "salas" not in st.session_state:
        st.session_state.salas = database.carregar_salas() or [
            Sala("Sala 1", 30, "normal"),
            Sala("Sala 2", 30, "normal"),
            Sala("Laboratório de Ciências", 25, "laboratório"),
            Sala("Auditório", 100, "auditório"),
        ]
    
    if "periodos" not in st.session_state:
        periodos_db = database.carregar_periodos()
        if periodos_db:
            st.session_state.periodos = periodos_db
        else:
            st.session_state.periodos = [
                {"nome": "1º Bimestre", "inicio": "2025-02-01", "fim": "2025-03-31", "id": str(uuid.uuid4())},
                {"nome": "2º Bimestre", "inicio": "2025-04-01", "fim": "2025-05-31", "id": str(uuid.uuid4())},
                {"nome": "3º Bimestre", "inicio": "2025-06-01", "fim": "2025-07-31", "id": str(uuid.uuid4())},
                {"nome": "4º Bimestre", "inicio": "2025-08-01", "fim": "2025-09-30", "id": str(uuid.uuid4())},
            ]
    
    if "feriados" not in st.session_state:
        feriados_db = database.carregar_feriados()
        if feriados_db:
            st.session_state.feriados = feriados_db
        else:
            st.session_state.feriados = [
                {"data": "2025-01-01", "motivo": "Ano Novo", "id": str(uuid.uuid4())},
                {"data": "2025-04-21", "motivo": "Tiradentes", "id": str(uuid.uuid4())},
                {"data": "2025-05-01", "motivo": "Dia do Trabalho", "id": str(uuid.uuid4())},
                {"data": "2025-09-07", "motivo": "Independência", "id": str(uuid.uuid4())},
                {"data": "2025-10-12", "motivo": "Nossa Sra. Aparecida", "id": str(uuid.uuid4())},
                {"data": "2025-11-02", "motivo": "Finados", "id": str(uuid.uuid4())},
                {"data": "2025-11-15", "motivo": "Proclamação da República", "id": str(uuid.uuid4())},
                {"data": "2025-12-25", "motivo": "Natal", "id": str(uuid.uuid4())},
            ]