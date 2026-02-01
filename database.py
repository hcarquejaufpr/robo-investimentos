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

# Caminho do banco de dados (será montado em volume Docker)
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'robo_investimentos.db')

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
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
            )
        ''')
        
        # Garante que usuário admin existe (atualiza se necessário)
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                'INSERT INTO users (username, password, name, email) VALUES (?, ?, ?, ?)',
                ('admin', 'investidor2026', 'Administrador', 'admin@robo-investimentos.com')
            )
            print("✅ Usuário admin criado")
        else:
            # Atualiza email se estiver vazio
            cursor.execute(
                'UPDATE users SET email = ? WHERE username = ? AND (email IS NULL OR email = "")',
                ('admin@robo-investimentos.com', 'admin')
            )
        
        conn.commit()
        print(f"✅ Banco de dados inicializado: {DB_PATH}")
        
        # Debug: mostra usuários existentes
        cursor.execute('SELECT username, email FROM users')
        users_list = cursor.fetchall()
        print(f"📊 Usuários no banco: {[dict(u) for u in users_list]}")

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
            'SELECT us_stocks, br_fiis, tesouro_direto FROM portfolios WHERE username = ? ORDER BY id DESC LIMIT 1',
            (username,)
        )
        row = cursor.fetchone()
        
        if row:
            return {
                'US_STOCKS': json.loads(row['us_stocks']) if row['us_stocks'] else [],
                'BR_FIIS': json.loads(row['br_fiis']) if row['br_fiis'] else [],
                'TESOURO_DIRETO': json.loads(row['tesouro_direto']) if row['tesouro_direto'] else {}
            }
        return None

def save_user_portfolio(username, portfolio):
    """Salva a carteira de um usuário."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Remove carteira anterior (mantém histórico se necessário)
        cursor.execute('DELETE FROM portfolios WHERE username = ?', (username,))
        
        # Insere nova carteira
        cursor.execute(
            '''INSERT INTO portfolios (username, us_stocks, br_fiis, tesouro_direto) 
               VALUES (?, ?, ?, ?)''',
            (
                username,
                json.dumps(portfolio.get('US_STOCKS', [])),
                json.dumps(portfolio.get('BR_FIIS', [])),
                json.dumps(portfolio.get('TESOURO_DIRETO', {}))
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
