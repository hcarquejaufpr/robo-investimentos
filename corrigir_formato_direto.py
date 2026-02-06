"""
Corrige o formato das quantidades DIRETAMENTE no SQLite (sem backup)
"""
import sqlite3
import json
import yfinance as yf
from datetime import datetime

print("="*80)
print("🔧 CORRIGINDO FORMATO DAS QUANTIDADES (DIRETO NO SQLITE)")
print("="*80)

db_path = "data/robo_investimentos.db"
username = 'hcarqueja'

# Conectar ao banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Buscar carteira
cursor.execute("""
    SELECT id, br_fiis, asset_quantities, updated_at
    FROM portfolios 
    WHERE username = ?
""", (username,))

row = cursor.fetchone()

if row:
    portfolio_id, br_fiis, asset_quantities, updated_at = row
    
    print(f"\n✅ Carteira encontrada")
    print(f"   ID: {portfolio_id}")
    print(f"   Usuário: {username}")
    print(f"   Atualizado: {updated_at}")
    
    # Parse JSON
    quantities = json.loads(asset_quantities) if asset_quantities else {}
    
    print(f"\n📊 Formato atual: {quantities}")
    
    # Corrige formato
    new_quantities = {}
    updated = False
    
    for ticker, value in quantities.items():
        if isinstance(value, (int, float)):
            # Valor simples - precisa converter para dict
            print(f"\n🔧  Corrigindo {ticker}: {value} → dict")
            
            # Busca preço atual
            preco_entrada = 0.0
            try:
                print(f"   Buscando preço de {ticker}...")
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1d")
                if not hist.empty:
                    preco_entrada = float(hist['Close'].iloc[-1])
                    print(f"   ✅ Preço: R$ {preco_entrada:.2f}")
            except Exception as e:
                print(f"   ⚠️ Não foi possível buscar preço, usando 0.0")
            
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
            print(f"\n⚠️  {ticker} tem formato desconhecido: {type(value)}")
            new_quantities[ticker] = value
    
    if updated:
        print(f"\n💾 Salvando formato corrigido DIRETO no SQLite...")
        
        # Atualiza no banco
        cursor.execute("""
            UPDATE portfolios 
            SET asset_quantities = ?,
                updated_at = ?
            WHERE username = ?
        """, (json.dumps(new_quantities), datetime.now().isoformat(), username))
        
        conn.commit()
        
        print(f"\n✅ Formato corrigido e salvo com sucesso!")
        print(f"\n📊 Novo formato:")
        for ticker, data in new_quantities.items():
            print(f"   {ticker}:")
            if isinstance(data, dict):
                print(f"      quantidade: {data.get('quantidade', 0)}")
                print(f"      preco_entrada: R$ {data.get('preco_entrada', 0):.2f}")
                print(f"      data_entrada: {data.get('data_entrada', 'N/A')}")
            else:
                print(f"      {data}")
        
        print(f"\n🎉 AGORA REINICIE O STREAMLIT:")
        print(f"   1. Ctrl+C para parar")
        print(f"   2. streamlit run main.py")
        print(f"   3. Login com hcarqueja")
        print(f"   4. A quantidade deve aparecer corretamente!")
    else:
        print(f"\n✅ Todos os dados já estão no formato correto")

else:
    print(f"\n❌ Carteira não encontrada")

conn.close()
print("\n" + "="*80)
