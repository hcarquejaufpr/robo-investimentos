"""
Sistema de Backup Automático para Persistência no Streamlit Cloud
==================================================================
Faz backup do SQLite para Google Sheets para garantir persistência.
"""

print("=" * 80)
print("🔍 [DEBUG BACKUP] Módulo backup_manager.py sendo carregado")
print("=" * 80)

import sqlite3
import json
import os
from datetime import datetime
import streamlit as st

print("🔍 [DEBUG BACKUP] Imports básicos OK")

# Tenta importar gspread (Google Sheets)
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False
    print("⚠️ gspread não instalado. Usando backup JSON local.")

# Caminhos
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'robo_investimentos.db')
LOCAL_BACKUP_PATH = os.path.join(os.path.dirname(__file__), 'data', 'db_backup.json')


def get_google_sheets_client():
    """Conecta ao Google Sheets usando credenciais do Streamlit Secrets."""
    if not GSPREAD_AVAILABLE:
        return None
    
    try:
        # Credenciais do Streamlit Secrets
        if 'gcp_service_account' not in st.secrets:
            print("⚠️ Credenciais Google Sheets não configuradas")
            return None
        
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
        )
        return gspread.authorize(credentials)
    except Exception as e:
        print(f"❌ Erro ao conectar Google Sheets: {e}")
        return None


def export_database_to_dict():
    """Exporta todo o banco SQLite para um dicionário."""
    if not os.path.exists(DB_PATH):
        return None
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    data = {
        'backup_date': datetime.now().isoformat(),
        'users': [],
        'portfolios': []
    }
    
    # Exporta usuários
    cursor.execute('SELECT * FROM users')
    for row in cursor.fetchall():
        data['users'].append(dict(row))
    
    # Exporta carteiras
    cursor.execute('SELECT * FROM portfolios')
    for row in cursor.fetchall():
        data['portfolios'].append(dict(row))
    
    conn.close()
    return data


def import_database_from_dict(data):
    """Importa dados de um dicionário para o banco SQLite."""
    if not data:
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Limpa tabelas existentes
        cursor.execute('DELETE FROM portfolios')
        cursor.execute('DELETE FROM users')
        
        # Importa usuários
        for user in data.get('users', []):
            cursor.execute('''
                INSERT OR REPLACE INTO users 
                (username, password, name, email, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                user['username'],
                user['password'],
                user['name'],
                user.get('email'),
                user.get('created_at')
            ))
        
        # Importa carteiras
        for portfolio in data.get('portfolios', []):
            cursor.execute('''
                INSERT INTO portfolios 
                (username, us_stocks, br_fiis, tesouro_direto, asset_quantities,
                 parametros, individual_multipliers, operations_history,
                 portfolio_snapshots, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                portfolio['username'],
                portfolio.get('us_stocks'),
                portfolio.get('br_fiis'),
                portfolio.get('tesouro_direto'),
                portfolio.get('asset_quantities'),
                portfolio.get('parametros'),
                portfolio.get('individual_multipliers'),
                portfolio.get('operations_history'),
                portfolio.get('portfolio_snapshots'),
                portfolio.get('updated_at')
            ))
        
        conn.commit()
        print(f"✅ Banco restaurado com {len(data.get('users', []))} usuários e {len(data.get('portfolios', []))} carteiras")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro ao importar dados: {e}")
        return False
    finally:
        conn.close()


