import sqlite3
import json
import uuid
from models import Turma, Professor, Disciplina, Sala, DisciplinaTurma

def init_db():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    
    # Turmas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id TEXT PRIMARY KEY,
            nome TEXT UNIQUE,
            serie TEXT,
            turno TEXT,
            disciplinas_turma TEXT
        )
    """)
    
    # Professores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            id TEXT PRIMARY KEY,
            nome TEXT UNIQUE,
            disciplinas TEXT,
            disponibilidade_dias TEXT,
            disponibilidade_horarios TEXT,
            restricoes TEXT
        )
    """)
    
    # Disciplinas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            id TEXT PRIMARY KEY,
            nome TEXT UNIQUE,
            carga_semanal INTEGER,
            tipo TEXT,
            series TEXT,
            cor_fundo TEXT,
            cor_fonte TEXT
        )
    """)
    
    # Salas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS salas (
            id TEXT PRIMARY KEY,
            nome TEXT UNIQUE,
            capacidade INTEGER,
            tipo TEXT
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
            "INSERT INTO turmas (id, nome, serie, turno, disciplinas_turma) VALUES (?, ?, ?, ?, ?)",
            (
                t.id,
                t.nome,
                t.serie,
                t.turno,
                json.dumps([dt.__dict__ for dt in t.disciplinas_turma])
            )
        )
    conn.commit()
    conn.close()

def carregar_turmas():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM turmas")
    rows = cursor.fetchall()
    conn.close()
    
    turmas = []
    for row in rows:
        discs_data = json.loads(row[4]) if row[4] else []
        discs_turma = [DisciplinaTurma(**d) for d in discs_data]
        turmas.append(Turma(
            nome=row[1],
            serie=row[2],
            turno=row[3],
            disciplinas_turma=discs_turma,
            id=row[0]
        ))
    return turmas

def salvar_professores(professores):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM professores")
    for p in professores:
        cursor.execute(
            "INSERT INTO professores (id, nome, disciplinas, disponibilidade_dias, disponibilidade_horarios, restricoes) VALUES (?, ?, ?, ?, ?, ?)",
            (
                p.id,
                p.nome,
                json.dumps(p.disciplinas),
                json.dumps(list(p.disponibilidade_dias)),
                json.dumps(list(p.disponibilidade_horarios)),
                json.dumps(list(p.restricoes))
            )
        )
    conn.commit()
    conn.close()

def carregar_professores():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professores")
    rows = cursor.fetchall()
    conn.close()
    
    return [
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

def salvar_disciplinas(disciplinas):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM disciplinas")
    for d in disciplinas:
        cursor.execute(
            "INSERT INTO disciplinas (id, nome, carga_semanal, tipo, series, cor_fundo, cor_fonte) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                d.id,
                d.nome,
                d.carga_semanal,
                d.tipo,
                json.dumps(d.series),
                d.cor_fundo,
                d.cor_fonte
            )
        )
    conn.commit()
    conn.close()

def carregar_disciplinas():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM disciplinas")
    rows = cursor.fetchall()
    conn.close()
    
    return [
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
    conn.close()
    
    return [
        Sala(nome=row[1], capacidade=row[2], tipo=row[3], id=row[0])
        for row in rows
    ]