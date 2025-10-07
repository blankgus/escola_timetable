import streamlit as st
import json
import pandas as pd
import io
import traceback
from session_state import init_session_state
from models import Turma, Professor, Disciplina, Sala
from scheduler_ortools import GradeHorariaORTools
from export import exportar_para_excel, exportar_para_pdf
import database
from simple_scheduler import SimpleGradeHoraria
import uuid

# Horários reais (7 períodos com recreio fixo na posição 4)
HORARIOS_REAIS = {
    1: "07:00-07:50",
    2: "07:50-08:40",
    3: "08:40-09:30",
    4: "09:30-10:00",  # RECREIO FIXO
    5: "10:00-10:50",
    6: "10:50-11:40",
    7: "11:40-12:30"
}

# Inicializar estado da sessão
try:
    init_session_state()
except Exception as e:
    st.error(f"❌ Erro na inicialização: {str(e)}")
    st.code(traceback.format_exc())
    st.stop()

def color_disciplina(val):
    """Aplica cores personalizadas de fundo e fonte"""
    if val:
        for d in st.session_state.disciplinas:
            if d.nome == val:
                return f'background-color: {d.cor_fundo}; color: {d.cor_fonte}; font-weight: bold'
    return ''

st.set_page_config(page_title="Escola Timetable", layout="wide")
st.title("🕒 Gerador Inteligente de Grade Horária")

# Criar abas (incluindo Feriados)
abas = st.tabs(["🏠 Início", "📚 Disciplinas", "👩‍🏫 Professores", "🎒 Turmas", "🏫 Salas", "📅 Calendário", "⚙️ Configurações", "🗓️ Feriados"])
aba1, aba2, aba3, aba4, aba5, aba6, aba7, aba8 = abas

# =================== ABA 8: FERIADOS ===================
with aba8:
    st.header("Feriados e Dias Sem Aula")
    
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
                        item for item in st.session_state.feriados if item["id"] != f["id"]
                    ]
                    st.rerun()

# =================== RESTANTE DAS ABAS ===================
# [Mantenha todo o código das abas 1-7 exatamente como no app.py anterior]
# A única diferença está na aba de disciplinas:

# =================== ABA 2: DISCIPLINAS (ATUALIZADA) ===================
with aba2:
    st.header("Disciplinas")
    with st.form("add_disc"):
        nome = st.text_input("Nome")
        carga = st.number_input("Carga", 1, 7, 3)
        tipo = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"])
        series = st.text_input("Séries", "6ano,7ano,8ano,9ano,1em,2em,3em")
        cor_fundo = st.color_picker("Cor de Fundo", "#4A90E2")
        cor_fonte = st.color_picker("Cor da Fonte", "white")
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

# [Copie o restante das abas 1, 3, 4, 5, 6, 7 do app.py anterior]
# (As abas de Início, Professores, Turmas, Salas, Calendário e Configurações permanecem iguais)