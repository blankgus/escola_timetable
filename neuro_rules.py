def eh_horario_ideal(tipo_disciplina: str, horario: int) -> bool:
    if tipo_disciplina == "pesada":
        return horario <= 3
    elif tipo_disciplina == "pratica":
        return horario >= 5
    else:
        return horario != 4