import streamlit as st
from models import Turma, Professor, Disciplina, Sala
import database

def init_session_state():
    database.init_db()
    
    # Apagar dados antigos
    st.session_state.turmas = []
    st.session_state.professores = []
    st.session_state.disciplinas = []
    st.session_state.salas = []

    # =================== TURMAS ===================
    # EF II (6º ao 9º ano) - 25 aulas/semana
    turmas_ef = []
    for ano in ["6ano", "7ano", "8ano", "9ano"]:
        turmas_ef.append(Turma(f"{ano}A", ano, "manha"))
        turmas_ef.append(Turma(f"{ano}B", ano, "manha"))

    # EM (1º ao 3º EM) - 35 aulas/semana
    turmas_em = []
    for ano in ["1em", "2em", "3em"]:
        turmas_em.append(Turma(f"{ano}A", ano, "manha"))
        turmas_em.append(Turma(f"{ano}B", ano, "manha"))

    st.session_state.turmas = turmas_ef + turmas_em

    # =================== DISCIPLINAS ===================
    # EF II (6º ao 9º ano) - Total: 25 aulas/semana
    disciplinas_ef = [
        Disciplina("Matemática", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#4A90E2", "#FFFFFF"),
        Disciplina("Português", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#D35400", "#FFFFFF"),
        Disciplina("Ciências", 3, "media", ["6ano", "7ano", "8ano"], "#1ABC9C", "#000000"),
        Disciplina("História", 3, "media", ["6ano", "7ano", "8ano", "9ano"], "#C0392B", "#FFFFFF"),
        Disciplina("Geografia", 2, "media", ["6ano", "7ano", "8ano", "9ano"], "#F39C12", "#000000"),
        Disciplina("Inglês", 3, "media", ["6ano", "7ano", "8ano", "9ano"], "#2C3E50", "#FFFFFF"),
        Disciplina("Artes", 2, "leve", ["6ano", "7ano", "8ano", "9ano"], "#E67E22", "#FFFFFF"),
        Disciplina("Educação Física", 2, "pratica", ["6ano", "7ano", "8ano", "9ano"], "#2ECC71", "#000000"),
        Disciplina("Ensino Religioso", 2, "leve", ["6ano", "7ano", "8ano", "9ano"], "#9B59B6", "#FFFFFF"),
    ]

    # EM (1º ao 3º EM) - Total: 35 aulas/semana
    disciplinas_em = [
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

    st.session_state.disciplinas = disciplinas_ef + disciplinas_em

    # =================== PROFESSORES ===================
    # Baseado no PDF (carga horária real de cada professor)
    professores = [
        # Professores de Matemática (4h EF, 5h EM)
        Professor("Ana A", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        Professor("Ana B", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        
        # Professores de Português (4h EF, 5h EM)
        Professor("Bruno A", ["Português"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        Professor("Bruno B", ["Português"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        
        # Professores de Ciências/Biologia (3h EF, 3h EM)
        Professor("Diego A", ["Ciências", "Biologia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        Professor("Diego B", ["Ciências", "Biologia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        
        # Professores de História/Geografia (3h EF, 3h EM)
        Professor("Carla A", ["História", "Geografia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        Professor("Carla B", ["História", "Geografia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        
        # Professores de Inglês (3h EF, 3h EM)
        Professor("Eliane A", ["Inglês"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        Professor("Eliane B", ["Inglês"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        
        # Professores de Artes (2h EF, 1h EM)
        Professor("Gisele A", ["Artes"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        Professor("Gisele B", ["Artes"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        
        # Professores de Educação Física (2h EF, 2h EM)
        Professor("Fábio A", ["Educação Física"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        Professor("Fábio B", ["Educação Física"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        
        # Professores de Ensino Religioso (2h EF)
        Professor("Isabel A", ["Ensino Religioso"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        Professor("Isabel B", ["Ensino Religioso"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        
        # Professores de Física (3h EM)
        Professor("Hugo A", ["Física"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        Professor("Hugo B", ["Física"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        
        # Professores de Química (3h EM)
        Professor("Jorge A", ["Química"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        Professor("Jorge B", ["Química"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        
        # Professores de Filosofia (2h EM)
        Professor("Paulo A", ["Filosofia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        Professor("Paulo B", ["Filosofia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        
        # Professores de Sociologia (2h EM)
        Professor("Renata A", ["Sociologia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
        Professor("Renata B", ["Sociologia"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
    ]

    st.session_state.professores = professores

    # =================== SALAS ===================
    salas = [
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

    st.session_state.salas = salas

    # Salvar no banco
    try:
        database.salvar_turmas(st.session_state.turmas)
        database.salvar_disciplinas(st.session_state.disciplinas)
        database.salvar_professores(st.session_state.professores)
        database.salvar_salas(st.session_state.salas)
        st.success("✅ Cadastro completo criado com base no PDF!")
    except Exception as e:
        st.error(f"❌ Erro ao salvar cadastro: {str(e)}")