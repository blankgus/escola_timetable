# session_state.py
import streamlit as st
from models import Turma, Professor, Disciplina, Sala
import database

def init_session_state():
    database.init_db()
    if "turmas" not in st.session_state:
        st.session_state.turmas = database.carregar_turmas() or []
    if "professores" not in st.session_state:
        st.session_state.professores = database.carregar_professores() or []
    if "disciplinas" not in st.session_state:
        st.session_state.disciplinas = database.carregar_disciplinas() or []
    if "salas" not in st.session_state:
        st.session_state.salas = database.carregar_salas() or []
    if "aulas" not in st.session_state:
        st.session_state.aulas = database.carregar_grade() or []