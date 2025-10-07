# simple_scheduler.py (trecho atualizado)
class SimpleGradeHoraria:
    def __init__(self, turmas, professores, disciplinas):
        self.turmas = turmas
        self.professores = {p.nome: p for p in professores}
        self.disciplinas = {d.nome: d for d in disciplinas}
        self.dias = ["seg", "ter", "qua", "qui", "sex"]
        self.horarios = [1, 2, 3, 5, 6, 7]  # ← Horários úteis
        # ... resto do código igual ...