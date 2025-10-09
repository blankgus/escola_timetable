import sqlite3
import json
from models import Turma, Professor, Disciplina, Sala, Aula

def init_db():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS turmas (
        id TEXT PRIMARY KEY,
        nome TEXT UNIQUE,
        serie TEXT,
        turno TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS professores (
        id TEXT PRIMARY KEY,
        nome TEXT UNIQUE,
        disciplinas TEXT,
        disponibilidade TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS disciplinas (
        id TEXT PRIMARY KEY,
        nome TEXT UNIQUE,
        carga_semanal INTEGER,
        tipo TEXT,
        series TEXT
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
        sala TEXT
    )''')
    conn.commit()
    conn.close()

def salvar_turmas(turmas):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM turmas")
    for t in turmas:
        c.execute("INSERT INTO turmas VALUES (?, ?, ?, ?)",
                  (t.id, t.nome, t.serie, t.turno))
    conn.commit()
    conn.close()

def carregar_turmas():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT * FROM turmas")
    rows = c.fetchall()
    conn.close()
    return [Turma(nome=r[1], serie=r[2], turno=r[3], id=r[0]) for r in rows]

def salvar_professores(professores):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM professores")
    for p in professores:
        c.execute("INSERT INTO professores VALUES (?, ?, ?, ?)",
                  (p.id, p.nome, json.dumps(p.disciplinas), json.dumps(list(p.disponibilidade))))
    conn.commit()
    conn.close()

def carregar_professores():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT * FROM professores")
    rows = c.fetchall()
    conn.close()
    return [
        Professor(nome=r[1], disciplinas=json.loads(r[2]), disponibilidade=set(json.loads(r[3])), id=r[0])
        for r in rows
    ]

def salvar_disciplinas(disciplinas):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM disciplinas")
    for d in disciplinas:
        c.execute("INSERT INTO disciplinas VALUES (?, ?, ?, ?, ?)",
                  (d.id, d.nome, d.carga_semanal, d.tipo, json.dumps(d.series)))
    conn.commit()
    conn.close()

def carregar_disciplinas():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT * FROM disciplinas")
    rows = c.fetchall()
    conn.close()
    return [
        Disciplina(nome=r[1], carga_semanal=r[2], tipo=r[3], series=json.loads(r[4]), id=r[0])
        for r in rows
    ]

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

# ✅ FUNÇÕES FALTANTES — ADICIONADAS
def salvar_grade(aulas):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM aulas")
    for aula in aulas:
        c.execute("INSERT INTO aulas VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (aula.id, aula.turma, aula.disciplina, aula.professor, aula.dia, aula.horario, aula.sala))
    conn.commit()
    conn.close()

def carregar_grade():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT * FROM aulas")
    rows = c.fetchall()
    conn.close()
    return [
        Aula(turma=r[1], disciplina=r[2], professor=r[3], dia=r[4], horario=r[5], sala=r[6], id=r[0])
        for r in rows
    ]