# export.py
import pandas as pd
from fpdf import FPDF

def exportar_para_excel(aulas, caminho="grade_horaria.xlsx"):
    df = pd.DataFrame([
        {"Turma": a.turma, "Disciplina": a.disciplina, "Professor": a.professor, "Dia": a.dia, "Horário": a.horario, "Sala": a.sala}
        for a in aulas
    ])
    HORARIOS_REAIS = {
        1: "07:00-07:50",
        2: "07:50-08:40",
        3: "08:40-09:30",
        4: "09:30-10:00", # INTERVALO
        5: "10:00-10:50",
        6: "10:50-11:40",
        7: "11:40-12:30"
    }
    df["Horário"] = df["Horário"].map(HORARIOS_REAIS).fillna("Horário Inválido")
    tabela = df.pivot_table(
        index=["Turma", "Horário"],
        columns="Dia",
        values="Disciplina",
        aggfunc=lambda x: x.iloc[0],
        fill_value=""
    ).reindex(columns=["dom", "seg", "ter", "qua", "qui", "sex", "sab"], fill_value="")
    with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
        tabela.to_excel(writer, sheet_name="Grade")
        df.to_excel(writer, sheet_name="Dados Brutos", index=False)

def exportar_para_pdf(aulas, caminho="grade_horaria.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Grade Horária Escolar", ln=True, align='C')
    pdf.ln(10)
    from collections import defaultdict
    turmas_aulas = defaultdict(list)
    for aula in aulas:
        turmas_aulas[aula.turma].append(aula)
    HORARIOS_REAIS = {
        1: "07:00-07:50",
        2: "07:50-08:40",
        3: "08:40-09:30",
        4: "09:30-10:00", # INTERVALO
        5: "10:00-10:50",
        6: "10:50-11:40",
        7: "11:40-12:30"
    }
    for turma in sorted(turmas_aulas.keys()):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt=f"Turma: {turma}", ln=True)
        pdf.set_font("Arial", size=10)
        aulas_ordenadas = sorted(turmas_aulas[turma], key=lambda x: (x.dia, x.horario))
        for aula in aulas_ordenadas:
            pdf.cell(0, 8, txt=f"{HORARIOS_REAIS.get(aula.horario, str(aula.horario))} - {aula.dia.upper()}: {aula.disciplina} ({aula.professor})", ln=True)
        pdf.ln(5)
    pdf.output(caminho)

def gerar_relatorio_professor(professor_nome, aulas):
    return pd.DataFrame([{"Professor": professor_nome, "Total Aulas": len([a for a in aulas if a.professor == professor_nome])}])

def gerar_relatorio_todos_professores(aulas):
    return pd.DataFrame([
        {"Professor": p, "Total Aulas": c}
        for p, c in pd.Series([a.professor for a in aulas]).value_counts().items()
    ])

def gerar_relatorio_disciplina_sala(aulas):
    return pd.DataFrame([
        {"Disciplina": a.disciplina, "Sala": a.sala, "Quantidade": 1}
        for a in aulas
    ]).groupby(["Disciplina", "Sala"]).sum().reset_index()

def gerar_grade_por_turma_semana(aulas, turma_nome, semana=1):
    dias = ["seg", "ter", "qua", "qui", "sex"]
    horarios = [1, 2, 3, 4, 5, 6, 7]
    grade = {h: {d: "Sem Aula" for d in dias} for h in horarios}
    for aula in aulas:
        if aula.turma == turma_nome and aula.dia in dias and aula.horario in horarios:
            grade[aula.horario][aula.dia] = aula.disciplina
    for h in [4]:
        for d in dias:
            grade[h][d] = "RECREIO"
    df = pd.DataFrame(grade).T
    df.index.name = "Horário"
    HORARIOS_REAIS = {
        1: "07:00-07:50",
        2: "07:50-08:40",
        3: "08:40-09:30",
        4: "09:30-10:00", # INTERVALO
        5: "10:00-10:50",
        6: "10:50-11:40",
        7: "11:40-12:30"
    }
    df.index = [HORARIOS_REAIS.get(h, str(h)) for h in df.index]
    return df

def gerar_grade_por_sala_semana(aulas, sala_nome, semana=1):
    dias = ["seg", "ter", "qua", "qui", "sex"]
    horarios = [1, 2, 3, 4, 5, 6, 7]
    grade = {h: {d: "Sem Aula" for d in dias} for h in horarios}
    for aula in aulas:
        if aula.sala == sala_nome and aula.dia in dias and aula.horario in horarios:
            grade[aula.horario][aula.dia] = aula.disciplina
    for h in [4]:
        for d in dias:
            grade[h][d] = "RECREIO"
    df = pd.DataFrame(grade).T
    df.index.name = "Horário"
    HORARIOS_REAIS = {
        1: "07:00-07:50",
        2: "07:50-08:40",
        3: "08:40-09:30",
        4: "09:30-10:00", # INTERVALO
        5: "10:00-10:50",
        6: "10:50-11:40",
        7: "11:40-12:30"
    }
    df.index = [HORARIOS_REAIS.get(h, str(h)) for h in df.index]
    return df

def gerar_grade_por_professor_semana(aulas, professor_nome, semana=1):
    dias = ["seg", "ter", "qua", "qui", "sex"]
    horarios = [1, 2, 3, 4, 5, 6, 7]
    grade = {h: {d: "Sem Aula" for d in dias} for h in horarios}
    for aula in aulas:
        if aula.professor == professor_nome and aula.dia in dias and aula.horario in horarios:
            grade[aula.horario][aula.dia] = f"{aula.disciplina}{aula.turma}"
    for h in [4]:
        for d in dias:
            grade[h][d] = "RECREIO"
    df = pd.DataFrame(grade).T
    df.index.name = "Horário"
    HORARIOS_REAIS = {
        1: "07:00-07:50",
        2: "07:50-08:40",
        3: "08:40-09:30",
        4: "09:30-10:00", # INTERVALO
        5: "10:00-10:50",
        6: "10:50-11:40",
        7: "11:40-12:30"
    }
    df.index = [HORARIOS_REAIS