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
        self.horarios = list(range(1, 7))
        
        # Mapear carga por turma
        self.carga_turma = defaultdict(lambda: defaultdict(int))
        for turma in turmas:
            for nome_disc, disc in self.disciplinas.items():
                if turma.serie in disc.series:
                    self.carga_turma[turma.nome][nome_disc] = disc.carga_semanal

    def gerar_grade(self):
        aulas = []
        prof_aulas = defaultdict(list)  # prof -> lista de aulas
        turma_aulas = defaultdict(list)  # turma -> lista de aulas
        
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
                # Tentar todos os dias/horários
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
            
            if not atribuido:
                # Forçar atribuição mesmo com conflito (último recurso)
                if profs_possiveis:
                    prof = profs_possiveis[0]
                    dia = list(prof.disponibilidade)[0] if prof.disponibilidade else "seg"
                    horario = 1
                    aula = Aula(turma_nome, disc_nome, prof.nome, dia, horario)
                    aulas.append(aula)
                    # Notificar no relatório
        
        return aulas