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
        Disciplina("Ciências B", 3, "media", ["6ano", "7ano", "8ano", "9ano"], "B"),  # ✅ CORRIGIDO
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
        "professores": professores,
        "disciplinas": disciplinas,
        "turmas": turmas,
        "salas": salas,
        "aulas": [],
        "feriados": [],
        "periodos": []
    }

# ... (o resto do arquivo permanece igual)
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

def carregar_turmas():
    dados = carregar_tudo()
    return [Turma(**t) for t in dados.get("turmas", [])]

def carregar_professores():
    dados = carregar_tudo()
    return [Professor(**p) for p in dados.get("professores", [])]

def carregar_disciplinas():
    dados = carregar_tudo()
    return [Disciplina(**d) for d in dados.get("disciplinas", [])]

def carregar_salas():
    dados = carregar_tudo()
    return [Sala(**s) for s in dados.get("salas", [])]

def carregar_grade():
    dados = carregar_tudo()
    return [Aula(**a) for a in dados.get("aulas", [])]

def carregar_feriados():
    dados = carregar_tudo()
    return dados.get("feriados", [])

def carregar_periodos():
    dados = carregar_tudo()
    return dados.get("periodos", [])

def salvar_turmas(turmas):
    dados = carregar_tudo()
    dados["turmas"] = [t.__dict__ for t in turmas]
    return salvar_tudo(dados)

def salvar_professores(professores):
    dados = carregar_tudo()
    dados["professores"] = [p.__dict__ for p in professores]
    return salvar_tudo(dados)

def salvar_disciplinas(disciplinas):
    dados = carregar_tudo()
    dados["disciplinas"] = [d.__dict__ for d in disciplinas]
    return salvar_tudo(dados)

def salvar_salas(salas):
    dados = carregar_tudo()
    dados["salas"] = [s.__dict__ for s in salas]
    return salvar_tudo(dados)

def salvar_grade(aulas):
    dados = carregar_tudo()
    dados["aulas"] = [a.__dict__ for a in aulas]
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
    dados_iniciais = criar_dados_iniciais()
    return salvar_tudo(dados_iniciais)