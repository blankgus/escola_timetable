import streamlit as st
import pandas as pd
import io
from session_state import init_session_state, importar_de_excel, exportar_para_excel_template
from models import Turma, Professor, Disciplina, Sala, DisciplinaTurma
import database
import uuid

# Inicializar estado da sessão
try:
    init_session_state()
except Exception as e:
    st.error(f"❌ Erro na inicialização: {str(e)}")
    st.stop()

st.set_page_config(page_title="Escola Timetable", layout="wide")
st.title("🕒 Gerador Inteligente de Grade Horária")

# === Abas ===
abas = st.tabs([
    "🏠 Início",
    "📚 Disciplinas",
    "👩‍🏫 Professores", 
    "🎒 Turmas",
    "🏫 Salas",
    "📥 Importar/Exportar"
])

(aba1, aba2, aba3, aba4, aba5, aba6) = abas

# =================== ABA 1: INÍCIO ===================
with aba1:
    st.header("Início")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Salvar no Banco"):
            try:
                database.salvar_turmas(st.session_state.turmas)
                database.salvar_professores(st.session_state.professores)
                database.salvar_disciplinas(st.session_state.disciplinas)
                database.salvar_salas(st.session_state.salas)
                st.success("✅ Dados salvos!")
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {str(e)}")
    
    with col2:
        if st.button("🔄 Carregar do Banco"):
            try:
                st.session_state.turmas = database.carregar_turmas()
                st.session_state.professores = database.carregar_professores()
                st.session_state.disciplinas = database.carregar_disciplinas()
                st.session_state.salas = database.carregar_salas()
                st.success("✅ Dados carregados!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao carregar: {str(e)}")

    # Visualizar turmas e disciplinas
    if st.session_state.turmas:
        st.subheader("📋 Turmas Cadastradas")
        for t in st.session_state.turmas:
            with st.expander(f"🎒 {t.nome} ({t.serie} - {t.turno})"):
                st.write("**Disciplinas:**")
                if t.disciplinas_turma:
                    df_discs = pd.DataFrame([
                        {
                            "Disciplina": dt.nome,
                            "Carga Semanal": dt.carga_semanal,
                            "Professor": dt.professor
                        }
                        for dt in t.disciplinas_turma
                    ])
                    st.dataframe(df_discs, use_container_width=True)
                else:
                    st.info("Nenhuma disciplina cadastrada.")
    else:
        st.info("⚠️ Nenhuma turma cadastrada.")

# =================== ABA 2: DISCIPLINAS ===================
with aba2:
    st.header("📚 Disciplinas Template")
    
    # Adicionar nova disciplina
    with st.form("add_disc"):
        nome = st.text_input("Nome")
        carga = st.number_input("Carga Semanal", 1, 10, 3)
        tipo = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"])
        series = st.text_input("Séries (separadas por vírgula)", "6ano,7ano,8ano,9ano")
        cor_fundo = st.color_picker("Cor de Fundo", "#4A90E2")
        cor_fonte = st.color_picker("Cor da Fonte", "#FFFFFF")
        
        if st.form_submit_button("➕ Adicionar"):
            if nome:
                series_list = [s.strip() for s in series.split(",") if s.strip()]
                nova_disc = Disciplina(
                    nome=nome,
                    carga_semanal=carga,
                    tipo=tipo,
                    series=series_list,
                    cor_fundo=cor_fundo,
                    cor_fonte=cor_fonte
                )
                st.session_state.disciplinas.append(nova_disc)
                st.success(f"✅ Disciplina '{nome}' adicionada!")
                st.rerun()
    
    # Listar disciplinas
    if st.session_state.disciplinas:
        st.subheader("📝 Disciplinas Cadastradas")
        for i, d in enumerate(st.session_state.disciplinas):
            with st.expander(f"📘 {d.nome}"):
                st.write(f"**Carga Semanal:** {d.carga_semanal}")
                st.write(f"**Tipo:** {d.tipo}")
                st.write(f"**Séries:** {', '.join(d.series)}")
                st.write(f"**Cor:** {d.cor_fundo}")
                
                col1, col2 = st.columns(2)
                if col1.button("🗑️ Excluir", key=f"del_disc_{i}"):
                    st.session_state.disciplinas.pop(i)
                    st.success(f"✅ Disciplina '{d.nome}' excluída!")
                    st.rerun()
    else:
        st.info("⚠️ Nenhuma disciplina cadastrada.")

