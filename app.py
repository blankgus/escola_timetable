import streamlit as st
import pandas as pd
import database
from session_state import init_session_state
from auto_save import salvar_tudo
from models import Turma, Professor, Disciplina, Sala, DIAS_SEMANA, HORARIOS_EFII, HORARIOS_EM, HORARIOS_REAIS_EFII, HORARIOS_REAIS_EM, obter_horarios_reais, obter_horarios_disponiveis
from scheduler_ortools import GradeHorariaORTools
from simple_scheduler import SimpleGradeHoraria
import io
import traceback

# Configuração da página
st.set_page_config(page_title="Escola Timetable", layout="wide")
st.title("🕒 Gerador Inteligente de Grade Horária - Horários Reais")

# Inicialização
try:
    init_session_state()
    st.success("✅ Sistema inicializado com sucesso!")
except Exception as e:
    st.error(f"❌ Erro na inicialização: {str(e)}")
    st.code(traceback.format_exc())
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

def obter_segmento_turma(turma_nome):
    """Determina o segmento da turma baseado no nome"""
    if 'em' in turma_nome.lower():
        return "EM"
    else:
        return "EF_II"

def obter_horarios_turma(turma_nome):
    """Retorna os horários disponíveis para a turma"""
    # Encontrar a turma pelo nome
    for turma in st.session_state.turmas:
        if turma.nome == turma_nome:
            if hasattr(turma, 'get_horarios'):
                return turma.get_horarios()
            else:
                return turma.get_horarios() if hasattr(turma, 'get_horarios') else HORARIOS_EFII
    
    # Fallback: determinar pelo nome
    if 'em' in turma_nome.lower():
        return HORARIOS_EM
    else:
        return HORARIOS_EFII

def obter_horario_real(turma_nome, horario):
    """Retorna o horário real formatado"""
    # Encontrar a turma pelo nome
    for turma in st.session_state.turmas:
        if turma.nome == turma_nome:
            if hasattr(turma, 'get_horario_real'):
                return turma.get_horario_real(horario)
    
    # Fallback: determinar pelo nome
    if 'em' in turma_nome.lower():
        return HORARIOS_REAIS_EM.get(horario, f"Horário {horario}")
    else:
        return HORARIOS_REAIS_EFII.get(horario, f"Horário {horario}")

# Função para calcular carga horária máxima por série
def calcular_carga_maxima(serie):
    """Calcula a carga horária máxima semanal baseada na série"""
    if 'em' in serie.lower() or 'medio' in serie.lower() or serie in ['1em', '2em', '3em']:
        return 35  # Ensino Médio: 35 horas (7 aulas/dia × 5 dias)
    else:
        return 25  # EF II: 25 horas (5 aulas/dia × 5 dias)

# Função para converter entre formatos de dias
def converter_dia_para_semana(dia):
    """Converte dia do formato completo para abreviado (DIAS_SEMANA)"""
    if dia == "segunda": return "seg"
    elif dia == "terca": return "ter"
    elif dia == "quarta": return "qua"
    elif dia == "quinta": return "qui"
    elif dia == "sexta": return "sex"
    else: return dia

def converter_dia_para_completo(dia):
    """Converte dia do formato abreviado para completo"""
    if dia == "seg": return "segunda"
    elif dia == "ter": return "terca"
    elif dia == "qua": return "quarta"
    elif dia == "qui": return "quinta"
    elif dia == "sex": return "sexta"
    else: return dia

def converter_disponibilidade_para_semana(disponibilidade):
    """Converte conjunto de disponibilidade para formato DIAS_SEMANA"""
    convertido = []
    for dia in disponibilidade:
        dia_convertido = converter_dia_para_semana(dia)
        if dia_convertido in DIAS_SEMANA:
            convertido.append(dia_convertido)
    return convertido

def converter_disponibilidade_para_completo(disponibilidade):
    """Converte conjunto de disponibilidade para formato completo"""
    convertido = set()
    for dia in disponibilidade:
        convertido.add(converter_dia_para_completo(dia))
    return convertido

