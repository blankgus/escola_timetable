import streamlit as st
from models import Turma, Professor, Disciplina, Sala, DIAS_SEMANA
import database
import uuid

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
        st.session_state.professores = database.carregar_professores() or [
            Professor("Ana A", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Ana B", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Bruno A", ["Português"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Bruno B", ["Português"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Carla A", ["História", "Geografia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Carla B", ["História", "Geografia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Diego A", ["Ciências"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Diego B", ["Ciências"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Eliane A", ["Inglês"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Eliane B", ["Inglês"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Fábio A", ["Educação Física"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Fábio B", ["Educação Física"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Gisele A", ["Artes"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Gisele B", ["Artes"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Isabel A", ["Ensino Religioso"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
            Professor("Isabel B", ["Ensino Religioso"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7,8}),
        ]
    if "disciplinas" not in st.session_state:
        st.session_state.disciplinas = database.carregar_disciplinas() or [
            Disciplina("Português", 5, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#D35400", "#FFFFFF"),
            Disciplina("Matemática", 5, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#4A90E2", "#FFFFFF"),
            Disciplina("Ciências", 3, "media", ["6ano", "7ano", "8ano"], "#1ABC9C", "#000000"),
            Disciplina("História", 3, "media", ["6ano", "7ano", "8ano", "9ano"], "#C0392B", "#FFFFFF"),
            Disciplina("Geografia", 2, "media", ["6ano", "7ano", "8ano", "9ano"], "#F39C12", "#000000"),
            Disciplina("Inglês", 2, "media", ["6ano", "7ano", "8ano", "9ano"], "#2C3E50", "#FFFFFF"),
            Disciplina("Artes", 2, "leve", ["6ano", "7ano", "8ano", "9ano"], "#E67E22", "#FFFFFF"),
            Disciplina("Educação Física", 2, "pratica", ["6ano", "7ano", "8ano", "9ano"], "#2ECC71", "#000000"),
            Disciplina("Ensino Religioso", 1, "leve", ["6ano", "7ano", "8ano", "9ano"], "#9B59B6", "#FFFFFF"),
        ]
    if "salas" not in st.session_state:
        st.session_state.salas = database.carregar_salas() or [
            Sala("Sala 1", 30, "normal"),
            Sala("Sala 2", 30, "normal"),
            Sala("Sala 3", 30, "normal"),
            Sala("Sala 4", 30, "normal"),
            Sala("Sala 5", 30, "normal"),
            Sala("Sala 6", 30, "normal"),
            Sala("Sala 7", 30, "normal"),
            Sala("Sala 8", 30, "normal"),
            Sala("Sala 9", 30, "normal"),
            Sala("Sala 10", 30, "normal"),
            Sala("Sala 11", 30, "normal"),
            Sala("Sala 12", 30, "normal"),
            Sala("Laboratório de Ciências", 25, "laboratório"),
            Sala("Auditório", 100, "auditório"),
        ]