"""
Sistema de auto-save para dados da aplicação
"""

import database
import streamlit as st

def salvar_tudo():
    """Salva todos os dados atuais"""
    try:
        if hasattr(st.session_state, 'turmas') and hasattr(st.session_state, 'professores'):
            sucesso = database.salvar_dados(
                st.session_state.turmas,
                st.session_state.professores, 
                st.session_state.disciplinas,
                st.session_state.salas
            )
            return sucesso
        return False
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False