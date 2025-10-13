# importador.py
import pandas as pd
from models import Professor

def carregar_professores_do_excel(caminho):
    # Ler a aba "Professores" do Excel
    df = pd.read_excel(caminho, sheet_name="Professores")
    
    professores = []
    for _, row in df.iterrows():
        nome = row["nome"]
        # Assume que a coluna "disciplinas" tem os nomes separados por vírgula
        disciplinas_str = row["disciplinas"]
        disciplinas = [d.strip() for d in disciplinas_str.split(",")]
        
        # Criar professor com disponibilidade padrão (todos os dias e horários)
        prof = Professor(
            nome=nome,
            disciplinas=disciplinas,
            disponibilidade_dias={"seg", "ter", "qua", "qui", "sex"},
            disponibilidade_horarios={1, 2, 3, 5, 6, 7}
        )
        professores.append(prof)
    
    return professores