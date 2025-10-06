import streamlit as st
import json
import pandas as pd
import io
# 🔑 REMOVA O PREFIXO: use imports diretos
from session_state import init_session_state
from models import Turma, Professor, Disciplina, Sala
from scheduler_ortools import GradeHorariaORTools
from export import exportar_para_excel, exportar_para_pdf
import database
from simple_scheduler import SimpleGradeHoraria
# 🔑 REMOVA O PREFIXO no auth também
from auth import login, handle_redirect

# Verificar login
if "user" not in st.session_state:
    st.set_page_config(page_title="Login - Escola Timetable")
    st.title("🔐 Acesso ao Sistema de Grade Horária")
    st.write("Por favor, faça login com sua conta Google para continuar.")
    login()
    handle_redirect()
    st.stop()

# Resto do código igual...
# [MANTENHA TODO O RESTANTE DO CÓDIGO DO APP.PY AQUI]

# Inicializar estado da sessão
init_session_state()

st.set_page_config(page_title="Escola Timetable", layout="wide")
st.title("🕒 Gerador Inteligente de Grade Horária")

# Abas
abas = st.tabs(["🏠 Início", "📚 Disciplinas", "👩‍🏫 Professores", "🎒 Turmas", "🏫 Salas", "📅 Calendário", "⚙️ Configurações"])
aba1, aba2, aba3, aba4, aba5, aba6, aba7 = abas

# =================== ABA 7: CONFIGURAÇÕES ===================
with aba7:
    st.header("Configurações Avançadas")
    st.write("Ajuste as regras para gerar a grade horária.")
    
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
        "Permitir janelas para professores (aulas não consecutivas)",
        value=st.session_state.get("permitir_janelas", True)
    )
    
    st.divider()
    st.subheader("Diagnóstico de Viabilidade")
    if st.button("🔍 Analisar Viabilidade"):
        total_aulas = 0
        for turma in st.session_state.turmas:
            for disc in st.session_state.disciplinas:
                if turma.serie in disc.series:
                    total_aulas += disc.carga_semanal
        
        capacidade_total = 0
        for prof in st.session_state.professores:
            dias = len(prof.disponibilidade)
            capacidade_total += dias * st.session_state.max_aulas_professor_dia
        
        st.metric("Total de aulas necessárias", total_aulas)
        st.metric("Capacidade total de professores", capacidade_total)
        
        if capacidade_total >= total_aulas:
            st.success("✅ Capacidade suficiente para gerar grade")
        else:
            st.error("⚠️ Capacidade insuficiente! Adicione mais professores ou reduza carga horária.")

