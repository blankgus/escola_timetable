"""
Operações de banco de dados simples usando JSON
"""

import json
import os
from models import Turma, Professor, Disciplina, Sala

# Arquivo de dados
DATA_FILE = "escola_data.json"

def salvar_dados(turmas, professores, disciplinas, salas):
    """Salva todos os dados no arquivo JSON"""
    try:
        dados = {
            'turmas': [turma.__dict__ for turma in turmas],
            'professores': [prof.__dict__ for prof in professores],
            'disciplinas': [disc.__dict__ for disc in disciplinas],
            'salas': [sala.__dict__ for sala in salas]
        }
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
        return False

def carregar_dados():
    """Carrega dados do arquivo JSON"""
    try:
        if not os.path.exists(DATA_FILE):
            return [], [], [], []
        
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Reconstruir objetos
        turmas = [Turma(**t) for t in dados.get('turmas', [])]
        professores = [Professor(**p) for p in dados.get('professores', [])]
        disciplinas = [Disciplina(**d) for d in dados.get('disciplinas', [])]
        salas = [Sala(**s) for s in dados.get('salas', [])]
        
        return turmas, professores, disciplinas, salas
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return [], [], [], []

def resetar_banco():
    """Reseta o banco de dados (apaga o arquivo)"""
    try:
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        return True
    except Exception as e:
        print(f"Erro ao resetar banco: {e}")
        return False