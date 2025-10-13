import streamlit as st
from models import Turma, Professor, Disciplina, Sala
import database
from importador import carregar_dados_do_excel

def init_session_state():
    database.init_db()
    if "turmas" not in st.session_state:
        # Tenta carregar do banco
        st.session_state.turmas = database.carregar_turmas()
        # Se banco vazio, tenta carregar do Excel
        if not st.session_state.turmas:
            try:
                turmas, profs, discs, salas = carregar_dados_do_excel("dados_reais.xlsx")
                st.session_state.turmas = turmas
                st.session_state.professores = profs
                st.session_state.disciplinas = discs
                st.session_state.salas = salas
            except FileNotFoundError:
                # Se não existir Excel, inicializa vazio
                st.session_state.turmas = []
                st.session_state.professores = []
                st.session_state.disciplinas = []
                st.session_state.salas = []
        else:
            # Se banco tem dados, carrega do banco
            st.session_state.professores = database.carregar_professores()
            st.session_state.disciplinas = database.carregar_disciplinas()
            st.session_state.salas = database.carregar_salas()
    if "aulas" not in st.session_state:
        st.session_state.aulas = database.carregar_grade()