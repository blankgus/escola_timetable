"""
Inicialização do estado da sessão Streamlit
"""

import streamlit as st
from models import Turma, Professor, Disciplina, Sala
from neuro_rules import PROFESSORES_NEURO, SALAS_NEURO, obter_disciplinas_por_serie, TURMAS_NEURO, obter_cor_disciplina
import database

def init_session_state():
    """Inicializa o estado da sessão Streamlit"""
    
    # Inicializar banco de dados
    if not database.init_db():
        st.error("❌ Erro ao inicializar banco de dados")
        return
    
    # Listas principais
    if 'turmas' not in st.session_state:
        st.session_state.turmas = []
    
    if 'professores' not in st.session_state:
        st.session_state.professores = []
    
    if 'disciplinas' not in st.session_state:
        st.session_state.disciplinas = []
    
    if 'salas' not in st.session_state:
        st.session_state.salas = []
    
    # Grades
    if 'grade_gerada' not in st.session_state:
        st.session_state.grade_gerada = None
    
    if 'grade_info' not in st.session_state:
        st.session_state.grade_info = None
    
    # Configurações
    if 'sistema_inicializado' not in st.session_state:
        st.session_state.sistema_inicializado = False
    
    # Tentar carregar dados salvos primeiro
    turmas_salvas, professores_salvas, disciplinas_salvas, salas_salvas = database.carregar_dados()
    
    if turmas_salvas and professores_salvas:
        # Usar dados salvos
        st.session_state.turmas = turmas_salvas
        st.session_state.professores = professores_salvas
        st.session_state.disciplinas = disciplinas_salvas
        st.session_state.salas = salas_salvas
        st.session_state.sistema_inicializado = True
        st.info(f"✅ Dados carregados: {len(turmas_salvas)} turmas, {len(professores_salvas)} professores")
    else:
        # Inicializar com dados padrão se estiver vazio
        if not st.session_state.turmas and not st.session_state.professores:
            _inicializar_dados_padrao()

def _inicializar_dados_padrao():
    """Inicializa com dados padrão da escola Neuro - DADOS REAIS"""
    
    st.info("🔄 Inicializando com dados reais da escola Neuro...")
    
    # Criar turmas
    for turma_info in TURMAS_NEURO:
        turma = Turma(
            nome=turma_info["nome"],
            serie=turma_info["serie"],
            turno=turma_info["turno"],
            grupo=turma_info["grupo"],
            segmento=turma_info["segmento"]
        )
        st.session_state.turmas.append(turma)
    
    # Criar professores
    for nome_prof, info_prof in PROFESSORES_NEURO.items():
        professor = Professor(
            nome=nome_prof,
            disciplinas=info_prof["disciplinas"],
            disponibilidade=set(info_prof["disponibilidade"]),
            grupo=info_prof["grupo"],
            horarios_indisponiveis=set(info_prof["horarios_indisponiveis"])
        )
        st.session_state.professores.append(professor)
    
    # Criar disciplinas - DADOS REAIS com grupos A e B separados
    disciplinas_criadas = {}
    
    # Para cada série e grupo, criar disciplinas específicas
    for turma in st.session_state.turmas:
        serie = turma.serie
        grupo = turma.grupo
        
        disciplinas_serie = obter_disciplinas_por_serie(serie, grupo)
        
        for disc_info in disciplinas_serie:
            chave = f"{disc_info['nome']}_{grupo}"
            
            if chave not in disciplinas_criadas:
                cor_info = obter_cor_disciplina(disc_info['nome'])
                
                # Encontrar todas as turmas deste grupo e série
                turmas_grupo = [t.nome for t in st.session_state.turmas 
                              if t.serie == serie and t.grupo == grupo]
                
                disciplina = Disciplina(
                    nome=disc_info['nome'],
                    carga_semanal=disc_info['carga'],
                    tipo=disc_info['tipo'],
                    turmas=turmas_grupo,
                    grupo=grupo,
                    cor_fundo=cor_info['fundo'],
                    cor_fonte=cor_info['fonte']
                )
                st.session_state.disciplinas.append(disciplina)
                disciplinas_criadas[chave] = disciplina
    
    # Criar salas
    for sala_info in SALAS_NEURO:
        sala = Sala(
            nome=sala_info["nome"],
            capacidade=sala_info["capacidade"],
            tipo=sala_info["tipo"]
        )
        st.session_state.salas.append(sala)
    
    st.session_state.sistema_inicializado = True
    
    # Salvar dados padrão
    if database.salvar_dados(
        st.session_state.turmas,
        st.session_state.professores,
        st.session_state.disciplinas,
        st.session_state.salas
    ):
        st.success(f"✅ Dados reais salvos: {len(st.session_state.turmas)} turmas, {len(st.session_state.professores)} professores, {len(st.session_state.disciplinas)} disciplinas")
    else:
        st.error("❌ Erro ao salvar dados reais")