import streamlit as st
from models import Turma, Professor, Disciplina, Sala
import database
from importador import carregar_professores_do_excel

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
        ]
    if "professores" not in st.session_state:
        # Tenta carregar do banco
        st.session_state.professores = database.carregar_professores()
        # Se banco vazio, tenta carregar do Excel
        if not st.session_state.professores:
            try:
                st.session_state.professores = carregar_professores_do_excel("prodis.xlsx")
            except FileNotFoundError:
                # Se não existir Excel, inicializa com os dados padrão
                st.session_state.professores = [
                    Professor("Ana A", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                    Professor("Ana B", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                    # ... adicione mais se quiser
                ]
        # Se banco tem dados, já foi carregado acima
    if "disciplinas" not in st.session_state:
        st.session_state.disciplinas = database.carregar_disciplinas() or [
            Disciplina("Português", 5, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#D35400", "#FFFFFF"),
            Disciplina("Matemática", 5, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#4A90E2", "#FFFFFF"),
            # ... adicione mais conforme seu Excel
        ]
    if "salas" not in st.session_state:
        st.session_state.salas = database.carregar_salas() or [
            Sala("Sala 1", 30, "normal"),
            Sala("Sala 2", 30, "normal"),
            # ... adicione mais se quiser
        ]
    if "aulas" not in st.session_state:
        st.session_state.aulas = database.carregar_grade()