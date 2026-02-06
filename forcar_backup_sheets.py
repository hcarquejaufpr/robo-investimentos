"""
Força backup completo do usuário hcarqueja para Google Sheets
"""
import database as db
from backup_manager import BackupManager

print("="*80)
print("💾 FORÇANDO BACKUP COMPLETO PARA GOOGLE SHEETS")
print("="*80)

username = 'hcarqueja'

# Carregar carteira do banco local
print(f"\n1️⃣ Carregando carteira de {username} do SQLite...")
portfolio = db.load_user_portfolio(username)

if portfolio:
    print(f"✅ Carteira carregada!")
    print(f"\n📊 Dados da carteira:")
    print(f"   BR_FIIS: {portfolio.get('BR_FIIS', [])}")
    print(f"   ASSET_QUANTITIES: {portfolio.get('ASSET_QUANTITIES', {})}")
    
    # Inicializar backup manager
    print(f"\n2️⃣ Inicializando BackupManager...")
    try:
        backup = BackupManager()
        print(f"✅ BackupManager inicializado!")
        
        # Forçar backup
        print(f"\n3️⃣ Executando backup para Google Sheets...")
        result = backup.backup_user_portfolio(username, portfolio)
        
        if result:
            print(f"\n✅ BACKUP CONCLUÍDO COM SUCESSO!")
            print(f"\n🔗 Acesse o Google Sheets:")
            print(f"   https://docs.google.com/spreadsheets/d/1m_D8SB1g-r2g6w96lzh5U9asrQfE4lFMwW3RXzDz9eE")
            print(f"   Aba: Carteira_{username}")
            print(f"\n✅ O HGRE11.SA com 83 cotas deve estar lá agora!")
        else:
            print(f"\n⚠️ Backup retornou False - pode ter havido um problema")
            
    except Exception as e:
        print(f"\n❌ Erro ao fazer backup: {e}")
        import traceback
        traceback.print_exc()
        
        print(f"\n💡 SOLUÇÃO ALTERNATIVA: Adicionar manualmente no Google Sheets")
        print(f"   Vou criar um script para isso...")
else:
    print(f"❌ Carteira não encontrada para {username}")

print("\n" + "="*80)