# =================== ABA 1: INÍCIO ===================
with aba1:
    st.header("Gerenciar Configuração e Gerar Grade")
    
    col_save, col_load = st.columns(2)
    
    with col_save:
        if st.button("💾 Salvar Tudo no Banco"):
            try:
                database.salvar_turmas(st.session_state.turmas)
                database.salvar_professores(st.session_state.professores)
                database.salvar_disciplinas(st.session_state.disciplinas)
                database.salvar_salas(st.session_state.salas)
                database.salvar_periodos(st.session_state.periodos)
                st.success("✅ Dados salvos no banco SQLite!")
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {str(e)}")
    
    with col_load:
        if st.button("🔄 Carregar do Banco"):
            try:
                st.session_state.turmas = database.carregar_turmas()
                st.session_state.professores = database.carregar_professores()
                st.session_state.disciplinas = database.carregar_disciplinas()
                st.session_state.salas = database.carregar_salas()
                st.session_state.periodos = database.carregar_periodos()
                st.success("✅ Dados carregados do banco!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao carregar: {str(e)}")

    st.divider()
    st.subheader("Gerar Grade Horária")
    
    if not st.session_state.turmas:
        st.warning("⚠️ Cadastre pelo menos uma turma.")
        st.stop()
    if not st.session_state.professores:
        st.warning("⚠️ Cadastre pelo menos um professor.")
        st.stop()
    if not st.session_state.disciplinas:
        st.warning("⚠️ Cadastre pelo menos uma disciplina.")
        st.stop()
    
    if st.button("🚀 Gerar Grade com Dados Atuais"):
        with st.spinner("Gerando grade..."):
            aulas = None
            metodo = ""
            try:
                # Primeiro: tentar com OR-Tools
                grade = GradeHorariaORTools(
                    st.session_state.turmas,
                    st.session_state.professores,
                    st.session_state.disciplinas,
                    relaxar_horario_ideal=st.session_state.relaxar_horario_ideal
                )
                aulas = grade.resolver()
                metodo = "Google OR-Tools (otimizado)"
                
            except Exception as e1:
                st.warning(f"⚠️ OR-Tools falhou: {str(e1)}. Tentando método simples...")
                try:
                    # Segundo: fallback com algoritmo simples
                    simple_grade = SimpleGradeHoraria(
                        st.session_state.turmas,
                        st.session_state.professores,
                        st.session_state.disciplinas
                    )
                    aulas = simple_grade.gerar_grade()
                    metodo = "Algoritmo Simples (fallback)"
                except Exception as e2:
                    st.error(f"❌ Ambos os métodos falharam:\n1. OR-Tools: {str(e1)}\n2. Simples: {str(e2)}")
                    st.stop()
            
            # Exibir resultados
            dados = []
            for aula in aulas:
                dados.append({
                    "Turma": aula.turma,
                    "Disciplina": aula.disciplina,
                    "Professor": aula.professor,
                    "Dia": aula.dia,
                    "Horário": aula.horario
                })
            
            df = pd.DataFrame(dados)
            tabela = df.pivot_table(
                index=["Turma", "Horário"],
                columns="Dia",
                values="Disciplina",
                aggfunc=lambda x: x.iloc[0],
                fill_value=""
            ).reindex(columns=["seg", "ter", "qua", "qui", "sex"], fill_value="")
            
            if "fallback" in metodo:
                st.warning(f"⚠️ Grade gerada com {metodo}. Pode haver pequenos conflitos.")
            else:
                st.success(f"✅ Grade gerada com {metodo}!")
            
            st.dataframe(tabela, use_container_width=True)
            
            # Exportar
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                tabela.to_excel(writer, sheet_name="Grade por Turma")
                df.to_excel(writer, sheet_name="Dados Brutos", index=False)
            output.seek(0)
            
            st.download_button(
                label="📥 Baixar Excel",
                data=output,
                file_name="grade_horaria.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            pdf_path = exportar_para_pdf(aulas)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Baixar PDF",
                    data=f.read(),
                    file_name="grade_horaria.pdf",
                    mime="application/pdf"
                )
            
            # Relatórios
            st.divider()
            st.subheader("📊 Relatórios")
            
            prof_horas = {}
            for aula in aulas:
                prof = aula.professor
                prof_horas[prof] = prof_horas.get(prof, 0) + 1
            df_prof = pd.DataFrame(list(prof_horas.items()), columns=["Professor", "Horas Semanais"])
            st.markdown("### ⏱️ Horas por Professor")
            st.dataframe(df_prof, use_container_width=True)
            
            disc_horas = {}
            for aula in aulas:
                disc = aula.disciplina
                disc_horas[disc] = disc_horas.get(disc, 0) + 1
            df_disc = pd.DataFrame(list(disc_horas.items()), columns=["Disciplina", "Horas Semanais"])
            st.markdown("### 📚 Horas por Disciplina")
            st.dataframe(df_disc, use_container_width=True)

