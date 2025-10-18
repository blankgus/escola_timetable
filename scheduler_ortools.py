from ortools.sat.python import cp_model
from collections import defaultdict
from models import Aula, DIAS_SEMANA, HORARIOS_DISPONIVEIS
import streamlit as st

class GradeHorariaORTools:
    def __init__(self, turmas, professores, disciplinas, relaxar_horario_ideal=False):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = {d.nome: d for d in disciplinas}
        self.dias = DIAS_SEMANA
        self.horarios = HORARIOS_DISPONIVEIS
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        self.solver.parameters.max_time_in_seconds = 30.0
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
                    for horario in self.horarios:
                        profs_validos = []
                        for p in self.professores:
                            horario_indisponivel = f"{dia}_{horario}" in p.horarios_indisponiveis
                            if (disc_nome in p.disciplinas and 
                                dia in p.disponibilidade and
                                not horario_indisponivel):
                                profs_validos.append(p.nome)
                        
                        if profs_validos:
                            self.atribuicoes_prof[(turma_nome, disc_nome, dia, horario)] = profs_validos

    def _criar_variaveis(self):
        for (turma, disc, dia, horario), profs in self.atribuicoes_prof.items():
            for prof in profs:
                var = self.model.NewBoolVar(f'aula_{turma}_{disc}_{dia}_{horario}_{prof}')
                self.variaveis[(turma, disc, dia, horario, prof)] = var

    def _adicionar_restricoes(self):
        # 1. Cada aula deve ser atribuída
        for turma_nome, disciplinas in self.disciplinas_por_turma.items():
            disc_contagem = defaultdict(int)
            for d in disciplinas:
                disc_contagem[d] += 1
            
            for disc_nome, total in disc_contagem.items():
                vars_disc = []
                for (t, d, di, h, p), var in self.variaveis.items():
                    if t == turma_nome and d == disc_nome:
                        vars_disc.append(var)
                if vars_disc:
                    self.model.Add(sum(vars_disc) == total)

        # 2. Professor não pode dar duas aulas ao mesmo tempo
        for prof in self.professores:
            for dia in self.dias:
                for horario in self.horarios:
                    vars_prof = []
                    for (t, d, di, h, p), var in self.variaveis.items():
                        if p == prof.nome and di == dia and h == horario:
                            vars_prof.append(var)
                    if len(vars_prof) > 1:
                        self.model.Add(sum(vars_prof) <= 1)

        # 3. Turma não pode ter duas aulas ao mesmo tempo
        for turma in self.turmas:
            for dia in self.dias:
                for horario in self.horarios:
                    vars_turma = []
                    for (t, d, di, h, p), var in self.variaveis.items():
                        if t == turma.nome and di == dia and h == horario:
                            vars_turma.append(var)
                    if len(vars_turma) > 1:
                        self.model.Add(sum(vars_turma) <= 1)

    def resolver(self):
        status = self.solver.Solve(self.model)
        aulas = []
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            for (turma, disc, dia, horario, prof), var in self.variaveis.items():
                if self.solver.Value(var) == 1:
                    grupo_turma = next((t.grupo for t in self.turmas if t.nome == turma), "A")
                    aulas.append(Aula(turma, disc, prof, dia, horario, "Sala 1", grupo_turma))
            
            st.success(f"✅ Solução encontrada: {len(aulas)} aulas alocadas")
        else:
            st.error("❌ Nenhuma solução viável encontrada")
            aulas = []
        
        return aulas