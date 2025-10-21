# Arquivo completo unificado - Execute este arquivo
print("Unindo arquivos...")

# Ler todos os arquivos
with open('app_part1.py', 'r', encoding='utf-8') as f1:
    part1 = f1.read()

with open('app_part2.py', 'r', encoding='utf-8') as f2:
    part2 = f2.read()

with open('app_part3.py', 'r', encoding='utf-8') as f3:
    part3 = f3.read()

with open('app_part4.py', 'r', encoding='utf-8') as f4:
    part4 = f4.read()

# Combinar os arquivos
codigo_completo = part1 + "\n" + part2 + "\n" + part3 + "\n" + part4

# Salvar arquivo completo
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(codigo_completo)

print("✅ Arquivo app.py criado com sucesso!")
print("🎯 Execute: streamlit run app.py")