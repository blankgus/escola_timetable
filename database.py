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
        Disciplina("Ciências B", 3, "media", ["6ano", "7ano", "8ano