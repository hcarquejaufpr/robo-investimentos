"""
Diagnóstico: Verifica se há problema com case-sensitivity
"""
import database as db

username = 'hcarqueja'
portfolio = db.load_user_portfolio(username)

print("="*80)
print("DIAGNÓSTICO DE SALVAMENTO")
print("="*80)

if portfolio:
    print("\n✅ Carteira encontrada!")
    print(f"\n📊 BR_FIIS cadastrados: {portfolio.get('BR_FIIS', [])}")
    print(f"   Tipo: {type(portfolio.get('BR_FIIS', []))}")
    
    for fii in portfolio.get('BR_FIIS', []):
        print(f"\n   FII: '{fii}'")
        print(f"   Caracteres: {[c for c in fii]}")
        print(f"   repr: {repr(fii)}")
    
    print(f"\n🔢 ASSET_QUANTITIES: {portfolio.get('ASSET_QUANTITIES', {})}")
    print(f"   Tipo: {type(portfolio.get('ASSET_QUANTITIES', {}))}")
    
    quantities = portfolio.get('ASSET_QUANTITIES', {})
    if quantities:
        for ticker, data in quantities.items():
            print(f"\n   Ticker: '{ticker}'")
            print(f"   Data: {data}")
            print(f"   repr ticker: {repr(ticker)}")
    else:
        print("   (vazio)")
    
    print("\n" + "="*80)
    print("INSTRUÇÕES PARA SALVAR PELA INTERFACE:")
    print("="*80)
    print("""
1. Execute: streamlit run main.py
2. Faça login com 'hcarqueja'
3. Na barra lateral, clique em '📊 Quantidades de Ativos'
4. Expanda '🇧🇷 Quantidades Brasil' 
5. Você verá uma tabela com HGRE11.SA
6. Edite a coluna 'Quantidade' (clique na célula e digite o número)
7. Role para baixo na barra lateral
8. Expanda '💾 Salvar Quantidades'
9. IMPORTANTE: Clique no botão '💾 SALVAR QUANTIDADES AGORA'
10. Aguarde a mensagem de sucesso aparecer
11. Clique em '🔄 Atualizar Cotações' para ver os dados atualizados
    """)
    
    print("\n💡 ATENÇÃO:")
    print("   • Apenas EDITAR a tabela NÃO salva")
    print("   • É OBRIGATÓRIO clicar no botão '💾 SALVAR QUANTIDADES AGORA'")
    print("   • O botão fica DENTRO do expander '💾 Salvar Quantidades'")
    
else:
    print("\n❌ Carteira não encontrada!")

print("\n" + "="*80)
