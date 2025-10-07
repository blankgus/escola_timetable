# scheduler_ortools.py (trecho atualizado)
class GradeHorariaORTools:
    def __init__(self, turmas, professores, disciplinas, relaxar_horario_ideal=False):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = {d.nome: d for d in disciplinas}
        self.dias = ["seg", "ter", "qua", "qui", "sex"]
        self.horarios = [1, 2, 3, 5, 6, 7]  # ← 6 horários úteis (recreio na posição 4)
        # ... resto do código igual ...