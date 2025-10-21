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
            horarios_possiveis = list(range(1, 9))  # Todos os horários possíveis
            
            # Coletar todas as aulas do professor
            aulas_professor = []
            for turma_nome, grade_turma in st.session_state.grade_gerada.items():
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
                # Criar grade do professor
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