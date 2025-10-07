# app.py (no topo, após imports)
try:
    init_session_state()
except Exception as e:
    st.error(f"❌ Erro na inicialização: {str(e)}")
    st.stop()