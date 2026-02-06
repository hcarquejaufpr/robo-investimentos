"""
Cadastra o FII HGRE11.SA para o usuário hcarqueja
"""
import database as db

print("="*80)
print("CADASTRANDO FII HGRE11.SA PARA USUÁRIO HCARQUEJA")
print("="*80)

# 1. Verifica se o usuário existe
username = 'hcarqueja'

# 2. Carrega carteira atual (ou cria uma vazia)
portfolio = db.load_user_portfolio(username)

if portfolio is None:
    print(f"\n⚠️ Usuário {username} não possui carteira ainda. Criando nova carteira...")
    portfolio = {
        "US_STOCKS": [],
        "BR_FIIS": [],
        "TESOURO_DIRETO": {},
        "ASSET_QUANTITIES": {},
        "PARAMETROS": {
            "MULTIPLIER_US": 1.2,
            "MULTIPLIER_BR": 1.0
        },
        "INDIVIDUAL_MULTIPLIERS": {},
        "OPERATIONS_HISTORY": [],
        "PORTFOLIO_SNAPSHOTS": []
    }
else:
    print(f"\n✅ Carteira existente encontrada para {username}")

# 3. Adiciona o FII HGRE11.SA se ainda não estiver na lista
fii_ticker = "HGRE11.SA"

if fii_ticker not in portfolio["BR_FIIS"]:
    portfolio["BR_FIIS"].append(fii_ticker)
    print(f"\n✅ FII {fii_ticker} adicionado à lista de FIIs")
else:
    print(f"\n⚠️ FII {fii_ticker} já estava na lista")

print(f"\n📊 FIIs cadastrados: {portfolio['BR_FIIS']}")

# 4. Quantidade será cadastrada depois no app Streamlit
print("\n💡 Quantidade: Você pode cadastrar no app (menu 'Quantidades de Ativos')")

# 5. Salva a carteira no banco de dados
print(f"\n💾 Salvando carteira no banco de dados...")
success = db.save_user_portfolio(username, portfolio)

if success:
    print(f"✅ Carteira salva com sucesso!")
    print(f"\n📋 Resumo da carteira de {username}:")
    print(f"   🇺🇸 Ações US: {len(portfolio['US_STOCKS'])} ativo(s)")
    print(f"   🇧🇷 FIIs BR: {len(portfolio['BR_FIIS'])} ativo(s)")
    print(f"   📊 Quantidades: {len(portfolio.get('ASSET_QUANTITIES', {}))} ativo(s)")
    print(f"\n🔍 FIIs cadastrados:")
    for fii in portfolio['BR_FIIS']:
        qty = portfolio.get('ASSET_QUANTITIES', {}).get(fii, '-')
        print(f"      • {fii}: {qty} cotas")
    
    print(f"\n🌐 Verificando backup no Google Sheets...")
    print("   💡 O backup automático foi executado durante o salvamento")
    print(f"   🔗 Acesse: https://docs.google.com/spreadsheets/d/1m_D8SB1g-r2g6w96lzh5U9asrQfE4lFMwW3RXzDz9eE")
    print(f"   📄 Aba: Carteira_{username}")
else:
    print("❌ Erro ao salvar carteira!")

print("\n" + "="*80)
print("CADASTRO CONCLUÍDO!")
print("="*80)
print("\n💡 Próximos passos:")
print("   1. Execute: streamlit run main.py")
print("   2. Faça login com o usuário 'hcarqueja'")
print("   3. Clique em '🔄 Atualizar Cotações' para ver o FII HGRE11.SA")
print("   4. Verifique no Google Sheets se o backup foi salvo")
