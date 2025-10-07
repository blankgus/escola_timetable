# export.py (trecho atualizado)
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
    
    # Horários reais para PDF
    HORARIOS_REAIS = {
        1: "07:00", 2: "07:50", 3: "08:40", 
        4: "10:00", 5: "10:50", 6: "11:40"
    }
    
    for turma in sorted(turmas_aulas.keys()):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt=f"Turma: {turma}", ln=True)
        pdf.set_font("Arial", size=10)
        for aula in sorted(turmas_aulas[turma], key=lambda x: (x.dia, x.horario)):
            horario_real = HORARIOS_REAIS.get(aula.horario, f"{aula.horario}ª")
            linha = f"{aula.dia.upper()} {horario_real}: {aula.disciplina} - Prof. {aula.professor}"
            pdf.cell(0, 6, txt=linha, ln=True)
        pdf.ln(5)
    
    pdf.output(caminho)
    return caminho