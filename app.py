import streamlit as st
import pandas as pd
import io
from session_state import init_session_state
from models import Turma, Professor, Disciplina, Sala
from scheduler_ortools import GradeHorariaORTools  # ← Deve funcionar agora
from export import exportar_para_excel, exportar_para_pdf
import database
from simple_scheduler import SimpleGradeHoraria
import uuid

# Horários reais (7 períodos com recreio fixo na 4ª posição)
HORARIOS_REAIS = {
    1: "07:00-07:50",
    2: "07:50-08:40",
    3: "08:40-09:30",
    4: "09:30-10:00",  # RECREIO (não terá aulas)
    5: "10:00-10:50",
    6: "10:50-11:40",
    7: "11:40-12:30"
}

init_session_state()

def color_disciplina(val):
    """Garante contraste entre texto e fundo"""
    if val:
        for d in st.session_state.disciplinas:
            if d.nome == val:
                # Garantir que a cor não seja branca pura
                if d.cor == "#ffffff" or d.cor == "#FFFFFF":
                    cor_fundo = "#f0f0f0"  # Cinza claro
                else:
                    cor_fundo = d.cor
                
                # Calcular cor do texto
                r, g, b = int(cor_fundo[1:3], 16), int(cor_fundo[3:5], 16), int(cor_fundo[5:7], 16)
                luminancia = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                cor_texto = "black" if luminancia > 0.5 else "white"
                return f'background-color: {cor_fundo}; color: {cor_texto}; font-weight: bold'
    return 'background-color: white; color: black'  # Padrão seguro

st.set_page_config(page_title="Escola Timetable", layout="wide")
st.title("🕒 Gerador Inteligente de Grade Horária")

# ... resto do código igual ao anterior ...
# (Mantenha todas as abas exatamente como no app.py anterior)