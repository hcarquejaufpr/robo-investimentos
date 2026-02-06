"""
Sistema de Backup para Google Sheets
"""
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import os

print("🔍 [BACKUP] Carregando módulo...")

class BackupManager:
    def __init__(self, credentials_file='gen-lang-client-0919671346-30ffdbafba47.json'):
        if not os.path.exists(credentials_file):
            raise FileNotFoundError(f"Credenciais não encontradas: {credentials_file}")
        
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        self.client = gspread.authorize(creds)
        self.spreadsheet = self.client.open('RoboInvestimentos_Backup')
        print(f"✅ Conectado: {self.spreadsheet.title}")
    
    def salvar_carteira(self, username, df_carteira):
        try:
            sheet_name = f"Carteira_{username}"
            try:
                worksheet = self.spreadsheet.worksheet(sheet_name)
            except:
                worksheet = self.spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)
            
            worksheet.clear()
            if not df_carteira.empty:
                data = [df_carteira.columns.values.tolist()] + df_carteira.values.tolist()
                worksheet.update('A1', data)
            
            print(f"✅ Backup {username}: {len(df_carteira)} ativos")
            return True
        except Exception as e:
            print(f"❌ Erro backup: {e}")
            return False
    
    def salvar_historico(self, username, operacao):
        try:
            sheet_name = f"Historico_{username}"
            try:
                worksheet = self.spreadsheet.worksheet(sheet_name)
            except:
                worksheet = self.spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=10)
                worksheet.append_row(['Timestamp', 'Tipo', 'Ativo', 'Qtd', 'Preço', 'Total', 'Obs'])
            
            operacao['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            row = [
                operacao.get('timestamp', ''),
                operacao.get('tipo', ''),
                operacao.get('ativo', ''),
                operacao.get('quantidade', ''),
                operacao.get('preco', ''),
                operacao.get('total', ''),
                operacao.get('observacao', '')
            ]
            worksheet.append_row(row)
            print(f"✅ Histórico {username}: {operacao.get('tipo')} {operacao.get('ativo')}")
            return True
        except Exception as e:
            print(f"❌ Erro histórico: {e}")
            return False
    
    def carregar_carteira(self, username):
        try:
            sheet_name = f"Carteira_{username}"
            worksheet = self.spreadsheet.worksheet(sheet_name)
            data = worksheet.get_all_records()
            return pd.DataFrame(data) if data else pd.DataFrame()
        except:
            return pd.DataFrame()
    
    def listar_usuarios(self):
        try:
            worksheets = self.spreadsheet.worksheets()
            usuarios = set()
            for ws in worksheets:
                if ws.title.startswith('Carteira_'):
                    usuarios.add(ws.title.replace('Carteira_', ''))
            return list(usuarios)
        except Exception as e:
            print(f"❌ Erro listar: {e}")
            return []

_backup_instance = None

def get_backup_manager():
    global _backup_instance
    if _backup_instance is None:
        try:
            _backup_instance = BackupManager()
        except Exception as e:
            print(f"⚠️ Backup indisponível: {e}")
    return _backup_instance

def auto_backup(username, portfolio_data):
    try:
        backup = get_backup_manager()
        if backup and portfolio_data:
            df = pd.DataFrame([portfolio_data]) if isinstance(portfolio_data, dict) else portfolio_data
            return backup.salvar_carteira(username, df)
    except Exception as e:
        print(f"⚠️ Backup falhou: {e}")
        return False

print("✅ [BACKUP] Módulo carregado com sucesso")