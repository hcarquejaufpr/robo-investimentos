"""
Restaura dados do Google Sheets para o banco SQLite
"""
import database as db
from backup_manager import BackupManager
import pandas as pd
import json

print("="*80)
print("📥 RESTAURANDO DADOS DO GOOGLE SHEETS PARA SQLITE")
print("="*80)

username = 'hcarqueja'

try:
    # Inicializar backup manager
    print(f"\n1️⃣ Conectando ao Google Sheets...")
    backup = BackupManager()
    print(f"✅ Conectado!")
    
    # Carregar carteira do Google Sheets
    print(f"\n2️⃣ Carregando carteira de {username} do Google Sheets...")
    df_carteira = backup.carregar_carteira(username)
    
    if df_carteira.empty:
        print(f"❌ Nenhum dado encontrado no Google Sheets para {username}")
    else:
        print(f"✅ {len(df_carteira)} ativo(s) encontrado(s)")
        print(f"\n📊 Dados encontrados:")
        print(df_carteira.to_string(index=False))
        
        # Converter DataFrame para o formato do portfolio
        print(f"\n3️⃣ Convertendo dados para formato do portfolio...")
        
        # Carregar portfolio atual (ou criar novo)
        portfolio = db.load_user_portfolio(username)
        if portfolio is None:
            print(f"⚠️ Portfolio não existe, criando novo...")
            portfolio = {
                "US_STOCKS": [],
                "BR_FIIS": [],
                "TESOURO_DIRETO": {},
                "ASSET_QUANTITIES": {},
                "PARAMETROS": {"MULTIPLIER_US": 1.2, "MULTIPLIER_BR": 1.0},
                "INDIVIDUAL_MULTIPLIERS": {},
                "OPERATIONS_HISTORY": [],
                "PORTFOLIO_SNAPSHOTS": []
            }
        
        # Processar cada ativo do Google Sheets
        br_fiis = []
        us_stocks = []
        asset_quantities = {}
        
        for _, row in df_carteira.iterrows():
            tipo = row.get('Tipo', '')
            ativo = row.get('Ativo', '')
            quantidade = row.get('Quantidade', 0)
            preco_entrada = row.get('Preço Entrada', 0.0)
            data_entrada = row.get('Data Entrada', '')
            
            print(f"\n   Processando: {ativo}")
            print(f"      Tipo: {tipo}")
            print(f"      Quantidade: {quantidade}")
            
            # Adicionar à lista apropriada
            if tipo == 'BR_FII':
                if ativo not in br_fiis:
                    br_fiis.append(ativo)
                    print(f"      ✅ Adicionado a BR_FIIS")
            elif tipo == 'US_STOCK':
                if ativo not in us_stocks:
                    us_stocks.append(ativo)
                    print(f"      ✅ Adicionado a US_STOCKS")
            
            # Adicionar quantidade
            if quantidade and quantidade > 0:
                asset_quantities[ativo] = {
                    'quantidade': float(quantidade),
                    'preco_entrada': float(preco_entrada) if preco_entrada else 0.0,
                    'data_entrada': str(data_entrada) if data_entrada else ''
                }
                print(f"      ✅ Quantidade configurada: {quantidade}")
        
        # Atualizar portfolio
        portfolio['BR_FIIS'] = br_fiis
        portfolio['US_STOCKS'] = us_stocks
        portfolio['ASSET_QUANTITIES'] = asset_quantities
        
        print(f"\n4️⃣ Salvando no banco SQLite...")
        print(f"   BR_FIIS: {br_fiis}")
        print(f"   US_STOCKS: {us_stocks}")
        print(f"   ASSET_QUANTITIES: {asset_quantities}")
        
        success = db.save_user_portfolio(username, portfolio)
        
        if success:
            print(f"\n✅ RESTAURAÇÃO CONCLUÍDA COM SUCESSO!")
            print(f"\n📊 Resumo:")
            print(f"   • {len(br_fiis)} FII(s) brasileiro(s)")
            print(f"   • {len(us_stocks)} ação(ões) US")
            print(f"   • {len(asset_quantities)} ativo(s) com quantidade")
            
            print(f"\n🎉 AGORA:")
            print(f"   1. Faça commit e push (para atualizar Streamlit Cloud)")
            print(f"   2. No Streamlit Cloud, faça logout e login")
            print(f"   3. A quantidade 83 deve aparecer corretamente!")
        else:
            print(f"\n❌ Erro ao salvar no banco SQLite")

except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
