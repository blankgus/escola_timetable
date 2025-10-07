# scheduler_ortools.py
from ortools.sat.python import cp_model
from neuro_rules import eh_horario_ideal
from collections import defaultdict
from models import Aula

class GradeHorariaORTools:
    def __init__(self, turmas, professores, disciplinas, relaxar_horario_ideal=False):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = {d.nome: d for d in disciplinas}
        self.dias = ["seg", "ter", "qua", "qui", "sex"]
        self.horarios = [1, 2, 3, 5, 6, 7]  # ← REMOVIDO horário 4 (recreio)
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        self.solver.parameters.max_time_in_seconds = 10.0
        self.relaxar_horario_ideal = relaxar_horario_ideal

        self.turma_idx = {t.nome: i for i, t in enumerate(turmas)}
        self.disciplinas_por_turma = self._disciplinas_por_turma()

        self.variaveis = {}
        self.atribuicoes_prof = {}

        self._preparar_dados()
        self._criar_variaveis()
        self._adicionar_restricoes()

    def _disciplinas_por_turma(self):
        dp = defaultdict(list)
        for turma in self.turmas:
            for nome_disc, disc in self.disciplinas.items():
                if turma.serie in disc.series:
                    for _ in range(disc.carga_semanal):
                        dp[turma.nome].append(nome_disc)
        return dp

    def _preparar_dados(self):
        for turma_nome, disciplinas in self.disciplinas_por_turma.items():
            for disc_nome in set(disciplinas):
                for dia in self.dias:
                    for horario in self.horarios:  # ← Usa horários sem recreio
                        profs_validos = [
                            p.nome for p in self.professores
                            if disc_nome in p.disciplinas and dia in p.disponibilidade
                        ]
                        if profs_validos:
                            self.atribuicoes_prof[(turma_nome, disc_nome, dia, horario)] = profs_validos

    def _criar_variaveis(self):
        for turma_nome, disciplinas in self.disciplinas_por_turma.items():
            contagem = defaultdict(int)
            for d in disciplinas:
                contagem[d] += 1

            for disc_nome, total in contagem.items():
                vars_disc = []
                for dia in self.dias:
                    for horario in self.horarios:  # ← Horários sem recreio
                        if (turma_nome, disc_nome, dia, horario) in self.atribuicoes_prof:
                            var = self.model.NewBoolVar(f"x_{turma_nome}_{disc_nome}_{dia}_{horario}")
                            self.variaveis[(turma_nome, disc_nome, dia, horario)] = var
                            vars_disc.append(var)
                
                if not vars_disc:
                    raise Exception(f"Sem atribuições possíveis para {turma_nome} - {disc_nome}")
                self.model.Add(sum(vars_disc) == total)

    def _adicionar_restricoes(self):
        # Restrição 1: uma turma só pode ter uma aula por horário
        for turma_nome in self.turma_idx:
            for dia in self.dias:
                for horario in self.horarios:  # ← Horários sem recreio
                    vars_horario = [
                        var for (t, d, d2, h2), var in self.variaveis.items()
                        if t == turma_nome and d2 == dia and h2 == horario
                    ]
                    if vars_horario:
                        self.model.Add(sum(vars_horario) <= 1)

        # Restrição 2: um professor só pode dar uma aula por horário
        for prof in self.professores:
            for dia in self.dias:
                if dia not in prof.disponibilidade:
                    continue
                for horario in self.horarios:  # ← Horários sem recreio
                    vars_prof = []
                    for (t, d, d2, h2), var in self.variaveis.items():
                        if d2 == dia and h2 == horario:
                            if d in prof.disciplinas:
                                vars_prof.append(var)
                    if vars_prof:
                        self.model.Add(sum(vars_prof) <= 1)

    def resolver(self):
        if not self.relaxar_horario_ideal:
            objetivo = []
            for (turma, disc, dia, horario), var in self.variaveis.items():
                if eh_horario_ideal(self.disciplinas[disc].tipo, horario):
                    objetivo.append(var)
            self.model.Maximize(sum(objetivo))
        
        status = self.solver.Solve(self.model)
        
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            aulas = []
            for (turma, disc, dia, horario), var in self.variaveis.items():
                if self.solver.BooleanValue(var):
                    profs = self.atribuicoes_prof.get((turma, disc, dia, horario), [])
                    if profs:
                        aulas.append(Aula(turma, disc, profs[0], dia, horario))
            return aulas
        else:
            raise Exception("❌ Nenhuma solução viável encontrada.")