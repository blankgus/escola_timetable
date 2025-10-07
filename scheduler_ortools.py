# scheduler_ortools.py (trecho atualizado)
def _criar_variaveis(self):
    for turma_nome, disciplinas in self.disciplinas_por_turma.items():
        contagem = defaultdict(int)
        for d in disciplinas:
            contagem[d] += 1

        for disc_nome, total in contagem.items():
            vars_disc = []
            for dia in self.dias:
                for horario in self.horarios:
                    # 🔑 PULAR HORÁRIO DO RECREIO (4ª posição = após 3 aulas)
                    if horario == 4:
                        continue
                    if (turma_nome, disc_nome, dia, horario) in self.atribuicoes_prof:
                        var = self.model.NewBoolVar(f"x_{turma_nome}_{disc_nome}_{dia}_{horario}")
                        self.variaveis[(turma_nome, disc_nome, dia, horario)] = var
                        vars_disc.append(var)
            
            if not vars_disc:
                raise Exception(f"Sem atribuições possíveis para {turma_nome} - {disc_nome}")
            self.model.Add(sum(vars_disc) == total)