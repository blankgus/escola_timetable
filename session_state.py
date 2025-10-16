# session_state.py
import streamlit as st
from models import Turma, Professor, Disciplina, Sala
import database

def init_session_state():
    database.init_db()
    
    # --- TURMAS ---
    if "turmas" not in st.session_state:
        turmas_carregadas = database.carregar_turmas()
        if turmas_carregadas:
            st.session_state.turmas = turmas_carregadas
        else:
            # Só carrega dados iniciais se NÃO houver nada salvo
            st.session_state.turmas = [
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

    # --- PROFESSORES ---
    if "professores" not in st.session_state:
        professores_carregados = database.carregar_professores()
        if professores_carregados:
            st.session_state.professores = professores_carregados
        else:
            # Só carrega dados iniciais se NÃO houver nada salvo
            st.session_state.professores = [
                Professor("Heliana", ["Português"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Deise", ["Português"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Loide", ["Português"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Tatiane", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Ricardo", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Laís", ["História"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Waldemar", ["História"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Rene", ["Geografia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Vladmir", ["Química"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Zabuor", ["Química"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Gisele", ["Geografia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Marina", ["Biologia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("César", ["Informática/Física"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Anna Maria", ["Filosofia/Sociologia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Marcão", ["Educação Física"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Andréia", ["Educação Física"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Vanessa", ["Arte"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
                Professor("Andréia Barreto", ["Dinâmica/Vida Pratica"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
            ]

    # --- DISCIPLINAS ---
    if "disciplinas" not in st.session_state:
        disciplinas_carregadas = database.carregar_disciplinas()
        if disciplinas_carregadas:
            st.session_state.disciplinas = disciplinas_carregadas
        else:
            # Só carrega dados iniciais se NÃO houver nada salvo
            st.session_state.disciplinas = [
                Disciplina("Português", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#D35400", "#FFFFFF"),
                Disciplina("Matemática", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#4A90E2", "#FFFFFF"),
                Disciplina("Ciências", 3, "media", ["6ano", "7ano", "8ano"], "#1ABC9C", "#000000"),
                Disciplina("História", 3, "media", ["6ano", "7ano", "8ano", "9ano"], "#C0392B", "#FFFFFF"),
                Disciplina("Geografia", 2, "media", ["6ano", "7ano", "8ano", "9ano"], "#F39C12", "#000000"),
                Disciplina("Inglês", 2, "media", ["6ano", "7ano", "8ano", "9ano"], "#2C3E50", "#FFFFFF"),
                Disciplina("Artes", 2, "leve", ["6ano", "7ano", "8ano", "9ano"], "#E67E22", "#FFFFFF"),
                Disciplina("Educação Física", 2, "pratica", ["6ano", "7ano", "8ano", "9ano"], "#2ECC71", "#000000"),
                Disciplina("Ensino Religioso", 1, "leve", ["6ano", "7ano", "8ano", "9ano"], "#9B59B6", "#FFFFFF"),
                
                # Ensino Médio
                Disciplina("Matemática", 5, "pesada", ["1em", "2em", "3em"], "#4A90E2", "#FFFFFF"),
                Disciplina("Português", 5, "pesada", ["1em", "2em", "3em"], "#D35400", "#FFFFFF"),
                Disciplina("Biologia", 3, "media", ["1em", "2em"], "#27AE60", "#FFFFFF"),
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

    # --- SALAS ---
    if "salas" not in st.session_state:
        salas_carregadas = database.carregar_salas()
        if salas_carregadas:
            st.session_state.salas = salas_carregadas
        else:
            # Só carrega dados iniciais se NÃO houver nada salvo
            st.session_state.salas = [
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