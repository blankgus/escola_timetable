import streamlit as st
import json
import pandas as pd
import io
from session_state import init_session_state
from models import Turma, Professor, Disciplina, Sala
from scheduler_ortools import GradeHorariaORTools
from export import exportar_para_excel, exportar_para_pdf
import database
from simple_scheduler import SimpleGradeHoraria

# Inicializar estado da sessão (SEM verificação de login)
init_session_state()

# Função para aplicar cores nas disciplinas
def color_disciplina(val):
    if val:
        for d in st.session_state.disciplinas:
            if d.nome == val:
                return f'background-color: {d.cor}; color: white; font-weight: bold'
    return ''

st.set_page_config(page_title="Escola Timetable", layout="wide")
st.title("🕒 Gerador Inteligente de Grade Horária")

# Abas
abas = st.tabs(["🏠 Início", "📚 Disciplinas", "👩‍🏫 Professores", "🎒 Turmas", "🏫 Salas", "📅 Calendário", "⚙️ Configurações"])
aba1, aba2, aba3, aba4, aba5, aba6, aba7 = abas

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
        max_value=6,
        value=st.session_state.get("max_aulas_professor_dia", 6)
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
            len(prof.disponibilidade) * st.session_state.max_aulas_professor_dia
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
                database.salvar_salas(st.session_state.salas)
                database.salvar_periodos(st.session_state.periodos)
                st.success("✅ Dados salvos!")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
    with col2:
        if st.button("🔄 Carregar do Banco"):
            try:
                st.session_state.turmas = database.carregar_turmas()
                st.session_state.professores = database.carregar_professores()
                st.session_state.disciplinas = database.carregar_disciplinas()
                st.session_state.salas = database.carregar_salas()
                st.session_state.periodos = database.carregar_periodos()
                st.success("✅ Dados carregados!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
    
    if not st.session_state.turmas or not st.session_state.professores or not st.session_state.disciplinas:
        st.warning("⚠️ Cadastre dados antes de gerar grade.")
        st.stop()
    
    if st.button("🚀 Gerar Grade"):
        with st.spinner("Gerando grade..."):
            try:
                grade = GradeHorariaORTools(
                    st.session_state.turmas,
                    st.session_state.professores,
                    st.session_state.disciplinas,
                    relaxar_horario_ideal=st.session_state.relaxar_horario_ideal
                )
                aulas = grade.resolver()
                metodo = "Google OR-Tools"
            except Exception as e1:
                st.warning(f"⚠️ OR-Tools falhou. Tentando método simples...")
                try:
                    simple_grade = SimpleGradeHoraria(
                        st.session_state.turmas,
                        st.session_state.professores,
                        st.session_state.disciplinas
                    )
                    aulas = simple_grade.gerar_grade()
                    metodo = "Algoritmo Simples"
                except Exception as e2:
                    st.error(f"❌ Falha total: {str(e2)}")
                    st.stop()
            
            # Preparar dados
            df = pd.DataFrame([
                {"Turma": a.turma, "Disciplina": a.disciplina, "Professor": a.professor, "Dia": a.dia, "Horário": a.horario}
                for a in aulas
            ])
            tabela = df.pivot_table(
                index=["Turma", "Horário"],
                columns="Dia",
                values="Disciplina",
                aggfunc=lambda x: x.iloc[0],
                fill_value=""
            ).reindex(columns=["seg", "ter", "qua", "qui", "sex"], fill_value="")
            
            st.success(f"✅ Grade gerada com {metodo}!")
            st.dataframe(tabela.style.applymap(color_disciplina), use_container_width=True)
            
            # Exportar
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                tabela.to_excel(writer, sheet_name="Grade")
                df.to_excel(writer, sheet_name="Dados", index=False)
            st.download_button("📥 Excel", output.getvalue(), "grade.xlsx")
            
            pdf_path = exportar_para_pdf(aulas)
            with open(pdf_path, "rb") as f:
                st.download_button("📄 PDF", f.read(), "grade.pdf")
            
            # Relatórios
            st.subheader("📊 Relatórios")
            prof_horas = pd.DataFrame([
                {"Professor": p, "Horas": c} 
                for p, c in pd.Series([a.professor for a in aulas]).value_counts().items()
            ])
            st.dataframe(prof_horas, use_container_width=True)

# =================== ABA 2: DISCIPLINAS ===================
with aba2:
    st.header("Disciplinas")
    with st.form("add_disc"):
        nome = st.text_input("Nome")
        carga = st.number_input("Carga", 1, 6, 3)
        tipo = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"])
        series = st.text_input("Séries", "6ano,7ano,8ano,9ano,1em,2em,3em")
        if st.form_submit_button("➕ Adicionar"):
            if nome:
                series_list = [s.strip() for s in series.split(",") if s.strip()]
                st.session_state.disciplinas.append(Disciplina(nome, carga, tipo, series_list))
                st.rerun()
    
    for i, d in enumerate(st.session_state.disciplinas[:]):
        with st.expander(f"{d.nome}"):
            with st.form(f"edit_disc_{i}"):
                nome = st.text_input("Nome", d.nome, key=f"n_{i}")
                carga = st.number_input("Carga", 1, 6, d.carga_semanal, key=f"c_{i}")
                tipo = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"], 
                                   index=["pesada", "media", "leve", "pratica"].index(d.tipo), key=f"t_{i}")
                series = st.text_input("Séries", ", ".join(d.series), key=f"s_{i}")
                if st.form_submit_button("💾 Salvar"):
                    series_list = [s.strip() for s in series.split(",") if s.strip()]
                    st.session_state.disciplinas[i] = Disciplina(nome, carga, tipo, series_list)
                    st.rerun()
                if st.form_submit_button("🗑️ Excluir"):
                    st.session_state.disciplinas.pop(i)
                    st.rerun()

