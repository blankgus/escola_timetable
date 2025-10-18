import streamlit as st
import pandas as pd
import database
from session_state import init_session_state
from auto_save import salvar_tudo
from models import Turma, Professor, Disciplina, Sala, DIAS_SEMANA, HORARIOS_DISPONIVEIS
import io

# Configuração da página
st.set_page_config(page_title="Escola Timetable", layout="wide")
st.title("🕒 Gerador Inteligente de Grade Horária - Grupos A e B")

# Inicialização
try:
    init_session_state()
    st.success("✅ Sistema inicializado com sucesso!")
except Exception as e:
    st.error(f"❌ Erro na inicialização: {str(e)}")
    if st.button("🔄 Resetar Banco de Dados"):
        database.resetar_banco()
        st.rerun()
    st.stop()

# Função auxiliar
def obter_grupo_seguro(objeto, opcoes=["A", "B", "AMBOS"]):
    try:
        if hasattr(objeto, 'grupo'):
            grupo = objeto.grupo
            if grupo in opcoes:
                return grupo
        return "A"
    except:
        return "A"

# Menu de abas
abas = st.tabs(["🏠 Início", "📚 Disciplinas", "👩‍🏫 Professores", "🎒 Turmas", "🏫 Salas", "🗓️ Gerar Grade"])

with abas[0]:  # ABA INÍCIO
    st.header("Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Turmas", len(st.session_state.turmas))
    with col2:
        st.metric("Professores", len(st.session_state.professores))
    with col3:
        st.metric("Disciplinas", len(st.session_state.disciplinas))
    with col4:
        st.metric("Salas", len(st.session_state.salas))
    
    if st.button("💾 Salvar Tudo no Banco"):
        if salvar_tudo():
            st.success("✅ Todos os dados salvos!")

