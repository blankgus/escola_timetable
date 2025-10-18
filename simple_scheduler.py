import random
from models import Aula

class SimpleGradeHoraria:
    def __init__(self, turmas, professores, disciplinas):
        self.turmas = turmas
        self.professores = professores
        self.disciplinas = disciplinas
        self.aulas_alocadas = []
        
    def obter_grupo_seguro(self, objeto):
        try:
            if hasattr(objeto, 'grupo'):
                grupo = objeto.grupo
                if grupo in ["A", "B", "AMBOS"]:
                    return grupo
            return "A"
        except:
            return "A"
    
    def gerar_grade(self):
        """Gera uma grade horária semanal tradicional"""
        self.aulas_alocadas = []
        
        # Dias da semana (segunda a sexta)
        dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
        # Horários disponíveis (apenas manhã - 7 horários)
        horarios = [1, 2, 3, 4, 5, 6, 7]
        
        st.info(f"📋 Gerando grade semanal para {len(self.turmas)} turmas...")
        
        progress_bar = st.progress(0)
        
        # Para cada turma, criar grade semanal
        for idx, turma in enumerate(self.turmas):
            grupo_turma = self.obter_grupo_seguro(turma)
            
            # CORREÇÃO CRÍTICA: Filtrar disciplinas APENAS do MESMO GRUPO
            disciplinas_turma = []
            for disc in self.disciplinas:
                disc_grupo = self.obter_grupo_seguro(disc)
                # SÓ inclui disciplinas do MESMO grupo
                if turma.serie in disc.series and disc_grupo == grupo_turma:
                    # Adiciona a disciplina repetidas vezes conforme carga semanal
                    for _ in range(disc.carga_semanal):
                        disciplinas_turma.append(disc)
            
            if not disciplinas_turma:
                st.warning(f"⚠️ Turma {turma.nome} [{grupo_turma}] não tem disciplinas do seu grupo")
                continue
            
            # Embaralhar disciplinas para distribuição
            random.shuffle(disciplinas_turma)
            
            # Alocar aulas para esta turma
            aulas_turma = self._alocar_turma_semanal(turma, disciplinas_turma, dias, horarios, grupo_turma)
            self.aulas_alocadas.extend(aulas_turma)
            
            progress_bar.progress((idx + 1) / len(self.turmas))
        
        st.success(f"✅ Grade gerada com {len(self.aulas_alocadas)} aulas!")
        return self.aulas_alocadas
    
    def _alocar_turma_semanal(self, turma, disciplinas_turma, dias, horarios, grupo_turma):
        """Aloca aulas para uma turma na semana toda"""
        aulas_turma = []
        disciplinas_restantes = disciplinas_turma.copy()
        
        # Tentar alocar em cada dia e horário
        for dia in dias:
            for horario in horarios:
                if not disciplinas_restantes:
                    break
                
                # Pegar próxima disciplina
                disciplina = disciplinas_restantes[0]
                
                # VERIFICAÇÃO DE SEGURANÇA: garantir que é do mesmo grupo
                disc_grupo = self.obter_grupo_seguro(disciplina)
                if disc_grupo != grupo_turma:
                    st.error(f"❌ ERRO CRÍTICO: Disciplina {disciplina.nome} [{disc_grupo}] para turma {turma.nome} [{grupo_turma}]")
                    disciplinas_restantes.pop(0)
                    continue
                
                # Encontrar professor compatível
                professor = self._encontrar_professor_compativel(disciplina.nome, dia, horario, grupo_turma)
                
                if professor:
                    sala = self._encontrar_sala_disponivel(dia, horario)
                    
                    aula = Aula(
                        turma=turma.nome,
                        disciplina=disciplina.nome,
                        professor=professor.nome,
                        dia=dia,
                        horario=horario,
                        sala=sala,
                        grupo=grupo_turma
                    )
                    
                    aulas_turma.append(aula)
                    disciplinas_restantes.pop(0)
        
        return aulas_turma
    
    def _encontrar_professor_compativel(self, disciplina_nome, dia, horario, grupo_turma):
        """Encontra professor que atende TODOS os critérios"""
        professores_candidatos = []
        
        for professor in self.professores:
            professor_grupo = self.obter_grupo_seguro(professor)
            
            # CRITÉRIOS DE COMPATIBILIDADE:
            # 1. Professor deve ministrar a disciplina
            # 2. Professor deve estar disponível no dia
            # 3. Professor não pode ter horário indisponível
            # 4. Professor deve ser do MESMO grupo ou AMBOS
           