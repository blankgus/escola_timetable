# export.py (mantenha como está, já suporta 7 horários)
# A única mudança é pular o recreio no PDF:
def exportar_para_pdf(aulas, caminho="grade_horaria.pdf"):
    # ...
    for aula in aulas_ordenadas:
        if aula.horario == 4:  # Pular recreio
            continue
        # ... resto do código ...