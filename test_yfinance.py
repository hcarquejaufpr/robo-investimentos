"""Script de teste para verificar yfinance"""
import yfinance as yf

print("Testando conexão com yfinance...")
print("-" * 50)

tickers = ['AAPL', 'NVDA']

for ticker in tickers:
    print(f"\nTestando {ticker}...")
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="5d")
        
        if df.empty:
            print(f"  ❌ {ticker}: DataFrame vazio")
        else:
            print(f"  ✅ {ticker}: {len(df)} dias de dados")
            print(f"  Último preço: ${df['Close'].iloc[-1]:.2f}")
            print(f"  Colunas: {list(df.columns)}")
    except Exception as e:
        print(f"  ❌ Erro: {e}")

print("\n" + "-" * 50)
print("Teste concluído!")
