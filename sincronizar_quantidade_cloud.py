"""
Script para sincronizar quantidade no Streamlit Cloud via Google Sheets
Execute este script NO STREAMLIT CLOUD para corrigir o formato
"""
import json
import sqlite3
from datetime import datetime

def corrigir_formato_cloud():
    """Corrige o formato das quantidades no banco do Streamlit Cloud"""
    
    print("="*80)
    print("🔧 CORRIGINDO FORMATO NO STREAMLIT CLOUD")
    print("="*80)
    
    # Caminho do banco no Streamlit Cloud (ou local)
    db_path = "data/robo_investimentos.db"
    username = 'hcarqueja'
    
    try:
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
            
            # Parse JSON
            quantities = json.loads(asset_quantities) if asset_quantities else {}
            
            print(f"\n📊 Formato atual: {quantities}")
            
            # Corrige formato
            new_quantities = {}
            updated = False
            
            for ticker, value in quantities.items():
                if isinstance(value, (int, float)):
                    # Valor simples - precisa converter para dict
                    print(f"\n🔧 Corrigindo {ticker}: {value} → dict")
                    
                    new_quantities[ticker] = {
                        'quantidade': float(value),
                        'preco_entrada': 0.0,  # Será atualizado ao clicar "Atualizar Cotações"
                        'data_entrada': datetime.now().strftime("%Y-%m-%d")
                    }
                    updated = True
                elif isinstance(value, dict):
                    # Já está no formato correto
                    print(f"\n✅ {ticker} já está no formato correto")
                    new_quantities[ticker] = value
                else:
                    new_quantities[ticker] = value
            
            if updated:
                print(f"\n💾 Salvando formato corrigido...")
                
                # Atualiza no banco
                cursor.execute("""
                    UPDATE portfolios 
                    SET asset_quantities = ?,
                        updated_at = ?
                    WHERE username = ?
                """, (json.dumps(new_quantities), datetime.now().isoformat(), username))
                
                conn.commit()
                
                print(f"\n✅ Formato corrigido com sucesso!")
                print(f"\n📊 Novo formato:")
                for ticker, data in new_quantities.items():
                    if isinstance(data, dict):
                        print(f"   {ticker}: {data.get('quantidade', 0)} cotas")
                
                print(f"\n🎉 AGORA:")
                print(f"   1. Reinicie o app no Streamlit Cloud")
                print(f"   2. Faça login com hcarqueja")
                print(f"   3. Clique em '🔄 Atualizar Cotações'")
                print(f"   4. A quantidade deve aparecer!")
            else:
                print(f"\n✅ Todos os dados já estão no formato correto")
        else:
            print(f"\n❌ Carteira não encontrada para {username}")
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)

if __name__ == "__main__":
    corrigir_formato_cloud()
