"""
Verifica se o FII HGRE11.SA está salvo no banco para hcarqueja
"""
import sqlite3
import json

conn = sqlite3.connect('data/robo_investimentos.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("="*80)
print("VERIFICANDO CARTEIRA DE HCARQUEJA NO BANCO SQLITE")
print("="*80)

# Busca a última carteira de hcarqueja
cursor.execute('''
    SELECT id, username, br_fiis, us_stocks, asset_quantities, updated_at 
    FROM portfolios 
    WHERE username = ? 
    ORDER BY id DESC 
    LIMIT 1
''', ('hcarqueja',))

row = cursor.fetchone()

if row:
    print(f"\n✅ Carteira encontrada!")
    print(f"   ID: {row['id']}")
    print(f"   Usuário: {row['username']}")
    print(f"   Atualizado em: {row['updated_at']}")
    
    if row['br_fiis']:
        fiis = json.loads(row['br_fiis'])
        print(f"\n📊 FIIs cadastrados ({len(fiis)}):")
        for fii in fiis:
            print(f"   • {fii}")
        
        if 'HGRE11.SA' in fiis:
            print(f"\n✅ HGRE11.SA ESTÁ na lista!")
        else:
            print(f"\n❌ HGRE11.SA NÃO está na lista")
    else:
        print(f"\n⚠️ Lista de FIIs está vazia")
    
    if row['us_stocks']:
        stocks = json.loads(row['us_stocks'])
        print(f"\n📈 Ações US cadastradas ({len(stocks)}):")
        for stock in stocks:
            print(f"   • {stock}")
    
    if row['asset_quantities']:
        quantities = json.loads(row['asset_quantities'])
        print(f"\n🔢 Quantidades cadastradas ({len(quantities)}):")
        for ticker, qty in quantities.items():
            print(f"   • {ticker}: {qty}")
else:
    print(f"\n❌ NENHUMA carteira encontrada para 'hcarqueja'")
    print(f"\n💡 Isso significa que:")
    print(f"   • O salvamento pela interface NÃO funcionou")
    print(f"   • OU você ainda não clicou em 'Salvar' após adicionar o FII")

conn.close()

print("\n" + "="*80)
