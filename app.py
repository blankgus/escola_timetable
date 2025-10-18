import streamlit as st
import pandas as pd
import database
from session_state import init_session_state
from auto_save import salvar_tudo
from models import Turma, Professor, Disciplina, Sala, DIAS_SEMANA, HORARIOS_DISPONIVEIS
from scheduler_ortools import GradeHorariaORTools
from simple_scheduler import SimpleGradeHoraria
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
    
    # Estatísticas por grupo
    turmas_a = [t for t in st.session_state.turmas if obter_grupo_seguro(t) == "A"]
    turmas_b = [t for t in st.session_state.turmas if obter_grupo_seguro(t) == "B"]
    
    st.subheader("📊 Estatísticas por Grupo")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Grupo A**")
        st.write(f"Turmas: {len(turmas_a)}")
        st.write(f"Disciplinas: {len([d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == 'A'])}")
    with col2:
        st.write("**Grupo B**")
        st.write(f"Turmas: {len(turmas_b)}")
        st.write(f"Disciplinas: {len([d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == 'B'])}")
    
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

with abas[2]:  # ABA PROFESSORES
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
        st.info("📝 Nenhum professor cadastrada. Use o formulário acima para adicionar.")
    
    for prof in professores_exibir:
        with st.expander(f"👨‍🏫 {prof.nome} [{obter_grupo_seguro(prof)}]", expanded=False):
            # Filtrar disciplinas válidas
            disciplinas_validas = [d for d in prof.disciplinas if d in disc_nomes]
            
            with st.form(f"edit_prof_{prof.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome", prof.nome, key=f"nome_prof_{prof.id}")
                    
                    # Usar apenas disciplinas válidas como default
                    novas_disciplinas = st.multiselect(
                        "Disciplinas", 
                        disc_nomes, 
                        default=disciplinas_validas,
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
                # Apenas turno MANHÃ disponível
                turno = st.selectbox("Turno*", ["manha"], disabled=True)
                grupo = st.selectbox("Grupo*", ["A", "B"])
            
            if st.form_submit_button("✅ Adicionar Turma"):
                if nome and serie:
                    nova_turma = Turma(nome, serie, "manha", grupo)
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
                    # Apenas turno MANHÃ, desabilitado para edição
                    st.text_input("Turno", "manha", disabled=True, key=f"turno_turma_{turma.id}")
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
                            turma.grupo = novo_grupo
                            # Turno permanece sempre "manha"
                            
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
    
    st.subheader("🎯 Configurações da Grade")
    
    col1, col2 = st.columns(2)
    with col1:
        # Opções simplificadas para apenas manhã
        tipo_grade = st.selectbox(
            "Tipo de Grade",
            [
                "Grade Completa - Todas as Turmas",
                "Grade por Grupo A",
                "Grade por Grupo B", 
                "Grade por Turma Específica"
            ]
        )
        
        # Seleção de turma específica
        if tipo_grade == "Grade por Turma Específica":
            turmas_opcoes = [t.nome for t in st.session_state.turmas]
            if turmas_opcoes:
                turma_selecionada = st.selectbox("Selecionar Turma", turmas_opcoes)
            else:
                st.warning("⚠️ Nenhuma turma cadastrada")
                turma_selecionada = None
    
    with col2:
        tipo_algoritmo = st.selectbox(
            "Algoritmo de Geração",
            ["Algoritmo Simples (Rápido)", "Google OR-Tools (Otimizado)"]
        )
        
        relaxar_horarios = st.checkbox(
            "Relaxar horários ideais",
            value=False,
            help="Permitir disciplinas pesadas em qualquer horário"
        )
    
    st.subheader("📊 Pré-análise de Viabilidade")
    
    # Calcular carga horária conforme seleção
    if tipo_grade == "Grade por Grupo A":
        turmas_filtradas = [t for t in st.session_state.turmas if obter_grupo_seguro(t) == "A"]
        grupo_texto = "Grupo A"
    elif tipo_grade == "Grade por Grupo B":
        turmas_filtradas = [t for t in st.session_state.turmas if obter_grupo_seguro(t) == "B"]
        grupo_texto = "Grupo B"
    elif tipo_grade == "Grade por Turma Específica" and turma_selecionada:
        turmas_filtradas = [t for t in st.session_state.turmas if t.nome == turma_selecionada]
        grupo_texto = f"Turma {turma_selecionada}"
    else:
        turmas_filtradas = st.session_state.turmas
        grupo_texto = "Todas as Turmas"
    
    # Todas as disciplinas são da manhã agora
    disciplinas_filtradas = st.session_state.disciplinas
    
    # Calcular total de aulas necessárias
    total_aulas = 0
    aulas_por_turma = {}
    
    for turma in turmas_filtradas:
        aulas_turma = 0
        for disc in disciplinas_filtradas:
            if turma.serie in disc.series:
                aulas_turma += disc.carga_semanal
                total_aulas += disc.carga_semanal
        aulas_por_turma[turma.nome] = aulas_turma
    
    capacidade_total = len(DIAS_SEMANA) * len(HORARIOS_DISPONIVEIS) * len(turmas_filtradas)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Turmas", len(turmas_filtradas))
    with col2:
        st.metric("Aulas Necessárias", total_aulas)
    with col3:
        st.metric("Capacidade Disponível", capacidade_total)
    
    # Verificar viabilidade
    if total_aulas == 0:
        st.error("❌ Nenhuma aula para alocar! Verifique se as disciplinas estão associadas às séries corretas.")
    elif total_aulas > capacidade_total:
        st.error("❌ Capacidade insuficiente! Reduza a carga horária.")
        st.write("**Aulas por turma:**")
        for turma, aulas in aulas_por_turma.items():
            st.write(f"- {turma}: {aulas} aulas")
    else:
        st.success("✅ Capacidade suficiente para gerar grade!")
        
        # BOTÃO PARA GERAR GRADE
        if st.button("🚀 Gerar Grade Horária", type="primary", use_container_width=True):
            if not turmas_filtradas:
                st.error("❌ Nenhuma turma selecionada para gerar grade!")
            elif not disciplinas_filtradas:
                st.error("❌ Nenhuma disciplina disponível para as turmas selecionadas!")
            else:
                with st.spinner(f"Gerando grade para {grupo_texto}..."):
                    try:
                        # Filtrar professores conforme o grupo
                        if tipo_grade == "Grade por Grupo A":
                            professores_filtrados = [p for p in st.session_state.professores 
                                                   if obter_grupo_seguro(p) in ["A", "AMBOS"]]
                        elif tipo_grade == "Grade por Grupo B":
                            professores_filtrados = [p for p in st.session_state.professores 
                                                   if obter_grupo_seguro(p) in ["B", "AMBOS"]]
                        else:
                            professores_filtrados = st.session_state.professores
                        
                        # Escolher algoritmo
                        if tipo_algoritmo == "Google OR-Tools (Otimizado)":
                            try:
                                grade = GradeHorariaORTools(
                                    turmas_filtradas,
                                    professores_filtrados,
                                    disciplinas_filtradas,
                                    relaxar_horario_ideal=relaxar_horarios
                                )
                                aulas = grade.resolver()
                                metodo = "Google OR-Tools"
                            except Exception as e:
                                st.warning(f"⚠️ OR-Tools falhou: {str(e)}. Usando algoritmo simples...")
                                simple_grade = SimpleGradeHoraria(
                                    turmas_filtradas,
                                    professores_filtrados,
                                    disciplinas_filtradas
                                )
                                aulas = simple_grade.gerar_grade()
                                metodo = "Algoritmo Simples (fallback)"
                        else:
                            simple_grade = SimpleGradeHoraria(
                                turmas_filtradas,
                                professores_filtrados,
                                disciplinas_filtradas
                            )
                            aulas = simple_grade.gerar_grade()
                            metodo = "Algoritmo Simples"
                        
                        # Filtrar aulas se for grade específica
                        if tipo_grade == "Grade por Turma Específica" and turma_selecionada:
                            aulas = [a for a in aulas if a.turma == turma_selecionada]
                        
                        st.session_state.aulas = aulas
                        if salvar_tudo():
                            st.success(f"✅ Grade {grupo_texto} gerada com {metodo}! ({len(aulas)} aulas)")
                        
                        # Exibir estatísticas
                        st.subheader("📈 Estatísticas da Grade Gerada")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total de Aulas", len(aulas))
                        with col2:
                            professores_utilizados = len(set(a.professor for a in aulas))
                            st.metric("Professores Utilizados", professores_utilizados)
                        with col3:
                            turmas_utilizadas = len(set(a.turma for a in aulas))
                            st.metric("Turmas com Aula", turmas_utilizadas)
                        
                        # Exibir grade gerada
                        st.subheader("📋 Grade Horária Gerada")
                        
                        if aulas:
                            # Criar DataFrame com as aulas
                            df_aulas = pd.DataFrame([
                                {
                                    "Turma": a.turma,
                                    "Disciplina": a.disciplina, 
                                    "Professor": a.professor,
                                    "Dia": a.dia,
                                    "Horário": f"{a.horario}º",
                                    "Sala": a.sala,
                                    "Grupo": a.grupo
                                }
                                for a in aulas
                            ])
                            
                            # Ordenar por turma, dia e horário
                            df_aulas = df_aulas.sort_values(["Turma", "Dia", "Horário"])
                            
                            # Exibir tabela
                            st.dataframe(df_aulas, use_container_width=True)
                            
                            # Download da grade
                            output = io.BytesIO()
                            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                df_aulas.to_excel(writer, sheet_name="Grade_Completa", index=False)
                                
                                # Adicionar estatísticas
                                stats_df = pd.DataFrame({
                                    "Estatística": ["Total de Aulas", "Professores Utilizados", "Turmas com Aula", "Método"],
                                    "Valor": [len(aulas), professores_utilizados, turmas_utilizadas, metodo]
                                })
                                stats_df.to_excel(writer, sheet_name="Estatísticas", index=False)
                            
                            st.download_button(
                                "📥 Baixar Grade em Excel",
                                output.getvalue(),
                                f"grade_{grupo_texto.replace(' ', '_')}.xlsx",
                                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                            
                            # Visualização por turma
                            st.subheader("👀 Visualização por Turma")
                            
                            turmas_com_aulas = sorted(set(a.turma for a in aulas))
                            for turma_nome in turmas_com_aulas:
                                with st.expander(f"Grade da Turma {turma_nome}", expanded=False):
                                    aulas_turma = [a for a in aulas if a.turma == turma_nome]
                                    
                                    # Criar grade visual
                                    dias = DIAS_SEMANA
                                    horarios = HORARIOS_DISPONIVEIS
                                    
                                    grade_visual = {}
                                    for horario in horarios:
                                        grade_visual[horario] = {}
                                        for dia in dias:
                                            grade_visual[horario][dia] = ""
                                    
                                    for aula in aulas_turma:
                                        if aula.dia in dias and aula.horario in horarios:
                                            grade_visual[aula.horario][aula.dia] = f"{aula.disciplina}\n({aula.professor})"
                                    
                                    # Converter para DataFrame
                                    df_grade = pd.DataFrame(grade_visual).T
                                    df_grade.index = [f"{h}º Horário" for h in df_grade.index]
                                    df_grade = df_grade.reindex(columns=dias)
                                    
                                    st.dataframe(df_grade, use_container_width=True)
                        else:
                            st.warning("⚠️ Nenhuma aula foi gerada. Verifique a configuração dos dados.")
                            
                    except Exception as e:
                        st.error(f"❌ Erro ao gerar grade: {str(e)}")
                        st.info("💡 Dicas para solucionar:")
                        st.write("- Verifique se os professores têm as disciplinas corretas")
                        st.write("- Confirme a disponibilidade dos professores")
                        st.write("- Verifique se as disciplinas estão associadas às séries das turmas")
    
    # Seção de troubleshooting
    with st.expander("🔍 Diagnóstico de Problemas", expanded=False):
        st.write("**Problemas comuns e soluções:**")
        
        st.write("1. **Nenhuma aula gerada:**")
        st.write("   - Verifique se as disciplinas estão associadas às séries das turmas")
        st.write("   - Confirme que os professores têm as disciplinas necessárias")
        st.write("   - Verifique a disponibilidade dos professores")
        
        st.write("2. **Capacidade insuficiente:**")
        st.write("   - Reduza a carga horária das disciplinas")
        st.write("   - Aumente os dias de aula disponíveis")
        st.write("   - Adicione mais horários disponíveis")
        
        st.write("3. **Professores sobrecarregados:**")
        st.write("   - Verifique os horários indisponíveis dos professores")
        st.write("   - Distribua melhor as disciplinas entre os professores")
        
        # Mostrar detalhes dos dados atuais
        st.write("**Dados atuais:**")
        st.write(f"- Turmas: {len(turmas_filtradas)}")
        st.write(f"- Disciplinas: {len(disciplinas_filtradas)}")
        st.write(f"- Professores: {len([p for p in st.session_state.professores if any(disc in p.disciplinas for disc in [d.nome for d in disciplinas_filtradas])])}")

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