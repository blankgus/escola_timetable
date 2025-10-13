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
    st.header("📚 Disciplinas")

    # --- Formulário para Adicionar Nova Disciplina ---
    with st.form("add_disc"):
        nome = st.text_input("Nome")
        # Valores padrão
        carga = st.number_input("Carga Semanal", min_value=1, max_value=10, value=3)
        tipo = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"], index=1) # 'media' como padrão

        # Usar checkboxes para as séries
        st.subheader("Séries Ofertadas")
        series_validas = get_series_validas()
        series_selecionadas = st.multiselect("Selecione as séries", series_validas, default=[])

        cor_fundo = st.color_picker("Cor de Fundo", "#4A90E2")
        cor_fonte = st.color_picker("Cor da Fonte", "#FFFFFF")

        if st.form_submit_button("➕ Adicionar"):
            if nome:
                # Verifica se já existe
                if any(d.nome.lower() == nome.lower() for d in st.session_state.disciplinas):
                     st.warning(f"⚠️ Disciplina '{nome}' já existe.")
                else:
                    nova_disciplina = Disciplina(
                        nome=nome,
                        carga_semanal=carga,
                        tipo=tipo,
                        series=series_selecionadas, # Usa a lista de séries selecionadas
                        cor_fundo=cor_fundo,
                        cor_fonte=cor_fonte
                    )
                    st.session_state.disciplinas.append(nova_disciplina)
                    st.success(f"✅ Disciplina '{nome}' adicionada!")
                    st.rerun() # Recarrega para mostrar a nova entrada

    # --- Listagem e Edição de Disciplinas Existentes ---
    if st.session_state.disciplinas:
        st.subheader("📝 Disciplinas Cadastradas")
        # Ordenar por nome para facilitar a visualização
        disciplinas_ordenadas = sorted(st.session_state.disciplinas, key=lambda d: d.nome.lower())

        for d in disciplinas_ordenadas:
             with st.expander(f"📘 {d.nome}"):
                with st.form(f"edit_disc_{d.id}"):
                    nome_edit = st.text_input("Nome", value=d.nome, key=f"edit_nome_{d.id}")
                    carga_edit = st.number_input("Carga Semanal", min_value=1, max_value=10, value=d.carga_semanal, key=f"edit_carga_{d.id}")
                    tipo_edit = st.selectbox("Tipo", ["pesada", "media", "leve", "pratica"], index=["pesada", "media", "leve", "pratica"].index(d.tipo), key=f"edit_tipo_{d.id}")

                    # Checkboxes para editar séries
                    st.subheader("Séries Ofertadas")
                    series_validas = get_series_validas()
                    series_edit = st.multiselect("Selecione as séries", series_validas, default=d.series, key=f"edit_series_{d.id}")

                    cor_fundo_edit = st.color_picker("Cor de Fundo", value=d.cor_fundo, key=f"edit_cor_fundo_{d.id}")
                    cor_fonte_edit = st.color_picker("Cor da Fonte", value=d.cor_fonte, key=f"edit_cor_fonte_{d.id}")

                    col1, col2 = st.columns(2)
                    if col1.form_submit_button("💾 Salvar"):
                        # Atualiza o objeto na lista
                        d.nome = nome_edit
                        d.carga_semanal = carga_edit
                        d.tipo = tipo_edit
                        d.series = series_edit
                        d.cor_fundo = cor_fundo_edit
                        d.cor_fonte = cor_fonte_edit
                        st.success(f"✅ Disciplina '{nome_edit}' atualizada!")
                        st.rerun()

                    if col2.form_submit_button("🗑️ Excluir"):
                        st.session_state.disciplinas = [disc for disc in st.session_state.disciplinas if disc.id != d.id]
                        st.success(f"🗑️ Disciplina '{d.nome}' excluída!")
                        st.rerun()
    else:
        st.info("📭 Nenhuma disciplina cadastrada ainda.")

