# database.py
import sqlite3
import json
import uuid
from models import Turma, Professor, Disciplina, Sala, DisciplinaTurma, Aula, Feriado

def init_db():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id TEXT PRIMARY KEY,
            nome TEXT,
            serie TEXT,
            turno TEXT,
            tipo TEXT,
            disciplinas_turma TEXT,
            regras_neuro TEXT
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
        CREATE TABLE IF NOT EXISTS grades (
            id TEXT PRIMARY KEY,
            turma TEXT,
            disciplina TEXT,
            professor TEXT,
            dia TEXT,
            horario INTEGER,
            sala TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS periodos (
            id TEXT PRIMARY KEY,
            
 TEXT,
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
    conn.commit()
    conn.close()

def salvar_turmas(turmas):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM turmas")
    for t in turmas:
        cursor.execute(
            "INSERT INTO turmas (id, nome, serie, turno, tipo, disciplinas_turma, regras_neuro) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                t.id,
                t.nome,
                t.serie,
                t.turno,
                t.tipo,
                json.dumps([dt.__dict__ for dt in t.disciplinas_turma]),
                json.dumps(t.regras_neuro)
            )
        )
    conn.commit()
    conn.close()

def carregar_turmas():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM turmas")
    rows = cursor.fetchall()
    from models import Turma, DisciplinaTurma
    turmas = []
    for row in rows:
        dt_list = [DisciplinaTurma(**dt) for dt in json.loads(row[5])]
        turmas.append(Turma(
            nome=row[1],
            serie=row[2],
            turno=row[3],
            tipo=row[4],
            disciplinas_turma=dt_list,
            regras_neuro=json.loads(row[6]),
            id=row[0]
        ))
    conn.close()
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
            (
                s.id,
                s.nome,
                s.capacidade,
                s.tipo
            )
        )
    conn.commit()
    conn.close()

def carregar_salas():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM salas")
    rows = cursor.fetchall()
    from models import Sala
    salas = [
        Sala(
            nome=row[1],
            capacidade=row[2],
            tipo=row[3],
            id=row[0]
        )
        for row in rows
    ]
    conn.close()
    return salas

def salvar_grade(aulas):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM grades")
    for a in aulas:
        cursor.execute(
            "INSERT INTO grades (id, turma, disciplina, professor, dia, horario, sala) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                a.id,
                a.turma,
                a.disciplina,
                a.professor,
                a.dia,
                a.horario,
                a.sala
            )
        )
    conn.commit()
    conn.close()

def carregar_grade():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grades")
    rows = cursor.fetchall()
    from models import Aula
    aulas = [
        Aula(
            turma=row[1],
            disciplina=row[2],
            professor=row[3],
            dia=row[4],
            horario=row[5],
            sala=row[6],
            id=row[0]
        )
        for row in rows
    ]
    conn.close()
    return aulas

def salvar_periodos(periodos):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM periodos")
    for p in periodos:
        cursor.execute(
            "INSERT INTO periodos (id, nome, inicio, fim) VALUES (?, ?, ?, ?)",
            (
                p.id,
                p.nome,
                p.inicio,
                p.fim
            )
        )
    conn.commit()
    conn.close()

def carregar_periodos():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM periodos")
    rows = cursor.fetchall()
    periodos = [
        {
            "nome": row[1],
            "inicio": row[2],
            "fim": row[3],
            "id": row[0]
        }
        for row in rows
    ]
    conn.close()
    return periodos

def salvar_feriados(feriados):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM feriados")
    for f in feriados:
        cursor.execute(
            "INSERT INTO feriados (id, data, motivo) VALUES (?, ?, ?)",
            (
                f.id,
                f.data,
                f.motivo
            )
        )
    conn.commit()
    conn.close()

def carregar_feriados():
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feriados")
    rows = cursor.fetchall()
    from models import Feriado
    feriados = [
        Feriado(
            data=row[1],
            motivo=row[2],
            id=row[0]
        )
        for row in rows
    ]
    conn.close()
    return feriados