# export.py
import pandas as pd
from fpdf import FPDF

def exportar_para_excel(aulas, caminho="grade_horaria.xlsx"):
    """Exporta a grade para Excel com horários reais"""
    df = pd.DataFrame([
        {"Turma": a.turma, "Disciplina": a.disciplina, "Professor": a.professor, "Dia": a.dia, "Horário": a.horario}
        for a in aulas
    ])
    
    # Mapear horários para rótulos reais
    HORARIOS_REAIS = {
        1: "07:00-07:50",
        2: "07:50-08:40",
        3: "08:40-09:30",
        4: "09:30-10:00",  # RECREIO
        5: "10:00-10:50",
        6: "10:50-11:40",
        7: "11:40-12:30"
    }
    
    # Converter horários numéricos para reais
    df["Horário"] = df["Horário"].map(HORARIOS_REAIS).fillna("Horário Inválido")
    
    # Criar tabela pivot
    tabela = df.pivot_table(
        index=["Turma", "Horário"],
        columns="Dia",
        values="Disciplina",
        aggfunc=lambda x: x.iloc[0],
        fill_value=""
    ).reindex(columns=["seg", "ter", "qua", "qui", "sex"], fill_value="")
    
    # Salvar Excel
    with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
        tabela.to_excel(writer, sheet_name="Grade por Turma")
        df.to_excel(writer, sheet_name="Dados Brutos", index=False)

def exportar_para_pdf(aulas, caminho="grade_horaria.pdf"):
    """Exporta a grade para PDF com horários reais"""
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
    
    # Horários reais para PDF
    HORARIOS_REAIS = {
        1: "07:00", 2: "07:50", 3: "08:40", 
        4: "09:30 (Recreio)", 
        5: "10:00", 6: "10:50", 7: "11:40"
    }
    
    for turma in sorted(turmas_aulas.keys()):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt=f"Turma: {turma}", ln=True)
        pdf.set_font("Arial", size=10)
        # Ordenar aulas por dia e horário
        aulas_ordenadas = sorted(turmas_aulas[turma], key=lambda x: (x.dia, x.horario))
        for aula in aulas_ordenadas:
            horario_real = HORARIOS_REAIS.get(aula.horario, f"{aula.horario}ª aula")
            # Pular recreio (não mostrar no PDF)
            if aula.horario == 4:
                continue
            linha = f"{aula.dia.upper()} {horario_real}: {aula.disciplina} - Prof. {aula.professor}"
            pdf.cell(0, 6, txt=linha, ln=True)
        pdf.ln(5)
    
    pdf.output(caminho)
    return caminho