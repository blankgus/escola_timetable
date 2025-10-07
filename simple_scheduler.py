# simple_scheduler.py
from models import Aula
from collections import defaultdict
import random

class SimpleGradeHoraria:
    def __init__(self, turmas, professores, disciplinas):
        self.turmas = turmas
        self.professores = {p.nome: p for p in professores}
        self.disciplinas = {d.nome: d for d in disciplinas}
        self.dias = ["seg", "ter", "qua", "qui", "sex"]
        # Horários úteis (recreio na posição 4)
        self.horarios = [1, 2, 3, 5, 6, 7]
        
        # Mapear carga por turma
        self.carga_turma = defaultdict(lambda: defaultdict(int))
        for turma in turmas:
            for nome_disc, disc in self.disciplinas.items():
                if turma.serie in disc.series:
                    self.carga_turma[turma.nome][nome_disc] = disc.carga_semanal

    def gerar_grade(self):  # ← NOME CORRETO DO MÉTODO!
        aulas = []
        prof_aulas = defaultdict(list)
        turma_aulas = defaultdict(list)
        
        # Criar lista de aulas pendentes
        pendentes = []
        for turma_nome in self.carga_turma:
            for disc, carga in self.carga_turma[turma_nome].items():
                for _ in range(carga):
                    pendentes.append((turma_nome, disc))
        
        # Embaralhar para evitar viés
        random.shuffle(pendentes)
        
        for turma_nome, disc_nome in pendentes:
            atribuido = False
            # Tentar todos os professores da disciplina
            profs_possiveis = [p for p in self.professores.values() if disc_nome in p.disciplinas]
            random.shuffle(profs_possiveis)
            
            for prof in profs_possiveis:
                # Tentar todas as combinações de dia/horário
                combinacoes = [(dia, h) for dia in self.dias for h in self.horarios]
                random.shuffle(combinacoes)
                
                for dia, horario in combinacoes:
                    if dia not in prof.disponibilidade:
                        continue
                    
                    # Verificar conflitos
                    conflito = False
                    for a in prof_aulas[prof.nome]:
                        if a.dia == dia and a.horario == horario:
                            conflito = True
                            break
                    for a in turma_aulas[turma_nome]:
                        if a.dia == dia and a.horario == horario:
                            conflito = True
                            break
                    
                    if not conflito:
                        aula = Aula(turma_nome, disc_nome, prof.nome, dia, horario)
                        aulas.append(aula)
                        prof_aulas[prof.nome].append(aula)
                        turma_aulas[turma_nome].append(aula)
                        atribuido = True
                        break
                
                if atribuido:
                    break
            
            # Se não conseguir atribuir, força com primeiro professor disponível
            if not atribuido and profs_possiveis:
                prof = profs_possiveis[0]
                dia = list(prof.disponibilidade)[0] if prof.disponibilidade else "seg"
                horario = self.horarios[0]  # Primeiro horário válido
                aula = Aula(turma_nome, disc_nome, prof.nome, dia, horario)
                aulas.append(aula)
        
        return aulas