with abas[1]:  # ABA DISCIPLINAS
    st.header("📚 Disciplinas")
    
    grupo_filtro = st.selectbox("Filtrar por Grupo", ["Todos", "A", "B"], key="filtro_disc")
    
    with st.expander("➕ Adicionar Nova Disciplina", expanded=False):
        with st.form("add_disc"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome da Disciplina*")
                carga = st.number_input("Carga Semanal*", 1, 10, 3)
                tipo = st.selectbox("Tipo*", ["pesada", "media", "leve", "pratica"])
            with col2:
                series = st.text_input("Séries* (separadas por vírgula)", "6ano,7ano,8ano,9ano,1em,2em,3em")
                grupo = st.selectbox("Grupo*", ["A", "B"])
                cor_fundo = st.color_picker("Cor de Fundo", "#4A90E2")
                cor_fonte = st.color_picker("Cor da Fonte", "#FFFFFF")
            
            if st.form_submit_button("✅ Adicionar Disciplina"):
                if nome and series:
                    series_list = [s.strip() for s in series.split(",") if s.strip()]
                    nova_disciplina = Disciplina(nome, carga, tipo, series_list, grupo, cor_fundo, cor_fonte)
                    st.session_state.disciplinas.append(nova_disciplina)
                    if salvar_tudo():
                        st.success(f"✅ Disciplina '{nome}' adicionada!")
                    st.rerun()
                else:
                    st.error("❌ Preencha todos os campos obrigatórios (*)")
    
    st.subheader("📋 Lista de Disciplinas")
    
    disciplinas_exibir = st.session_state.disciplinas
    if grupo_filtro != "Todos":
        disciplinas_exibir = [d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == grupo_filtro]
    
    if not disciplinas_exibir:
        st.info("📝 Nenhuma disciplina cadastrada. Use o formulário acima para adicionar.")
    
    for disc in disciplinas_exibir:
        with st.expander(f"📖 {disc.nome} [{obter_grupo_seguro(disc)}]", expanded=False):
            with st.form(f"edit_disc_{disc.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome", disc.nome, key=f"nome_{disc.id}")
                    nova_carga = st.number_input("Carga Semanal", 1, 10, disc.carga_semanal, key=f"carga_{disc.id}")
                    novo_tipo = st.selectbox(
                        "Tipo", 
                        ["pesada", "media", "leve", "pratica"],
                        index=["pesada", "media", "leve", "pratica"].index(disc.tipo),
                        key=f"tipo_{disc.id}"
                    )
                with col2:
                    novas_series = st.text_input("Séries", ", ".join(disc.series), key=f"series_{disc.id}")
                    novo_grupo = st.selectbox(
                        "Grupo", 
                        ["A", "B"],
                        index=0 if obter_grupo_seguro(disc) == "A" else 1,
                        key=f"grupo_{disc.id}"
                    )
                    nova_cor_fundo = st.color_picker("Cor de Fundo", disc.cor_fundo, key=f"cor_fundo_{disc.id}")
                    nova_cor_fonte = st.color_picker("Cor da Fonte", disc.cor_fonte, key=f"cor_fonte_{disc.id}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar Alterações"):
                        if novo_nome and novas_series:
                            series_list = [s.strip() for s in novas_series.split(",") if s.strip()]
                            disc.nome = novo_nome
                            disc.carga_semanal = nova_carga
                            disc.tipo = novo_tipo
                            disc.series = series_list
                            disc.grupo = novo_grupo
                            disc.cor_fundo = nova_cor_fundo
                            disc.cor_fonte = nova_cor_fonte
                            
                            if salvar_tudo():
                                st.success("✅ Disciplina atualizada!")
                            st.rerun()
                        else:
                            st.error("❌ Preencha todos os campos obrigatórios")
                
                with col2:
                    if st.form_submit_button("🗑️ Excluir Disciplina", type="secondary"):
                        st.session_state.disciplinas.remove(disc)
                        if salvar_tudo():
                            st.success("✅ Disciplina excluída!")
                        st.rerun()

with abas[2]:  # ABA PROFESSORES (CORRIGIDA)
    st.header("👩‍🏫 Professores")
    
    grupo_filtro = st.selectbox("Filtrar por Grupo", ["Todos", "A", "B", "AMBOS"], key="filtro_prof")
    disc_nomes = [d.nome for d in st.session_state.disciplinas]
    
    with st.expander("➕ Adicionar Novo Professor", expanded=False):
        with st.form("add_prof"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome do Professor*")
                disciplinas = st.multiselect("Disciplinas*", disc_nomes)
                grupo = st.selectbox("Grupo*", ["A", "B", "AMBOS"])
            with col2:
                disponibilidade = st.multiselect("Dias Disponíveis*", DIAS_SEMANA, default=DIAS_SEMANA)
                st.write("**Horários Indisponíveis:**")
                
                horarios_indisponiveis = []
                for dia in DIAS_SEMANA:
                    with st.container():
                        st.write(f"**{dia.upper()}:**")
                        horarios_cols = st.columns(4)
                        for i, horario in enumerate(HORARIOS_DISPONIVEIS):
                            with horarios_cols[i % 4]:
                                if st.checkbox(f"{horario}º", key=f"add_{dia}_{horario}"):
                                    horarios_indisponiveis.append(f"{dia}_{horario}")
            
            if st.form_submit_button("✅ Adicionar Professor"):
                if nome and disciplinas and disponibilidade:
                    novo_professor = Professor(
                        nome, 
                        disciplinas, 
                        set(disponibilidade), 
                        grupo,
                        set(horarios_indisponiveis)
                    )
                    st.session_state.professores.append(novo_professor)
                    if salvar_tudo():
                        st.success(f"✅ Professor '{nome}' adicionado!")
                    st.rerun()
                else:
                    st.error("❌ Preencha todos os campos obrigatórios (*)")
    
    st.subheader("📋 Lista de Professores")
    
    professores_exibir = st.session_state.professores
    if grupo_filtro != "Todos":
        professores_exibir = [p for p in st.session_state.professores if obter_grupo_seguro(p) == grupo_filtro]
    
    if not professores_exibir:
        st.info("📝 Nenhum professor cadastrado. Use o formulário acima para adicionar.")
    
    for prof in professores_exibir:
        with st.expander(f"👨‍🏫 {prof.nome} [{obter_grupo_seguro(prof)}]", expanded=False):
            # ✅ CORREÇÃO: Filtrar disciplinas válidas
            disciplinas_validas = [d for d in prof.disciplinas if d in disc_nomes]
            
            with st.form(f"edit_prof_{prof.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome", prof.nome, key=f"nome_prof_{prof.id}")
                    
                    # ✅ CORREÇÃO: Usar apenas disciplinas válidas como default
                    novas_disciplinas = st.multiselect(
                        "Disciplinas", 
                        disc_nomes, 
                        default=disciplinas_validas,  # ✅ Só disciplinas que existem
                        key=f"disc_prof_{prof.id}"
                    )
                    
                    novo_grupo = st.selectbox(
                        "Grupo", 
                        ["A", "B", "AMBOS"],
                        index=["A", "B", "AMBOS"].index(obter_grupo_seguro(prof)),
                        key=f"grupo_prof_{prof.id}"
                    )
                with col2:
                    nova_disponibilidade = st.multiselect(
                        "Dias Disponíveis", 
                        DIAS_SEMANA, 
                        default=list(prof.disponibilidade),
                        key=f"disp_prof_{prof.id}"
                    )
                    
                    st.write("**Horários Indisponíveis:**")
                    novos_horarios_indisponiveis = []
                    for dia in DIAS_SEMANA:
                        with st.container():
                            st.write(f"**{dia.upper()}:**")
                            horarios_cols = st.columns(4)
                            for i, horario in enumerate(HORARIOS_DISPONIVEIS):
                                with horarios_cols[i % 4]:
                                    checked = f"{dia}_{horario}" in prof.horarios_indisponiveis
                                    if st.checkbox(
                                        f"{horario}º", 
                                        value=checked,
                                        key=f"edit_{prof.id}_{dia}_{horario}"
                                    ):
                                        novos_horarios_indisponiveis.append(f"{dia}_{horario}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar Alterações"):
                        if novo_nome and novas_disciplinas and nova_disponibilidade:
                            prof.nome = novo_nome
                            prof.disciplinas = novas_disciplinas
                            prof.grupo = novo_grupo
                            prof.disponibilidade = set(nova_disponibilidade)
                            prof.horarios_indisponiveis = set(novos_horarios_indisponiveis)
                            
                            if salvar_tudo():
                                st.success("✅ Professor atualizado!")
                            st.rerun()
                        else:
                            st.error("❌ Preencha todos os campos obrigatórios")
                
                with col2:
                    if st.form_submit_button("🗑️ Excluir Professor", type="secondary"):
                        st.session_state.professores.remove(prof)
                        if salvar_tudo():
                            st.success("✅ Professor excluído!")
                        st.rerun()

with abas[3]:  # ABA TURMAS
    st.header("🎒 Turmas")
    
    grupo_filtro = st.selectbox("Filtrar por Grupo", ["Todos", "A", "B"], key="filtro_turma")
    
    with st.expander("➕ Adicionar Nova Turma", expanded=False):
        with st.form("add_turma"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome da Turma* (ex: 8anoA)")
                serie = st.text_input("Série* (ex: 8ano)")
            with col2:
                turno = st.selectbox("Turno*", ["manha", "tarde"])
                grupo = st.selectbox("Grupo*", ["A", "B"])
            
            if st.form_submit_button("✅ Adicionar Turma"):
                if nome and serie:
                    nova_turma = Turma(nome, serie, turno, grupo)
                    st.session_state.turmas.append(nova_turma)
                    if salvar_tudo():
                        st.success(f"✅ Turma '{nome}' adicionada!")
                    st.rerun()
                else:
                    st.error("❌ Preencha todos os campos obrigatórios (*)")
    
    st.subheader("📋 Lista de Turmas")
    
    turmas_exibir = st.session_state.turmas
    if grupo_filtro != "Todos":
        turmas_exibir = [t for t in st.session_state.turmas if obter_grupo_seguro(t) == grupo_filtro]
    
    if not turmas_exibir:
        st.info("📝 Nenhuma turma cadastrada. Use o formulário acima para adicionar.")
    
    for turma in turmas_exibir:
        with st.expander(f"🎒 {turma.nome} [{obter_grupo_seguro(turma)}]", expanded=False):
            with st.form(f"edit_turma_{turma.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome", turma.nome, key=f"nome_turma_{turma.id}")
                    nova_serie = st.text_input("Série", turma.serie, key=f"serie_turma_{turma.id}")
                with col2:
                    novo_turno = st.selectbox(
                        "Turno", 
                        ["manha", "tarde"],
                        index=0 if turma.turno == "manha" else 1,
                        key=f"turno_turma_{turma.id}"
                    )
                    novo_grupo = st.selectbox(
                        "Grupo", 
                        ["A", "B"],
                        index=0 if obter_grupo_seguro(turma) == "A" else 1,
                        key=f"grupo_turma_{turma.id}"
                    )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar Alterações"):
                        if novo_nome and nova_serie:
                            turma.nome = novo_nome
                            turma.serie = nova_serie
                            turma.turno = novo_turno
                            turma.grupo = novo_grupo
                            
                            if salvar_tudo():
                                st.success("✅ Turma atualizada!")
                            st.rerun()
                        else:
                            st.error("❌ Preencha todos os campos obrigatórios")
                
                with col2:
                    if st.form_submit_button("🗑️ Excluir Turma", type="secondary"):
                        st.session_state.turmas.remove(turma)
                        if salvar_tudo():
                            st.success("✅ Turma excluída!")
                        st.rerun()

with abas[4]:  # ABA SALAS
    st.header("🏫 Salas")
    
    with st.expander("➕ Adicionar Nova Sala", expanded=False):
        with st.form("add_sala"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome da Sala*")
                capacidade = st.number_input("Capacidade*", 1, 100, 30)
            with col2:
                tipo = st.selectbox("Tipo*", ["normal", "laboratório", "auditório"])
            
            if st.form_submit_button("✅ Adicionar Sala"):
                if nome:
                    nova_sala = Sala(nome, capacidade, tipo)
                    st.session_state.salas.append(nova_sala)
                    if salvar_tudo():
                        st.success(f"✅ Sala '{nome}' adicionada!")
                    st.rerun()
                else:
                    st.error("❌ Preencha todos os campos obrigatórios (*)")
    
    st.subheader("📋 Lista de Salas")
    
    if not st.session_state.salas:
        st.info("📝 Nenhuma sala cadastrada. Use o formulário acima para adicionar.")
    
    for sala in st.session_state.salas:
        with st.expander(f"🏫 {sala.nome}", expanded=False):
            with st.form(f"edit_sala_{sala.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome", sala.nome, key=f"nome_sala_{sala.id}")
                    nova_capacidade = st.number_input("Capacidade", 1, 100, sala.capacidade, key=f"cap_sala_{sala.id}")
                with col2:
                    novo_tipo = st.selectbox(
                        "Tipo", 
                        ["normal", "laboratório", "auditório"],
                        index=["normal", "laboratório", "auditório"].index(sala.tipo),
                        key=f"tipo_sala_{sala.id}"
                    )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar Alterações"):
                        if novo_nome:
                            sala.nome = novo_nome
                            sala.capacidade = nova_capacidade
                            sala.tipo = novo_tipo
                            
                            if salvar_tudo():
                                st.success("✅ Sala atualizada!")
                            st.rerun()
                        else:
                            st.error("❌ Preencha todos os campos obrigatórios")
                
                with col2:
                    if st.form_submit_button("🗑️ Excluir Sala", type="secondary"):
                        st.session_state.salas.remove(sala)
                        if salvar_tudo():
                            st.success("✅ Sala excluída!")
                        st.rerun()

with abas[5]:  # ABA GERAR GRADE
    st.header("🗓️ Gerar Grade Horária")
    st.info("🔧 Funcionalidade em desenvolvimento...")
    st.write("Configure primeiro as disciplinas, professores e turmas acima.")

# Sidebar
st.sidebar.title("⚙️ Configurações")
if st.sidebar.button("🔄 Resetar Banco de Dados"):
    database.resetar_banco()
    st.sidebar.success("✅ Banco resetado! Recarregue a página.")

st.sidebar.write("### Status do Sistema:")
st.sidebar.write(f"**Turmas:** {len(st.session_state.turmas)}")
st.sidebar.write(f"**Professores:** {len(st.session_state.professores)}")
st.sidebar.write(f"**Disciplinas:** {len(st.session_state.disciplinas)}")
st.sidebar.write(f"**Salas:** {len(st.session_state.salas)}")
st.sidebar.write(f"**Aulas na Grade:** {len(st.session_state.get('aulas', []))}")