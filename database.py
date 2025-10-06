import sqlite3
import json
from models import Turma, Professor, Disciplina, Sala

def init_db():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS turmas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        serie TEXT,
        turno TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS professores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        disciplinas TEXT,
        disponibilidade TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        carga_semanal INTEGER,
        tipo TEXT,
        series TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS salas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        capacidade INTEGER,
        tipo TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS periodos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        inicio TEXT,
        fim TEXT
    )''')
    
    conn.commit()
    conn.close()

# === TURMAS ===
def salvar_turmas(turmas):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM turmas")
    for t in turmas:
        c.execute("INSERT INTO turmas (nome, serie, turno) VALUES (?, ?, ?)", (t.nome, t.serie, t.turno))
    conn.commit()
    conn.close()

def carregar_turmas():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT nome, serie, turno FROM turmas")
    rows = c.fetchall()
    conn.close()
    return [Turma(row[0], row[1], row[2]) for row in rows]

# === PROFESSORES ===
def salvar_professores(professores):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM professores")
    for p in professores:
        c.execute("INSERT INTO professores (nome, disciplinas, disponibilidade) VALUES (?, ?, ?)",
                  (p.nome, json.dumps(p.disciplinas), json.dumps(list(p.disponibilidade))))
    conn.commit()
    conn.close()

def carregar_professores():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT nome, disciplinas, disponibilidade FROM professores")
    rows = c.fetchall()
    conn.close()
    professores = []
    for row in rows:
        nome, disc_json, disp_json = row
        disciplinas = json.loads(disc_json) if disc_json else []
        disponibilidade = set(json.loads(disp_json)) if disp_json else set()
        professores.append(Professor(nome, disciplinas, disponibilidade))
    return professores

# === DISCIPLINAS ===
def salvar_disciplinas(disciplinas):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM disciplinas")
    for d in disciplinas:
        c.execute("INSERT INTO disciplinas (nome, carga_semanal, tipo, series) VALUES (?, ?, ?, ?)",
                  (d.nome, d.carga_semanal, d.tipo, json.dumps(d.series)))
    conn.commit()
    conn.close()

def carregar_disciplinas():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT nome, carga_semanal, tipo, series FROM disciplinas")
    rows = c.fetchall()
    conn.close()
    disciplinas = []
    for row in rows:
        nome, carga, tipo, series_json = row
        series = json.loads(series_json) if series_json else []
        disciplinas.append(Disciplina(nome, carga, tipo, series))
    return disciplinas

# === SALAS ===
def salvar_salas(salas):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM salas")
    for s in salas:
        c.execute("INSERT INTO salas (nome, capacidade, tipo) VALUES (?, ?, ?)",
                  (s.nome, s.capacidade, s.tipo))
    conn.commit()
    conn.close()

def carregar_salas():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT nome, capacidade, tipo FROM salas")
    rows = c.fetchall()
    conn.close()
    return [Sala(row[0], row[1], row[2]) for row in rows]

# === PERÍODOS ===
def salvar_periodos(periodos):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM periodos")
    for p in periodos:
        c.execute("INSERT INTO periodos (nome, inicio, fim) VALUES (?, ?, ?)",
                  (p["nome"], p["inicio"], p["fim"]))
    conn.commit()
    conn.close()

def carregar_periodos():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT nome, inicio, fim FROM periodos")
    rows = c.fetchall()
    conn.close()
    return [{"nome": row[0], "inicio": row[1], "fim": row[2]} for row in rows]