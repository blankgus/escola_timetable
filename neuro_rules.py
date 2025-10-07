# neuro_rules.py
def eh_horario_ideal(tipo_disciplina: str, horario: int) -> bool:
    """
    Horários ideais considerando 7 períodos com recreio na posição 4
    """
    if tipo_disciplina == "pesada":
        # Disciplinas pesadas: até a 3ª aula (antes do recreio)
        return horario <= 3
    elif tipo_disciplina == "pratica":
        # Práticas: após o recreio (5ª, 6ª, 7ª)
        return horario >= 5
    else:
        # Médias/leves: qualquer horário exceto recreio (4)
        return horario != 4