# =================== ABA 3: PROFESSORES ===================
with aba3:
    st.header("👩‍🏫 Professores")
    
    # Adicionar novo professor
    disc_nomes = [d.nome for d in st.session_state.disciplinas] if st.session_state.disciplinas else ["Nenhuma"]
    
    with st.form("add_prof"):
        nome = st.text_input("Nome")
        discs = st.multiselect("Disciplinas que pode lecionar", disc_nomes)
        dias = st.multiselect("Dias disponíveis", ["seg", "ter", "qua", "qui", "sex"], default=["seg", "ter", "qua", "qui", "sex"])
        horarios = st.multiselect("Horários disponíveis", [1,2,3,4,5,6,7], default=[1,2,3,5,6,7])
        restricoes = st.text_input("Restrições (ex: seg_1, qua_3)")
        
        if st.form_submit_button("➕ Adicionar"):
            if nome and discs:
                restricoes_set = set()
                if restricoes.strip():
                    restricoes_set = {r.strip() for r in restricoes.split(",")}
                
                novo_prof = Professor(
                    nome=nome,
                    disciplinas=discs,
                    disponibilidade_dias=set(dias),
                    disponibilidade_horarios=set(horarios),
                    restricoes=restricoes_set
                )
                st.session_state.professores.append(novo_prof)
                st.success(f"✅ Professor '{nome}' adicionado!")
                st.rerun()
    
    # Listar professores
    if st.session_state.professores:
        st.subheader("👥 Professores Cadastrados")
        for i, p in enumerate(st.session_state.professores):
            with st.expander(f"👤 {p.nome}"):
                st.write(f"**Disciplinas:** {', '.join(p.disciplinas)}")
                st.write(f"**Dias disponíveis:** {', '.join(sorted(p.disponibilidade_dias))}")
                st.write(f"**Horários disponíveis:** {sorted(p.disponibilidade_horarios)}")
                if p.restricoes:
                    st.write(f"**Restrições:** {', '.join(sorted(p.restricoes))}")
                
                col1, col2 = st.columns(2)
                if col1.button("🗑️ Excluir", key=f"del_prof_{i}"):
                    st.session_state.professores.pop(i)
                    st.success(f"✅ Professor '{p.nome}' excluído!")
                    st.rerun()
    else:
        st.info("⚠️ Nenhum professor cadastrado.")

