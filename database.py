# database.py (trecho de feriados adicionado)
import sqlite3
import json
from models import Turma, Professor, Disciplina, Sala

def init_db():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    
    # ... tabelas existentes ...
    
    c.execute('''CREATE TABLE IF NOT EXISTS feriados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        motivo TEXT
    )''')
    
    conn.commit()
    conn.close()

# === FERIADOS ===
def salvar_feriados(feriados):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("DELETE FROM feriados")
    for f in feriados:
        c.execute("INSERT INTO feriados (data, motivo) VALUES (?, ?)",
                  (f["data"], f["motivo"]))
    conn.commit()
    conn.close()

def carregar_feriados():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute("SELECT data, motivo FROM feriados")
    rows = c.fetchall()
    conn.close()
    feriados = []
    for row in rows:
        feriados.append({
            "data": row[0],
            "motivo": row[1],
            "id": str(uuid.uuid4())
        })
    return feriados

# ... resto do arquivo igual ...