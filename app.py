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
    gerar_grade_por_turma_semana,
    gerar_grade_por_sala_semana,
    gerar_grade_por_professor_semana
)
import database
from simple_scheduler import SimpleGradeHoraria
import uuid

HORARIOS_REAIS = {
    1: "07:00-07:50",
    2: "07:50-08:40",
    3: "08:40-09:30",
    4: "09:30-10:00",  # INTERVALO
    5: "10:00-10:50",
    6: "10:50-11:40",
    7: "11:40-12:30"
}

try:
    init_session_state()
    if "aulas" not in st.session_state:
        st.session_state.aulas = []
except Exception as e:
    st.error(f"❌ Erro na inicialização: {str(e)}")
    st.code(traceback.format_exc())
    st.stop()

def color_disciplina(val):
    if val:
        for d in st.session_state.disciplinas:
            if d.nome == val:
                return f'background-color: {d.cor_fundo}; color: {d.cor_fonte}; font-weight: bold'
    if val == "INTERVALO":
        return 'background-color: #FFD700; color: black; font-weight: bold; text-align: center'
    if val == "Sem Aula":
        return 'background-color: #F0F0F0; color: #666666; font-style: italic; text-align: center'
    return ''

st.set_page_config(page_title="Escola Timetable", layout="wide")
st.title("🕒 Gerador Inteligente de Grade Horária")

abas = st.tabs([
    "🏠 Início", "📚 Disciplinas", "👩‍🏫 Professores", "🎒 Turmas",
    "🏫 Salas", "📅 Calendário", "⚙️ Configurações", "🗓️ Feriados",
    "🎒 Grade por Turma", "🏫 Grade por Sala", "👨‍🏫 Grade por Professor"
])
(aba1, aba2, aba3, aba4, aba5, aba6, aba7, aba8, aba9, aba10, aba11) = abas

# =================== ABA 2: DISCIPLINAS ===================
with aba2:
    st.header("Disciplinas")
    with st.form("add_disc"):
        nome = st.text_input("Nome")
        carga = st.number_input("Carga", 1, 7, 3)
        tipo = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"])
        series = st.text_input("Séries", "6ano,7ano,8ano,9ano")
        cor_fundo = st.color_picker("Cor de Fundo", "#4A90E2")
        cor_fonte = st.color_picker("Cor da Fonte", "#000000")
        if st.form_submit_button("➕ Adicionar"):
            if nome:
                series_list = [s.strip() for s in series.split(",") if s.strip()]
                st.session_state.disciplinas.append(Disciplina(nome, carga, tipo, series_list, cor_fundo, cor_fonte))
                st.rerun()
    for d in st.session_state.disciplinas[:]:
        with st.expander(f"{d.nome}"):
            with st.form(f"edit_disc_{d.id}"):
                nome = st.text_input("Nome", d.nome, key=f"n_{d.id}")
                carga = st.number_input("Carga", 1, 7, d.carga_semanal, key=f"c_{d.id}")
                tipo = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"], 
                                   index=["pesada", "media", "leve", "pratica"].index(d.tipo), key=f"t_{d.id}")
                series = st.text_input("Séries", ", ".join(d.series), key=f"s_{d.id}")
                cor_fundo = st.color_picker("Cor de Fundo", d.cor_fundo, key=f"cor_fundo_{d.id}")
                cor_fonte = st.color_picker("Cor da Fonte", d.cor_fonte, key=f"cor_fonte_{d.id}")
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    series_list = [s.strip() for s in series.split(",") if s.strip()]
                    st.session_state.disciplinas = [
                        Disciplina(nome, carga, tipo, series_list, cor_fundo, cor_fonte, d.id) if item.id == d.id else item
                        for item in st.session_state.disciplinas
                    ]
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.disciplinas = [
                        item for item in st.session_state.disciplinas if item.id != d.id
                    ]
                    st.rerun()

