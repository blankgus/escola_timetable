# session_state.py
import streamlit as st
from models import Turma, Professor, Disciplina, Sala, DisciplinaTurma
import database

def init_session_state():
    database.init_db()
    if "turmas" not in st.session_state:
        st.session_state.turmas = database.carregar_turmas() or [
            Turma("6anoA", "6ano", "manha", [
                DisciplinaTurma("Matemática", 4, "Ana A"),
                DisciplinaTurma("Português", 4, "Bruno A"),
            ]),
            Turma("6anoB", "6ano", "manha", [
                DisciplinaTurma("Matemática", 4, "Ana B"),
                DisciplinaTurma("Português", 4, "Bruno B"),
            ]),
            # Adicione mais turmas conforme necessário
        ]
    if "professores" not in st.session_state:
        st.session_state.professores = database.carregar_professores() or [
            Professor("Ana A", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
            Professor("Ana B", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
            Professor("Bruno A", ["Português"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
            Professor("Bruno B", ["Português"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
            # Adicione mais professores conforme necessário
        ]
    if "disciplinas" not in st.session_state:
        st.session_state.disciplinas = database.carregar_disciplinas() or [
            Disciplina("Matemática", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#4A90E2", "#FFFFFF"),
            Disciplina("Português", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#D35400", "#FFFFFF"),
            # Adicione mais disciplinas conforme necessário
        ]
    if "salas" not in st.session_state:
        st.session_state.salas = database.carregar_salas() or [
            Sala("Sala 1", 30, "normal"),
            Sala("Sala 2", 30, "normal"),
            # Adicione mais salas conforme necessário
        ]