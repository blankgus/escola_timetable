# app.py (substitua as primeiras linhas por isto)
import streamlit as st
import traceback

try:
    from session_state import init_session_state
    init_session_state()
except Exception as e:
    st.error(f"❌ Erro na inicialização: {str(e)}")
    st.code(traceback.format_exc())
    st.stop()

# Resto do código normal...