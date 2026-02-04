"""
Módulo de Banco de Dados - SQLite com Persistência
===================================================
Gerencia usuários e carteiras com armazenamento persistente.
"""

import sqlite3
import json
import os
from datetime import datetime
from contextlib import contextmanager

print("=" * 80)
print("🔍 [DEBUG] database.py sendo carregado...")
print(f"🔍 [DEBUG] Diretório: {os.getcwd()}")
print(f"🔍 [DEBUG] Arquivos no diretório: {os.listdir('.')}")
print("=" * 80)

# Importa backup manager se disponível
BACKUP_ENABLED = False
print("🔍 [DEBUG] Tentando importar backup_manager...")
try:
    import backup_manager
    BACKUP_ENABLED = True
    print("✅ [BACKUP] Sistema de backup carregado!")
    print(f"🔍 [DEBUG] backup_manager file: {backup_manager.__file__}")
except ImportError as e:
    print(f"❌ [BACKUP] ImportError: {e}")
except Exception as e:
    print(f"❌ [BACKUP] Erro inesperado: {e}")

print(f"🔍 [DEBUG] BACKUP_ENABLED = {BACKUP_ENABLED}")
print("=" * 80)

# Caminho do banco de dados (será montado em volume Docker)
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'robo_investimentos.db')
BACKUP_PATH = os.path.join(os.path.dirname(__file__), 'data', 'users_backup.json')

# Garante que o diretório existe
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

@contextmanager
def get_db_connection():
    """Context manager para conexão com banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    try:
        yield conn
        conn.commit()
        print(f"🔍 [DEBUG] Após commit - BACKUP_ENABLED = {BACKUP_ENABLED}")
        # Backup automático após commit
        if BACKUP_ENABLED:
            print("🔍 [DEBUG] BACKUP_ENABLED é True, chamando auto_backup()...")
            try:
                backup_manager.auto_backup()
                print("✅ [BACKUP] auto_backup() executado com sucesso")
            except Exception as e:
                print(f"❌ [BACKUP] Erro em auto_backup(): {e}")
                import traceback
                traceback.print_exc()
        else:
            print("⚠️ [DEBUG] BACKUP_ENABLED é False, backup não executado")
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_database():
    """Inicializa o banco de dados com as tabelas necessárias."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Adiciona coluna email se não existir (para bancos existentes)
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN email TEXT')
        except sqlite3.OperationalError:
            pass  # Coluna já existe
        
        # Tabela de carteiras
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                us_stocks TEXT,
                br_fiis TEXT,
                tesouro_direto TEXT,
                asset_quantities TEXT,
                parametros TEXT,
                individual_multipliers TEXT,
                operations_history TEXT,
                portfolio_snapshots TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
            )
        ''')
        
        # Adiciona novas colunas se não existirem (para bancos existentes)
        for column in ['asset_quantities', 'parametros', 'individual_multipliers', 
                       'operations_history', 'portfolio_snapshots']:
            try:
                cursor.execute(f'ALTER TABLE portfolios ADD COLUMN {column} TEXT')
            except sqlite3.OperationalError:
                pass  # Coluna já existe
        
        # Restaura usuários do backup se banco estiver vazio
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            restore_users_from_backup()
        
        # Garante que usuário admin existe (atualiza se necessário)
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                'INSERT INTO users (username, password, name, email) VALUES (?, ?, ?, ?)',
                ('admin', 'investidor2026', 'Administrador', 'admin@robo-investimentos.com')
            )
        else:
            # Atualiza email se estiver vazio
            cursor.execute(
                'UPDATE users SET email = ? WHERE username = ? AND (email IS NULL OR email = "")',
                ('admin@robo-investimentos.com', 'admin')
            )
        
        conn.commit()

# ============================================================================
# FUNÇÕES DE BACKUP/RESTORE
# ============================================================================

def backup_users():
    """Faz backup dos usuários em arquivo JSON."""
    try:
        users = {}
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT username, password, name, email FROM users')
            rows = cursor.fetchall()
            
            for row in rows:
                users[row['username']] = {
                    'password': row['password'],
                    'name': row['name'],
                    'email': row['email'] if row['email'] else ''
                }
        
        with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Erro ao fazer backup: {e}")
        return False

def restore_users_from_backup():
    """Restaura usuários do arquivo de backup."""
    try:
        if not os.path.exists(BACKUP_PATH):
            return False
        
        with open(BACKUP_PATH, 'r', encoding='utf-8') as f:
            users = json.load(f)
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            for username, data in users.items():
                # Verifica se usuário já existe
                cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
                if cursor.fetchone()[0] == 0:
                    cursor.execute(
                        'INSERT INTO users (username, password, name, email) VALUES (?, ?, ?, ?)',
                        (username, data['password'], data['name'], data.get('email', ''))
                    )
            conn.commit()
        
        return True
    except Exception as e:
        print(f"Erro ao restaurar backup: {e}")
        return False

# ============================================================================
# FUNÇÕES DE USUÁRIOS
# ============================================================================

def load_users():
    """Carrega todos os usuários do banco de dados."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username, password, name, email FROM users')
        rows = cursor.fetchall()
        
        users = {}
        for row in rows:
            users[row['username']] = {
                'password': row['password'],
                'name': row['name'],
                'email': row['email'] if row['email'] else ''
            }
        return users

def save_user(username, password, name, email=''):
    """Salva um novo usuário no banco de dados."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, password, name, email) VALUES (?, ?, ?, ?)',
            (username, password, name, email)
        )
        # Faz backup automático após criar usuário
        backup_users()
        return True

def user_exists(username):
    """Verifica se um usuário existe."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
        return cursor.fetchone()[0] > 0

# ============================================================================
# FUNÇÕES DE CARTEIRAS
# ============================================================================

def load_user_portfolio(username):
    """Carrega a carteira de um usuário específico."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT us_stocks, br_fiis, tesouro_direto, asset_quantities, parametros, individual_multipliers, operations_history, portfolio_snapshots FROM portfolios WHERE username = ? ORDER BY id DESC LIMIT 1',
            (username,)
        )
        row = cursor.fetchone()
        
        if row:
            return {
                'US_STOCKS': json.loads(row['us_stocks']) if row['us_stocks'] else [],
                'BR_FIIS': json.loads(row['br_fiis']) if row['br_fiis'] else [],
                'TESOURO_DIRETO': json.loads(row['tesouro_direto']) if row['tesouro_direto'] else {},
                'ASSET_QUANTITIES': json.loads(row['asset_quantities']) if row['asset_quantities'] else {},
                'PARAMETROS': json.loads(row['parametros']) if row['parametros'] else {},
                'INDIVIDUAL_MULTIPLIERS': json.loads(row['individual_multipliers']) if row['individual_multipliers'] else {},
                'OPERATIONS_HISTORY': json.loads(row['operations_history']) if row['operations_history'] else [],
                'PORTFOLIO_SNAPSHOTS': json.loads(row['portfolio_snapshots']) if row['portfolio_snapshots'] else []
            }
        return None

def save_user_portfolio(username, portfolio):
    """Salva a carteira de um usuário."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Remove carteira anterior (mantém histórico se necessário)
        cursor.execute('DELETE FROM portfolios WHERE username = ?', (username,))
        
        # Insere nova carteira COM TODAS AS COLUNAS
        cursor.execute(
            '''INSERT INTO portfolios (username, us_stocks, br_fiis, tesouro_direto, 
                                        asset_quantities, parametros, individual_multipliers, 
                                        operations_history, portfolio_snapshots) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                username,
                json.dumps(portfolio.get('US_STOCKS', [])),
                json.dumps(portfolio.get('BR_FIIS', [])),
                json.dumps(portfolio.get('TESOURO_DIRETO', {})),
                json.dumps(portfolio.get('ASSET_QUANTITIES', {})),
                json.dumps(portfolio.get('PARAMETROS', {})),
                json.dumps(portfolio.get('INDIVIDUAL_MULTIPLIERS', {})),
                json.dumps(portfolio.get('OPERATIONS_HISTORY', [])),
                json.dumps(portfolio.get('PORTFOLIO_SNAPSHOTS', []))
            )
        )
        return True

