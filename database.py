"""
Operações de banco de dados simples usando JSON
"""

import json
import os
from models import Turma, Professor, Disciplina, Sala

# Arquivo de dados
DATA_FILE = "escola_data.json"

def init_db():
    """Inicializa o banco de dados (cria arquivo se não existir)"""
    try:
        if not os.path.exists(DATA_FILE):
            # Criar arquivo vazio
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'turmas': [],
                    'professores': [],
                    'disciplinas': [],
                    'salas': []
                }, f, ensure_ascii=False, indent=2)
            print("✅ Banco de dados inicializado")
            return True
        print("✅ Banco de dados já existe")
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        return False

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
        
        print("✅ Dados salvos com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")
        return False

def carregar_dados():
    """Carrega dados do arquivo JSON"""
    try:
        if not os.path.exists(DATA_FILE):
            print("ℹ️ Arquivo de dados não encontrado, retornando dados vazios")
            return [], [], [], []
        
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        print("✅ Dados carregados do arquivo")
        
        # Reconstruir objetos
        turmas = []
        for t in dados.get('turmas', []):
            try:
                turma = Turma(
                    nome=t.get('nome', ''),
                    serie=t.get('serie', ''),
                    turno=t.get('turno', 'manha'),
                    grupo=t.get('grupo', 'A'),
                    segmento=t.get('segmento')
                )
                turma.id = t.get('id', turma.id)
                turmas.append(turma)
            except Exception as e:
                print(f"❌ Erro ao carregar turma: {e}")
        
        professores = []
        for p in dados.get('professores', []):
            try:
                professor = Professor(
                    nome=p.get('nome', ''),
                    disciplinas=p.get('disciplinas', []),
                    disponibilidade=set(p.get('disponibilidade', [])),
                    grupo=p.get('grupo', 'AMBOS'),
                    horarios_indisponiveis=set(p.get('horarios_indisponiveis', []))
                )
                professor.id = p.get('id', professor.id)
                professores.append(professor)
            except Exception as e:
                print(f"❌ Erro ao carregar professor: {e}")
        
        disciplinas = []
        for d in dados.get('disciplinas', []):
            try:
                disciplina = Disciplina(
                    nome=d.get('nome', ''),
                    carga_semanal=d.get('carga_semanal', 3),
                    tipo=d.get('tipo', 'media'),
                    turmas=d.get('turmas', []),
                    grupo=d.get('grupo', 'A'),
                    cor_fundo=d.get('cor_fundo', '#4A90E2'),
                    cor_fonte=d.get('cor_fonte', '#FFFFFF')
                )
                disciplina.id = d.get('id', disciplina.id)
                disciplinas.append(disciplina)
            except Exception as e:
                print(f"❌ Erro ao carregar disciplina: {e}")
        
        salas = []
        for s in dados.get('salas', []):
            try:
                sala = Sala(
                    nome=s.get('nome', ''),
                    capacidade=s.get('capacidade', 30),
                    tipo=s.get('tipo', 'normal')
                )
                sala.id = s.get('id', sala.id)
                salas.append(sala)
            except Exception as e:
                print(f"❌ Erro ao carregar sala: {e}")
        
        return turmas, professores, disciplinas, salas
        
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return [], [], [], []

def resetar_banco():
    """Reseta o banco de dados (apaga o arquivo)"""
    try:
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            print("✅ Banco de dados resetado")
        return init_db()  # Recria o arquivo vazio
    except Exception as e:
        print(f"❌ Erro ao resetar banco: {e}")
        return False