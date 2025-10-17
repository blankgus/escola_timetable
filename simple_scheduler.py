from models import Aula, DIAS_SEMANA
from collections import defaultdict
import random
import streamlit as st

class SimpleGradeHoraria:
    def __init__(self, turmas, professores, disciplinas):
        self.turmas = turmas
        self.professores = {p.nome: p for p in professores}
        self.disciplinas = {d.nome: d for d in disciplinas}
        self.dias = DIAS_SEMANA  # 7 dias
        self.horarios = [1, 2, 3, 5, 6, 7]  # Sem recreio
        
        self.carga_turma = defaultdict(lambda: defaultdict(int))
        for turma in turmas:
            for nome_disc, disc in self.disciplinas.items():
                if turma.serie in disc.series:
                    self.carga_turma[turma.nome][nome_disc] = disc.carga_semanal

    def gerar_grade(self):
        aulas = []
        prof_aulas = defaultdict(list)
        turma_aulas = defaultdict(list)
        
        pendentes = []
        for turma_nome in self.carga_turma:
            for disc, carga in self.carga_turma[turma_nome].items():
                for _ in range(carga):
                    pendentes.append((turma_nome, disc))
        
        random.shuffle(pendentes)
        
        for turma_nome, disc_nome in pendentes:
            atribuido = False
            profs_possiveis = [p for p in self.professores.values() if disc_nome in p.disciplinas]
            random.shuffle(profs_possiveis)
            
            for prof in profs_possiveis:
                combinacoes = [(dia, h) for dia in self.dias for h in self.horarios]
                random.shuffle(combinacoes)
                
                for dia, horario in combinacoes:
                    if dia not in prof.disponibilidade:
                        continue
                    
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
                        salas = st.session_state.salas if 'salas' in st.session_state else []
                        sala_nome = salas[0].nome if salas else "Sala 1"
                        aula = Aula(turma_nome, disc_nome, prof.nome, dia, horario, sala_nome)
                        aulas.append(aula)
                        prof_aulas[prof.nome].append(aula)
                        turma_aulas[turma_nome].append(aula)
                        atribuido = True
                        break
                
                if atribuido:
                    break
            
            if not atribuido and profs_possiveis:
                prof = profs_possiveis[0]
                dia = list(prof.disponibilidade)[0] if prof.disponibilidade else "seg"
                horario = self.horarios[0]
                salas = st.session_state.salas if 'salas' in st.session_state else []
                sala_nome = salas[0].nome if salas else "Sala 1"
                aula = Aula(turma_nome, disc_nome, prof.nome, dia, horario, sala_nome)
                aulas.append(aula)
        
        return aulas