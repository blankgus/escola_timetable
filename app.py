# Dentro da aba1, no botão "Gerar Grade"
if st.button("🚀 Gerar Grade com Dados Atuais"):
    with st.spinner("Gerando grade..."):
        try:
            # Primeiro: tentar com OR-Tools
            grade = GradeHorariaORTools(
                st.session_state.turmas,
                st.session_state.professores,
                st.session_state.disciplinas,
                relaxar_horario_ideal=st.session_state.relaxar_horario_ideal
            )
            aulas = grade.resolver()
            metodo = "Google OR-Tools (otimizado)"
            
        except Exception as e1:
            st.warning(f"⚠️ OR-Tools falhou: {str(e1)}. Tentando método simples...")
            try:
                # Segundo: fallback com algoritmo simples
                from simple_scheduler import SimpleGradeHoraria
                simple_grade = SimpleGradeHoraria(
                    st.session_state.turmas,
                    st.session_state.professores,
                    st.session_state.disciplinas
                )
                aulas = simple_grade.gerar_grade()
                metodo = "Algoritmo Simples (fallback)"
                st.info(f"✅ Grade gerada com {metodo}!")
            except Exception as e2:
                st.error(f"❌ Ambos os métodos falharam:\n1. OR-Tools: {str(e1)}\n2. Simples: {str(e2)}")
                st.stop()
        
        # ... resto do código para exibir/exportar ...
        st.success(f"✅ Grade gerada com {metodo}!")
        # [resto do código igual]
