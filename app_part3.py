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
        
        carga_maxima = calcular_carga_maxima(turma.serie)
        if aulas_turma > carga_maxima:
            problemas_carga.append(f"{turma.nome} [{grupo_turma}]: {aulas_turma}h > {carga_maxima}h máximo")
    
    # ✅ CAPACIDADE COM HORÁRIOS REAIS
    capacidade_total = 0
    for turma in turmas_filtradas:
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

    # Exibir grade gerada
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
            # Mostrar grade completa com horários reais
            for turma_nome, grade_turma in st.session_state.grade_gerada.items():
                st.write(f"### 🎒 {turma_nome}")
                
                # Criar DataFrame para exibição
                dias_completos = ["segunda", "terca", "quarta", "quinta", "sexta"]
                horarios_turma = obter_horarios_turma(turma_nome)
                
                dados_grade = []
                for horario in horarios_turma:
                    linha = {"Horário": f"{horario}º - {obter_horario_real(turma_nome, horario)}"}
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
                
                dias_completos = ["segunda", "terca", "quarta", "quinta", "sexta"]
                horarios_turma = obter_horarios_turma(turma_selecionada)
                
                dados_grade = []
                for horario in horarios_turma:
                    linha = {"Horário": f"{horario}º - {obter_horario_real(turma_selecionada, horario)}"}
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
                    dias_completos = ["segunda", "terca", "quarta", "quinta", "sexta"]
                    horarios_turma = obter_horarios_turma(turma_nome)
                    
                    dados_grade = []
                    for horario in horarios_turma:
                        linha = {"Horário": f"{horario}º - {obter_horario_real(turma_nome, horario)}"}
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