# =================== ABA 3: PROFESSORES ===================
with aba3:
    st.header("👩‍🏫 Professores")

    # --- Botão para Carregar Professores Padrão do PDF ---
    if st.button("📥 Carregar Professores Padrão (PDF)"):
        # Lista de professores com carga horária e apelidos do PDF
        # Vamos criar uma lista básica com nomes e apelidos
        professores_padrao = [
            ("Luciana Aparecida Barbosa da Silva", "Lan", 35), # Assumindo EM por padrão, ajuste se necessário
            ("Jussara Aparecida Ribeiro", "Ju", 35),
            ("Juliana Ferreira da Silva", "Ju Ferreira", 35),
            ("Marisa Aparecida Barbosa da Silva", "Mari", 35),
            ("Silvana Aparecida Barbosa da Silva", "Sil", 35),
            ("Rosana Aparecida Barbosa da Silva", "Ro", 35),
            ("Rosimeire Aparecida Barbosa da Silva", "Rosy", 35),
            ("Ana Claudia Barbosa da Silva", "Claudi", 35),
            ("Lucimar Aparecida Barbosa da Silva", "Luci", 35),
            ("Luciene Aparecida Barbosa da Silva", "Luciene", 35),
            ("Ana Paula Barbosa da Silva", "Paulinha", 35),
            ("Marlene Aparecida Barbosa da Silva", "Marlene", 35),
            ("Simone Aparecida Barbosa da Silva", "Simone", 35),
            ("Elaine Aparecida Barbosa da Silva", "Elaine", 35),
            ("Lucineia Aparecida Barbosa da Silva", "Lucineia", 35),
            ("Fabiana Aparecida Barbosa da Silva", "Fabiana", 35),
            ("Luciana Ferreira da Silva", "Lu Ferreira", 35),
            ("Patricia Aparecida Barbosa da Silva", "Paty", 35),
            ("Marinalva Aparecida Barbosa da Silva", "Marinalva", 35),
            ("Lucicleide Aparecida Barbosa da Silva", "Lucicleide", 35),
            ("Lucineide Aparecida Barbosa da Silva", "Lucineide", 35),
            ("Lucimar Barbosa da Silva", "Lucimar B", 35),
            ("Luciene Barbosa da Silva", "Luciene B", 35),
            ("Luciana Barbosa da Silva", "Luciana B", 35),
            ("Luciene Ferreira da Silva", "Luciene F", 35),
            ("Luciana Ferreira da Silva", "Luciana F", 35),
            # Adicione mais conforme necessário ou repita para EF com 25h se for o caso
        ]

        # Determinar quais disciplinas já existem
        nomes_disc_existentes = [d.nome for d in st.session_state.disciplinas]

        novos_professores_adicionados = 0
        for nome_completo, apelido, carga_horaria in professores_padrao:
            nome_usado = apelido if apelido else nome_completo.split()[0] # Usa apelido ou primeiro nome

            # Verifica se o professor já existe (pelo nome completo ou apelido)
            if any(p.nome.lower() == nome_completo.lower() or p.nome.lower() == nome_usado.lower() for p in st.session_state.professores):
                st.warning(f"⚠️ Professor '{nome_usado}' já existe e foi ignorado.")
                continue

            # Determina disponibilidade com base na carga horária (simplificado)
            # Para 25h (EF): seg, ter, qua, qui, sex (5 dias) * 5h = 25h -> Vamos assumir horários 1-5
            # Para 35h (EM): seg, ter, qua, qui, sex (5 dias) * 7h = 35h -> Vamos assumir horários 1-7
            # Esta lógica pode ser refinada depois.
            dias_disponiveis = {"seg", "ter", "qua", "qui", "sex"}
            if carga_horaria == 25:
                 # Exemplo: 25h pode ser 5 dias * 5 horas (assumindo horários 1-5)
                 horarios_disponiveis = {1, 2, 3, 5, 6} # Exclui recreio (4) e talvez o último
            else: # 35h
                 horarios_disponiveis = {1, 2, 3, 5, 6, 7} # Inclui todos exceto recreio (4)


            novo_professor = Professor(
                nome=nome_usado,
                disciplinas=[], # Inicialmente sem disciplinas associadas
                disponibilidade_dias=dias_disponiveis,
                disponibilidade_horarios=horarios_disponiveis,
                restricoes=set() # Nenhuma restrição inicial
            )
            st.session_state.professores.append(novo_professor)
            novos_professores_adicionados += 1

        if novos_professores_adicionados > 0:
            st.success(f"✅ {novos_professores_adicionados} professores padrão carregados!")
            st.rerun()
        else:
             st.info("ℹ️ Nenhum novo professor foi adicionado (todos já existiam).")


    # --- Formulário para Adicionar Novo Professor ---
    disc_nomes = [d.nome for d in st.session_state.disciplinas] if st.session_state.disciplinas else []
    with st.form("add_prof"):
        nome = st.text_input("Nome (ou Apelido)")
        discs = st.multiselect("Disciplinas que pode lecionar", disc_nomes, default=[])

        st.subheader("Disponibilidade")
        # Seleção de Dias
        dias_semana = ["seg", "ter", "qua", "qui", "sex"] # Dias úteis
        dias_default = ["seg", "ter", "qua", "qui", "sex"] # Todos por padrão
        dias_disp = st.multiselect("Dias disponíveis", dias_semana, default=dias_default)

        # Seleção de Horários
        # Supondo horários de 1 a 7
        horarios_possiveis = list(range(1, 8)) # [1, 2, 3, 4, 5, 6, 7]
        horarios_default = [1, 2, 3, 5, 6, 7] # Exclui recreio (4) por padrão? Ou inclui todos?
        horarios_disp = st.multiselect("Horários disponíveis", horarios_possiveis, default=horarios_default)

        if st.form_submit_button("➕ Adicionar"):
            if nome:
                # Verifica se já existe
                if any(p.nome.lower() == nome.lower() for p in st.session_state.professores):
                    st.warning(f"⚠️ Professor '{nome}' já existe.")
                else:
                    novo_professor = Professor(
                        nome=nome,
                        disciplinas=discs,
                        disponibilidade_dias=set(dias_disp),
                        disponibilidade_horarios=set(horarios_disp),
                        restricoes=set() # Inicialmente sem restrições
                    )
                    st.session_state.professores.append(novo_professor)
                    st.success(f"✅ Professor '{nome}' adicionado!")
                    st.rerun()

    # --- Listagem e Edição de Professores Existentes ---
    if st.session_state.professores:
        st.subheader("👥 Professores Cadastrados")
        # Ordenar por nome para facilitar a visualização
        professores_ordenados = sorted(st.session_state.professores, key=lambda p: p.nome.lower())

        for p in professores_ordenados:
            with st.expander(f"👤 {p.nome}"):
                with st.form(f"edit_prof_{p.id}"):
                    nome_edit = st.text_input("Nome (ou Apelido)", value=p.nome, key=f"edit_nome_{p.id}")
                    # Garantir que as disciplinas válidas sejam usadas
                    disc_nomes = [d.nome for d in st.session_state.disciplinas] if st.session_state.disciplinas else []
                    discs_validas = [d for d in p.disciplinas if d in disc_nomes]
                    discs_edit = st.multiselect("Disciplinas que pode lecionar", disc_nomes, default=discs_validas, key=f"edit_discs_{p.id}")

                    st.subheader("Disponibilidade")
                    dias_semana = ["seg", "ter", "qua", "qui", "sex"]
                    dias_edit = st.multiselect("Dias disponíveis", dias_semana, default=list(p.disponibilidade_dias), key=f"edit_dias_{p.id}")

                    horarios_possiveis = list(range(1, 8)) # [1, 2, 3, 4, 5, 6, 7]
                    horarios_edit = st.multiselect("Horários disponíveis", horarios_possiveis, default=list(p.disponibilidade_horarios), key=f"edit_horarios_{p.id}")

                    # Campo para restrições (opcional, avançado)
                    restricoes_atuais = ", ".join(sorted(p.restricoes)) if p.restricoes else ""
                    restricoes_input = st.text_input(
                        "Restrições (opcional, formato: dia_horario, ex: seg_1, qua_3)",
                        value=restricoes_atuais,
                        help="Separe múltiplas restrições por vírgula.",
                        key=f"edit_restricoes_{p.id}"
                    )

                    col1, col2 = st.columns(2)
                    if col1.form_submit_button("💾 Salvar"):
                        # Processa as restrições
                        novas_restricoes = set()
                        if restricoes_input.strip():
                             novas_restricoes = {r.strip().lower() for r in restricoes_input.split(',') if r.strip()}

                        # Atualiza o objeto na lista
                        p.nome = nome_edit
                        p.disciplinas = discs_edit
                        p.disponibilidade_dias = set(dias_edit)
                        p.disponibilidade_horarios = set(horarios_edit)
                        p.restricoes = novas_restricoes
                        st.success(f"✅ Professor '{nome_edit}' atualizado!")
                        st.rerun()

                    if col2.form_submit_button("🗑️ Excluir"):
                        st.session_state.professores = [prof for prof in st.session_state.professores if prof.id != p.id]
                        st.success(f"🗑️ Professor '{p.nome}' excluído!")
                        st.rerun()
    else:
        st.info("📭 Nenhum professor cadastrado ainda. Use o botão 'Carregar Professores Padrão (PDF)' ou adicione manualmente.")
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
