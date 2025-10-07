# simple_scheduler.py (trecho atualizado)
def gerar_grade(self):
    # ...
    for turma_nome, disc_nome in pendentes:
        atribuido = False
        profs_possiveis = [p for p in self.professores.values() if disc_nome in p.disciplinas]
        random.shuffle(profs_possiveis)
        
        for prof in profs_possiveis:
            # 🔑 PULAR HORÁRIO DO RECREIO
            combinacoes = [(dia, h) for dia in self.dias for h in self.horarios if h != 4]
            random.shuffle(combinacoes)
            # ... resto do código ...