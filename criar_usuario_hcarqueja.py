"""
Script para criar/recuperar o usuário hcarqueja
"""
import database as db

print("\n" + "="*70)
print("CRIANDO USUÁRIO HCARQUEJA")
print("="*70)

# Inicializa banco
db.init_database()

# Dados do usuário
username = "hcarqueja"
password = input("\nDigite a senha para o usuário hcarqueja: ")
name = input("Digite o nome completo: ")
email = input("Digite o email: ")

# Verifica se já existe
if db.user_exists(username):
    print(f"\n⚠️ Usuário '{username}' já existe no banco!")
    resposta = input("Deseja atualizar os dados? (s/n): ")
    
    if resposta.lower() == 's':
        # Atualiza via SQL direto
        from database import get_db_connection
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET password = ?, name = ?, email = ? WHERE username = ?',
                (password, name, email, username)
            )
            conn.commit()
        print(f"✅ Usuário '{username}' atualizado com sucesso!")
else:
    # Cria novo usuário
    db.save_user(username, password, name, email)
    print(f"\n✅ Usuário '{username}' criado com sucesso!")

print("\n" + "="*70)
print("USUÁRIO CRIADO/ATUALIZADO")
print("="*70)
print(f"Usuário: {username}")
print(f"Nome: {name}")
print(f"Email: {email}")
print(f"Senha: {'*' * len(password)}")
print("="*70)

# Faz backup
print("\n📦 Fazendo backup dos usuários...")
if db.backup_users():
    print("✅ Backup criado com sucesso!")
else:
    print("❌ Erro ao criar backup")

print("\n💡 Agora você pode fazer login no sistema com estas credenciais.")
print("   No Streamlit Cloud, será necessário fazer o upload do arquivo")
print("   'data/users_backup.json' para restaurar os usuários.\n")