# =================== ABA 4: TURMAS ===================
with aba4:
    st.header("🎒 Turmas")
    
    # Adicionar nova turma
    with st.form("add_turma"):
        nome = st.text_input("Nome (ex: 6anoA)")
        serie = st.text_input("Série (ex: 6ano)")
        turno = st.selectbox("Turno", ["manha", "tarde"])
        
        if st.form_submit_button("➕ Adicionar"):
            if nome and serie:
                nova_turma = Turma(nome=nome, serie=serie, turno=turno)
                st.session_state.turmas.append(nova_turma)
                st.success(f"✅ Turma '{nome}' adicionada!")
                st.rerun()
    
    # Listar e editar turmas
    if st.session_state.turmas:
        st.subheader("🏫 Turmas Cadastradas")
        for i, t in enumerate(st.session_state.turmas):
            with st.expander(f"🎒 {t.nome} ({t.serie} - {t.turno})"):
                st.write("**Disciplinas da Turma:**")
                
                # Selecionar disciplinas para a turma
                disc_options = [d.nome for d in st.session_state.disciplinas]
                if disc_options:
                    selected_discs = st.multiselect(
                        "Selecione as disciplinas", 
                        disc_options,
                        default=[dt.nome for dt in t.disciplinas_turma],
                        key=f"sel_disc_{i}"
                    )
                    
                    # Para cada disciplina selecionada, definir carga e professor
                    novas_discs_turma = []
                    for disc_nome in selected_discs:
                        # Buscar carga padrão
                        carga_padrao = 3
                        for d in st.session_state.disciplinas:
                            if d.nome == disc_nome:
                                carga_padrao = d.carga_semanal
                                break
                        
                        # Buscar professor atual (se existir)
                        prof_atual = ""
                        carga_atual = carga_padrao
                        for dt in t.disciplinas_turma:
                            if dt.nome == disc_nome:
                                prof_atual = dt.professor
                                carga_atual = dt.carga_semanal
                                break
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            carga = st.number_input(
                                f"Carga {disc_nome}", 
                                1, 10, 
                                carga_atual,
                                key=f"carga_{i}_{disc_nome}"
                            )
                        with col2:
                            # Selecionar professor (apenas os que lecionam essa disciplina)
                            profs_disc = [p.nome for p in st.session_state.professores if disc_nome in p.disciplinas]
                            prof = st.selectbox(
                                f"Professor {disc_nome}",
                                profs_disc,
                                index=profs_disc.index(prof_atual) if prof_atual in profs_disc else 0,
                                key=f"prof_{i}_{disc_nome}"
                            )
                        with col3:
                            if st.button("➕", key=f"add_dt_{i}_{disc_nome}"):
                                novas_discs_turma.append(DisciplinaTurma(
                                    nome=disc_nome,
                                    carga_semanal=carga,
                                    professor=prof
                                ))
                                st.success(f"✅ {disc_nome} adicionada!")
                    
                    # Atualizar disciplinas da turma
                    if st.button("💾 Salvar Disciplinas", key=f"save_dt_{i}"):
                        st.session_state.turmas[i].disciplinas_turma = novas_discs_turma
                        st.success("✅ Disciplinas da turma atualizadas!")
                        st.rerun()
                
                # Mostrar disciplinas atuais
                if t.disciplinas_turma:
                    df_discs = pd.DataFrame([
                        {
                            "Disciplina": dt.nome,
                            "Carga Semanal": dt.carga_semanal,
                            "Professor": dt.professor
                        }
                        for dt in t.disciplinas_turma
                    ])
                    st.dataframe(df_discs, use_container_width=True)
                else:
                    st.info("Nenhuma disciplina cadastrada para esta turma.")
                
                # Botão de exclusão
                if st.button("🗑️ Excluir Turma", key=f"del_turma_{i}"):
                    st.session_state.turmas.pop(i)
                    st.success(f"✅ Turma '{t.nome}' excluída!")
                    st.rerun()
    else:
        st.info("⚠️ Nenhuma turma cadastrada.")

# =================== ABA 5: SALAS ===================
with aba5:
    st.header("🏫 Salas")
    
    # Adicionar nova sala
    with st.form("add_sala"):
        nome = st.text_input("Nome")
        capacidade = st.number_input("Capacidade", 1, 100, 30)
        tipo = st.selectbox("Tipo", ["normal", "laboratório", "auditório"])
        
        if st.form_submit_button("➕ Adicionar"):
            if nome:
                nova_sala = Sala(nome=nome, capacidade=capacidade, tipo=tipo)
                st.session_state.salas.append(nova_sala)
                st.success(f"✅ Sala '{nome}' adicionada!")
                st.rerun()
    
    # Listar salas
    if st.session_state.salas:
        st.subheader("Hotéis Salas Cadastradas")
        for i, s in enumerate(st.session_state.salas):
            with st.expander(f"🏫 {s.nome}"):
                st.write(f"**Capacidade:** {s.capacidade}")
                st.write(f"**Tipo:** {s.tipo}")
                
                col1, col2 = st.columns(2)
                if col1.button("🗑️ Excluir", key=f"del_sala_{i}"):
                    st.session_state.salas.pop(i)
                    st.success(f"✅ Sala '{s.nome}' excluída!")
                    st.rerun()
    else:
        st.info("⚠️ Nenhuma sala cadastrada.")

# =================== ABA 6: IMPORTAR/EXPORTAR ===================
with aba6:
    st.header("📥 Importar/Exportar Dados")
    
    # === EXPORTAR TEMPLATE ===
    st.subheader("📄 Baixar Template Excel")
    template_data = exportar_para_excel_template()
    st.download_button(
        label="📥 Baixar Template.xlsx",
        data=template_data,
        file_name="template_importacao.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.info("Use este template para importar turmas, professores e disciplinas.")
    
    # === IMPORTAR DADOS ===
    st.subheader("⬆️ Importar Dados de Excel")
    uploaded_file = st.file_uploader("Escolha um arquivo Excel (.xlsx)", type="xlsx")
    
    if uploaded_file:
        if st.button("📤 Importar Dados"):
            sucesso = importar_de_excel(uploaded_file)
            if sucesso:
                st.success("✅ Dados importados com sucesso! Recarregue a página para ver as mudanças.")
                st.rerun()