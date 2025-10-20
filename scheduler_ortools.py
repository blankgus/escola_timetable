from ortools.sat.python import cp_model
from collections import defaultdict
from models import Aula, DIAS_SEMANA, HORARIOS_REAIS
import streamlit as st

class GradeHorariaORTools:
    def __init__(self, turmas, professores, disciplinas, dias_em_estendido=None, relaxar_horario_ideal=False):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = {d.nome: d for d in disciplinas}
        self.dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']  # ✅ Usar formato completo
        self.dias_em_estendido = dias_em_estendido or []
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        self.solver.parameters.max_time_in_seconds = 60.0
        self.relaxar_horario_ideal = relaxar_horario_ideal

        self.turma_idx = {t.nome: i for i, t in enumerate(turmas)}
        self.prof_idx = {p.nome: i for i, p in enumerate(professores)}
        self.disciplinas_por_turma = self._disciplinas_por_turma()

        self.variaveis = {}
        self.atribuicoes_prof = {}

        self._preparar_dados()
        self._criar_variaveis()
        self._adicionar_restricoes()

    def _obter_segmento_turma(self, turma_nome):
        """Determina o segmento da turma"""
        if 'em' in turma_nome.lower():
            return "EM"
        else:
            return "EF_II"

    def _obter_horarios_turma(self, turma_nome, dia):
        """Retorna os horários disponíveis para a turma considerando o dia"""
        segmento = self._obter_segmento_turma(turma_nome)
        
        if segmento == "EM":
            # EM: 7 períodos, mas pode variar por dia
            if dia in self.dias_em_estendido:
                return [1, 2, 3, 4, 5, 6, 7]  # Até 13:10
            else:
                return [1, 2, 3, 4, 5, 6]  # Até 12:20
        else:
            # EF II: sempre 6 períodos (07:50-12:20)
            return [1, 2, 3, 4, 5, 6]

    def _eh_horario_intervalo(self, turma_nome, horario):
        """Verifica se o horário é de intervalo"""
        segmento = self._obter_segmento_turma(turma_nome)
        
        if segmento == "EF_II":
            return horario == 3  # EF II: intervalo no 3º horário
        else:
            return horario == 4  # EM: intervalo no 4º horário

    def _disciplinas_por_turma(self):
        dp = defaultdict(list)
        for turma in self.turmas:
            for nome_disc, disc in self.disciplinas.items():
                # ✅ CORREÇÃO: Verificar vínculo direto turma-disciplina
                if turma.nome in disc.turmas:
                    for _ in range(disc.carga_semanal):
                        dp[turma.nome].append(nome_disc)
        return dp

    def _preparar_dados(self):
        st.info("🔧 Preparando dados para otimização...")
        st.info(f"📅 Dias EM estendido: {self.dias_em_estendido}")
        
        for turma_nome, disciplinas in self.disciplinas_por_turma.items():
            for disc_nome in set(disciplinas):
                for dia in self.dias:
                    # ✅ CORREÇÃO: Obter horários específicos por dia e turma
                    horarios_disponiveis = self._obter_horarios_turma(turma_nome, dia)
                    
                    for horario in horarios_disponiveis:
                        # Pular horário de intervalo
                        if self._eh_horario_intervalo(turma_nome, horario):
                            continue
                            
                        profs_validos = []
                        for p in self.professores:
                            # Verificar se professor pode dar esta disciplina
                            if disc_nome not in p.disciplinas:
                                continue
                            
                            # Verificar disponibilidade do dia (já está no formato correto)
                            if dia not in p.disponibilidade:
                                continue
                            
                            # Verificar horário indisponível
                            if f"{dia}_{horario}" in p.horarios_indisponiveis:
                                continue
                            
                            # Verificar grupo
                            prof_grupo = getattr(p, 'grupo', 'A')
                            turma_grupo = next((t.grupo for t in self.turmas if t.nome == turma_nome), 'A')
                            if prof_grupo not in [turma_grupo, "AMBOS"]:
                                continue
                            
                            profs_validos.append(p.nome)
                        
                        if profs_validos:
                            self.atribuicoes_prof[(turma_nome, disc_nome, dia, horario)] = profs_validos

    def _criar_variaveis(self):
        st.info("📊 Criando variáveis de decisão...")
        for (turma, disc, dia, horario), profs in self.atribuicoes_prof.items():
            for prof in profs:
                var = self.model.NewBoolVar(f'aula_{turma}_{disc}_{dia}_{horario}_{prof}')
                self.variaveis[(turma, disc, dia, horario, prof)] = var

    def _adicionar_restricoes(self):
        st.info("🔒 Adicionando restrições...")
        
        # 1. Cada aula pendente deve ser atribuída exatamente uma vez
        aulas_necessarias = 0
        for turma_nome, disciplinas in self.disciplinas_por_turma.items():
            disc_contagem = defaultdict(int)
            for d in disciplinas:
                disc_contagem[d] += 1
                aulas_necessarias += 1
            
            for disc_nome, total in disc_contagem.items():
                vars_disc = []
                for (t, d, di, h, p), var in self.variaveis.items():
                    if t == turma_nome and d == disc_nome:
                        vars_disc.append(var)
                
                if vars_disc:
                    self.model.Add(sum(vars_disc) == total)
        
        st.write(f"📋 Total de aulas necessárias: {aulas_necessarias}")

        # 2. Um professor não pode dar duas aulas ao mesmo tempo
        for prof in self.professores:
            for dia in self.dias:
                for horario in range(1, 8):  # Todos os horários possíveis (1-7)
                    vars_prof = []
                    for (t, d, di, h, p), var in self.variaveis.items():
                        if p == prof.nome and di == dia and h == horario:
                            vars_prof.append(var)
                    
                    if len(vars_prof) > 1:
                        self.model.Add(sum(vars_prof) <= 1)

        # 3. Uma turma não pode ter duas aulas ao mesmo tempo
        for turma in self.turmas:
            for dia in self.dias:
                for horario in range(1, 8):  # Todos os horários possíveis (1-7)
                    vars_turma = []
                    for (t, d, di, h, p), var in self.variaveis.items():
                        if t == turma.nome and di == dia and h == horario:
                            vars_turma.append(var)
                    
                    if len(vars_turma) > 1:
                        self.model.Add(sum(vars_turma) <= 1)

    def resolver(self):
        st.info("🎯 Resolvendo otimização...")
        status = self.solver.Solve(self.model)
        aulas = []
        
        if status == cp_model.OPTIMAL:
            st.success("✅ Solução ótima encontrada!")
        elif status == cp_model.FEASIBLE:
            st.success("✅ Solução viável encontrada!")
        else:
            st.error("❌ Nenhuma solução viável encontrada")
            st.info("💡 Tente ajustar as restrições ou usar o algoritmo simples")
            return aulas
        
        # Coletar aulas alocadas
        for (turma, disc, dia, horario, prof), var in self.variaveis.items():
            if self.solver.Value(var) == 1:
                grupo_turma = next((t.grupo for t in self.turmas if t.nome == turma), "A")
                aulas.append(Aula(turma, disc, prof, dia, horario, "Sala 1", grupo_turma))
        
        st.success(f"📊 {len(aulas)} aulas alocadas com sucesso!")
        return aulas