# =================== ABA 3: PROFESSORES ===================
with aba3:
    st.header("Professores")
    disc_nomes = [d.nome for d in st.session_state.disciplinas] or ["Nenhuma"]
    with st.form("add_prof"):
        nome = st.text_input("Nome")
        discs = st.multiselect("Disciplinas", disc_nomes)
        dias = st.multiselect("Disponibilidade", ["seg", "ter", "qua", "qui", "sex"], default=["seg", "ter", "qua", "qui", "sex"])
        if st.form_submit_button("➕ Adicionar"):
            if nome and discs:
                st.session_state.professores.append(Professor(nome, discs, set(dias)))
                st.rerun()
    
    for i, p in enumerate(st.session_state.professores[:]):
        with st.expander(p.nome):
            with st.form(f"edit_prof_{i}"):
                nome = st.text_input("Nome", p.nome, key=f"pn_{i}")
                discs_validas = [d for d in p.disciplinas if d in disc_nomes]
                discs = st.multiselect("Disciplinas", disc_nomes, default=discs_validas, key=f"pd_{i}")
                dias = st.multiselect("Disponibilidade", ["seg", "ter", "qua", "qui", "sex"], 
                                     default=list(p.disponibilidade), key=f"pdias_{i}")
                if st.form_submit_button("💾 Salvar"):
                    st.session_state.professores[i] = Professor(nome, discs, set(dias))
                    st.rerun()
                if st.form_submit_button("🗑️ Excluir"):
                    st.session_state.professores.pop(i)
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
    
    for i, t in enumerate(st.session_state.turmas[:]):
        with st.expander(f"{t.nome}"):
            with st.form(f"edit_turma_{i}"):
                nome = st.text_input("Nome", t.nome, key=f"tn_{i}")
                serie = st.text_input("Série", t.serie, key=f"ts_{i}")
                turno = st.selectbox("Turno", ["manha", "tarde"], 
                                    index=["manha", "tarde"].index(t.turno), key=f"tt_{i}")
                if st.form_submit_button("💾 Salvar"):
                    st.session_state.turmas[i] = Turma(nome, serie, turno)
                    st.rerun()
                if st.form_submit_button("🗑️ Excluir"):
                    st.session_state.turmas.pop(i)
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
    
    for i, s in enumerate(st.session_state.salas[:]):
        with st.expander(s.nome):
            with st.form(f"edit_sala_{i}"):
                nome = st.text_input("Nome", s.nome, key=f"sn_{i}")
                cap = st.number_input("Capacidade", 1, 100, s.capacidade, key=f"sc_{i}")
                tipo = st.selectbox("Tipo", ["normal", "laboratório", "auditório"], 
                                   index=["normal", "laboratório", "auditório"].index(s.tipo), key=f"st_{i}")
                if st.form_submit_button("💾 Salvar"):
                    st.session_state.salas[i] = Sala(nome, cap, tipo)
                    st.rerun()
                if st.form_submit_button("🗑️ Excluir"):
                    st.session_state.salas.pop(i)
                    st.rerun()

# =================== ABA 6: CALENDÁRIO ===================
with aba6:
    st.header("Períodos")
    with st.form("add_periodo"):
        nome = st.text_input("Nome (ex: 1º Bimestre)")
        inicio = st.date_input("Início")
        fim = st.date_input("Fim")
        if st.form_submit_button("➕ Adicionar"):
            if nome:
                st.session_state.periodos.append({"nome": nome, "inicio": str(inicio), "fim": str(fim)})
                st.rerun()
    
    for i, p in enumerate(st.session_state.periodos[:]):
        with st.expander(p["nome"]):
            with st.form(f"edit_periodo_{i}"):
                nome = st.text_input("Nome", p["nome"], key=f"pn_{i}")
                inicio = st.date_input("Início", value=pd.to_datetime(p["inicio"]), key=f"pi_{i}")
                fim = st.date_input("Fim", value=pd.to_datetime(p["fim"]), key=f"pf_{i}")
                if st.form_submit_button("💾 Salvar"):
                    st.session_state.periodos[i] = {"nome": nome, "inicio": str(inicio), "fim": str(fim)}
                    st.rerun()
                if st.form_submit_button("🗑️ Excluir"):
                    st.session_state.periodos.pop(i)
                    st.rerun()
