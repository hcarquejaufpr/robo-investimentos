"""
Força o recarregamento dos dados na interface Streamlit
"""

print("="*80)
print("🔄 RECARREGANDO DADOS NA INTERFACE STREAMLIT")
print("="*80)

print("""
A quantidade está salva no banco, mas a interface usa CACHE para otimização.

📋 SOLUÇÕES PARA VER A QUANTIDADE NA INTERFACE:

OPÇÃO 1 - Limpar Cache pelo Streamlit (RECOMENDADO):
   1. Abra o Streamlit (streamlit run main.py)
   2. Na barra lateral, clique no botão "🔄 Atualizar Cotações"
   3. Isso limpa o cache e recarrega todos os dados
   4. A quantidade 83 deve aparecer

OPÇÃO 2 - Fechar e Reabrir o Streamlit:
   1. Pressione Ctrl+C no terminal do Streamlit
   2. Execute novamente: streamlit run main.py
   3. Faça login com 'hcarqueja'
   4. A quantidade deve aparecer

OPÇÃO 3 - Limpar Cache Manualmente (pelo menu):
   1. No Streamlit, pressione 'C' no teclado
   2. Ou clique nos 3 pontinhos (⋮) no canto superior direito
   3. Selecione "Clear cache"
   4. Recarregue a página (F5)

OPÇÃO 4 - Forçar Rerun via código (automático):
   O botão "🔄 Atualizar Cotações" já faz isso:
   - st.cache_data.clear()
   - st.rerun()

═══════════════════════════════════════════════════════════════════════════

🔍 VERIFICANDO SE OS DADOS ESTÃO CORRETOS NO BANCO:
""")

import database as db

username = 'hcarqueja'
portfolio = db.load_user_portfolio(username)

if portfolio:
    print(f"\n✅ Dados no banco SQLite:")
    print(f"   FIIs: {portfolio.get('BR_FIIS', [])}")
    
    quantities = portfolio.get('ASSET_QUANTITIES', {})
    if quantities:
        print(f"   Quantidades:")
        for ticker, qty in quantities.items():
            if isinstance(qty, dict):
                print(f"      • {ticker}: {qty.get('quantidade', 0)} cotas")
            else:
                print(f"      • {ticker}: {qty} cotas")
    
    print(f"\n✅ Os dados ESTÃO no banco!")
    print(f"   O Streamlit só precisa recarregar o cache.")

print("""

═══════════════════════════════════════════════════════════════════════════

💡 INSTRUÇÕES PASSO A PASSO:

1. Se o Streamlit já está aberto:
   → Na barra lateral, clique em "🔄 Atualizar Cotações"
   
2. Se não está aberto:
   → Execute: streamlit run main.py
   → Faça login com 'hcarqueja'
   → Clique em "🔄 Atualizar Cotações"

3. Depois disso, você verá:
   📊 Seção "🇧🇷 FIIs Brasileiros"
   ├─ HGRE11.SA
   ├─ Quantidade: 83 cotas
   ├─ Preço atual: R$ XX,XX
   └─ Valor total: R$ X.XXX,XX

═══════════════════════════════════════════════════════════════════════════
""")

print("✅ Siga as instruções acima para ver a quantidade na interface!")
print("="*80)
