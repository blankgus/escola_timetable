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

# Função para calcular carga horária máxima por série
def calcular_carga_maxima(serie):
    """Calcula a carga horária máxima semanal baseada na série"""
    if 'em' in serie.lower() or 'medio' in serie.lower() or serie in ['1em', '2em', '3em']:
        return 32  # Ensino Médio: 32 horas
    else:
        return 25  # EF II: 25 horas

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
    
    # Verificação de carga horária - CORRIGIDA: SEPARA POR GRUPO
    st.subheader("📈 Verificação de Carga Horária")
    for turma in st.session_state.turmas:
        carga_total = 0
        disciplinas_turma = []
        grupo_turma = obter_grupo_seguro(turma)
        
        for disc in st.session_state.disciplinas:
            # CORREÇÃO: Só soma disciplinas do MESMO GRUPO da turma
            if turma.serie in disc.series and obter_grupo_seguro(disc) == grupo_turma:
                carga_total += disc.carga_semanal
                disciplinas_turma.append(f"{disc.nome} ({disc.carga_semanal}h)")
        
        carga_maxima = calcular_carga_maxima(turma.serie)
        status = "✅" if carga_total <= carga_maxima else "❌"
        
        st.write(f"**{turma.nome}** [{grupo_turma}] ({turma.serie}): {carga_total}/{carga_maxima}h {status}")
        if disciplinas_turma:
            st.caption(f"Disciplinas: {', '.join(disciplinas_turma)}")
        else:
            st.caption("⚠️ Nenhuma disciplina atribuída para este grupo")
    
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
            
            # Mostrar carga horária máxima baseada na série
            if serie:
                carga_maxima = calcular_carga_maxima(serie)
                nivel = "Ensino Médio" if carga_maxima == 32 else "EF II"
                st.info(f"💡 {nivel}: Carga horária máxima semanal = {carga_maxima}h")
            
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
                
                # CORREÇÃO: Mostrar estatísticas considerando apenas disciplinas do MESMO GRUPO
                grupo_turma = obter_grupo_seguro(turma)
                carga_atual = 0
                disciplinas_turma = []
                for disc in st.session_state.disciplinas:
                    # Só conta disciplinas do MESMO GRUPO
                    if turma.serie in disc.series and obter_grupo_seguro(disc) == grupo_turma:
                        carga_atual += disc.carga_semanal
                        disciplinas_turma.append(disc.nome)
                
                carga_maxima = calcular_carga_maxima(turma.serie)
                st.write(f"**Carga horária atual:** {carga_atual}/{carga_maxima}h")
                if disciplinas_turma:
                    st.caption(f"Disciplinas do Grupo {grupo_turma}: {', '.join(disciplinas_turma)}")
                else:
                    st.caption("⚠️ Nenhuma disciplina do mesmo grupo atribuída")
                
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
    
    # CORREÇÃO: Filtrar disciplinas pelo GRUPO CORRETO
    if tipo_grade == "Grade por Grupo A":
        disciplinas_filtradas = [d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == "A"]
    elif tipo_grade == "Grade por Grupo B":
        disciplinas_filtradas = [d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == "B"]
    else:
        # Para grade completa, usar todas as disciplinas (cada turma só pega as do seu grupo)
        disciplinas_filtradas = st.session_state.disciplinas
    
    # Calcular total de aulas necessárias - CORRIGIDO: SEPARA POR GRUPO
    total_aulas = 0
    aulas_por_turma = {}
    problemas_carga = []
    
    for turma in turmas_filtradas:
        aulas_turma = 0
        disciplinas_turma = []
        grupo_turma = obter_grupo_seguro(turma)
        
        for disc in disciplinas_filtradas:
            # CORREÇÃO: Só soma disciplinas do MESMO GRUPO da turma
            if turma.serie in disc.series and obter_grupo_seguro(disc) == grupo_turma:
                aulas_turma += disc.carga_semanal
                total_aulas += disc.carga_semanal
                disciplinas_turma.append(disc.nome)
        
        aulas_por_turma[turma.nome] = aulas_turma
        
        # Verificar se excede carga máxima
        carga_maxima = calcular_carga_maxima(turma.serie)
        if aulas_turma > carga_maxima:
            problemas_carga.append(f"{turma.nome} [{grupo_turma}]: {aulas_turma}h > {carga_maxima}h máximo")
    
    capacidade_total = len(DIAS_SEMANA) * len(HORARIOS_DISPONIVEIS) * len(turmas_filtradas)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Turmas", len(turmas_filtradas))
    with col2:
        st.metric("Aulas Necessárias", total_aulas)
    with col3:
        st.metric("Capacidade Disponível", capacidade_total)
    
    # Mostrar problemas de carga horária
    if problemas_carga:
        st.error("❌ Problemas de carga horária detectados:")
        for problema in problemas_carga:
            st.write(f"- {problema}")
        st.info("💡 **Solução:** Reduza a carga horária das disciplinas ou ajuste as séries")
    
    # Verificar viabilidade
    if total_aulas == 0:
        st.error("❌ Nenhuma aula para alocar! Verifique se as disciplinas estão associadas às séries corretas.")
    elif total_aulas > capacidade_total:
        st.error("❌ Capacidade insuficiente! Reduza a carga horária.")
        st.write("**Aulas por turma:**")
        for turma, aulas in aulas_por_turma.items():
            grupo_turma = obter_grupo_seguro(next(t for t in turmas_filtradas if t.nome == turma))
            carga_maxima = calcular_carga_maxima(next(t for t in turmas_filtradas if t.nome == turma).serie)
            status = "✅" if aulas <= carga_maxima else "❌"
            st.write(f"- {turma} [{grupo_turma}]: {aulas}/{carga_maxima}h {status}")
    elif problemas_carga:
        st.error("❌ Corrija os problemas de carga horária antes de gerar a grade!")
    else:
        st.success("✅ Capacidade suficiente para gerar grade!")
        
        # BOTÃO PARA GERAR GRADE
        if st.button("🚀 Gerar Grade Horária", type="primary", use_container_width=True):
            if not turmas_filtradas:
                st.error("❌ Nenhuma turma selecionada para gerar grade!")
            elif not disciplinas_filtradas:
                st.error("❌ Nenhuma disciplina disponível para as turmas selecionadas!")
            elif problemas_carga:
                st.error("❌ Corrija os problemas de carga horária antes de gerar!")
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
                        
                        # Resto do código para exibir a grade gerada...
                        # [Mantido igual da versão anterior]
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao gerar grade: {str(e)}")

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

st.sidebar.write("### 💡 Informações:")
st.sidebar.write("**Carga Horária Máxima:**")
st.sidebar.write("- EF II: 25h semanais")
st.sidebar.write("- EM: 32h semanais")
st.sidebar.write("**Grupos Separados:**")
st.sidebar.write- Cada turma só considera disciplinas do seu grupo")