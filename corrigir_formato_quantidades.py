"""
Corrige o formato das quantidades no banco de dados
"""
import database as db
import yfinance as yf
from datetime import datetime

print("="*80)
print("🔧 CORRIGINDO FORMATO DAS QUANTIDADES")
print("="*80)

username = 'hcarqueja'

# Carrega carteira
portfolio = db.load_user_portfolio(username)

if portfolio:
    print(f"\n✅ Carteira encontrada")
    
    quantities = portfolio.get('ASSET_QUANTITIES', {})
    print(f"\n📊 Formato atual: {quantities}")
    
    # Corrige formato
    new_quantities = {}
    updated = False
    
    for ticker, value in quantities.items():
        if isinstance(value, (int, float)):
            # Valor simples - precisa converter para dict
            print(f"\n🔧 Corrigindo {ticker}: {value} → dict")
            
            # Busca preço atual
            preco_entrada = None
            try:
                print(f"   Buscando preço de {ticker}...")
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1d")
                if not hist.empty:
                    preco_entrada = float(hist['Close'].iloc[-1])
                    print(f"   ✅ Preço: R$ {preco_entrada:.2f}")
            except Exception as e:
                print(f"   ⚠️ Não foi possível buscar preço: {e}")
                preco_entrada = 0.0
            
            new_quantities[ticker] = {
                'quantidade': float(value),
                'preco_entrada': preco_entrada,
                'data_entrada': datetime.now().strftime("%Y-%m-%d")
            }
            updated = True
        elif isinstance(value, dict):
            # Já está no formato correto
            print(f"\n✅ {ticker} já está no formato correto")
            new_quantities[ticker] = value
        else:
            print(f"\n⚠️ {ticker} tem formato desconhecido: {type(value)}")
            new_quantities[ticker] = value
    
    if updated:
        print(f"\n💾 Salvando formato corrigido...")
        portfolio['ASSET_QUANTITIES'] = new_quantities
        success = db.save_user_portfolio(username, portfolio)
        
        if success:
            print(f"\n✅ Formato corrigido e salvo com sucesso!")
            print(f"\n📊 Novo formato:")
            for ticker, data in new_quantities.items():
                print(f"   {ticker}:")
                if isinstance(data, dict):
                    print(f"      quantidade: {data.get('quantidade', 0)}")
                    print(f"      preco_entrada: {data.get('preco_entrada', 0)}")
                    print(f"      data_entrada: {data.get('data_entrada', 'N/A')}")
                else:
                    print(f"      {data}")
            
            print(f"\n🎉 AGORA REINICIE O STREAMLIT:")
            print(f"   1. Ctrl+C para parar")
            print(f"   2. streamlit run main.py")
            print(f"   3. Login com hcarqueja")
            print(f"   4. A quantidade deve aparecer corretamente!")
        else:
            print(f"\n❌ Erro ao salvar")
    else:
        print(f"\n✅ Todos os dados já estão no formato correto")

else:
    print(f"\n❌ Carteira não encontrada")

print("\n" + "="*80)