def eh_horario_intervalo_prof(horario, segmento_turma=None):
    """Verifica se é horário de intervalo"""
    if segmento_turma == "EF_II":
        return horario == 3  # EF II: intervalo no 3º horário
    elif segmento_turma == "EM":
        return horario == 4  # EM: intervalo no 4º horário
    return False

# Menu de abas
abas = st.tabs(["🏠 Início", "📚 Disciplinas", "👩‍🏫 Professores", "🎒 Turmas", "🏫 Salas", "🗓️ Gerar Grade", "👨‍🏫 Grade por Professor"])

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
    
    # Estatísticas por grupo e segmento - CORRIGIDO
    st.subheader("📊 Estatísticas por Segmento")
    
    turmas_efii = [t for t in st.session_state.turmas if hasattr(t, 'segmento') and t.segmento == "EF_II" or obter_segmento_turma(t.nome) == "EF_II"]
    turmas_em = [t for t in st.session_state.turmas if hasattr(t, 'segmento') and t.segmento == "EM" or obter_segmento_turma(t.nome) == "EM"]
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Ensino Fundamental II**")
        st.write(f"Turmas: {len(turmas_efii)}")
        st.write(f"Horário: 07:50 - 12:20")
        st.write(f"Períodos: 5 aulas + intervalo (25h semanais)")
        
    with col2:
        st.write("**Ensino Médio**")
        st.write(f"Turmas: {len(turmas_em)}")
        st.write(f"Horário: 07:00 - 13:10")
        st.write(f"Períodos: 7 aulas + intervalo (35h semanais)")
    
    # Verificação de carga horária - CORRIGIDO
    st.subheader("📈 Verificação de Carga Horária")
    for turma in st.session_state.turmas:
        carga_total = 0
        disciplinas_turma = []
        grupo_turma = obter_grupo_seguro(turma)
        
        # Determinar segmento corretamente
        if hasattr(turma, 'segmento'):
            segmento = turma.segmento
        else:
            segmento = obter_segmento_turma(turma.nome)
        
        # ✅ CORREÇÃO: Verificar disciplinas vinculadas DIRETAMENTE à turma
        for disc in st.session_state.disciplinas:
            if turma.nome in disc.turmas and obter_grupo_seguro(disc) == grupo_turma:
                carga_total += disc.carga_semanal
                disciplinas_turma.append(f"{disc.nome} ({disc.carga_semanal}h)")
        
        # Usar método da turma para carga máxima ou calcular
        if hasattr(turma, 'get_carga_maxima'):
            carga_maxima = turma.get_carga_maxima()
        else:
            carga_maxima = calcular_carga_maxima(turma.serie)
        
        status = "✅" if carga_total <= carga_maxima else "❌"
        
        st.write(f"**{turma.nome}** [{grupo_turma}] ({segmento}): {carga_total}/{carga_maxima}h {status}")
        if disciplinas_turma:
            st.caption(f"Disciplinas: {', '.join(disciplinas_turma)}")
        else:
            st.caption("⚠️ Nenhuma disciplina atribuída para este grupo")
    
    if st.button("💾 Salvar Tudo no Banco"):
        try:
            if salvar_tudo():
                st.success("✅ Todos os dados salvos!")
            else:
                st.error("❌ Erro ao salvar dados")
        except Exception as e:
            st.error(f"❌ Erro ao salvar: {str(e)}")

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
                # ✅ MUDANÇA: Selecionar turmas específicas em vez de séries
                turmas_opcoes = [t.nome for t in st.session_state.turmas]
                turmas_selecionadas = st.multiselect("Turmas*", turmas_opcoes)
                grupo = st.selectbox("Grupo*", ["A", "B"])
                cor_fundo = st.color_picker("Cor de Fundo", "#4A90E2")
                cor_fonte = st.color_picker("Cor da Fonte", "#FFFFFF")
            
            if st.form_submit_button("✅ Adicionar Disciplina"):
                if nome and turmas_selecionadas:
                    try:
                        nova_disciplina = Disciplina(
                            nome, carga, tipo, turmas_selecionadas, grupo, cor_fundo, cor_fonte
                        )
                        st.session_state.disciplinas.append(nova_disciplina)
                        if salvar_tudo():
                            st.success(f"✅ Disciplina '{nome}' adicionada!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar disciplina: {str(e)}")
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
                    # ✅ MUDANÇA: Editar turmas específicas
                    turmas_opcoes = [t.nome for t in st.session_state.turmas]
                    turmas_selecionadas = st.multiselect(
                        "Turmas", 
                        turmas_opcoes,
                        default=disc.turmas,
                        key=f"turmas_{disc.id}"
                    )
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
                        if novo_nome and turmas_selecionadas:
                            try:
                                disc.nome = novo_nome
                                disc.carga_semanal = nova_carga
                                disc.tipo = novo_tipo
                                disc.turmas = turmas_selecionadas
                                disc.grupo = novo_grupo
                                disc.cor_fundo = nova_cor_fundo
                                disc.cor_fonte = nova_cor_fonte
                                
                                if salvar_tudo():
                                    st.success("✅ Disciplina atualizada!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao atualizar: {str(e)}")
                        else:
                            st.error("❌ Preencha todos os campos obrigatórios")
                
                with col2:
                    if st.form_submit_button("🗑️ Excluir Disciplina", type="secondary"):
                        try:
                            st.session_state.disciplinas.remove(disc)
                            if salvar_tudo():
                                st.success("✅ Disciplina excluída!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao excluir: {str(e)}")

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
                        # Mostrar todos os horários possíveis (1-8)
                        horarios_cols = st.columns(4)
                        horarios_todos = list(range(1, 9))
                        for i, horario in enumerate(horarios_todos):
                            with horarios_cols[i % 4]:
                                if st.checkbox(f"{horario}º", key=f"add_{dia}_{horario}"):
                                    horarios_indisponiveis.append(f"{dia}_{horario}")
            
            if st.form_submit_button("✅ Adicionar Professor"):
                if nome and disciplinas and disponibilidade:
                    try:
                        # Converter para formato completo para compatibilidade
                        disponibilidade_completa = converter_disponibilidade_para_completo(disponibilidade)
                        
                        novo_professor = Professor(
                            nome, 
                            disciplinas, 
                            disponibilidade_completa, 
                            grupo,
                            set(horarios_indisponiveis)
                        )
                        st.session_state.professores.append(novo_professor)
                        if salvar_tudo():
                            st.success(f"✅ Professor '{nome}' adicionado!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar professor: {str(e)}")
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
            disciplinas_validas = [d for d in prof.disciplinas if d in disc_nomes]
            
            with st.form(f"edit_prof_{prof.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome", prof.nome, key=f"nome_prof_{prof.id}")
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
                    # ✅ CORREÇÃO: Converter disponibilidade para formato DIAS_SEMANA
                    disponibilidade_convertida = converter_disponibilidade_para_semana(prof.disponibilidade)
                    
                    nova_disponibilidade = st.multiselect(
                        "Dias Disponíveis", 
                        DIAS_SEMANA, 
                        default=disponibilidade_convertida,
                        key=f"disp_prof_{prof.id}"
                    )
                    
                    st.write("**Horários Indisponíveis:**")
                    novos_horarios_indisponiveis = []
                    horarios_todos = list(range(1, 9))
                    for dia in DIAS_SEMANA:
                        with st.container():
                            st.write(f"**{dia.upper()}:**")
                            horarios_cols = st.columns(4)
                            for i, horario in enumerate(horarios_todos):
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
                            try:
                                prof.nome = novo_nome
                                prof.disciplinas = novas_disciplinas
                                prof.grupo = novo_grupo
                                
                                # Converter de volta para formato completo
                                disponibilidade_completa = converter_disponibilidade_para_completo(nova_disponibilidade)
                                
                                prof.disponibilidade = disponibilidade_completa
                                prof.horarios_indisponiveis = set(novos_horarios_indisponiveis)
                                
                                if salvar_tudo():
                                    st.success("✅ Professor atualizado!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao atualizar: {str(e)}")
                        else:
                            st.error("❌ Preencha todos os campos obrigatórios")
                
                with col2:
                    if st.form_submit_button("🗑️ Excluir Professor", type="secondary"):
                        try:
                            st.session_state.professores.remove(prof)
                            if salvar_tudo():
                                st.success("✅ Professor excluído!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao excluir: {str(e)}")

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
                turno = st.selectbox("Turno*", ["manha"], disabled=True)
                grupo = st.selectbox("Grupo*", ["A", "B"])
            
            # Determinar segmento automaticamente
            segmento = "EM" if serie and 'em' in serie.lower() else "EF_II"
            carga_maxima = 35 if segmento == "EM" else 25
            
            # Mostrar informações corretas
            if segmento == "EM":
                st.info(f"💡 Segmento: Ensino Médio - 35h semanais (07:00 - 13:10)")
            else:
                st.info(f"💡 Segmento: EF II - 25h semanais (07:50 - 12:20)")
            
            if st.form_submit_button("✅ Adicionar Turma"):
                if nome and serie:
                    try:
                        nova_turma = Turma(nome, serie, "manha", grupo, segmento)
                        st.session_state.turmas.append(nova_turma)
                        if salvar_tudo():
                            st.success(f"✅ Turma '{nome}' adicionada!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar turma: {str(e)}")
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
                    st.text_input("Turno", "manha", disabled=True, key=f"turno_turma_{turma.id}")
                    novo_grupo = st.selectbox(
                        "Grupo", 
                        ["A", "B"],
                        index=0 if obter_grupo_seguro(turma) == "A" else 1,
                        key=f"grupo_turma_{turma.id}"
                    )
                
                # Mostrar informações da turma - CORRIGIDO
                segmento = turma.segmento if hasattr(turma, 'segmento') else obter_segmento_turma(turma.nome)
                horarios = turma.get_horarios() if hasattr(turma, 'get_horarios') else obter_horarios_turma(turma.nome)
                
                if segmento == "EM":
                    st.write(f"**Segmento:** Ensino Médio (35h semanais)")
                    st.write(f"**Horário:** 07:00 - 13:10")
                    st.write(f"**Aulas por dia:** 7 + intervalo")
                else:
                    st.write(f"**Segmento:** EF II (25h semanais)")
                    st.write(f"**Horário:** 07:50 - 12:20")
                    st.write(f"**Aulas por dia:** 5 + intervalo")
                
                grupo_turma = obter_grupo_seguro(turma)
                carga_atual = 0
                disciplinas_turma = []
                
                # ✅ CORREÇÃO: Verificar disciplinas vinculadas DIRETAMENTE à turma
                for disc in st.session_state.disciplinas:
                    if turma.nome in disc.turmas and obter_grupo_seguro(disc) == grupo_turma:
                        carga_atual += disc.carga_semanal
                        disciplinas_turma.append(disc.nome)
                
                carga_maxima = turma.get_carga_maxima() if hasattr(turma, 'get_carga_maxima') else calcular_carga_maxima(turma.serie)
                st.write(f"**Carga horária atual:** {carga_atual}/{carga_maxima}h")
                
                if disciplinas_turma:
                    st.caption(f"Disciplinas do Grupo {grupo_turma}: {', '.join(disciplinas_turma)}")
                else:
                    st.caption("⚠️ Nenhuma disciplina do mesmo grupo atribuída")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar Alterações"):
                        if novo_nome and nova_serie:
                            try:
                                turma.nome = novo_nome
                                turma.serie = nova_serie
                                turma.grupo = novo_grupo
                                # Atualizar segmento se a série mudou
                                novo_segmento = "EM" if 'em' in nova_serie.lower() else "EF_II"
                                if hasattr(turma, 'segmento'):
                                    turma.segmento = novo_segmento
                                
                                if salvar_tudo():
                                    st.success("✅ Turma atualizada!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao atualizar: {str(e)}")
                        else:
                            st.error("❌ Preencha todos os campos obrigatórios")
                
                with col2:
                    if st.form_submit_button("🗑️ Excluir Turma", type="secondary"):
                        try:
                            st.session_state.turmas.remove(turma)
                            if salvar_tudo():
                                st.success("✅ Turma excluída!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao excluir: {str(e)}")

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
                    try:
                        nova_sala = Sala(nome, capacidade, tipo)
                        st.session_state.salas.append(nova_sala)
                        if salvar_tudo():
                            st.success(f"✅ Sala '{nome}' adicionada!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar sala: {str(e)}")
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
                            try:
                                sala.nome = novo_nome
                                sala.capacidade = nova_capacidade
                                sala.tipo = novo_tipo
                                
                                if salvar_tudo():
                                    st.success("✅ Sala atualizada!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao atualizar: {str(e)}")
                        else:
                            st.error("❌ Preencha todos os campos obrigatórios")
                
                with col2:
                    if st.form_submit_button("🗑️ Excluir Sala", type="secondary"):
                        try:
                            st.session_state.salas.remove(sala)
                            if salvar_tudo():
                                st.success("✅ Sala excluída!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao excluir: {str(e)}")