# =================== ABA 2: DISCIPLINAS ===================
with aba2:
    st.header("Gerenciar Disciplinas")
    
    with st.form("add_disciplina"):
        st.subheader("Adicionar Disciplina")
        nome_disc = st.text_input("Nome da Disciplina")
        carga = st.number_input("Carga Semanal (aulas/semana)", min_value=1, max_value=6, value=3)
        tipo = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"])
        series_input = st.text_input("Séries (ex: 6ano,7ano,1em,2em)", value="6ano,7ano,8ano,9ano,1em,2em,3em")
        series = [s.strip() for s in series_input.split(",") if s.strip()]
        
        if st.form_submit_button("➕ Adicionar Disciplina"):
            if nome_disc and series:
                st.session_state.disciplinas.append(Disciplina(nome_disc, int(carga), tipo, series))
                st.success(f"✅ Disciplina '{nome_disc}' adicionada!")
                st.rerun()
            else:
                st.error("⚠️ Preencha nome e pelo menos uma série.")
    
    st.subheader("Disciplinas Cadastradas")
    for i, disc in enumerate(st.session_state.disciplinas[:]):
        with st.expander(f"📘 {disc.nome} | Carga: {disc.carga_semanal} | Tipo: {disc.tipo}"):
            with st.form(f"edit_disc_{i}"):
                nome = st.text_input("Nome", disc.nome, key=f"nome_{i}")
                carga = st.number_input("Carga Semanal", min_value=1, max_value=6, value=disc.carga_semanal, key=f"carga_{i}")
                tipo = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"], 
                                   index=["pesada", "media", "leve", "pratica"].index(disc.tipo), key=f"tipo_{i}")
                series_str = st.text_input("Séries", ", ".join(disc.series), key=f"series_{i}")
                series = [s.strip() for s in series_str.split(",") if s.strip()]
                
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.disciplinas[i] = Disciplina(nome, carga, tipo, series)
                    st.success("✅ Atualizado!")
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.disciplinas.pop(i)
                    st.rerun()

# =================== ABA 3: PROFESSORES ===================
with aba3:
    st.header("Gerenciar Professores")
    
    disc_nomes = [d.nome for d in st.session_state.disciplinas] or ["Nenhuma disciplina cadastrada"]
    
    with st.form("add_prof"):
        st.subheader("Adicionar Professor")
        nome_prof = st.text_input("Nome do Professor")
        disc_selecionadas = st.multiselect("Disciplinas que leciona", disc_nomes)
        dias = ["seg", "ter", "qua", "qui", "sex"]
        disp_selecionada = st.multiselect("Disponibilidade (dias da semana)", dias, default=dias)
        
        if st.form_submit_button("➕ Adicionar Professor"):
            if nome_prof and disc_selecionadas:
                st.session_state.professores.append(Professor(nome_prof, disc_selecionadas, set(disp_selecionada)))
                st.success(f"✅ Professor '{nome_prof}' adicionado!")
                st.rerun()
            else:
                st.error("⚠️ Preencha nome e pelo menos uma disciplina.")
    
    st.subheader("Professores Cadastrados")
    for i, prof in enumerate(st.session_state.professores[:]):
        with st.expander(f"🧑‍🏫 {prof.nome} | Disciplinas: {', '.join(prof.disciplinas)}"):
            with st.form(f"edit_prof_{i}"):
                nome = st.text_input("Nome", prof.nome, key=f"p_nome_{i}")
                
                disc_validas = [d for d in prof.disciplinas if d in disc_nomes]
                disc_atual = st.multiselect("Disciplinas", disc_nomes, default=disc_validas, key=f"p_disc_{i}")
                
                dias = ["seg", "ter", "qua", "qui", "sex"]
                disp_atual = st.multiselect("Disponibilidade", dias, default=list(prof.disponibilidade), key=f"p_disp_{i}")
                
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.professores[i] = Professor(nome, disc_atual, set(disp_atual))
                    st.success("✅ Atualizado!")
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.professores.pop(i)
                    st.rerun()

# =================== ABA 4: TURMAS ===================
with aba4:
    st.header("Gerenciar Turmas")
    
    with st.form("add_turma"):
        st.subheader("Adicionar Turma")
        nome_turma = st.text_input("Nome da Turma (ex: 9anoA, 2emB)")
        serie_turma = st.text_input("Série (ex: 9ano, 2em)")
        turno = st.selectbox("Turno", ["manha", "tarde"])
        
        if st.form_submit_button("➕ Adicionar Turma"):
            if nome_turma and serie_turma:
                st.session_state.turmas.append(Turma(nome_turma, serie_turma, turno))
                st.success(f"✅ Turma '{nome_turma}' adicionada!")
                st.rerun()
            else:
                st.error("⚠️ Preencha nome e série.")
    
    st.subheader("Turmas Cadastradas")
    for i, turma in enumerate(st.session_state.turmas[:]):
        with st.expander(f"🎒 {turma.nome} | Série: {turma.serie} | Turno: {turma.turno}"):
            with st.form(f"edit_turma_{i}"):
                nome = st.text_input("Nome", turma.nome, key=f"t_nome_{i}")
                serie = st.text_input("Série", turma.serie, key=f"t_serie_{i}")
                turno = st.selectbox("Turno", ["manha", "tarde"], 
                                    index=["manha", "tarde"].index(turma.turno), key=f"t_turno_{i}")
                
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.turmas[i] = Turma(nome, serie, turno)
                    st.success("✅ Atualizado!")
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.turmas.pop(i)
                    st.rerun()

