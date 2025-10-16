# session_state.py
import streamlit as st
from models import Turma, Professor, Disciplina, Sala
import database

def init_session_state():
    database.init_db()
    if "turmas" not in st.session_state:
        st.session_state.turmas = database.carregar_turmas() or [
            Turma("6anoA", "6ano", "manha"),
            Turma("6anoB", "6ano", "manha"),
            Turma("7anoA", "7ano", "manha"),
            Turma("7anoB", "7ano", "manha"),
            Turma("8anoA", "8ano", "manha"),
            Turma("8anoB", "8ano", "manha"),
            Turma("9anoA", "9ano", "manha"),
            Turma("9anoB", "9ano", "manha"),
            Turma("1emA", "1em", "manha"),
            Turma("1emB", "1em", "manha"),
            Turma("2emA", "2em", "manha"),
            Turma("2emB", "2em", "manha"),
            Turma("3emA", "3em", "manha"),
            Turma("3emB", "3em", "manha"),
         ]
    if "professores" not in st.session_state:
        st.session_state.professores = database.carregar_professores() or [
            Professor("Heliana", ["Português"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
            Professor("Deise", ["Português"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
            # ... adicione mais professores conforme necessário ...
        ]
    if "disciplinas" not in st.session_state:
        st.session_state.disciplinas = database.carregar_disciplinas() or [
            Disciplina("Português", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#D35400", "#FFFFFF"),
            Disciplina("Matemática", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#4A90E2", "#FFFFFF"),
            # ... adicione mais disciplinas conforme necessário ...
        ]
    if "salas" not in st.session_state:
        st.session_state.salas = database.carregar_salas() or [
            Sala("Sala 1", 30, "normal"),
            Sala("Sala 2", 30, "normal"),
            # ... adicione mais salas conforme necessário ...
        ]
