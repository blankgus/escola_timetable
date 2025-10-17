# database.py
import sqlite3
import json
import uuid

def init_db():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    # Criar tabelas se não existirem
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id TEXT PRIMARY KEY,
            nome TEXT,
            serie TEXT,
            turno TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            id TEXT PRIMARY KEY,
            nome TEXT,
            disciplinas TEXT,
            disponibilidade_dias TEXT,
            disponibilidade_horarios TEXT,
            restricoes TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            id TEXT PRIMARY KEY,
            nome TEXT,
            carga_semanal INTEGER,
            tipo TEXT,
            series TEXT,
            cor_fundo TEXT,
            cor_fonte TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS salas (
            id TEXT PRIMARY KEY,
            nome TEXT,
            capacidade INTEGER,
            tipo TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS periodos (
            id TEXT PRIMARY KEY,
            nome TEXT,
            inicio TEXT,
            fim TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feriados (
            id TEXT PRIMARY KEY,
            data TEXT,
            motivo TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aulas (
            id TEXT PRIMARY KEY,
            turma TEXT,
            disciplina TEXT,
            professor TEXT,
            dia TEXT,
            horario INTEGER,
            sala TEXT
        )
    """)
    conn.commit()
    conn.close()

def salvar_turmas(turmas):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM turmas")
    for t in turmas:
        cursor.execute(
            "INSERT INTO turmas (id, nome, serie, turno) VALUES (?, ?, ?, ?)",
            (t.id, t.nome, t.serie, t.turno)
        )
    conn.commit()
    conn.close()

def carregar_turmas():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM turmas")
    rows = cursor.fetchall()
    from models import Turma
    turmas = [Turma(nome=row[1], serie=row[2], turno=row[3], id=row[0]) for row in rows]
    conn.close()
    return turmas

def salvar_professores(professores):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM professores")
    for p in professores:
        cursor.execute(
            "INSERT INTO professores (id, nome, disciplinas, disponibilidade_dias, disponibilidade_horarios, restricoes) VALUES (?, ?, ?, ?, ?, ?)",
            (p.id, p.nome, json.dumps(p.disciplinas), json.dumps(list(p.disponibilidade_dias)), json.dumps(list(p.disponibilidade_horarios)), json.dumps(list(p.restricoes)))
        )
    conn.commit()
    conn.close()

def carregar_professores():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professores")
    rows = cursor.fetchall()
    from models import Professor
    professores = [
        Professor(
            nome=row[1],
            disciplinas=json.loads(row[2]),
            disponibilidade_dias=set(json.loads(row[3])),
            disponibilidade_horarios=set(json.loads(row[4])),
            restricoes=set(json.loads(row[5])),
            id=row[0]
        )
        for row in rows
    ]
    conn.close()
    return professores

def salvar_disciplinas(disciplinas):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM disciplinas")
    for d in disciplinas:
        cursor.execute(
            "INSERT INTO disciplinas (id, nome, carga_semanal, tipo, series, cor_fundo, cor_fonte) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (d.id, d.nome, d.carga_semanal, d.tipo, json.dumps(d.series), d.cor_fundo, d.cor_fonte)
        )
    conn.commit()
    conn.close()

def carregar_disciplinas():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM disciplinas")
    rows = cursor.fetchall()
    from models import Disciplina
    disciplinas = [
        Disciplina(
            nome=row[1],
            carga_semanal=row[2],
            tipo=row[3],
            series=json.loads(row[4]),
            cor_fundo=row[5],
            cor_fonte=row[6],
            id=row[0]
        )
        for row in rows
    ]
    conn.close()
    return disciplinas

def salvar_salas(salas):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM salas")
    for s in salas:
        cursor.execute(
            "INSERT INTO salas (id, nome, capacidade, tipo) VALUES (?, ?, ?, ?)",
            (s.id, s.nome, s.capacidade, s.tipo)
        )
    conn.commit()
    conn.close()

def carregar_salas():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM salas")
    rows = cursor.fetchall()
    from models import Sala
    salas = [Sala(nome=row[1], capacidade=row[2], tipo=row[3], id=row[0]) for row in rows]
    conn.close()
    return salas

def salvar_periodos(periodos):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM periodos")
    for p in periodos:
        cursor.execute(
            "INSERT INTO periodos (id, nome, inicio, fim) VALUES (?, ?, ?, ?)",
            (p["id"], p["nome"], p["inicio"], p["fim"])
        )
    conn.commit()
    conn.close()

def carregar_periodos():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM periodos")
    rows = cursor.fetchall()
    return [{"nome": r[1], "inicio": r[2], "fim": r[3], "id": r[0]} for r in rows]

def salvar_feriados(feriados):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM feriados")
    for f in feriados:
        cursor.execute(
            "INSERT INTO feriados (id, data, motivo) VALUES (?, ?, ?)",
            (f["id"], f["data"], f["motivo"])
        )
    conn.commit()
    conn.close()

def carregar_feriados():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feriados")
    rows = cursor.fetchall()
    return [{"data": r[1], "motivo": r[2], "id": r[0]} for r in rows]

def salvar_grade(aulas):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM aulas")
    for aula in aulas:
        cursor.execute(
            "INSERT INTO aulas (id, turma, disciplina, professor, dia, horario, sala) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (aula.id, aula.turma, aula.disciplina, aula.professor, aula.dia, aula.horario, aula.sala)
        )
    conn.commit()
    conn.close()

def carregar_grade():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM aulas")
    rows = cursor.fetchall()
    from models import Aula
    aulas = [Aula(turma=r[1], disciplina=r[2], professor=r[3], dia=r[4], horario=r[5], sala=r[6], id=r[0]) for r in rows]
    conn.close()
    return aulas