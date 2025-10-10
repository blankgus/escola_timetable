import streamlit as st
from models import Turma, Professor, Disciplina, Sala, DisciplinaTurma, DIAS_SEMANA
import database
import uuid

def init_session_state():
    database.init_db()
    if "turmas" not in st.session_state:
        st.session_state.turmas = database.carregar_turmas() or [
            Turma("6anoA", "6ano", "manha", "pcd", [
                DisciplinaTurma("Matemática", 3, "Ana A"),
                DisciplinaTurma("Português", 3, "Bruno A"),
                DisciplinaTurma("Ciências", 2, "Diego A"),
            ]),
            Turma("6anoB", "6ano", "manha", "inclusao", [
                DisciplinaTurma("Matemática", 4, "Ana B"),
                DisciplinaTurma("Português", 4, "Bruno B"),
                DisciplinaTurma("Ciências", 2, "Diego B"),
            ]),
            Turma("7anoA", "7ano", "manha", "pcd", [
                DisciplinaTurma("Matemática", 3, "Ana A"),
                DisciplinaTurma("Português", 3, "Bruno A"),
                DisciplinaTurma("História", 2, "Carla A"),
            ]),
            Turma("7anoB", "7ano", "manha", "inclusao", [
                DisciplinaTurma("Matemática", 4, "Ana B"),
                DisciplinaTurma("Português", 4, "Bruno B"),
                DisciplinaTurma("História", 2, "Carla B"),
            ]),
            # Adicione mais turmas A e B para 8ano, 9ano, 1em, 2em, 3em
            # ...
        ]
    if "professores" not in st.session_state:
        st.session_state.professores = database.carregar_professores() or [
            Professor("Ana A", ["Matemática"], set(), set()),
            Professor("Ana B", ["Matemática"], set(), set()),
            Professor("Bruno A", ["Português"], set(), set()),
            Professor("Bruno B", ["Português"], set(), set()),
            Professor("Carla A", ["História", "Geografia"], set(), set()),
            Professor("Carla B", ["História", "Geografia"], set(), set()),
            Professor("Diego A", ["Ciências", "Biologia"], set(), set()),
            Professor("Diego B", ["Ciências", "Biologia"], set(), set()),
            Professor("Eliane A", ["Inglês"], set(), set()),
            Professor("Eliane B", ["Inglês"], set(), set()),
            Professor("Fábio A", ["Educação Física"], set(), set()),
            Professor("Fábio B", ["Educação Física"], set(), set()),
            Professor("Gisele A", ["Artes"], set(), set()),
            Professor("Gisele B", ["Artes"], set(), set()),
            Professor("Hugo A", ["Física", "Matemática"], set(), set()),
            Professor("Hugo B", ["Física", "Matemática"], set(), set()),
            Professor("Isabel A", ["Química"], set(), set()),
            Professor("Isabel B", ["Química"], set(), set()),
            Professor("Jorge A", ["Filosofia", "Sociologia"], set(), set()),
            Professor("Jorge B", ["Filosofia", "Sociologia"], set(), set()),
        ]
    if "disciplinas" not in st.session_state:
        st.session_state.disciplinas = database.carregar_disciplinas() or [
            Disciplina("Matemática", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#4A90E2", "#FFFFFF"),
            Disciplina("Português", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#D35400", "#FFFFFF"),
            Disciplina("Ciências", 3, "media", ["6ano", "7ano", "8ano"], "#1ABC9C", "#000000"),
            Disciplina("História", 3, "media", ["6ano", "7ano", "8ano", "9ano"], "#C0392B", "#FFFFFF"),
            Disciplina("Geografia", 2, "media", ["6ano", "7ano", "8ano", "9ano"], "#F39C12", "#000000"),
            Disciplina("Inglês", 3, "media", ["6ano", "7ano", "8ano", "9ano"], "#2C3E50", "#FFFFFF"),
            Disciplina("Artes", 2, "leve", ["6ano", "7ano", "8ano", "9ano"], "#E67E22", "#FFFFFF"),
            Disciplina("Educação Física", 2, "pratica", ["6ano", "7ano", "8ano", "9ano"], "#2ECC71", "#000000"),
            Disciplina("Ensino Religioso", 2, "leve", ["6ano", "7ano", "8ano", "9ano"], "#9B59B6", "#FFFFFF"),
            Disciplina("Matemática", 5, "pesada", ["1em", "2em", "3em"], "#4A90E2", "#FFFFFF"),
            Disciplina("Português", 5, "pesada", ["1em", "2em", "3em"], "#D35400", "#FFFFFF"),
            Disciplina("Biologia", 3, "media", ["1em", "2em", "3em"], "#27AE60", "#FFFFFF"),
            Disciplina("Física", 3, "pesada", ["2em", "3em"], "#8E44AD", "#FFFFFF"),
            Disciplina("Química", 3, "pesada", ["1em", "2em", "3em"], "#2980B9", "#FFFFFF"),
            Disciplina("História", 3, "media", ["1em", "2em", "3em"], "#C0392B", "#FFFFFF"),
            Disciplina("Geografia", 2, "media", ["1em"], "#F39C12", "#000000"),
            Disciplina("Inglês", 3, "media", ["1em", "2em", "3em"], "#2C3E50", "#FFFFFF"),
            Disciplina("Artes", 1, "leve", ["1em", "2em", "3em"], "#E67E22", "#FFFFFF"),
            Disciplina("Educação Física", 2, "pratica", ["1em", "2em", "3em"], "#2ECC71", "#000000"),
            Disciplina("Filosofia", 2, "leve", ["1em", "2em", "3em"], "#9B59B6", "#FFFFFF"),
            Disciplina("Sociologia", 2, "leve", ["2em", "3em"], "#16A085", "#FFFFFF"),
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