# =================== ABA 5: SALAS ===================
with aba5:
    st.header("Gerenciar Salas")
    
    with st.form("add_sala"):
        st.subheader("Adicionar Sala")
        nome_sala = st.text_input("Nome da Sala")
        capacidade = st.number_input("Capacidade", min_value=1, value=30)
        tipo = st.selectbox("Tipo", ["normal", "laboratório", "auditório"])
        
        if st.form_submit_button("➕ Adicionar Sala"):
            if nome_sala:
                st.session_state.salas.append(Sala(nome_sala, capacidade, tipo))
                st.success(f"✅ Sala '{nome_sala}' adicionada!")
                st.rerun()
            else:
                st.error("⚠️ Preencha o nome da sala.")
    
    st.subheader("Salas Cadastradas")
    for i, sala in enumerate(st.session_state.salas[:]):
        with st.expander(f"🏫 {sala.nome} | Capacidade: {sala.capacidade} | Tipo: {sala.tipo}"):
            with st.form(f"edit_sala_{i}"):
                nome = st.text_input("Nome", sala.nome, key=f"s_nome_{i}")
                capacidade = st.number_input("Capacidade", min_value=1, value=sala.capacidade, key=f"s_cap_{i}")
                tipo = st.selectbox("Tipo", ["normal", "laboratório", "auditório"], 
                                   index=["normal", "laboratório", "auditório"].index(sala.tipo), key=f"s_tipo_{i}")
                
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.salas[i] = Sala(nome, capacidade, tipo)
                    st.success("✅ Atualizado!")
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.salas.pop(i)
                    st.rerun()

# =================== ABA 6: CALENDÁRIO ===================
with aba6:
    st.header("Gerenciar Períodos Escolares")
    
    with st.form("add_periodo"):
        st.subheader("Adicionar Período")
        nome_periodo = st.text_input("Nome do Período (ex: 1º Bimestre)")
        inicio = st.date_input("Data de Início")
        fim = st.date_input("Data de Fim")
        
        if st.form_submit_button("➕ Adicionar Período"):
            if nome_periodo:
                st.session_state.periodos.append({
                    "nome": nome_periodo,
                    "inicio": str(inicio),
                    "fim": str(fim)
                })
                st.success(f"✅ Período '{nome_periodo}' adicionado!")
                st.rerun()
            else:
                st.error("⚠️ Preencha o nome do período.")
    
    st.subheader("Períodos Cadastrados")
    for i, periodo in enumerate(st.session_state.periodos[:]):
        with st.expander(f"📅 {periodo['nome']} | {periodo['inicio']} a {periodo['fim']}"):
            with st.form(f"edit_periodo_{i}"):
                nome = st.text_input("Nome", periodo["nome"], key=f"p_nome_{periodo['nome'].replace(' ', '_')}_{i}")
                inicio = st.date_input("Início", value=pd.to_datetime(periodo["inicio"]), key=f"p_inicio_{i}")
                fim = st.date_input("Fim", value=pd.to_datetime(periodo["fim"]), key=f"p_fim_{i}")
                
                col1, col2 = st.columns(2)
                if col1.form_submit_button("💾 Salvar"):
                    st.session_state.periodos[i] = {
                        "nome": nome,
                        "inicio": str(inicio),
                        "fim": str(fim)
                    }
                    st.success("✅ Atualizado!")
                    st.rerun()
                if col2.form_submit_button("🗑️ Excluir"):
                    st.session_state.periodos.pop(i)
                    st.rerun()
