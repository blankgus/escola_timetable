import streamlit as st
import json
import pandas as pd
import io
import traceback
from session_state import init_session_state
from models import Turma, Professor, Disciplina, Sala, DIAS_SEMANA
from scheduler_ortools import GradeHorariaORTools
from export import (
    exportar_para_excel,
    exportar_para_pdf,
    gerar_relatorio_professor,
    gerar_relatorio_todos_professores,
    gerar_relatorio_disciplina_sala,
    gerar_grade_por_turma_semana,
    gerar_grade_por_sala_semana,
    gerar_grade_por_professor_semana,
    exportar_grade_por_tipo
)
import database
from simple_scheduler import SimpleGradeHoraria
from auto_save import salvar_tudo
import uuid

HORARIOS_REAIS = {
    1: "07:00-07:50",
    2: "07:50-08:40",
    3: "08:40-09:30",
    4: "09:30-10:00",
    5: "10:00-10:50",
    6: "10:50-11:40",
    7: "11:40-12:30"
}

try:
    init_session_state()
    
    # ✅ VERIFICAR SE DADOS FORAM CARREGADOS
    if not any([st.session_state.turmas, st.session_state.professores, st.session_state.disciplinas]):
        st.info("📥 Carregando dados do banco...")
        st.session_state.turmas = database.carregar_turmas() or st.session_state.turmas
        st.session_state.professores = database.carregar_professores() or st.session_state.professores
        st.session_state.disciplinas = database.carregar_disciplinas() or st.session_state.disciplinas
        st.session_state.salas = database.carregar_salas() or st.session_state.salas
        
except Exception as e:
    st.error(f"❌ Erro na inicialização: {str(e)}")
    st.code(traceback.format_exc())
    st.stop()

def color_disciplina(val):
    if val:
        for d in st.session_state.disciplinas:
            if d.nome == val:
                return f'background-color: {d.cor_fundo}; color: {d.cor_fonte}; font-weight: bold'
    if val == "RECREIO":
        return 'background-color: #FFD700; color: black; font-weight: bold; text-align: center'
    if val == "Sem Aula":
        return 'background-color: #F0F0F0; color: #666666; font-style: italic; text-align: center'
    return ''

st.set_page_config(page_title="Escola Timetable", layout="wide")
st.title("🕒 Gerador Inteligente de Grade Horária - Grupos A e B")

abas = st.tabs(["🏠 Início", "📚 Disciplinas", "👩‍🏫 Professores", "🎒 Turmas", "🏫 Salas", "📅 Calendário", "⚙️ Configurações", "🗓️ Feriados"])
aba1, aba2, aba3, aba4, aba5, aba6, aba7, aba8 = abas