def load_all_portfolios():
    """Carrega todas as carteiras (para admin)."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT DISTINCT p.username, p.us_stocks, p.br_fiis, p.tesouro_direto 
               FROM portfolios p
               INNER JOIN (
                   SELECT username, MAX(id) as max_id 
                   FROM portfolios 
                   GROUP BY username
               ) latest ON p.username = latest.username AND p.id = latest.max_id'''
        )
        rows = cursor.fetchall()
        
        portfolios = {}
        for row in rows:
            portfolios[row['username']] = {
                'US_STOCKS': json.loads(row['us_stocks']) if row['us_stocks'] else [],
                'BR_FIIS': json.loads(row['br_fiis']) if row['br_fiis'] else [],
                'TESOURO_DIRETO': json.loads(row['tesouro_direto']) if row['tesouro_direto'] else {}
            }
        return portfolios

# ============================================================================
# MIGRAÇÃO DE DADOS JSON PARA SQLITE
# ============================================================================

def migrate_json_to_sqlite():
    """Migra dados dos arquivos JSON antigos para o SQLite."""
    import os
    
    migrated = False
    
    # Migrar usuários
    if os.path.exists('users.json'):
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
            
            with get_db_connection() as conn:
                cursor = conn.cursor()
                for username, data in users.items():
                    # Verifica se usuário já existe
                    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
                    if cursor.fetchone()[0] == 0:
                        cursor.execute(
                            'INSERT INTO users (username, password, name) VALUES (?, ?, ?)',
                            (username, data.get('password', ''), data.get('name', username))
                        )
                        migrated = True
            
            # Renomeia arquivo antigo
            os.rename('users.json', 'users.json.backup')
            print("✅ Usuários migrados de users.json para SQLite")
        except Exception as e:
            print(f"⚠️ Erro ao migrar users.json: {e}")
    
    # Migrar carteiras
    if os.path.exists('user_portfolios.json'):
        try:
            with open('user_portfolios.json', 'r') as f:
                portfolios = json.load(f)
            
            for username, portfolio in portfolios.items():
                save_user_portfolio(username, portfolio)
                migrated = True
            
            # Renomeia arquivo antigo
            os.rename('user_portfolios.json', 'user_portfolios.json.backup')
            print("✅ Carteiras migradas de user_portfolios.json para SQLite")
        except Exception as e:
            print(f"⚠️ Erro ao migrar user_portfolios.json: {e}")
    
    if migrated:
        print("🎉 Migração concluída com sucesso!")
    
    return migrated

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

# Inicializa o banco automaticamente ao importar o módulo
init_database()

# Tenta migrar dados antigos se existirem
migrate_json_to_sqlite()
