import pandas as pd
from models import Professor

def carregar_professores_do_excel(caminho="prodis.xlsx"):
    try:
        # Listar abas para depuração
        xls = pd.ExcelFile(caminho)
        print("🔍 Abas disponíveis no Excel:", xls.sheet_names)
    except FileNotFoundError:
        print("❌ Arquivo Excel não encontrado!")
        return []
    except Exception as e:
        print(f"❌ Erro ao ler o arquivo: {e}")
        return []

    # Ler a aba "Professores"
    try:
        df = pd.read_excel(caminho, sheet_name="Professores")
        print("✅ Aba 'Professores' encontrada.")
    except ValueError as e:
        print(f"❌ Erro ao ler a aba 'Professores': {e}")
        return []
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return []

    # Verificar se as colunas 'nome' e 'disciplinas' existem
    if "nome" not in df.columns or "disciplinas" not in df.columns:
        print("❌ Colunas 'nome' ou 'disciplinas' não encontradas no Excel.")
        print("Colunas disponíveis:", df.columns.tolist())
        return []

    print(f"✅ Dados lidos: {len(df)} linhas encontradas.")
    print("Prime