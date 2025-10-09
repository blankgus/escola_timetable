from ortools.sat.python import cp_model
from collections import defaultdict
from models import Aula, DIAS_SEMANA
import streamlit as st

class GradeHorariaORTools:
    def __init__(self, turmas, professores, disciplinas, relaxar_horario_ideal=False):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = {d.nome: d for d in disciplinas}
        self.dias = DIAS_SEMANA  # 7 dias: dom a sab
        self.horarios = [1, 2, 3, 4, 5, 6, 7]  # Todos os horários (incluindo recreio)
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
            for nome_disc, disc in self.discipl