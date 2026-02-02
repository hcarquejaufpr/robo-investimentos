"""
Diagnóstico completo do banco de dados
"""

import sqlite3
import json

DB_PATH = 'data/robo_investimentos.db'

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Lista TODOS os registros
cursor.execute('SELECT * FROM portfolios ORDER BY id')
rows = cursor.fetchall()

print(f"\n{'='*100}")
print(f"TODOS OS REGISTROS NO BANCO - Total: {len(rows)}")
print(f"{'='*100}\n")

for row in rows:
    print(f"\n{'='*100}")
    print(f"ID: {row['id']} | Username: {row['username']} | Updated: {row['updated_at']}")
    print(f"{'='*100}")
    
    print("\n📊 ASSET_QUANTITIES:")
    if row['asset_quantities']:
        qty = json.loads(row['asset_quantities'])
        if qty:
            for ticker, data in qty.items():
                print(f"  {ticker}: {data}")
        else:
            print("  VAZIO")
    else:
        print("  NULL")
    
    print("\n🇺🇸 US_STOCKS:")
    if row['us_stocks']:
        stocks = json.loads(row['us_stocks'])
        print(f"  {stocks}")
    else:
        print("  NULL")
    
    print("\n🇧🇷 BR_FIIS:")
    if row['br_fiis']:
        fiis = json.loads(row['br_fiis'])
        print(f"  {fiis}")
    else:
        print("  NULL")

conn.close()
