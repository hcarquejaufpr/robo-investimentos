import database as db

# Inicializa banco
db.init_database()

# Carrega usuários
users = db.load_users()

print("\n" + "="*60)
print("USUÁRIOS CADASTRADOS NO BANCO")
print("="*60)

if 'hcarqueja' in users:
    print("\n✅ Usuário 'hcarqueja' ENCONTRADO:")
    print(f"   Nome: {users['hcarqueja']['name']}")
    print(f"   Email: {users['hcarqueja']['email']}")
    print(f"   Senha: {users['hcarqueja']['password']}")
else:
    print("\n❌ Usuário 'hcarqueja' NÃO ENCONTRADO no banco local")

print("\n📋 Todos os usuários cadastrados:")
for username in users.keys():
    print(f"   - {username} ({users[username]['name']})")

print("\n" + "="*60)

# Verifica carteira
if 'hcarqueja' in users:
    portfolio = db.load_user_portfolio('hcarqueja')
    if portfolio:
        print("\n💼 Carteira encontrada para hcarqueja:")
        print(f"   Ações US: {portfolio.get('US_STOCKS', [])}")
        print(f"   FIIs BR: {portfolio.get('BR_FIIS', [])}")
        print(f"   Tesouro: {list(portfolio.get('TESOURO_DIRETO', {}).keys())}")
        print(f"   Quantidades: {portfolio.get('ASSET_QUANTITIES', {})}")
    else:
        print("\n⚠️ Nenhuma carteira encontrada para hcarqueja")
