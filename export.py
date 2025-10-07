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
        4: "09:30-10:00",
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
    ).reindex(columns=["seg", "ter", "qua", "qui", "sex"], fill_value="")
    
    with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
        tabela.to_excel(writer, sheet_name="Grade por Turma")
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
        4: "09:30-10:00",
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
            if aula.horario == 4:
                continue
            horario_real = HORARIOS_REAIS.get(aula.horario, f"{aula.horario}ª aula")
            linha = f"{aula.dia.upper()} {horario_real}: {aula.disciplina} - Prof. {aula.professor} ({aula.sala})"
            pdf.cell(0, 6, txt=linha, ln=True)
        pdf.ln(5)
    
    pdf.output(caminho)
    return caminho

def gerar_relatorio_professor(aulas, professor_nome):
    """Gera relatório semanal de um professor específico"""
    aulas_prof = [a for a in aulas if a.professor == professor_nome]
    
    if not aulas_prof:
        return f"Professor {professor_nome} não tem aulas cadastradas."
    
    HORARIOS_REAIS = {
        1: "07:00-07:50",
        2: "07:50-08:40", 
        3: "08:40-09:30",
        4: "09:30-10:00",
        5: "10:00-10:50",
        6: "10:50-11:40",
        7: "11:40-12:30"
    }
    
    dados = []
    for aula in aulas_prof:
        dados.append({
            "Dia": aula.dia.upper(),
            "Horário": HORARIOS_REAIS[aula.horario],
            "Disciplina": aula.disciplina,
            "Turma": aula.turma,
            "Sala": aula.sala
        })
    
    df = pd.DataFrame(dados)
    ordem_dias = {"SEG": 0, "TER": 1, "QUA": 2, "QUI": 3, "SEX": 4}
    df["ordem_dia"] = df["Dia"].map(ordem_dias)
    df = df.sort_values(["ordem_dia", "Horário"]).drop("ordem_dia", axis=1)
    
    return df

def gerar_relatorio_todos_professores(aulas):
    """Gera relatório de todos os professores"""
    professores = list(set(a.professor for a in aulas))
    relatorios = {}
    
    for prof in sorted(professores):
        relatorios[prof] = gerar_relatorio_professor(aulas, prof)
    
    return relatorios

def gerar_relatorio_disciplina_sala(aulas):
    """Gera relatório de disciplina x sala x semana"""
    if not aulas:
        return "Nenhuma aula cadastrada."
    
    HORARIOS_REAIS = {
        1: "07:00-07:50",
        2: "07:50-08:40", 
        3: "08:40-09:30",
        4: "09:30-10:00",
        5: "10:00-10:50",
        6: "10:50-11:40",
        7: "11:40-12:30"
    }
    
    dados = []
    for aula in aulas:
        dados.append({
            "Disciplina": aula.disciplina,
            "Sala": aula.sala,
            "Dia": aula.dia.upper(),
            "Horário": HORARIOS_REAIS[aula.horario],
            "Turma": aula.turma,
            "Professor": aula.professor
        })
    
    df = pd.DataFrame(dados)
    ordem_dias = {"SEG": 0, "TER": 1, "QUA": 2, "QUI": 3, "SEX": 4}
    df["ordem_dia"] = df["Dia"].map(ordem_dias)
    df = df.sort_values(["Disciplina", "Sala", "ordem_dia", "Horário"]).drop("ordem_dia", axis=1)
    
    return df