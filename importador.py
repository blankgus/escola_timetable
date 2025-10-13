# importador.py
import pandas as pd
from models import Turma, Professor, Disciplina, Sala

def carregar_dados_do_excel(caminho):
    # Ler abas do Excel
    df_turmas = pd.read_excel(caminho, sheet_name="Turmas")
    df_professores = pd.read_excel(caminho, sheet_name="Professores")
    df_disciplinas = pd.read_excel(caminho, sheet_name="Disciplinas")
    df_salas = pd.read_excel(caminho, sheet_name="Salas")

    turmas = [Turma(row["nome"], row["serie"], row["turno"]) for _, row in df_turmas.iterrows()]
    professores = [Professor(
        row["nome"],
        row["disciplinas"].split(","),
        set(row["dias_disponiveis"].split(",")),
        set([int(h) for h in row["horarios_disponiveis"].split(",")])
    ) for _, row in df_professores.iterrows()]
    disciplinas = [Disciplina(
        row["nome"],
        row["carga_semanal"],
        row["tipo"],
        row["series"].split(",")
    ) for _, row in df_disciplinas.iterrows()]
    salas = [Sala(row["nome"], row["capacidade"], row["tipo"]) for _, row in df_salas.iterrows()]

    return turmas, professores, disciplinas, salas