# =================== ABA 2: DISCIPLINAS ===================
with aba2:
    st.header("Disciplinas")
    
    # ✅ FILTRAR POR GRUPO
    grupo_filtro = st.selectbox("Filtrar por Grupo", ["Todos", "A", "B"], key="filtro_disc")
    
    with st.form("add_disc"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome")
            carga = st.number_input("Carga", 1, 7, 3)
            tipo = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"])
            series = st.text_input("Séries", "6ano,7ano,8ano,9ano,1em,2em,3em")
        with col2:
            grupo = st.selectbox("Grupo", ["A", "B"], key="add_disc_grupo")
            cor_fundo = st.color_picker("Cor de Fundo", "#4A90E2")
            cor_fonte = st.color_picker("Cor da Fonte", "#000000")
        
        if st.form_submit_button("➕ Adicionar"):
            if nome:
                series_list = [s.strip() for s in series.split(",") if s.strip()]
                st.session_state.disciplinas.append(Disciplina(nome, carga, tipo, series_list, grupo, cor_fundo, cor_fonte))
                if salvar_tudo():
                    st.success(f"✅ Disciplina {grupo} adicionada e salva!")
                st.rerun()
    
    # ✅ FILTRAR DISCIPLINAS PARA EXIBIÇÃO
    disciplinas_exibir = st.session_state.disciplinas
    if grupo_filtro != "Todos":
        disciplinas_exibir = [d for d in st.session_state.disciplinas if d.grupo == grupo_filtro]
    
    for d in disciplinas_exibir[:]:
        with st.expander(f"{d.nome} [{d.grupo}]"):
            with st.form(f"edit_disc_{d.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    nome = st.text_input("Nome", d.nome, key=f"n_{d.id}")
                    carga = st.number_input("Carga", 1, 7, d.carga_semanal, key=f"c_{d.id}")
                    tipo = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"], 
                                       index=["pesada", "media", "leve", "pratica"].index(d.tipo), key=f"t_{d.id}")
                    series = st.text_input("Séries", ", ".join(d.series), key=f"s_{d.id}")
                with col2:
                    grupo = st.selectbox("Grupo", ["A", "B"], index=0 if d.grupo == "A" else 1, key=f"g_{d.id}")
                    cor_fundo = st.color_picker("Cor de Fundo", d.cor_fundo, key=f"cor_fundo_{d.id}")
                    cor_fonte = st.color_picker("Cor da Fonte", d.cor_fonte, key=f"cor_fonte_{d.id}")
                
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    series_list = [s.strip() for s in series.split(",") if s.strip()]
                    st.session_state.disciplinas = [
                        Disciplina(nome, carga, tipo, series_list, grupo, cor_fundo, cor_fonte, d.id) if item.id == d.id else item
                        for item in st.session_state.disciplinas
                    ]
                    if salvar_tudo():
                        st.success("✅ Disciplina atualizada e salva!")
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.disciplinas = [
                        item for item in st.session_state.disciplinas if item.id != d.id
                    ]
                    if salvar_tudo():
                        st.success("✅ Disciplina excluída e salva!")
                    st.rerun()

# =================== ABA 3: PROFESSORES ===================
with aba3:
    st.header("Professores")
    
    # ✅ FILTRAR POR GRUPO
    grupo_filtro_prof = st.selectbox("Filtrar por Grupo", ["Todos", "A", "B", "AMBOS"], key="filtro_prof")
    
    disc_nomes = [d.nome for d in st.session_state.disciplinas] or ["Nenhuma"]
    with st.form("add_prof"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome")
            discs = st.multiselect("Disciplinas", disc_nomes)
            grupo = st.selectbox("Grupo", ["A", "B", "AMBOS"], key="add_prof_grupo")
        with col2:
            dias = st.multiselect("Disponibilidade", DIAS_SEMANA, default=["seg", "ter", "qua", "qui", "sex"])
        
        if st.form_submit_button("➕ Adicionar"):
            if nome and discs:
                st.session_state.professores.append(Professor(nome, discs, set(dias), grupo))
                if salvar_tudo():
                    st.success(f"✅ Professor {grupo} adicionado e salvo!")
                st.rerun()
    
    # ✅ FILTRAR PROFESSORES PARA EXIBIÇÃO
    professores_exibir = st.session_state.professores
    if grupo_filtro_prof != "Todos":
        professores_exibir = [p for p in st.session_state.professores if p.grupo == grupo_filtro_prof]
    
    for p in professores_exibir[:]:
        with st.expander(f"{p.nome} [{p.grupo}]"):
            with st.form(f"edit_prof_{p.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    nome = st.text_input("Nome", p.nome, key=f"pn_{p.id}")
                    discs_validas = [d for d in p.disciplinas if d in disc_nomes]
                    discs = st.multiselect("Disciplinas", disc_nomes, default=discs_validas, key=f"pd_{p.id}")
                    grupo = st.selectbox("Grupo", ["A", "B", "AMBOS"], 
                                       index=["A", "B", "AMBOS"].index(p.grupo), key=f"pg_{p.id}")
                with col2:
                    dias = st.multiselect("Disponibilidade", DIAS_SEMANA, 
                                         default=list(p.disponibilidade), key=f"pdias_{p.id}")
                
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.professores = [
                        Professor(nome, discs, set(dias), grupo, p.id) if item.id == p.id else item
                        for item in st.session_state.professores
                    ]
                    if salvar_tudo():
                        st.success("✅ Professor atualizado e salvo!")
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.professores = [
                        item for item in st.session_state.professores if item.id != p.id
                    ]
                    if salvar_tudo():
                        st.success("✅ Professor excluído e salvo!")
                    st.rerun()

# =================== ABA 4: TURMAS ===================
with aba4:
    st.header("Turmas")
    
    # ✅ FILTRAR POR GRUPO
    grupo_filtro_turma = st.selectbox("Filtrar por Grupo", ["Todos", "A", "B"], key="filtro_turma")
    
    with st.form("add_turma"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome (ex: 8anoA)")
            serie = st.text_input("Série (ex: 8ano)")
        with col2:
            turno = st.selectbox("Turno", ["manha", "tarde"])
            grupo = st.selectbox("Grupo", ["A", "B"], key="add_turma_grupo")
        
        if st.form_submit_button("➕ Adicionar"):
            if nome and serie:
                st.session_state.turmas.append(Turma(nome, serie, turno, grupo))
                if salvar_tudo():
                    st.success(f"✅ Turma {grupo} adicionada e salva!")
                st.rerun()
    
    # ✅ FILTRAR TURMAS PARA EXIBIÇÃO
    turmas_exibir = st.session_state.turmas
    if grupo_filtro_turma != "Todos":
        turmas_exibir = [t for t in st.session_state.turmas if t.grupo == grupo_filtro_turma]
    
    for t in turmas_exibir[:]:
        with st.expander(f"{t.nome} [{t.grupo}]"):
            with st.form(f"edit_turma_{t.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    nome = st.text_input("Nome", t.nome, key=f"tn_{t.id}")
                    serie = st.text_input("Série", t.serie, key=f"ts_{t.id}")
                with col2:
                    turno = st.selectbox("Turno", ["manha", "tarde"], 
                                        index=["manha", "tarde"].index(t.turno), key=f"tt_{t.id}")
                    grupo = st.selectbox("Grupo", ["A", "B"], 
                                       index=0 if t.grupo == "A" else 1, key=f"tg_{t.id}")
                
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.turmas = [
                        Turma(nome, serie, turno, grupo, t.id) if item.id == t.id else item
                        for item in st.session_state.turmas
                    ]
                    if salvar_tudo():
                        st.success("✅ Turma atualizada e salva!")
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.turmas = [
                        item for item in st.session_state.turmas if item.id != t.id
                    ]
                    if salvar_tudo():
                        st.success("✅ Turma excluída e salva!")
                    st.rerun()

# =================== ABA 1: INÍCIO ===================
with aba1:
    st.header("Gerar Grade Horária")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Salvar Tudo no Banco"):
            try:
                if salvar_tudo():
                    st.success("✅ Todos os dados salvos!")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
    with col2:
        if st.button("🔄 Carregar do Banco"):
            try:
                st.session_state.turmas = database.carregar_turmas()
                st.session_state.professores = database.carregar_professores()
                st.session_state.disciplinas = database.carregar_disciplinas()
                st.session_state.salas = database.carregar_salas()
                st.session_state.periodos = database.carregar_periodos() or []
                st.session_state.feriados = database.carregar_feriados() or []
                st.session_state.aulas = database.carregar_grade()
                st.success("✅ Dados carregados!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
    with col3:
        if st.button("🗃️ Ver Status do Banco"):
            try:
                st.write(f"📚 Turmas: {len(database.carregar_turmas())}")
                st.write(f"👨‍🏫 Professores: {len(database.carregar_professores())}")
                st.write(f"📖 Disciplinas: {len(database.carregar_disciplinas())}")
                st.write(f"🏫 Salas: {len(database.carregar_salas())}")
                st.write(f"📅 Aulas na grade: {len(database.carregar_grade())}")
                
                # ✅ ESTATÍSTICAS POR GRUPO
                turmas_a = [t for t in database.carregar_turmas() if t.grupo == "A"]
                turmas_b = [t for t in database.carregar_turmas() if t.grupo == "B"]
                st.write(f"🎯 Turmas Grupo A: {len(turmas_a)}")
                st.write(f"🎯 Turmas Grupo B: {len(turmas_b)}")
                
            except Exception as e:
                st.error(f"❌ Erro ao verificar banco: {str(e)}")
    
    if not st.session_state.turmas or not st.session_state.professores or not st.session_state.disciplinas:
        st.warning("⚠️ Cadastre dados antes de gerar grade.")
        st.stop()
    
    st.subheader("🎯 Escolha o grupo para gerar grade")
    
    grupo_grade = st.radio(
        "Grupo da Grade",
        ["Grupo A", "Grupo B", "Ambos os Grupos"],
        index=0
    )
    
    tipo_grade = st.radio(
        "Tipo de Grade",
        ["Grade Completa (Turmas)", "Grade por Turma", "Grade por Sala", "Grade por Professor"],
        index=0
    )
    
    if st.button("🚀 Gerar Grade"):
        with st.spinner("Gerando grade..."):
            try:
                # ✅ FILTRAR DADOS POR GRUPO
                if grupo_grade == "Grupo A":
                    turmas_filtradas = [t for t in st.session_state.turmas if t.grupo == "A"]
                    professores_filtrados = [p for p in st.session_state.professores if p.grupo in ["A", "AMBOS"]]
                    disciplinas_filtradas = [d for d in st.session_state.disciplinas if d.grupo == "A"]
                elif grupo_grade == "Grupo B":
                    turmas_filtradas = [t for t in st.session_state.turmas if t.grupo == "B"]
                    professores_filtrados = [p for p in st.session_state.professores if p.grupo in ["B", "AMBOS"]]
                    disciplinas_filtradas = [d for d in st.session_state.disciplinas if d.grupo == "B"]
                else:  # Ambos
                    turmas_filtradas = st.session_state.turmas
                    professores_filtrados = st.session_state.professores
                    disciplinas_filtradas = st.session_state.disciplinas
                
                grade = GradeHorariaORTools(
                    turmas_filtradas,
                    professores_filtrados,
                    disciplinas_filtradas,
                    relaxar_horario_ideal=st.session_state.get("relaxar_horario_ideal", False)
                )
                aulas = grade.resolver()
                metodo = "Google OR-Tools"
                
            except Exception as e1:
                st.warning("⚠️ OR-Tools falhou. Tentando método simples...")
                try:
                    simple_grade = SimpleGradeHoraria(
                        turmas_filtradas,
                        professores_filtrados,
                        disciplinas_filtradas
                    )
                    aulas = simple_grade.gerar_grade()
                    metodo = "Algoritmo Simples"
                except Exception as e2:
                    st.error(f"❌ Falha total: {str(e2)}")
                    st.stop()
            
            st.session_state.aulas = aulas
            if salvar_tudo():
                st.success(f"✅ Grade {grupo_grade} gerada com {metodo} e salva!")

            # EXIBIR GRADE (código existente continua igual)
            if tipo_grade == "Grade Completa (Turmas)":
                df = pd.DataFrame([
                    {"Turma": a.turma, "Disciplina": a.disciplina, "Professor": a.professor, "Dia": a.dia, "Horário": a.horario, "Sala": a.sala, "Grupo": a.grupo}
                    for a in aulas
                ])
                # ... resto do código para exibir grade continua igual

# CONTINUAÇÃO DO CÓDIGO PARA AS OUTRAS ABAS (SALAS, CALENDÁRIO, FERIADOS, CONFIGURAÇÕES)
# ... (o código das outras abas permanece similar, apenas adicionando auto-save)