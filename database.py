import sqlite3
import json
from models import Turma, Professor, Disciplina, Sala, Aula

def init_db():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    
    # ✅ RECRIAR TODAS AS TABELAS COM ESTRUTURA ATUALIZADA
    c.execute('''CREATE TABLE IF NOT EXISTS turmas (
        id TEXT PRIMARY KEY,
        nome TEXT UNIQUE,
        serie TEXT,
        turno TEXT,
        grupo TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS professores (
        id TEXT PRIMARY KEY,
        nome TEXT UNIQUE,
        disciplinas TEXT,
        disponibilidade TEXT,
        grupo TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS disciplinas (
        id TEXT PRIMARY KEY,
        nome TEXT UNIQUE,
        carga_semanal INTEGER,
        tipo TEXT,
        series TEXT,
        grupo TEXT,
        cor_fundo TEXT,
        cor_fonte TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS salas (
        id TEXT PRIMARY KEY,
        nome TEXT UNIQUE,
        capacidade INTEGER,
        tipo TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS periodos (
        id TEXT PRIMARY KEY,
        nome TEXT,
        inicio TEXT,
        fim TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS feriados (
        id TEXT PRIMARY KEY,
        data TEXT,
        motivo TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS aulas (
        id TEXT PRIMARY KEY,
        turma TEXT,
        disciplina TEXT,
        professor TEXT,
        dia TEXT,
        horario INTEGER,
        sala TEXT,
        grupo TEXT
    )''')
    
    conn.commit()
    conn.close()

def salvar_turmas(turmas):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM turmas")
    for t in turmas:
        c.execute("INSERT INTO turmas VALUES (?, ?, ?, ?, ?)",
                  (t.id, t.nome, t.serie, t.turno, t.grupo))
    conn.commit()
    conn.close()

def carregar_turmas():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT * FROM turmas")
    rows = c.fetchall()
    conn.close()
    
    turmas = []
    for r in rows:
        # ✅ VERIFICAR SE TEM O CAMPO GRUPO (posição 4)
        if len(r) >= 5:
            turmas.append(Turma(nome=r[1], serie=r[2], turno=r[3], grupo=r[4], id=r[0]))
        else:
            # Se não tem grupo, assume "A" como padrão
            turmas.append(Turma(nome=r[1], serie=r[2], turno=r[3], grupo="A", id=r[0]))
    return turmas

def salvar_professores(professores):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM professores")
    for p in professores:
        c.execute("INSERT INTO professores VALUES (?, ?, ?, ?, ?)",
                  (p.id, p.nome, json.dumps(p.disciplinas), json.dumps(list(p.disponibilidade)), p.grupo))
    conn.commit()
    conn.close()

def carregar_professores():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT * FROM professores")
    rows = c.fetchall()
    conn.close()
    
    professores = []
    for r in rows:
        if len(r) >= 5:
            professores.append(Professor(
                nome=r[1], 
                disciplinas=json.loads(r[2]), 
                disponibilidade=set(json.loads(r[3])), 
                grupo=r[4],
                id=r[0]
            ))
        else:
            # Se não tem grupo, assume "A" como padrão
            professores.append(Professor(
                nome=r[1], 
                disciplinas=json.loads(r[2]), 
                disponibilidade=set(json.loads(r[3])), 
                grupo="A",
                id=r[0]
            ))
    return professores

def salvar_disciplinas(disciplinas):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM disciplinas")
    for d in disciplinas:
        c.execute("INSERT INTO disciplinas VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (d.id, d.nome, d.carga_semanal, d.tipo, json.dumps(d.series), d.grupo, d.cor_fundo, d.cor_fonte))
    conn.commit()
    conn.close()

def carregar_disciplinas():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT * FROM disciplinas")
    rows = c.fetchall()
    conn.close()
    
    disciplinas = []
    for r in rows:
        if len(r) >= 8:  # Tem todos os campos incluindo cores
            disciplinas.append(Disciplina(
                nome=r[1], 
                carga_semanal=r[2], 
                tipo=r[3], 
                series=json.loads(r[4]), 
                grupo=r[5],
                cor_fundo=r[6],
                cor_fonte=r[7],
                id=r[0]
            ))
        elif len(r) >= 6:  # Tem grupo mas não tem cores
            disciplinas.append(Disciplina(
                nome=r[1], 
                carga_semanal=r[2], 
                tipo=r[3], 
                series=json.loads(r[4]), 
                grupo=r[5],
                id=r[0]
            ))
        else:  # Estrutura antiga
            disciplinas.append(Disciplina(
                nome=r[1], 
                carga_semanal=r[2], 
                tipo=r[3], 
                series=json.loads(r[4]), 
                grupo="A",
                id=r[0]
            ))
    return disciplinas

def salvar_salas(salas):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM salas")
    for s in salas:
        c.execute("INSERT INTO salas VALUES (?, ?, ?, ?)",
                  (s.id, s.nome, s.capacidade, s.tipo))
    conn.commit()
    conn.close()

def carregar_salas():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT * FROM salas")
    rows = c.fetchall()
    conn.close()
    return [Sala(nome=r[1], capacidade=r[2], tipo=r[3], id=r[0]) for r in rows]

def salvar_periodos(periodos):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM periodos")
    for p in periodos:
        c.execute("INSERT INTO periodos VALUES (?, ?, ?, ?)",
                  (p["id"], p["nome"], p["inicio"], p["fim"]))
    conn.commit()
    conn.close()

def carregar_periodos():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT * FROM periodos")
    rows = c.fetchall()
    conn.close()
    return [{"nome": r[1], "inicio": r[2], "fim": r[3], "id": r[0]} for r in rows]

def salvar_feriados(feriados):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM feriados")
    for f in feriados:
        c.execute("INSERT INTO feriados VALUES (?, ?, ?)",
                  (f["id"], f["data"], f["motivo"]))
    conn.commit()
    conn.close()

def carregar_feriados():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT * FROM feriados")
    rows = c.fetchall()
    conn.close()
    return [{"data": r[1], "motivo": r[2], "id": r[0]} for r in rows]

def salvar_grade(aulas):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM aulas")
    for aula in aulas:
        c.execute("INSERT INTO aulas VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (aula.id, aula.turma, aula.disciplina, aula.professor, aula.dia, aula.horario, aula.sala, aula.grupo))
    conn.commit()
    conn.close()

def carregar_grade():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT * FROM aulas")
    rows = c.fetchall()
    conn.close()
    
    aulas = []
    for r in rows:
        if len(r) >= 8:  # Tem grupo
            aulas.append(Aula(
                turma=r[1], 
                disciplina=r[2], 
                professor=r[3], 
                dia=r[4], 
                horario=r[5], 
                sala=r[6],
                grupo=r[7],
                id=r[0]
            ))
        else:  # Estrutura antiga
            aulas.append(Aula(
                turma=r[1], 
                disciplina=r[2], 
                professor=r[3], 
                dia=r[4], 
                horario=r[5], 
                sala=r[6],
                grupo="A",  # Assume grupo A
                id=r[0]
            ))
    return aulas

def resetar_banco():
    """Função para resetar completamente o banco de dados (útil para desenvolvimento)"""
    import os
    if os.path.exists('escola.db'):
        os.remove('escola.db')
    init_db()