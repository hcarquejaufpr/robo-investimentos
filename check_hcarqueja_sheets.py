"""
Script Rápido: Verifica carteira hcarqueja no Google Sheets
"""
try:
    from backup_manager import BackupManager
    import pandas as pd
    
    print("="*80)
    print("🔍 VERIFICANDO CARTEIRA HCARQUEJA NO GOOGLE SHEETS")
    print("="*80)
    
    # Conecta ao backup manager
    backup = BackupManager()
    print(f"✅ Conectado: {backup.spreadsheet.title}")
    print(f"🔗 URL: {backup.spreadsheet.url}\n")
    
    # Busca a aba da carteira
    try:
        worksheet = backup.spreadsheet.worksheet("Carteira_hcarqueja")
        print(f"✅ Aba encontrada: Carteira_hcarqueja")
        
        # Pega todos os dados
        data = worksheet.get_all_values()
        
        if len(data) > 1:  # Tem header + dados
            df = pd.DataFrame(data[1:], columns=data[0])
            print(f"\n📊 Total de ativos: {len(df)}")
            print(f"\n📋 Colunas: {', '.join(df.columns.tolist())}\n")
            print(df.to_string(index=False))
            
            # Verifica se tem HGRE11.SA
            if 'Ticker' in df.columns:
                hgre_rows = df[df['Ticker'].str.contains('HGRE11', case=False, na=False)]
                if not hgre_rows.empty:
                    print(f"\n✅ HGRE11.SA ENCONTRADO no Google Sheets!")
                    print(f"   Quantidade: {hgre_rows.iloc[0].get('Quantidade', 'N/A')}")
                else:
                    print(f"\n❌ HGRE11.SA NÃO encontrado")
        else:
            print(f"\n⚠️ Aba está vazia (apenas header ou sem dados)")
            
    except Exception as e:
        print(f"❌ Erro ao ler aba: {e}")
        print(f"\n💡 Possíveis causas:")
        print(f"   • Aba 'Carteira_hcarqueja' não existe")
        print(f"   • Dados nunca foram salvos no Google Sheets")
        
    print("\n" + "="*80)
    
except ImportError:
    print("❌ backup_manager não disponível")
    print("   Execute: pip install gspread google-auth")
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
    print(f"\n💡 Verifique:")
    print(f"   • Credenciais Google em .streamlit/secrets.toml")
    print(f"   • Arquivo gen-lang-client-*.json no diretório")
