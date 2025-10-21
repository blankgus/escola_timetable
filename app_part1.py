import streamlit as st
import pandas as pd
import database
from session_state import init_session_state
from auto_save import salvar_tudo
from models import Turma, Professor, Disciplina, Sala, DIAS_SEMANA, HORARIOS_EFII, HORARIOS_EM, HORARIOS_REAIS_EFII, HORARIOS_REAIS_EM, obter_horarios_reais
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
    segmento = obter_segmento_turma(turma_nome)
    if segmento == "EM":
        return HORARIOS_EM
    else:
        return HORARIOS_EFII

def obter_horario_real(turma_nome, horario):
    """Retorna o horário real formatado"""
    segmento = obter_segmento_turma(turma_nome)
    if segmento == "EM":
        return HORARIOS_REAIS_EM.get(horario, f"Horário {horario}")
    else:
        return HORARIOS_REAIS_EFII.get(horario, f"Horário {horario}")

# Função para calcular carga horária máxima por série
def calcular_carga_maxima(serie):
    """Calcula a carga horária máxima semanal baseada na série"""
    if 'em' in serie.lower() or 'medio' in serie.lower() or serie in ['1em', '2em', '3em']:
        return 35  # Ensino Médio: 35 horas
    else:
        return 25  # EF II: 25 horas

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
    
    # Estatísticas por grupo e segmento
    st.subheader("📊 Estatísticas por Segmento")
    
    turmas_efii = [t for t in st.session_state.turmas if obter_segmento_turma(t.nome) == "EF_II"]
    turmas_em = [t for t in st.session_state.turmas if obter_segmento_turma(t.nome) == "EM"]
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Ensino Fundamental II**")
        st.write(f"Turmas: {len(turmas_efii)}")
        st.write(f"Horário: 07:50 - 12:20")
        st.write(f"Períodos: 6 aulas + intervalo")
        
    with col2:
        st.write("**Ensino Médio**")
        st.write(f"Turmas: {len(turmas_em)}")
        st.write(f"Horário: 07:00 - 13:10")
        st.write(f"Períodos: 7 aulas + intervalo")
    
    # Verificação de carga horária
    st.subheader("📈 Verificação de Carga Horária")
    for turma in st.session_state.turmas:
        carga_total = 0
        disciplinas_turma = []
        grupo_turma = obter_grupo_seguro(turma)
        segmento = obter_segmento_turma(turma.nome)
        
        # ✅ CORREÇÃO: Verificar disciplinas vinculadas DIRETAMENTE à turma
        for disc in st.session_state.disciplinas:
            if turma.nome in disc.turmas and obter_grupo_seguro(disc) == grupo_turma:
                carga_total += disc.carga_semanal
                disciplinas_turma.append(f"{disc.nome} ({disc.carga_semanal}h)")
        
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