# =================== ABA 3: PROFESSORES ===================
with aba3:
    st.header("Professores")
    disc_nomes = [d.nome for d in st.session_state.disciplinas] or ["Nenhuma"]
    with st.form("add_prof"):
        nome = st.text_input("Nome")
        discs = st.multiselect("Disciplinas", disc_nomes)
        dias = st.multiselect("Dias disponíveis", DIAS_SEMANA, default=["seg", "ter", "qua", "qui", "sex"])
        horarios_disp = st.multiselect("Horários disponíveis", [1,2,3,5,6,7], default=[1,2,3,5,6,7])
        restricoes_text = st.text_input("Restrições Específicas (ex: seg_4,qua_7)", "")
        if st.form_submit_button("➕ Adicionar"):
            if nome and discs:
                restricoes_set = set([r.strip() for r in restricoes_text.split(",") if r.strip()])
                st.session_state.professores.append(Professor(
                    nome=nome,
                    disciplinas=discs,
                    disponibilidade_dias=set(dias),
                    disponibilidade_horarios=set(horarios_disp),
                    restricoes=restricoes_set
                ))
                st.rerun()
    for p in st.session_state.professores[:]:
        with st.expander(p.nome):
            with st.form(f"edit_prof_{p.id}"):
                nome = st.text_input("Nome", p.nome, key=f"pn_{p.id}")
                discs_validas = [d for d in p.disciplinas if d in disc_nomes]
                discs = st.multiselect("Disciplinas", disc_nomes, default=discs_validas, key=f"pd_{p.id}")
                dias = st.multiselect("Dias disponíveis", DIAS_SEMANA, 
                                     default=list(p.disponibilidade_dias), key=f"pdias_{p.id}")
                horarios_disp = st.multiselect("Horários disponíveis", [1,2,3,5,6,7],
                                              default=list(p.disponibilidade_horarios), key=f"phor_{p.id}")
                restricoes_text = st.text_input("Restrições Específicas (ex: seg_4,qua_7)", ", ".join(p.restricoes), key=f"restr_{p.id}")
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    restricoes_set = set([r.strip() for r in restricoes_text.split(",") if r.strip()])
                    st.session_state.professores = [
                        Professor(nome, discs, set(dias), set(horarios_disp), restricoes_set, p.id) if item.id == p.id else item
                        for item in st.session_state.professores
                    ]
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.professores = [
                        item for item in st.session_state.professores if item.id != p.id
                    ]
                    st.rerun()

# =================== ABA 4: TURMAS ===================
with aba4:
    st.header("Turmas")
    with st.form("add_turma"):
        nome = st.text_input("Nome (ex: 8anoA)")
        serie = st.text_input("Série (ex: 8ano)")
        turno = st.selectbox("Turno", ["manha", "tarde"])
        if st.form_submit_button("➕ Adicionar"):
            if nome and serie:
                st.session_state.turmas.append(Turma(nome, serie, turno))
                st.rerun()
    for t in st.session_state.turmas[:]:
        with st.expander(f"{t.nome}"):
            with st.form(f"edit_turma_{t.id}"):
                nome = st.text_input("Nome", t.nome, key=f"tn_{t.id}")
                serie = st.text_input("Série", t.serie, key=f"ts_{t.id}")
                turno = st.selectbox("Turno", ["manha", "tarde"], 
                                    index=["manha", "tarde"].index(t.turno), key=f"tt_{t.id}")
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.turmas = [
                        Turma(nome, serie, turno, t.id) if item.id == t.id else item
                        for item in st.session_state.turmas
                    ]
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.turmas = [
                        item for item in st.session_state.turmas if item.id != t.id
                    ]
                    st.rerun()

# =================== ABA 5: SALAS ===================
with aba5:
    st.header("Salas")
    with st.form("add_sala"):
        nome = st.text_input("Nome")
        cap = st.number_input("Capacidade", 1, 100, 30)
        tipo = st.selectbox("Tipo", ["normal", "laboratório", "auditório"])
        if st.form_submit_button("➕ Adicionar"):
            if nome:
                st.session_state.salas.append(Sala(nome, cap, tipo))
                st.rerun()
    for s in st.session_state.salas[:]:
        with st.expander(s.nome):
            with st.form(f"edit_sala_{s.id}"):
                nome = st.text_input("Nome", s.nome, key=f"sn_{s.id}")
                cap = st.number_input("Capacidade", 1, 100, s.capacidade, key=f"sc_{s.id}")
                tipo = st.selectbox("Tipo", ["normal", "laboratório", "auditório"], 
                                   index=["normal", "laboratório", "auditório"].index(s.tipo), key=f"st_{s.id}")
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.salas = [
                        Sala(nome, cap, tipo, s.id) if item.id == s.id else item
                        for item in st.session_state.salas
                    ]
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.salas = [
                        item for item in st.session_state.salas if item.id != s.id
                    ]
                    st.rerun()

