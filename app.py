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
    
    if st.button("💾 Salvar Tudo no Banco"):
        if salvar_tudo():
            st.success("✅ Todos os dados salvos!")

# ... (as abas de Disciplinas, Professores, Turmas e Salas permanecem IGUAIS)
# Copie o conteúdo das abas 1-4 do código anterior aqui

with abas[5]:  # ✅ ABA GERAR GRADE (COMPLETAMENTE IMPLEMENTADA)
    st.header("🗓️ Gerar Grade Horária")
    
    st.subheader("🎯 Configurações da Grade")
    
    col1, col2 = st.columns(2)
    with col1:
        # Opções de grade
        tipo_grade = st.selectbox(
            "Tipo de Grade",
            [
                "Grade Completa - Todas as Turmas",
                "Grade por Grupo A (Manhã)",
                "Grade por Grupo B (Tarde)", 
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
    if tipo_grade == "Grade por Grupo A (Manhã)":
        turmas_filtradas = [t for t in st.session_state.turmas if obter_grupo_seguro(t) == "A"]
        grupo_texto = "Grupo A"
    elif tipo_grade == "Grade por Grupo B (Tarde)":
        turmas_filtradas = [t for t in st.session_state.turmas if obter_grupo_seguro(t) == "B"]
        grupo_texto = "Grupo B"
    elif tipo_grade == "Grade por Turma Específica" and turma_selecionada:
        turmas_filtradas = [t for t in st.session_state.turmas if t.nome == turma_selecionada]
        grupo_texto = f"Turma {turma_selecionada}"
    else:
        turmas_filtradas = st.session_state.turmas
        grupo_texto = "Todas as Turmas"
    
    # Filtrar disciplinas conforme o grupo
    if tipo_grade == "Grade por Grupo A (Manhã)":
        disciplinas_filtradas = [d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == "A"]
    elif tipo_grade == "Grade por Grupo B (Tarde)":
        disciplinas_filtradas = [d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == "B"]
    else:
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
        
        # ✅ BOTÃO PARA GERAR GRADE
        if st.button("🚀 Gerar Grade Horária", type="primary", use_container_width=True):
            if not turmas_filtradas:
                st.error("❌ Nenhuma turma selecionada para gerar grade!")
            elif not disciplinas_filtradas:
                st.error("❌ Nenhuma disciplina disponível para as turmas selecionadas!")
            else:
                with st.spinner(f"Gerando grade para {grupo_texto}..."):
                    try:
                        # Filtrar professores conforme o grupo
                        if tipo_grade == "Grade por Grupo A (Manhã)":
                            professores_filtrados = [p for p in st.session_state.professores 
                                                   if obter_grupo_seguro(p) in ["A", "AMBOS"]]
                        elif tipo_grade == "Grade por Grupo B (Tarde)":
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