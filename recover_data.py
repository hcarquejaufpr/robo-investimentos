"""
Script de Recuperação de Dados
Mostra histórico de salvamentos para recuperar quantidades perdidas
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = 'data/robo_investimentos.db'

def show_portfolio_history(username='admin'):
    """Mostra histórico de todos os salvamentos de carteira."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Busca todos os registros (não apenas o último)
    cursor.execute('''
        SELECT id, username, asset_quantities, updated_at 
        FROM portfolios 
        WHERE username = ?
        ORDER BY id DESC
        LIMIT 50
    ''', (username,))
    
    rows = cursor.fetchall()
    
    print(f"\n{'='*80}")
    print(f"HISTÓRICO DE CARTEIRAS - Usuário: {username}")
    print(f"{'='*80}\n")
    
    for i, row in enumerate(rows, 1):
        print(f"\n{'-'*80}")
        print(f"Registro #{row['id']} - {row['updated_at']}")
        print(f"{'-'*80}")
        
        if row['asset_quantities']:
            try:
                quantities = json.loads(row['asset_quantities'])
                if quantities:
                    print("\nQuantidades cadastradas:")
                    for ticker, data in quantities.items():
                        if isinstance(data, dict):
                            qty = data.get('quantidade', 0)
                            price = data.get('preco_entrada', 0)
                            print(f"  {ticker:10} - Qtd: {qty:>12.6f}  |  Preço Entrada: ${price:.2f}")
                        else:
                            print(f"  {ticker:10} - Qtd: {data:>12.6f}")
                else:
                    print("  (nenhuma quantidade cadastrada)")
            except json.JSONDecodeError:
                print("  (erro ao ler dados)")
        else:
            print("  (nenhuma quantidade cadastrada)")
    
    conn.close()
    
    print(f"\n{'='*80}\n")
    print("INSTRUÇÕES PARA RECUPERAR:")
    print("1. Identifique o registro com suas quantidades corretas")
    print("2. Anote o ID do registro")
    print("3. Execute: python recover_data.py restore <ID>")
    print(f"{'='*80}\n")

def restore_portfolio(record_id, username='admin'):
    """Restaura uma carteira específica como a atual."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Busca o registro antigo
    cursor.execute('''
        SELECT us_stocks, br_fiis, tesouro_direto, asset_quantities, 
               parametros, individual_multipliers, operations_history, portfolio_snapshots
        FROM portfolios 
        WHERE id = ? AND username = ?
    ''', (record_id, username))
    
    row = cursor.fetchone()
    
    if not row:
        print(f"❌ Registro {record_id} não encontrado!")
        return
    
    # Cria novo registro (cópia do antigo)
    cursor.execute('''
        INSERT INTO portfolios 
        (username, us_stocks, br_fiis, tesouro_direto, asset_quantities, 
         parametros, individual_multipliers, operations_history, portfolio_snapshots, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], datetime.now()))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Carteira do registro #{record_id} restaurada com sucesso!")
    print("⚠️ Recarregue a página do Streamlit para ver as mudanças")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'restore':
        if len(sys.argv) > 2:
            record_id = int(sys.argv[2])
            restore_portfolio(record_id)
        else:
            print("❌ Uso: python recover_data.py restore <ID>")
    else:
        show_portfolio_history()