# =================== ABA 6: CALENDÁRIO ===================
with aba6:
    st.header("Períodos")
    if "periodos" not in st.session_state:
        st.session_state.periodos = []
    with st.form("add_periodo"):
        nome = st.text_input("Nome (ex: 1º Bimestre)")
        inicio = st.date_input("Início")
        fim = st.date_input("Fim")
        if st.form_submit_button("➕ Adicionar"):
            if nome:
                st.session_state.periodos.append({
                    "nome": nome,
                    "inicio": str(inicio),
                    "fim": str(fim),
                    "id": str(uuid.uuid4())
                })
                st.rerun()
    for p in st.session_state.periodos[:]:
        with st.expander(p["nome"]):
            with st.form(f"edit_periodo_{p['id']}"):
                nome = st.text_input("Nome", p["nome"], key=f"pn_{p['id']}")
                inicio = st.date_input("Início", value=pd.to_datetime(p["inicio"]), key=f"pi_{p['id']}")
                fim = st.date_input("Fim", value=pd.to_datetime(p["fim"]), key=f"pf_{p['id']}")
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.periodos = [
                        {**item, "nome": nome, "inicio": str(inicio), "fim": str(fim)} 
                        if item["id"] == p["id"] else item
                        for item in st.session_state.periodos
                    ]
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.periodos = [
                        item for item in st.session_state.periodos if item.id != p["id"]
                    ]
                    st.rerun()

# =================== ABA 8: FERIADOS ===================
with aba8:
    st.header("Feriados e Dias Sem Aula")
    if "feriados" not in st.session_state:
        st.session_state.feriados = []
    with st.form("add_feriado"):
        data = st.date_input("Data")
        motivo = st.text_input("Motivo")
        if st.form_submit_button("➕ Adicionar Feriado"):
            st.session_state.feriados.append({
                "data": str(data),
                "motivo": motivo,
                "id": str(uuid.uuid4())
            })
            st.rerun()
    for f in st.session_state.feriados[:]:
        with st.expander(f"{f['data']} - {f['motivo']}"):
            with st.form(f"edit_feriado_{f['id']}"):
                data = st.date_input("Data", value=pd.to_datetime(f["data"]), key=f"data_{f['id']}")
                motivo = st.text_input("Motivo", f["motivo"], key=f"motivo_{f['id']}")
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.feriados = [
                        {**item, "data": str(data), "motivo": motivo} 
                        if item["id"] == f["id"] else item
                        for item in st.session_state.feriados
                    ]
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.feriados = [
                        item for item in st.session_state.feriados if item.id != f["id"]
                    ]
                    st.rerun()

# =================== ABA 7: CONFIGURAÇÕES ===================
with aba7:
    st.header("Configurações Avançadas")
    st.session_state.relaxar_horario_ideal = st.checkbox(
        "✅ Relaxar horário ideal (disciplinas pesadas podem ser à tarde)",
        value=st.session_state.get("relaxar_horario_ideal", False)
    )
    st.session_state.max_aulas_professor_dia = st.slider(
        "Máximo de aulas por professor por dia",
        min_value=4,
        max_value=7,
        value=st.session_state.get("max_aulas_professor_dia", 7)
    )
    st.session_state.permitir_janelas = st.checkbox(
        "Permitir janelas para professores",
        value=st.session_state.get("permitir_janelas", True)
    )
    if st.button("🔍 Analisar Viabilidade"):
        total_aulas = sum(
            disc.carga_semanal 
            for turma in st.session_state.turmas 
            for disc in st.session_state.disciplinas 
            if turma.serie in disc.series
        )
        capacidade_total = sum(
            len(prof.disponibilidade_dias) * len(prof.disponibilidade_horarios)
            for prof in st.session_state.professores
        )
        st.metric("Aulas necessárias", total_aulas)
        st.metric("Capacidade total", capacidade_total)
        if capacidade_total >= total_aulas:
            st.success("✅ Capacidade suficiente")
        else:
            st.error("⚠️ Capacidade insuficiente")

# =================== ABA 1: INÍCIO ===================
with aba1:
    st.header("Gerar Grade Horária")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Salvar no Banco"):
            try:
                database.salvar_turmas(st.session_state.turmas)
                database.salvar_professores(st.session_state.professores)
                database.salvar_disciplinas(st.session_state.disciplinas)
                database.salvar_salas(st)