def backup_to_google_sheets():
    """Faz backup do banco para Google Sheets."""
    client = get_google_sheets_client()
    if not client:
        return backup_to_local_json()
    
    try:
        # Nome da planilha (configurável nos secrets)
        sheet_name = st.secrets.get('backup_sheet_name', 'RoboInvestimentos_Backup')
        
        # Abre ou cria a planilha
        try:
            spreadsheet = client.open(sheet_name)
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create(sheet_name)
            print(f"✅ Planilha criada: {sheet_name}")
            
            # Compartilha automaticamente com o usuário (se configurado)
            try:
                user_email = st.secrets.get('owner_email')
                if user_email:
                    spreadsheet.share(user_email, perm_type='user', role='writer')
                    print(f"✅ Planilha compartilhada com: {user_email}")
            except Exception as e:
                print(f"⚠️ Não foi possível compartilhar automaticamente: {e}")
        
        # Exporta dados
        data = export_database_to_dict()
        if not data:
            return False
        
        # Salva em worksheet
        try:
            worksheet = spreadsheet.worksheet('backup')
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet('backup', rows=100, cols=20)
        
        # Atualiza célula com JSON
        worksheet.update('A1', json.dumps(data, ensure_ascii=False))
        
        print(f"✅ Backup realizado no Google Sheets: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no backup Google Sheets: {e}")
        return backup_to_local_json()


def restore_from_google_sheets():
    """Restaura banco de dados do Google Sheets."""
    client = get_google_sheets_client()
    if not client:
        return restore_from_local_json()
    
    try:
        sheet_name = st.secrets.get('backup_sheet_name', 'RoboInvestimentos_Backup')
        spreadsheet = client.open(sheet_name)
        worksheet = spreadsheet.worksheet('backup')
        
        # Lê dados
        json_data = worksheet.acell('A1').value
        if not json_data:
            print("⚠️ Nenhum backup encontrado no Google Sheets")
            return restore_from_local_json()
        
        data = json.loads(json_data)
        success = import_database_from_dict(data)
        
        if success:
            print(f"✅ Dados restaurados do Google Sheets (backup de {data.get('backup_date', 'data desconhecida')})")
        return success
        
    except gspread.SpreadsheetNotFound:
        print("⚠️ Planilha de backup não encontrada")
        return restore_from_local_json()
    except Exception as e:
        print(f"❌ Erro ao restaurar do Google Sheets: {e}")
        return restore_from_local_json()


def backup_to_local_json():
    """Backup local em JSON (fallback)."""
    try:
        data = export_database_to_dict()
        if not data:
            return False
        
        os.makedirs(os.path.dirname(LOCAL_BACKUP_PATH), exist_ok=True)
        with open(LOCAL_BACKUP_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Backup local realizado: {LOCAL_BACKUP_PATH}")
        return True
    except Exception as e:
        print(f"❌ Erro no backup local: {e}")
        return False


def restore_from_local_json():
    """Restaura do backup local JSON."""
    try:
        if not os.path.exists(LOCAL_BACKUP_PATH):
            print("⚠️ Nenhum backup local encontrado")
            return False
        
        with open(LOCAL_BACKUP_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        success = import_database_from_dict(data)
        if success:
            print(f"✅ Dados restaurados do backup local (backup de {data.get('backup_date', 'data desconhecida')})")
        return success
        
    except Exception as e:
        print(f"❌ Erro ao restaurar backup local: {e}")
        return False


def auto_backup():
    """Executa backup automático (tenta Google Sheets, fallback para local)."""
    if GSPREAD_AVAILABLE and 'gcp_service_account' in st.secrets:
        return backup_to_google_sheets()
    else:
        return backup_to_local_json()


def auto_restore():
    """Executa restore automático ao iniciar aplicação."""
    # Verifica se banco está vazio
    if not os.path.exists(DB_PATH):
        print("📦 Banco não existe, tentando restaurar...")
        if GSPREAD_AVAILABLE and 'gcp_service_account' in st.secrets:
            return restore_from_google_sheets()
        else:
            return restore_from_local_json()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    conn.close()
    
    if user_count <= 1:  # Apenas admin
        print("📦 Banco quase vazio, tentando restaurar...")
        if GSPREAD_AVAILABLE and 'gcp_service_account' in st.secrets:
            return restore_from_google_sheets()
        else:
            return restore_from_local_json()
    
    return False
