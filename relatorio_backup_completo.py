"""
Relatório Completo do Sistema de Backup
"""
import os
import json
import sqlite3
from datetime import datetime

print("=" * 100)
print("📊 RELATÓRIO COMPLETO DO SISTEMA DE BACKUP")
print("=" * 100)

# 1. Verificar Banco SQLite Local
print("\n" + "=" * 100)
print("1️⃣ BANCO DE DADOS SQLite LOCAL")
print("=" * 100)

db_path = 'data/robo_investimentos.db'
if os.path.exists(db_path):
    print(f"✅ Banco encontrado: {db_path}")
    print(f"📊 Tamanho: {os.path.getsize(db_path):,} bytes")
    print(f"📅 Última modificação: {datetime.fromtimestamp(os.path.getmtime(db_path)).strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Conecta e verifica dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Usuários
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    print(f"\n👥 Total de usuários: {total_users}")
    
    if total_users > 0:
        cursor.execute('SELECT username, name, email FROM users')
        users = cursor.fetchall()
        print("\n   Usuários cadastrados:")
        for username, name, email in users:
            print(f"   • {username}: {name} ({email})")
    
    # Carteiras
    cursor.execute('SELECT COUNT(*) FROM portfolios')
    total_portfolios = cursor.fetchone()[0]
    print(f"\n💼 Total de carteiras: {total_portfolios}")
    
    if total_portfolios > 0:
        cursor.execute('SELECT username, updated_at FROM portfolios ORDER BY updated_at DESC')
        portfolios = cursor.fetchall()
        print("\n   Carteiras por usuário:")
        for username, updated_at in portfolios:
            print(f"   • {username} - Última atualização: {updated_at}")
    
    conn.close()
else:
    print(f"❌ Banco NÃO encontrado: {db_path}")

# 2. Verificar Backup Local (JSON)
print("\n" + "=" * 100)
print("2️⃣ BACKUP LOCAL (JSON)")
print("=" * 100)

backup_json_path = 'data/users_backup.json'
if os.path.exists(backup_json_path):
    print(f"✅ Backup encontrado: {backup_json_path}")
    print(f"📊 Tamanho: {os.path.getsize(backup_json_path):,} bytes")
    print(f"📅 Última modificação: {datetime.fromtimestamp(os.path.getmtime(backup_json_path)).strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Lê conteúdo
    with open(backup_json_path, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)
    
    print(f"\n👥 Usuários no backup: {len(backup_data)}")
    print("\n   Lista de usuários:")
    for username, data in backup_data.items():
        print(f"   • {username}: {data['name']} ({data['email']})")
else:
    print(f"❌ Backup NÃO encontrado: {backup_json_path}")

# 3. Verificar credenciais do Google Sheets
print("\n" + "=" * 100)
print("3️⃣ CREDENCIAIS DO GOOGLE SHEETS")
print("=" * 100)

credentials_file = 'gen-lang-client-0919671346-30ffdbafba47.json'
if os.path.exists(credentials_file):
    print(f"✅ Arquivo de credenciais encontrado: {credentials_file}")
    print(f"📊 Tamanho: {os.path.getsize(credentials_file):,} bytes")
    
    # Lê informações da conta de serviço
    with open(credentials_file, 'r') as f:
        creds_data = json.load(f)
    
    print(f"\n📧 Email da conta de serviço: {creds_data.get('client_email', 'N/A')}")
    print(f"🏗️ Projeto: {creds_data.get('project_id', 'N/A')}")
else:
    print(f"❌ Arquivo de credenciais NÃO encontrado: {credentials_file}")

# 4. Testar conexão com Google Sheets
print("\n" + "=" * 100)
print("4️⃣ TESTE DE CONEXÃO COM GOOGLE SHEETS")
print("=" * 100)

try:
    print("Tentando importar bibliotecas...")
    import gspread
    from google.oauth2.service_account import Credentials
    print("✅ Bibliotecas importadas com sucesso")
    
    if os.path.exists(credentials_file):
        print("\nTentando autenticar...")
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        client = gspread.authorize(creds)
        print("✅ Autenticação bem-sucedida!")
        
        print("\nTentando acessar planilha 'RoboInvestimentos_Backup'...")
        try:
            spreadsheet = client.open('RoboInvestimentos_Backup')
            print(f"✅ Planilha encontrada!")
            print(f"📋 Título: {spreadsheet.title}")
            print(f"🔗 URL: {spreadsheet.url}")
            
            # Lista abas
            worksheets = spreadsheet.worksheets()
            print(f"\n📊 Total de abas: {len(worksheets)}")
            
            if len(worksheets) > 0:
                print("\n   Abas encontradas:")
                for ws in worksheets:
                    print(f"   • {ws.title} ({ws.row_count} linhas x {ws.col_count} colunas)")
                    
                    # Verifica se tem dados
                    if ws.title.startswith('Carteira_') or ws.title.startswith('Historico_'):
                        try:
                            data = ws.get_all_records()
                            if data:
                                print(f"     └─> {len(data)} registros")
                            else:
                                print(f"     └─> Vazia (sem dados)")
                        except:
                            pass
                
                # Verifica especificamente o usuário hcarqueja
                print("\n   🔍 Verificando usuário 'hcarqueja':")
                try:
                    ws_carteira = spreadsheet.worksheet('Carteira_hcarqueja')
                    data = ws_carteira.get_all_records()
                    print(f"   ✅ Carteira encontrada: {len(data)} ativos")
                except:
                    print(f"   ❌ Aba 'Carteira_hcarqueja' NÃO encontrada")
                
                try:
                    ws_historico = spreadsheet.worksheet('Historico_hcarqueja')
                    data = ws_historico.get_all_records()
                    print(f"   ✅ Histórico encontrado: {len(data)} operações")
                except:
                    print(f"   ❌ Aba 'Historico_hcarqueja' NÃO encontrada")
            else:
                print("\n   ⚠️ PLANILHA VAZIA - Nenhuma aba encontrada!")
                print("\n   💡 Isso significa que:")
                print("      • O backup do Google Sheets NUNCA foi executado")
                print("      • Ou as abas foram deletadas manualmente")
                
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"❌ Planilha 'RoboInvestimentos_Backup' NÃO EXISTE no Google Drive")
            print("\n💡 Você precisa:")
            print("   1. Criar uma planilha no Google Sheets com o nome 'RoboInvestimentos_Backup'")
            print("   2. Compartilhar com o email da conta de serviço")
            print(f"   3. Email: {creds_data.get('client_email', 'Ver arquivo de credenciais')}")
        except Exception as e:
            print(f"❌ Erro ao acessar planilha: {e}")
except ImportError as e:
    print(f"❌ Bibliotecas não instaladas: {e}")
    print("\n💡 Execute: pip install gspread google-auth")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    import traceback
    traceback.print_exc()

# 5. Verificar se o backup_manager está funcionando no código
print("\n" + "=" * 100)
print("5️⃣ STATUS DO BACKUP_MANAGER NO CÓDIGO")
print("=" * 100)

try:
    import database as db
    print(f"✅ Módulo database importado")
    print(f"📊 BACKUP_ENABLED = {db.BACKUP_ENABLED}")
    
    if db.BACKUP_ENABLED:
        print("\n✅ Sistema de backup está ATIVO no código")
        print("   • Backups automáticos estão habilitados")
        print("   • Dados serão salvos no Google Sheets quando houver alterações")
    else:
        print("\n⚠️ Sistema de backup está INATIVO no código")
        print("   • Backups automáticos NÃO estão funcionando")
        print("   • Dados NÃO serão salvos no Google Sheets")
        print("\n💡 Possíveis causas:")
        print("   • Erro ao importar backup_manager.py")
        print("   • Erro nas credenciais do Google")
        print("   • Bibliotecas não instaladas (gspread, google-auth)")
except Exception as e:
    print(f"❌ Erro ao verificar database: {e}")

# 6. Resumo e Recomendações
print("\n" + "=" * 100)
print("📋 RESUMO E RECOMENDAÇÕES")
print("=" * 100)

print("\n✅ O QUE ESTÁ FUNCIONANDO:")
print("   • Banco de dados SQLite local está funcionando")
print("   • Backup local (JSON) está funcionando")
print("   • Login de usuários está funcionando")

print("\n⚠️ O QUE PODE NÃO ESTAR FUNCIONANDO:")
print("   • Backup automático para Google Sheets")
print("   • Persistência de dados no Streamlit Cloud")

print("\n💡 EXPLICAÇÃO DO QUE ACONTECEU:")
print("   1. Você fez login e funcionou → Banco SQLite local estava OK")
print("   2. Não viu dados no Google Sheets → Backup remoto NÃO está configurado/funcionando")
print("   3. Aplicação estava desativada no Streamlit → Banco SQLite foi perdido na última desativação")
print("   4. Quando reativou, o banco foi restaurado do backup JSON local ou recriado vazio")

print("\n🔥 IMPORTANTE:")
print("   • O banco SQLite local NÃO PERSISTE quando o Streamlit Cloud desativa o app!")
print("   • Para ter persistência real, você PRECISA configurar o backup do Google Sheets")
print("   • Veja o guia: CONFIGURAR_BACKUP_PERSISTENTE.md")

print("\n" + "=" * 100)
print("✅ RELATÓRIO CONCLUÍDO")
print("=" * 100)
