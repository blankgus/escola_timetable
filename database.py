import json
import os
from models import Turma, Professor, Disciplina, Sala, Aula

# Arquivo de database
DB_FILE = "escola_database.json"

def criar_dados_iniciais():
    """Cria dados iniciais para teste"""
    
    # Professores reais
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
    
    # Turmas
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
    
    # ✅ CORREÇÃO: Disciplinas vinculadas DIRETAMENTE às turmas
    disciplinas = [
        # GRUPO A - EF II
        Disciplina("Português A", 5, "pesada", ["6anoA", "7anoA", "8anoA", "9anoA"], "A"),
        Disciplina("Matemática A", 5, "pesada", ["6anoA", "7anoA", "8anoA", "9anoA"], "A"),
        Disciplina("História A", 2, "media", ["6anoA", "7anoA", "8anoA", "9anoA"], "A"),
        Disciplina("Geografia A", 2, "media", ["6anoA", "7anoA", "8anoA", "9anoA"], "A"),
        Disciplina("Ciências A", 3, "media", ["6anoA", "7anoA", "8anoA", "9anoA"], "A"),
        Disciplina("Inglês A", 2, "leve", ["6anoA", "7anoA", "8anoA", "9anoA"], "A"),
        Disciplina("Arte A", 2, "leve", ["6anoA", "7anoA", "8anoA", "9anoA"], "A"),
        Disciplina("Educação Física A", 2, "pratica", ["6anoA", "7anoA", "8anoA", "9anoA"], "A"),
        
        # GRUPO B - EF II
        Disciplina("Português B", 5, "pesada", ["6anoB", "7anoB", "8anoB", "9anoB"], "B"),
        Disciplina("Matemática B", 5, "pesada", ["6anoB", "7anoB", "8anoB", "9anoB"], "B"),
        Disciplina("História B", 2, "media", ["6anoB", "7anoB", "8anoB", "9anoB"], "B"),
        Disciplina("Geografia B", 2, "media", ["6anoB", "7anoB", "8anoB", "9anoB"], "B"),
        Disciplina("Ciências B", 3, "media", ["6anoB", "7anoB", "8anoB", "9anoB"], "B"),
        Disciplina("Inglês B", 2, "leve", ["6anoB", "7anoB", "8anoB", "9anoB"], "B"),
        Disciplina("Arte B", 2, "leve", ["6anoB", "7anoB", "8anoB", "9anoB"], "B"),
        Disciplina("Educação Física B", 2, "pratica", ["6anoB", "7anoB", "8anoB", "9anoB"], "B"),
        
        # GRUPO A - EM
        Disciplina("Português A", 5, "pesada", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Matemática A", 5, "pesada", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("História A", 3, "media", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Geografia A", 3, "media", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Biologia A", 3, "media", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Física A", 3, "pesada", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Química A", 3, "pesada", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Inglês A", 2, "leve", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Arte A", 1, "leve", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Educação Física A", 2, "pratica", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Filosofia A", 2, "media", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Sociologia A", 2, "media", ["1emA", "2emA", "3emA"], "A"),
        
        # GRUPO B - EM
        Disciplina("Português B", 5, "pesada", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Matemática B", 5, "pesada", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("História B", 3, "media", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Geografia B", 3, "media", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Biologia B", 3, "media", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Física B", 3, "pesada", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Química B", 3, "pesada", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Inglês B", 2, "leve", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Arte B", 1, "leve", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Educação Física B", 2, "pratica", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Filosofia B", 2, "media", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Sociologia B", 2, "media", ["1emB", "2emB", "3emB"], "B"),
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

# Funções de carregamento
def carregar_turmas():
    dados = carregar_tudo()
    turmas = dados.get("turmas", [])
    resultado = []
    
    for item in turmas:
        if isinstance(item, dict):
            resultado.append(Turma(**item))
        elif hasattr(item, 'nome') and hasattr(item, 'serie'):
            resultado.append(item)
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

# Funções de salvamento
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
    return True