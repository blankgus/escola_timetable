def eh_horario_ideal(tipo_disciplina: str, horario: int) -> bool:
    if tipo_disciplina == "pesada":
        return horario <= 4
    elif tipo_disciplina == "pratica":
        return horario >= 4
    return True