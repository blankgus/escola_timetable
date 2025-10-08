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
st.title("🕒 Gerador Inteligente de Grade Horária")

abas = st.tabs(["🏠 Início", "📚 Disciplinas", "👩‍🏫 Professores", "🎒 Turmas", "🏫 Salas", "📅 Calendário", "⚙️ Configurações", "🗓️ Feriados"])
aba1, aba2, aba3, aba4, aba5, aba6, aba7, aba8 = abas

# =================== ABA 1: INÍCIO ===================
with aba1:
    st.subheader("🎯 Escolha o tipo de grade a gerar")
    tipo_grade = st.radio(
        "Tipo de Grade",
        ["Grade Completa (Turmas)", "Grade por Turma", "Grade por Sala", "Grade por Professor"],
        index=0
    )

    if st.button("🚀 Gerar Grade"):
        with st.spinner("Gerando grade..."):
            try:
                grade = GradeHorariaORTools(st.session_state.turmas, st.session_state.professores, st.session_state.disciplinas)
                aulas = grade.resolver()
                metodo = "Google OR-Tools"
            except Exception as e1:
                st.warning("⚠️ OR-Tools falhou. Tentando método simples...")
                try:
                    simple_grade = SimpleGradeHoraria(st.session_state.turmas, st.session_state.professores, st.session_state.disciplinas)
                    aulas = simple_grade.gerar_grade()
                    metodo = "Algoritmo Simples"
                except Exception as e2:
                    st.error("❌ Falha total ao gerar grade.")
                    st.code(traceback.format_exc())
                    st.stop()

        st.success(f"✅ Grade gerada com sucesso usando {metodo}!")

        if tipo_grade == "Grade Completa (Turmas)":
            df = pd.DataFrame([
                {"Turma": a.turma, "Disciplina": a.disciplina, "Professor": a.professor, "Dia": a.dia, "Horário": a.horario, "Sala": a.sala}
                for a in aulas
            ])
            tabela = df.pivot_table(
                index=["Turma", "Horário"],
                columns="Dia",
                values="Disciplina",
                aggfunc=lambda x: x.iloc[0],
                fill_value=""
            ).reindex(columns=["dom", "seg", "ter", "qua", "qui", "sex", "sab"], fill_value="")
            novo_indice = []
            for turma, horario_num in tabela.index:
                horario_real = HORARIOS_REAIS.get(horario_num, f"{horario_num}ª aula")
                novo_indice.append((turma, horario_real))
            tabela.index = pd.MultiIndex.from_tuples(novo_indice)
            st.dataframe(tabela.style.applymap(color_disciplina), use_container_width=True)

        elif tipo_grade == "Grade por Turma":
            st.markdown("### 🎒 Grade por Turma")
            turmas_lista = sorted(list(set(a.turma for a in aulas)))
            if turmas_lista:
                turma_selecionada = st.selectbox("Selecione a turma", turmas_lista, key="turma_escolhida")
                for semana in range(1, 6):
                    st.markdown(f"#### Semana {semana}")
                    df = gerar_grade_por_turma_semana(aulas, turma_selecionada, semana)
                    st.dataframe(df.style.applymap(color_disciplina), use_container_width=True)

        elif tipo_grade == "Grade por Sala":
            st.markdown("### 🏫 Grade por Sala")
            salas_lista = sorted(list(set(a.sala for a in aulas)))
            if salas_lista:
                sala_selecionada = st.selectbox("Selecione a sala", salas_lista, key="sala_escolhida")
                for semana in range(1, 6):
                    st.markdown(f"#### Semana {semana}")
                    df = gerar_grade_por_sala_semana(aulas, sala_selecionada, semana)
                    st.dataframe(df.style.applymap(color_disciplina), use_container_width=True)

        elif tipo_grade == "Grade por Professor":
            st.markdown("### 👨‍🏫 Grade por Professor")
            professores_lista = sorted(list(set(a.professor for a in aulas)))
            if professores_lista:
                prof_selecionado = st.selectbox("Selecione o professor", professores_lista, key="prof_escolhido")
                for semana in range(1, 6):
                    st.markdown(f"#### Semana {semana}")
                    df = gerar_grade_por_professor_semana(aulas, prof_selecionado, semana)
                    st.dataframe(df.style.applymap(color_disciplina), use_container_width=True)

        # Botão de exportação
        if st.button("📤 Exportar Esta Grade"):
            output = io.BytesIO()
            exportar_grade_por_tipo(aulas, tipo_grade, output)
            st.download_button(
                "📥 Baixar Grade",
                output.getvalue(),
                "grade_exportada.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# =================== ABAS RESTANTES ===================
# Mantenha as outras abas como estão (disciplinas, professores, etc.)
# Elas não precisam de alterações para estas correções.
with aba2:
    st.header("📚 Disciplinas")
    st.info("Configure disciplinas na aba original.")

with aba3:
    st.header("👩‍🏫 Professores")
    st.info("Configure professores na aba original.")

with aba4:
    st.header("🎒 Turmas")
    st.info("Configure turmas na aba original.")

with aba5:
    st.header("🏫 Salas")
    st.info("Configure salas na aba original.")

with aba6:
    st.header("📅 Calendário")
    st.info("Calendário completo (domingo a sábado).")

with aba7:
    st.header("⚙️ Configurações")
    st.info("Configurações avançadas.")

with aba8:
    st.header("🗓️ Feriados")
    st.info("Gerencie feriados aqui.")