with abas[5]:  # ABA GERAR GRADE
    st.header("🗓️ Gerar Grade Horária")
    
    st.subheader("🎯 Configurações da Grade")
    
    col1, col2 = st.columns(2)
    with col1:
        tipo_grade = st.selectbox(
            "Tipo de Grade",
            [
                "Grade Completa - Todas as Turmas",
                "Grade por Grupo A",
                "Grade por Grupo B", 
                "Grade por Turma Específica"
            ]
        )
        
        if tipo_grade == "Grade por Turma Específica":
            turmas_opcoes = [t.nome for t in st.session_state.turmas]
            if turmas_opcoes:
                turma_selecionada = st.selectbox("Selecionar Turma", turmas_opcoes)
            else:
                turma_selecionada = None
    
    with col2:
        tipo_algoritmo = st.selectbox(
            "Algoritmo de Geração",
            ["Algoritmo Simples (Rápido)", "Google OR-Tools (Otimizado)"]
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
    
    # Filtrar disciplinas pelo GRUPO CORRETO
    if tipo_grade == "Grade por Grupo A":
        disciplinas_filtradas = [d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == "A"]
    elif tipo_grade == "Grade por Grupo B":
        disciplinas_filtradas = [d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == "B"]
    else:
        disciplinas_filtradas = st.session_state.disciplinas
    
    # Calcular total de aulas necessárias
    total_aulas = 0
    aulas_por_turma = {}
    problemas_carga = []
    
    for turma in turmas_filtradas:
        aulas_turma = 0
        grupo_turma = obter_grupo_seguro(turma)
        
        # ✅ CORREÇÃO: Contar aulas baseado no vínculo DIRETO turma-disciplina
        for disc in disciplinas_filtradas:
            disc_grupo = obter_grupo_seguro(disc)
            # AGORA: Verifica se a disciplina está vinculada a ESTA turma específica
            if turma.nome in disc.turmas and disc_grupo == grupo_turma:
                aulas_turma += disc.carga_semanal
                total_aulas += disc.carga_semanal
        
        aulas_por_turma[turma.nome] = aulas_turma
        
        # Usar carga máxima correta
        if hasattr(turma, 'get_carga_maxima'):
            carga_maxima = turma.get_carga_maxima()
        else:
            carga_maxima = calcular_carga_maxima(turma.serie)
            
        if aulas_turma > carga_maxima:
            problemas_carga.append(f"{turma.nome} [{grupo_turma}]: {aulas_turma}h > {carga_maxima}h máximo")
    
    # ✅ CAPACIDADE COM HORÁRIOS REAIS CORRETOS
    capacidade_total = 0
    for turma in turmas_filtradas:
        # Usar horários corretos de cada turma
        if hasattr(turma, 'get_horarios'):
            horarios_turma = turma.get_horarios()
        else:
            horarios_turma = obter_horarios_turma(turma.nome)
        capacidade_total += len(DIAS_SEMANA) * len(horarios_turma)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Turmas", len(turmas_filtradas))
    with col2:
        st.metric("Aulas Necessárias", total_aulas)
    with col3:
        st.metric("Capacidade Disponível", capacidade_total)
    
    if problemas_carga:
        st.error("❌ Problemas de carga horária detectados:")
        for problema in problemas_carga:
            st.write(f"- {problema}")
    
    if total_aulas == 0:
        st.error("❌ Nenhuma aula para alocar! Verifique se as disciplinas estão vinculadas às turmas corretas.")
    elif total_aulas > capacidade_total:
        st.error("❌ Capacidade insuficiente! Reduza a carga horária.")
    elif problemas_carga:
        st.error("❌ Corrija os problemas de carga horária antes de gerar a grade!")
    else:
        st.success("✅ Capacidade suficiente para gerar grade!")
        
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
                        if tipo_grade == "Grade por Grupo A":
                            professores_filtrados = [p for p in st.session_state.professores 
                                                   if obter_grupo_seguro(p) in ["A", "AMBOS"]]
                        elif tipo_grade == "Grade por Grupo B":
                            professores_filtrados = [p for p in st.session_state.professores 
                                                   if obter_grupo_seguro(p) in ["B", "AMBOS"]]
                        else:
                            professores_filtrados = st.session_state.professores
                        
                        if tipo_algoritmo == "Google OR-Tools (Otimizado)":
                            try:
                                grade = GradeHorariaORTools(
                                    turmas_filtradas,
                                    professores_filtrados,
                                    disciplinas_filtradas,
                                    st.session_state.salas
                                )
                                sucesso, mensagem = grade.gerar_grade()
                                
                                if sucesso:
                                    st.session_state.grade_gerada = grade.grade
                                    st.session_state.grade_info = grade.info_grade
                                    st.success(f"✅ {mensagem}")
                                else:
                                    st.error(f"❌ {mensagem}")
                                    
                            except Exception as e:
                                st.error(f"❌ Erro no OR-Tools: {str(e)}")
                                st.info("🔄 Tentando com algoritmo simples...")
                                tipo_algoritmo = "Algoritmo Simples (Rápido)"
                        
                        if tipo_algoritmo == "Algoritmo Simples (Rápido)":
                            grade = SimpleGradeHoraria(
                                turmas_filtradas,
                                professores_filtrados,
                                disciplinas_filtradas,
                                st.session_state.salas
                            )
                            sucesso, mensagem = grade.gerar_grade()
                            
                            if sucesso:
                                st.session_state.grade_gerada = grade.grade
                                st.session_state.grade_info = grade.info_grade
                                st.success(f"✅ {mensagem}")
                            else:
                                st.error(f"❌ {mensagem}")
                                
                    except Exception as e:
                        st.error(f"❌ Erro ao gerar grade: {str(e)}")
                        st.code(traceback.format_exc())

    # Exibir grade gerada - CORRIGIDO
    if hasattr(st.session_state, 'grade_gerada') and st.session_state.grade_gerada:
        st.subheader("📅 Grade Horária Gerada")
        
        # Opções de visualização
        col1, col2 = st.columns(2)
        with col1:
            formato_exibicao = st.selectbox(
                "Formato de Exibição",
                ["Grade Completa", "Por Turma", "Por Professor", "Exportar Excel"]
            )
        
        with col2:
            if st.button("🔄 Gerar Nova Grade"):
                if 'grade_gerada' in st.session_state:
                    del st.session_state.grade_gerada
                if 'grade_info' in st.session_state:
                    del st.session_state.grade_info
                st.rerun()
        
        if formato_exibicao == "Grade Completa":
            # Mostrar grade completa com horários reais CORRETOS
            for turma_nome, grade_turma in st.session_state.grade_gerada.items():
                st.write(f"### 🎒 {turma_nome}")
                
                # Encontrar a turma para obter informações corretas
                turma_info = None
                for t in st.session_state.turmas:
                    if t.nome == turma_nome:
                        turma_info = t
                        break
                
                # Criar DataFrame para exibição
                dias_completos = ["segunda", "terca", "quarta", "quinta", "sexta"]
                
                # Obter horários CORRETOS para esta turma
                if turma_info and hasattr(turma_info, 'get_horarios'):
                    horarios_turma = turma_info.get_horarios()
                else:
                    horarios_turma = obter_horarios_turma(turma_nome)
                
                dados_grade = []
                for horario in horarios_turma:
                    if turma_info and hasattr(turma_info, 'get_horario_real'):
                        horario_real = turma_info.get_horario_real(horario)
                    else:
                        horario_real = obter_horario_real(turma_nome, horario)
                        
                    linha = {"Horário": f"{horario}º - {horario_real}"}
                    for dia in dias_completos:
                        aula = grade_turma.get(dia, {}).get(horario, {})
                        if aula:
                            disciplina = aula.get('disciplina', '')
                            professor = aula.get('professor', '')
                            sala = aula.get('sala', '')
                            linha[dia.capitalize()] = f"{disciplina}\n({professor}) - {sala}"
                        else:
                            linha[dia.capitalize()] = "Livre"
                    dados_grade.append(linha)
                
                if dados_grade:
                    df = pd.DataFrame(dados_grade)
                    st.dataframe(df, use_container_width=True)
                st.markdown("---")
        
        elif formato_exibicao == "Por Turma":
            turma_selecionada = st.selectbox(
                "Selecionar Turma",
                list(st.session_state.grade_gerada.keys())
            )
            
            if turma_selecionada:
                st.write(f"### 📋 Grade da {turma_selecionada}")
                grade_turma = st.session_state.grade_gerada[turma_selecionada]
                
                # Encontrar a turma para obter informações corretas
                turma_info = None
                for t in st.session_state.turmas:
                    if t.nome == turma_selecionada:
                        turma_info = t
                        break
                
                dias_completos = ["segunda", "terca", "quarta", "quinta", "sexta"]
                
                # Obter horários CORRETOS para esta turma
                if turma_info and hasattr(turma_info, 'get_horarios'):
                    horarios_turma = turma_info.get_horarios()
                else:
                    horarios_turma = obter_horarios_turma(turma_selecionada)
                
                dados_grade = []
                for horario in horarios_turma:
                    if turma_info and hasattr(turma_info, 'get_horario_real'):
                        horario_real = turma_info.get_horario_real(horario)
                    else:
                        horario_real = obter_horario_real(turma_selecionada, horario)
                        
                    linha = {"Horário": f"{horario}º - {horario_real}"}
                    for dia in dias_completos:
                        aula = grade_turma.get(dia, {}).get(horario, {})
                        if aula:
                            disciplina = aula.get('disciplina', '')
                            professor = aula.get('professor', '')
                            sala = aula.get('sala', '')
                            cor = aula.get('cor', '#FFFFFF')
                            
                            # Aplicar cores
                            estilo = f"background-color: {cor}; color: {aula.get('cor_fonte', '#000000')}; padding: 5px; border-radius: 3px;"
                            linha[dia.capitalize()] = f'<div style="{estilo}"><strong>{disciplina}</strong><br>({professor})<br>{sala}</div>'
                        else:
                            linha[dia.capitalize()] = "Livre"
                    dados_grade.append(linha)
                
                if dados_grade:
                    df = pd.DataFrame(dados_grade)
                    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)
        
        elif formato_exibicao == "Exportar Excel":
            st.info("💾 Gerando arquivo Excel para download...")
            
            # Criar arquivo Excel com múltiplas abas
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                for turma_nome, grade_turma in st.session_state.grade_gerada.items():
                    # Encontrar a turma para obter informações corretas
                    turma_info = None
                    for t in st.session_state.turmas:
                        if t.nome == turma_nome:
                            turma_info = t
                            break
                    
                    dias_completos = ["segunda", "terca", "quarta", "quinta", "sexta"]
                    
                    # Obter horários CORRETOS para esta turma
                    if turma_info and hasattr(turma_info, 'get_horarios'):
                        horarios_turma = turma_info.get_horarios()
                    else:
                        horarios_turma = obter_horarios_turma(turma_nome)
                    
                    dados_grade = []
                    for horario in horarios_turma:
                        if turma_info and hasattr(turma_info, 'get_horario_real'):
                            horario_real = turma_info.get_horario_real(horario)
                        else:
                            horario_real = obter_horario_real(turma_nome, horario)
                            
                        linha = {"Horário": f"{horario}º - {horario_real}"}
                        for dia in dias_completos:
                            aula = grade_turma.get(dia, {}).get(horario, {})
                            if aula:
                                disciplina = aula.get('disciplina', '')
                                professor = aula.get('professor', '')
                                sala = aula.get('sala', '')
                                linha[dia.capitalize()] = f"{disciplina} ({professor}) - {sala}"
                            else:
                                linha[dia.capitalize()] = "Livre"
                        dados_grade.append(linha)
                    
                    if dados_grade:
                        df = pd.DataFrame(dados_grade)
                        df.to_excel(writer, sheet_name=turma_nome[:31], index=False)
            
            output.seek(0)
            
            st.download_button(
                label="📥 Baixar Grade em Excel",
                data=output,
                file_name="grade_horaria.xlsx",
                mime="application/vnd.ms-excel"
            )

