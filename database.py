def salvar_grade(aulas):
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS aulas (
        id TEXT PRIMARY KEY,
        turma TEXT,
        disciplina TEXT,
        professor TEXT,
        dia TEXT,
        horario INTEGER,
        sala TEXT
    )''')
    c.execute("DELETE FROM aulas")
    for aula in aulas:
        c.execute("INSERT INTO aulas VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (aula.id, aula.turma, aula.disciplina, aula.professor, aula.dia, aula.horario, aula.sala))
    conn.commit()
    conn.close()

def carregar_grade():
    conn = sqlite3.connect('escola.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS aulas (
        id TEXT PRIMARY KEY,
        turma TEXT,
        disciplina TEXT,
        professor TEXT,
        dia TEXT,
        horario INTEGER,
        sala TEXT
    )''')
    c.execute("SELECT * FROM aulas")
    rows = c.fetchall()
    conn.close()
    from models import Aula
    return [
        Aula(turma=r[1], disciplina=r[2], professor=r[3], dia=r[4], horario=r[5], sala=r[6], id=r[0])
        for r in rows
    ]