import json
import os
from models import Turma, Professor, Disciplina, Sala, Aula

# Arquivo de database
DB_FILE = "escola_database.json"

def criar_dados_iniciais():
    """Cria dados iniciais para teste"""
    
    # Professores reais que você forneceu
    professores = [
        Professor("Heliana", ["Português"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Deise", ["Português"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Loide", ["Português"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Tatiane", ["Matemática"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Ricardo", ["Matemática"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Laís", ["História"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Waldemar", ["História"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Rene", ["Geografia"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Vladmir", ["Química"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Zabuor", ["Química"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Gisele", ["Geografia"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Marina", ["Biologia"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("César", ["Informática", "Física"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Anna Maria", ["Filosofia", "Sociologia"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Marcão", ["Educação Física"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Andréia", ["Educação Física"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Vanessa", ["Arte"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
        Professor("Andréia Barreto", ["Dinâmica", "Vida Pratica"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS", {f"{dia}_{horario}" for dia in ["segunda", "terca", "quarta", "quinta", "sexta"] for horario in [1,2,3,5,6,7]}),
    ]
    
    # Disciplinas básicas para EF II e EM
    disciplinas = [
        # EF II - Grupo A
        Disciplina("Português A", 5, "pesada", ["6ano", "7ano", "8ano", "9ano"], "A"),
        Disciplina("Matemática A", 5, "pesada", ["6ano", "7ano", "8ano", "9ano"], "A"),
        Disciplina("História A", 2, "media", ["6ano", "7ano", "8ano", "9ano"], "A"),
        Disciplina("Geografia A", 2, "media", ["6ano", "7ano", "8ano", "9ano"], "A"),
        Disciplina("Ciências A", 3, "media", ["6ano", "7ano", "8ano", "9ano"], "A"),
        Disciplina("Inglês A", 2, "leve", ["6ano", "7ano", "8ano", "9ano"], "A"),
        Disciplina("Arte A", 2, "leve", ["6ano", "7ano", "8ano", "9ano"], "A"),
        Disciplina("Educação Física A", 2, "pratica", ["6ano", "7ano", "8ano", "9ano"], "A"),
        
        # EF II - Grupo B
        Disciplina("Português B", 5, "pesada", ["6ano", "7ano", "8ano", "9ano"], "B"),
        Disciplina("Matemática B", 5, "pesada", ["6ano", "7ano", "8ano", "9ano"], "B"),
        Disciplina("História B", 2, "media", ["6ano", "7ano", "8ano", "9ano"], "B"),
        Disciplina("Geografia B", 2, "media", ["6ano", "7ano", "8ano", "9ano"], "B"),
        Disciplina("Ciências B", 3, "media", ["6ano", "7ano", "8ano", "9ano"], "B"),
        Disciplina("Inglês B", 2, "leve", ["6ano", "7ano", "8ano", "9ano"], "B"),
        Disciplina("Arte B", 2, "leve", ["6ano", "7ano", "8ano", "9ano"], "B"),
        Disciplina("Educação Física B", 2, "pratica", ["6ano", "7ano", "8ano", "9ano"], "B"),
        
        # EM - Grupo A
        Disciplina("Português A", 5, "pesada", ["1em", "2em", "3em"], "A"),
        Disciplina("Matemática A", 5, "pesada", ["1em", "2em", "3em"], "A"),
        Disciplina("História A", 3, "media", ["1em", "2em", "3em"], "A"),
        Disciplina("Geografia A", 3, "media", ["1em", "2em", "3em"], "A"),
        Disciplina("Biologia A", 3, "media", ["1em", "2em", "3em"], "A"),
        Disciplina("Física A", 3, "pesada", ["1em", "2em", "3em"], "A"),
        Disciplina("Química A", 3, "pesada", ["1em", "2em", "3em"], "A"),
        Disciplina("Inglês A", 2, "leve", ["1em", "2em", "3em"], "A"),
        Disciplina("Arte A", 1, "leve", ["1em", "2em", "3em"], "A"),
        Disciplina("Educação Física A", 2, "pratica", ["1em", "2em", "3em"], "A"),
        Disciplina("Filosofia A", 2, "media", ["1em", "2em", "3em"], "A"),
        Disciplina("Sociologia A", 2, "media", ["1em", "2em", "3em"], "A"),
        
        # EM - Grupo B
        Disciplina("Português B", 5, "pesada", ["1em", "2em", "3em"], "B"),
        Disciplina("Matemática B", 5, "pesada", ["1em", "2em", "3em"], "B"),
        Disciplina("História B", 3, "media", ["1em", "2em", "3em"], "B"),
        Disciplina("Geografia B", 3, "media", ["1em", "2em", "3em"], "B"),
        Disciplina("Biologia B", 3, "media", ["1em", "2em", "3em"], "B"),
        Disciplina("Física B", 3, "pesada", ["1em", "2em", "3em"], "B"),
        Disciplina("Química B", 3, "pesada", ["1em", "2em", "3em"], "B"),
        Disciplina("Inglês B", 2, "leve", ["1em", "2em", "3em"], "B"),
        Disciplina("Arte B", 1, "leve", ["1em", "2em", "3em"], "B"),
        Disciplina("Educação Física B", 2, "pratica", ["1em", "2em", "3em"], "B"),
        Disciplina("Filosofia B", 2, "media", ["1em", "2em", "3em"], "B"),
        Disciplina("Sociologia B", 2, "media", ["1em", "2em", "3em"], "B"),
    ]
    
    turmas = [
        Turma("6anoA", "6ano", "manha", "A"),
        Turma("7anoA", "7ano", "manha", "A"),
        Turma("8anoA", "8ano", "manha", "A"),
        Turma("9anoA", "9ano", "manha", "A"),
        Turma("1emA", "1em", "manha", "A"),
        Turma("2emA", "2em", "manha", "A"),
        Turma("3emA", "3em", "manha", "A"),
        Turma("6anoB", "6ano", "manha", "B"),
        Turma("7anoB", "7ano", "manha", "B"),
        Turma("8anoB", "8ano", "manha", "B"),
        Turma("9anoB", "9ano", "manha", "B"),
        Turma("1emB", "1em", "manha", "B"),
        Turma("2emB", "2em", "manha", "B"),
        Turma("3emB", "3em", "manha", "B"),
    ]
    
    salas = [
        Sala("Sala 1", 30, "normal"),
        Sala("Sala 2", 30, "normal"),
        Sala("Sala 3", 30, "normal"),
        Sala("Laboratório de Ciências", 25, "laboratório"),
        Sala("Auditório", 100, "auditório"),
    ]
    
    return {
        "professores": [p.__dict__ for p in professores],
        "disciplinas": [d.__dict__ for d in disciplinas],
        "turmas": [t.__dict__ for t in turmas],
        "salas": [s.__dict__ for s in salas],
        "aulas": [],
        "feriados": [],
        "periodos": []
    }

def init_db():
    """Inicializa o banco de dados com dados padrão se não existir"""
    if not os.path.exists(DB_FILE):
        dados_iniciais = criar_dados_iniciais()
        salvar_tudo(dados_iniciais)

def carregar_tudo():
    """Carrega todos os dados do banco"""
    if not os.path.exists(DB_FILE):
        init_db()
    
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return criar_dados_iniciais()

def salvar_tudo(dados):
    """Salva todos os dados no banco"""
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return False

# ✅ FUNÇÕES DE CARREGAMENTO COMPLETAMENTE CORRIGIDAS
def carregar_turmas():
    dados = carregar_tudo()
    turmas = dados.get("turmas", [])
    resultado = []
    
    for item in turmas:
        # Se for dicionário, criar nova Turma
        if isinstance(item, dict):
            resultado.append(Turma(**item))
        # Se já for objeto Turma, usar diretamente
        elif hasattr(item, 'nome') and hasattr(item, 'serie'):
            resultado.append(item)
        # Caso contrário, pular item inválido
        else:
            print(f"Item inválido em turmas: {item}")
    
    return resultado

def carregar_professores():
    dados = carregar_tudo()
    professores = dados.get("professores", [])
    resultado = []
    
    for item in professores:
        if isinstance(item, dict):
            resultado.append(Professor(**item))
        elif hasattr(item, 'nome') and hasattr(item, 'disciplinas'):
            resultado.append(item)
        else:
            print(f"Item inválido em professores: {item}")
    
    return resultado

def carregar_disciplinas():
    dados = carregar_tudo()
    disciplinas = dados.get("disciplinas", [])
    resultado = []
    
    for item in disciplinas:
        if isinstance(item, dict):
            resultado.append(Disciplina(**item))
        elif hasattr(item, 'nome') and hasattr(item, 'carga_semanal'):
            resultado.append(item)
        else:
            print(f"Item inválido em disciplinas: {item}")
    
    return resultado

def carregar_salas():
    dados = carregar_tudo()
    salas = dados.get("salas", [])
    resultado = []
    
    for item in salas:
        if isinstance(item, dict):
            resultado.append(Sala(**item))
        elif hasattr(item, 'nome') and hasattr(item, 'capacidade'):
            resultado.append(item)
        else:
            print(f"Item inválido em salas: {item}")
    
    return resultado

def carregar_grade():
    dados = carregar_tudo()
    aulas = dados.get("aulas", [])
    resultado = []
    
    for item in aulas:
        if isinstance(item, dict):
            resultado.append(Aula(**item))
        elif hasattr(item, 'turma') and hasattr(item, 'disciplina'):
            resultado.append(item)
        else:
            print(f"Item inválido em aulas: {item}")
    
    return resultado

def carregar_feriados():
    dados = carregar_tudo()
    return dados.get("feriados", [])

def carregar_periodos():
    dados = carregar_tudo()
    return dados.get("periodos", [])

# ✅ FUNÇÕES DE SALVAMENTO CORRIGIDAS
def _converter_para_dict(obj):
    """Converte objeto para dicionário se for um objeto models"""
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    return obj

def salvar_turmas(turmas):
    dados = carregar_tudo()
    dados["turmas"] = [_converter_para_dict(t) for t in turmas]
    return salvar_tudo(dados)

def salvar_professores(professores):
    dados = carregar_tudo()
    dados["professores"] = [_converter_para_dict(p) for p in professores]
    return salvar_tudo(dados)

def salvar_disciplinas(disciplinas):
    dados = carregar_tudo()
    dados["disciplinas"] = [_converter_para_dict(d) for d in disciplinas]
    return salvar_tudo(dados)

def salvar_salas(salas):
    dados = carregar_tudo()
    dados["salas"] = [_converter_para_dict(s) for s in salas]
    return salvar_tudo(dados)

def salvar_grade(aulas):
    dados = carregar_tudo()
    dados["aulas"] = [_converter_para_dict(a) for a in aulas]
    return salvar_tudo(dados)

def salvar_feriados(feriados):
    dados = carregar_tudo()
    dados["feriados"] = feriados
    return salvar_tudo(dados)

def salvar_periodos(periodos):
    dados = carregar_tudo()
    dados["periodos"] = periodos
    return salvar_tudo(dados)

def resetar_banco():
    """Reseta o banco de dados para os valores iniciais"""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    init_db()
    return True    8: "12:20-13:10"
}

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

# Função para calcular carga horária máxima por série
def calcular_carga_maxima(serie):
    """Calcula a carga horária máxima semanal baseada na série"""
    if 'em' in serie.lower() or 'medio' in serie.lower() or serie in ['1em', '2em', '3em']:
        return 32  # Ensino Médio: 32 horas
    else:
        return 25  # EF II: 25 horas

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
    
    # Estatísticas por grupo
    turmas_a = [t for t in st.session_state.turmas if obter_grupo_seguro(t) == "A"]
    turmas_b = [t for t in st.session_state.turmas if obter_grupo_seguro(t) == "B"]
    
    st.subheader("📊 Estatísticas por Grupo")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Grupo A**")
        st.write(f"Turmas: {len(turmas_a)}")
        st.write(f"Disciplinas: {len([d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == 'A'])}")
    with col2:
        st.write("**Grupo B**")
        st.write(f"Turmas: {len(turmas_b)}")
        st.write(f"Disciplinas: {len([d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == 'B'])}")
    
    # Verificação de carga horária
    st.subheader("📈 Verificação de Carga Horária")
    for turma in st.session_state.turmas:
        carga_total = 0
        disciplinas_turma = []
        grupo_turma = obter_grupo_seguro(turma)
        
        for disc in st.session_state.disciplinas:
            if turma.serie in disc.series and obter_grupo_seguro(disc) == grupo_turma:
                carga_total += disc.carga_semanal
                disciplinas_turma.append(f"{disc.nome} ({disc.carga_semanal}h)")
        
        carga_maxima = calcular_carga_maxima(turma.serie)
        status = "✅" if carga_total <= carga_maxima else "❌"
        
        st.write(f"**{turma.nome}** [{grupo_turma}] ({turma.serie}): {carga_total}/{carga_maxima}h {status}")
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
                series = st.text_input("Séries* (separadas por vírgula)", "6ano,7ano,8ano,9ano,1em,2em,3em")
                grupo = st.selectbox("Grupo*", ["A", "B"])
                cor_fundo = st.color_picker("Cor de Fundo", "#4A90E2")
                cor_fonte = st.color_picker("Cor da Fonte", "#FFFFFF")
            
            if st.form_submit_button("✅ Adicionar Disciplina"):
                if nome and series:
                    try:
                        series_list = [s.strip() for s in series.split(",") if s.strip()]
                        nova_disciplina = Disciplina(nome, carga, tipo, series_list, grupo, cor_fundo, cor_fonte)
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
                    novas_series = st.text_input("Séries", ", ".join(disc.series), key=f"series_{disc.id}")
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
                        if novo_nome and novas_series:
                            try:
                                series_list = [s.strip() for s in novas_series.split(",") if s.strip()]
                                disc.nome = novo_nome
                                disc.carga_semanal = nova_carga
                                disc.tipo = novo_tipo
                                disc.series = series_list
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
                        horarios_cols = st.columns(4)
                        for i, horario in enumerate(HORARIOS_DISPONIVEIS):  # ✅ 8 HORÁRIOS
                            with horarios_cols[i % 4]:
                                if st.checkbox(f"{horario}º", key=f"add_{dia}_{horario}"):
                                    horarios_indisponiveis.append(f"{dia}_{horario}")
            
            if st.form_submit_button("✅ Adicionar Professor"):
                if nome and disciplinas and disponibilidade:
                    try:
                        novo_professor = Professor(
                            nome, 
                            disciplinas, 
                            set(disponibilidade), 
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
                    nova_disponibilidade = st.multiselect(
                        "Dias Disponíveis", 
                        DIAS_SEMANA, 
                        default=list(prof.disponibilidade),
                        key=f"disp_prof_{prof.id}"
                    )
                    
                    st.write("**Horários Indisponíveis:**")
                    novos_horarios_indisponiveis = []
                    for dia in DIAS_SEMANA:
                        with st.container():
                            st.write(f"**{dia.upper()}:**")
                            horarios_cols = st.columns(4)
                            for i, horario in enumerate(HORARIOS_DISPONIVEIS):  # ✅ 8 HORÁRIOS
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
                                prof.disponibilidade = set(nova_disponibilidade)
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
            
            if serie:
                carga_maxima = calcular_carga_maxima(serie)
                nivel = "Ensino Médio" if carga_maxima == 32 else "EF II"
                st.info(f"💡 {nivel}: Carga horária máxima semanal = {carga_maxima}h")
            
            if st.form_submit_button("✅ Adicionar Turma"):
                if nome and serie:
                    try:
                        nova_turma = Turma(nome, serie, "manha", grupo)
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
                
                grupo_turma = obter_grupo_seguro(turma)
                carga_atual = 0
                disciplinas_turma = []
                for disc in st.session_state.disciplinas:
                    if turma.serie in disc.series and obter_grupo_seguro(disc) == grupo_turma:
                        carga_atual += disc.carga_semanal
                        disciplinas_turma.append(disc.nome)
                
                carga_maxima = calcular_carga_maxima(turma.serie)
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
        
        relaxar_horarios = st.checkbox(
            "Relaxar horários ideais",
            value=False,
            help="Permitir disciplinas pesadas em qualquer horário"
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
        
        for disc in disciplinas_filtradas:
            if turma.serie in disc.series and obter_grupo_seguro(disc) == grupo_turma:
                aulas_turma += disc.carga_semanal
                total_aulas += disc.carga_semanal
        
        aulas_por_turma[turma.nome] = aulas_turma
        
        carga_maxima = calcular_carga_maxima(turma.serie)
        if aulas_turma > carga_maxima:
            problemas_carga.append(f"{turma.nome} [{grupo_turma}]: {aulas_turma}h > {carga_maxima}h máximo")
    
    # ✅ CAPACIDADE COM 8 HORÁRIOS
    capacidade_total = len(DIAS_SEMANA) * len(HORARIOS_DISPONIVEIS) * len(turmas_filtradas)
    
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
        st.error("❌ Nenhuma aula para alocar! Verifique se as disciplinas estão associadas às séries corretas.")
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
                        
                        if tipo_grade == "Grade por Turma Específica" and turma_selecionada:
                            aulas = [a for a in aulas if a.turma == turma_selecionada]
                        
                        st.session_state.aulas = aulas
                        if salvar_tudo():
                            st.success(f"✅ Grade {grupo_texto} gerada com {metodo}! ({len(aulas)} aulas)")
                        
                        if aulas:
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
                            
                            df_aulas = df_aulas.sort_values(["Turma", "Dia", "Horário"])
                            st.dataframe(df_aulas, use_container_width=True)
                            
                            output = io.BytesIO()
                            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                df_aulas.to_excel(writer, sheet_name="Grade_Completa", index=False)
                                stats_df = pd.DataFrame({
                                    "Estatística": ["Total de Aulas", "Professores Utilizados", "Turmas com Aula", "Método"],
                                    "Valor": [len(aulas), len(set(a.professor for a in aulas)), len(set(a.turma for a in aulas)), metodo]
                                })
                                stats_df.to_excel(writer, sheet_name="Estatísticas", index=False)
                            
                            st.download_button(
                                "📥 Baixar Grade em Excel",
                                output.getvalue(),
                                f"grade_{grupo_texto.replace(' ', '_')}.xlsx",
                                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        else:
                            st.warning("⚠️ Nenhuma aula foi gerada.")
                            
                    except Exception as e:
                        st.error(f"❌ Erro ao gerar grade: {str(e)}")

# Sidebar
st.sidebar.title("⚙️ Configurações")
if st.sidebar.button("🔄 Resetar Banco de Dados"):
    try:
        database.resetar_banco()
        st.sidebar.success("✅ Banco resetado! Recarregue a página.")
    except Exception as e:
        st.sidebar.error(f"❌ Erro ao resetar: {str(e)}")

st.sidebar.write("### Status do Sistema:")
st.sidebar.write(f"**Turmas:** {len(st.session_state.turmas)}")
st.sidebar.write(f"**Professores:** {len(st.session_state.professores)}")
st.sidebar.write(f"**Disciplinas:** {len(st.session_state.disciplinas)}")
st.sidebar.write(f"**Salas:** {len(st.session_state.salas)}")
st.sidebar.write(f"**Aulas na Grade:** {len(st.session_state.get('aulas', []))}")

# Sidebar
st.sidebar.title("⚙️ Configurações")
if st.sidebar.button("🔄 Resetar Banco de Dados"):
    try:
        database.resetar_banco()
        st.sidebar.success("✅ Banco resetado! Recarregue a página.")
    except Exception as e:
        st.sidebar.error(f"❌ Erro ao resetar: {str(e)}")

st.sidebar.write("### Status do Sistema:")
st.sidebar.write(f"**Turmas:** {len(st.session_state.turmas)}")
st.sidebar.write(f"**Professores:** {len(st.session_state.professores)}")
st.sidebar.write(f"**Disciplinas:** {len(st.session_state.disciplinas)}")
st.sidebar.write(f"**Salas:** {len(st.session_state.salas)}")
st.sidebar.write(f"**Aulas na Grade:** {len(st.session_state.get('aulas', []))}")

st.sidebar.write("### 💡 Informações:")
st.sidebar.write("**Carga Horária Máxima:**")
st.sidebar.write("- EF II: 25h semanais")
st.sidebar.write("- EM: 32h semanais")

st.sidebar.write("### 🕒 Horários Reais:")
for horario, periodo in HORARIOS_REAIS.items():
    st.sidebar.write(f"**{horario}º:** {periodo}")