with abas[6]:  # ABA GRADE POR PROFESSOR
    st.header("👨‍🏫 Grade por Professor")
    
    if not hasattr(st.session_state, 'grade_gerada') or not st.session_state.grade_gerada:
        st.info("ℹ️ Gere uma grade horária primeiro na aba 'Gerar Grade'")
    else:
        professor_selecionado = st.selectbox(
            "Selecionar Professor",
            [p.nome for p in st.session_state.professores]
        )
        
        if professor_selecionado:
            st.write(f"### 📅 Grade do Professor: {professor_selecionado}")
            
            # Encontrar aulas do professor
            dias_completos = ["segunda", "terca", "quarta", "quinta", "sexta"]
            
            # Coletar todas as aulas do professor
            aulas_professor = []
            for turma_nome, grade_turma in st.session_state.grade_gerada.items():
                # Obter horários corretos para esta turma
                horarios_turma = obter_horarios_turma(turma_nome)
                
                for dia in dias_completos:
                    for horario in horarios_turma:
                        aula = grade_turma.get(dia, {}).get(horario, {})
                        if aula and aula.get('professor') == professor_selecionado:
                            aulas_professor.append({
                                'turma': turma_nome,
                                'dia': dia,
                                'horario': horario,
                                'horario_real': obter_horario_real(turma_nome, horario),
                                'disciplina': aula.get('disciplina', ''),
                                'sala': aula.get('sala', '')
                            })
            
            if not aulas_professor:
                st.info("📝 Nenhuma aula encontrada para este professor na grade atual")
            else:
                # Criar grade do professor (todos os horários possíveis 1-8)
                horarios_possiveis = list(range(1, 9))
                dados_grade = []
                for horario in horarios_possiveis:
                    linha = {"Horário": f"{horario}º"}
                    for dia in dias_completos:
                        aula_dia = next((a for a in aulas_professor if a['dia'] == dia and a['horario'] == horario), None)
                        if aula_dia:
                            linha[dia.capitalize()] = f"{aula_dia['disciplina']}\n{aula_dia['turma']}\n{aula_dia['sala']}"
                        else:
                            linha[dia.capitalize()] = "Livre"
                    dados_grade.append(linha)
                
                df = pd.DataFrame(dados_grade)
                st.dataframe(df, use_container_width=True)
                
                # Estatísticas do professor
                st.subheader("📊 Estatísticas do Professor")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    total_aulas = len(aulas_professor)
                    st.metric("Total de Aulas", total_aulas)
                
                with col2:
                    turmas_unicas = len(set(a['turma'] for a in aulas_professor))
                    st.metric("Turmas Diferentes", turmas_unicas)
                
                with col3:
                    disciplinas_unicas = len(set(a['disciplina'] for a in aulas_professor))
                    st.metric("Disciplinas", disciplinas_unicas)
                
                # Detalhamento das aulas
                st.subheader("📋 Detalhamento das Aulas")
                for aula in sorted(aulas_professor, key=lambda x: (x['dia'], x['horario'])):
                    st.write(
                        f"**{aula['dia'].capitalize()} - {aula['horario_real']}**: "
                        f"{aula['disciplina']} - {aula['turma']} ({aula['sala']})"
                    )

# Rodapé
st.markdown("---")
st.caption("Sistema de Grade Horária - Desenvolvido para otimização de horários escolares")
