# NO database.py, atualize a função criar_dados_iniciais():

def criar_dados_iniciais():
    """Cria dados iniciais para teste"""
    
    # ✅ CORREÇÃO: Professores com nomes EXATOS das disciplinas e grupo AMBOS
    professores = [
        Professor("Heliana", ["Português A", "Português B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Deise", ["Português A", "Português B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Loide", ["Português A", "Português B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Tatiane", ["Matemática A", "Matemática B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Ricardo", ["Matemática A", "Matemática B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Laís", ["História A", "História B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Waldemar", ["História A", "História B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Rene", ["Geografia A", "Geografia B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Vladmir", ["Química A", "Química B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Zabuor", ["Química A", "Química B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Gisele", ["Geografia A", "Geografia B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Marina", ["Biologia A", "Biologia B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("César", ["Informática A", "Informática B", "Física A", "Física B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Anna Maria", ["Filosofia A", "Filosofia B", "Sociologia A", "Sociologia B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Marcão", ["Educação Física A", "Educação Física B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Andréia", ["Educação Física A", "Educação Física B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Vanessa", ["Arte A", "Arte B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
        Professor("Andréia Barreto", ["Dinâmica A", "Dinâmica B", "Vida Pratica A", "Vida Pratica B"], {"segunda", "terca", "quarta", "quinta", "sexta"}, "AMBOS"),
    ]
    
    # ✅ CORREÇÃO: Turmas com segmento correto
    turmas = [
        Turma("6anoA", "6ano", "manha", "A", "EF_II"),
        Turma("7anoA", "7ano", "manha", "A", "EF_II"),
        Turma("8anoA", "8ano", "manha", "A", "EF_II"),
        Turma("9anoA", "9ano", "manha", "A", "EF_II"),
        Turma("1emA", "1em", "manha", "A", "EM"),
        Turma("2emA", "2em", "manha", "A", "EM"),
        Turma("3emA", "3em", "manha", "A", "EM"),
        Turma("6anoB", "6ano", "manha", "B", "EF_II"),
        Turma("7anoB", "7ano", "manha", "B", "EF_II"),
        Turma("8anoB", "8ano", "manha", "B", "EF_II"),
        Turma("9anoB", "9ano", "manha", "B", "EF_II"),
        Turma("1emB", "1em", "manha", "B", "EM"),
        Turma("2emB", "2em", "manha", "B", "EM"),
        Turma("3emB", "3em", "manha", "B", "EM"),
    ]
    
    # ✅ CORREÇÃO: Disciplinas vinculadas às turmas específicas
    disciplinas = [
        # GRUPO A - TURMAS A
        Disciplina("Português A", 5, "pesada", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"], "A"),
        Disciplina("Matemática A", 5, "pesada", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"], "A"),
        Disciplina("História A", 2, "media", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"], "A"),
        Disciplina("Geografia A", 2, "media", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"], "A"),
        Disciplina("Ciências A", 2, "media", ["6anoA", "7anoA", "8anoA", "9anoA"], "A"),
        Disciplina("Biologia A", 2, "media", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Física A", 2, "pesada", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Química A", 2, "pesada", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Inglês A", 2, "leve", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"], "A"),
        Disciplina("Arte A", 2, "leve", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"], "A"),
        Disciplina("Educação Física A", 2, "pratica", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"], "A"),
        Disciplina("Filosofia A", 2, "media", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Sociologia A", 2, "media", ["1emA", "2emA", "3emA"], "A"),
        Disciplina("Informática A", 2, "leve", ["6anoA", "7anoA", "8anoA", "9anoA", "1emA", "2emA", "3emA"], "A"),
        Disciplina("Dinâmica A", 1, "leve", ["6anoA", "7anoA", "8anoA", "9anoA"], "A"),
        Disciplina("Vida Pratica A", 1, "leve", ["6anoA", "7anoA", "8anoA", "9anoA"], "A"),
        
        # GRUPO B - TURMAS B
        Disciplina("Português B", 5, "pesada", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"], "B"),
        Disciplina("Matemática B", 5, "pesada", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"], "B"),
        Disciplina("História B", 2, "media", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"], "B"),
        Disciplina("Geografia B", 2, "media", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"], "B"),
        Disciplina("Ciências B", 2, "media", ["6anoB", "7anoB", "8anoB", "9anoB"], "B"),
        Disciplina("Biologia B", 2, "media", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Física B", 2, "pesada", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Química B", 2, "pesada", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Inglês B", 2, "leve", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"], "B"),
        Disciplina("Arte B", 2, "leve", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"], "B"),
        Disciplina("Educação Física B", 3, "pratica", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"], "B"),
        Disciplina("Filosofia B", 2, "media", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Sociologia B", 2, "media", ["1emB", "2emB", "3emB"], "B"),
        Disciplina("Informática B", 2, "leve", ["6anoB", "7anoB", "8anoB", "9anoB", "1emB", "2emB", "3emB"], "B"),
        Disciplina("Dinâmica B", 1, "leve", ["6anoB", "7anoB", "8anoB", "9anoB"], "B"),
        Disciplina("Vida Pratica B", 1, "leve", ["6anoB", "7anoB", "8anoB", "9anoB"], "B"),
    ]
    
    # ... resto do código igual
