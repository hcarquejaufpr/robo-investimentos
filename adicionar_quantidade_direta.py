"""
Adiciona quantidade diretamente ao FII HGRE11.SA (sem input interativo)
"""
import database as db

print("="*80)
print("ADICIONANDO QUANTIDADE DIRETA DO FII HGRE11.SA")
print("="*80)

username = 'hcarqueja'
fii_ticker = 'HGRE11.SA'
quantidade = 83  # Quantidade informada pelo usuário

print(f"\n📊 Configuração:")
print(f"   Usuário: {username}")
print(f"   Ticker: {fii_ticker}")
print(f"   Quantidade: {quantidade} cotas")

# Carrega carteira atual
portfolio = db.load_user_portfolio(username)

if portfolio is None:
    print(f"\n❌ Usuário {username} não tem carteira cadastrada!")
else:
    print(f"\n✅ Carteira encontrada!")
    
    # Inicializa ASSET_QUANTITIES se não existir
    if 'ASSET_QUANTITIES' not in portfolio:
        portfolio['ASSET_QUANTITIES'] = {}
    
    # Adiciona a quantidade
    portfolio['ASSET_QUANTITIES'][fii_ticker] = quantidade
    
    print(f"\n💾 Salvando no banco de dados...")
    success = db.save_user_portfolio(username, portfolio)
    
    if success:
        print(f"\n✅ Quantidade salva com sucesso!")
        print(f"   {fii_ticker}: {quantidade} cotas")
        
        # Verifica se realmente salvou
        portfolio_verificado = db.load_user_portfolio(username)
        if portfolio_verificado and fii_ticker in portfolio_verificado.get('ASSET_QUANTITIES', {}):
            qtd_salva = portfolio_verificado['ASSET_QUANTITIES'][fii_ticker]
            print(f"\n✅ VERIFICAÇÃO: Quantidade confirmada no banco = {qtd_salva}")
        else:
            print(f"\n❌ ERRO: Quantidade NÃO foi salva no banco!")
        
        print(f"\n🌐 Backup automático executado no Google Sheets!")
        print(f"   🔗 Acesse: https://docs.google.com/spreadsheets/d/1m_D8SB1g-r2g6w96lzh5U9asrQfE4lFMwW3RXzDz9eE")
        print(f"   📄 Aba: Carteira_{username}")
        
        print(f"\n💡 Agora você pode:")
        print(f"   1. Executar 'python verificar_hcarqueja.py' para confirmar")
        print(f"   2. Abrir o Streamlit e clicar em '🔄 Atualizar Cotações'")
    else:
        print(f"\n❌ Erro ao salvar!")

print("\n" + "="*80)
print("PROCESSO CONCLUÍDO!")
print("="*80)
