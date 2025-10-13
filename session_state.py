import streamlit as st
from models import Turma, Professor, Disciplina, Sala, DisciplinaTurma
import database
import pandas as pd
import io

def init_session_state():
    database.init_db()
    
    # === TURMAS ===
    if "turmas" not in st.session_state:
        st.session_state.turmas = database.carregar_turmas() or [
            Turma("6anoA", "6ano", "manha", [
                DisciplinaTurma("Matemática", 4, "Ana A"),
                DisciplinaTurma("Português", 4, "Bruno A"),
            ]),
            Turma("6anoB", "6ano", "manha", [
                DisciplinaTurma("Matemática", 4, "Ana B"),
                DisciplinaTurma("Português", 4, "Bruno B"),
            ]),
            # Adicione mais turmas A e B conforme necessário
        ]
    
    # === PROFESSORES ===
    if "professores" not in st.session_state:
        st.session_state.professores = database.carregar_professores() or [
            Professor("Ana A", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
            Professor("Ana B", ["Matemática"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
            Professor("Bruno A", ["Português"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
            Professor("Bruno B", ["Português"], {"seg", "ter", "qua", "qui", "sex"}, {1,2,3,5,6,7}),
            # Adicione mais professores conforme necessário
        ]
    
    # === DISCIPLINAS TEMPLATE ===
    if "disciplinas" not in st.session_state:
        st.session_state.disciplinas = database.carregar_disciplinas() or [
            Disciplina("Matemática", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#4A90E2", "#FFFFFF"),
            Disciplina("Português", 4, "pesada", ["6ano", "7ano", "8ano", "9ano"], "#D35400", "#FFFFFF"),
            # Adicione mais disciplinas conforme necessário
        ]
    
    # === SALAS ===
    if "salas" not in st.session_state:
        st.session_state.salas = database.carregar_salas() or [
            Sala("Sala 1", 30, "normal"),
            Sala("Sala 2", 30, "normal"),
            # Adicione mais salas conforme necessário
        ]

def importar_de_excel(uploaded_file):
    """Importa turmas, professores e disciplinas de um arquivo Excel."""
    try:
        # Ler abas do Excel
        turmas_df = pd.read_excel(uploaded_file, sheet_name="turmas")
        profs_df = pd.read_excel(uploaded_file, sheet_name="professores")
        discs_df = pd.read_excel(uploaded_file, sheet_name="disciplinas")

        # Converter para objetos
        turmas = []
        for _, row in turmas_df.iterrows():
            # Converter string de disciplinas para lista de DisciplinaTurma
            discs_str = row.get("disciplinas_turma", "[]")
            discs_data = eval(discs_str) if isinstance(discs_str, str) else []
            discs_turma = [DisciplinaTurma(**d) for d in discs_data]
            turmas.append(Turma(
                nome=row["nome"],
                serie=row["serie"],
                turno=row["turno"],
                disciplinas_turma=discs_turma,
                id=str(row.get("id", str(uuid.uuid4())))
            ))

        professores = []
        for _, row in profs_df.iterrows():
            professores.append(Professor(
                nome=row["nome"],
                disciplinas=eval(row["disciplinas"]),
                disponibilidade_dias=set(eval(row["disponibilidade_dias"])),
                disponibilidade_horarios=set(eval(row["disponibilidade_horarios"])),
                restricoes=set(eval(row.get("restricoes", "set()"))),
                id=str(row.get("id", str(uuid.uuid4())))
            ))

        disciplinas = []
        for _, row in discs_df.iterrows():
            disciplinas.append(Disciplina(
                nome=row["nome"],
                carga_semanal=row["carga_semanal"],
                tipo=row["tipo"],
                series=eval(row["series"]),
                cor_fundo=row["cor_fundo"],
                cor_fonte=row["cor_fonte"],
                id=str(row.get("id", str(uuid.uuid4())))
            ))

        # Atualizar session_state
        st.session_state.turmas = turmas
        st.session_state.professores = professores
        st.session_state.disciplinas = disciplinas
        st.success("✅ Dados importados com sucesso!")
        return True
    except Exception as e:
        st.error(f"❌ Erro ao importar: {str(e)}")
        return False

def exportar_para_excel_template():
    """Gera um template Excel para importação."""
    # Template de turmas
    turmas_template = pd.DataFrame([{
        "nome": "6anoA",
        "serie": "6ano",
        "turno": "manha",
        "disciplinas_turma": "[{'nome': 'Matemática', 'carga_semanal': 4, 'professor': 'Ana A'}]"
    }])

    # Template de professores
    profs_template = pd.DataFrame([{
        "nome": "Ana A",
        "disciplinas": "['Matemática']",
        "disponibilidade_dias": "{'seg', 'ter', 'qua', 'qui', 'sex'}",
        "disponibilidade_horarios": "{1, 2, 3, 5, 6, 7}",
        "restricoes": "set()"
    }])

    # Template de disciplinas
    discs_template = pd.DataFrame([{
        "nome": "Matemática",
        "carga_semanal": 4,
        "tipo": "pesada",
        "series": "['6ano', '7ano', '8ano', '9ano']",
        "cor_fundo": "#4A90E2",
        "cor_fonte": "#FFFFFF"
    }])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        turmas_template.to_excel(writer, sheet_name="turmas", index=False)
        profs_template.to_excel(writer, sheet_name="professores", index=False)
        discs_template.to_excel(writer, sheet_name="disciplinas", index=False)
    return output.getvalue()