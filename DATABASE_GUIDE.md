# 🗄️ Banco de Dados Persistente

## O que foi implementado?

O sistema agora usa **SQLite** com **volumes Docker persistentes** para garantir que seus dados (login e carteiras) não sejam perdidos quando o container for reiniciado.

## 📋 Mudanças Realizadas

### 1. Novo Módulo: `database.py`
- ✅ Banco de dados SQLite para armazenar usuários e carteiras
- ✅ Migração automática dos arquivos JSON antigos
- ✅ Persistência de dados entre reinicializações

### 2. Docker Volume Persistente
Atualizado [`docker-compose.yml`](docker-compose.yml) para incluir:
```yaml
volumes:
  - robo-data:/app/data  # Volume persistente
```

### 3. Atualização do `main.py`
- Substituiu funções de leitura/gravação JSON por chamadas ao banco de dados
- Manteve compatibilidade com o código existente

## 🚀 Como Usar

### Primeira Execução (Migração Automática)
Se você já tem dados em `users.json` ou `user_portfolios.json`, eles serão migrados automaticamente para o SQLite na primeira execução.

```bash
docker-compose up --build
```

### Onde os Dados Ficam Armazenados?

**Dentro do Docker:**
- `/app/data/robo_investimentos.db` - Banco de dados SQLite

**Volume Docker (persistente):**
- `robo-data` - Volume nomeado que persiste entre reinicializações

### Verificar Dados do Banco

Para ver o conteúdo do banco de dados:

```bash
# Entrar no container
docker exec -it robo-investimentos-app bash

# Abrir SQLite
sqlite3 /app/data/robo_investimentos.db

# Comandos úteis:
.tables                          # Lista todas as tabelas
SELECT * FROM users;             # Ver usuários
SELECT * FROM portfolios;        # Ver carteiras
.exit                            # Sair
```

## 📊 Estrutura do Banco de Dados

### Tabela: `users`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| username | TEXT | Nome de usuário (chave primária) |
| password | TEXT | Senha do usuário |
| name | TEXT | Nome completo |
| created_at | TIMESTAMP | Data de criação |

### Tabela: `portfolios`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | ID único (auto-incremento) |
| username | TEXT | Usuário proprietário |
| us_stocks | TEXT | Ações americanas (JSON) |
| br_fiis | TEXT | FIIs brasileiros (JSON) |
| tesouro_direto | TEXT | Tesouro Direto (JSON) |
| updated_at | TIMESTAMP | Data da última atualização |

## ⚠️ Importante

### Backup dos Dados

Para fazer backup do banco de dados:

```bash
# Copiar banco para seu computador
docker cp robo-investimentos-app:/app/data/robo_investimentos.db ./backup_db.sqlite

# Restaurar backup
docker cp ./backup_db.sqlite robo-investimentos-app:/app/data/robo_investimentos.db
```

### Resetar Todos os Dados

Se quiser começar do zero:

```bash
# Parar containers
docker-compose down

# Remover volume
docker volume rm robo_investimentos_robo-data

# Subir novamente
docker-compose up --build
```

## 🔄 Migração de Dados Antigos

O sistema detecta automaticamente arquivos `users.json` e `user_portfolios.json` e:

1. Migra todos os dados para o SQLite
2. Renomeia os arquivos antigos para `.backup`
3. Exibe mensagens de confirmação no console

**Arquivos de backup criados:**
- `users.json.backup`
- `user_portfolios.json.backup`

Você pode deletá-los após confirmar que tudo está funcionando.

## ✅ Vantagens

✅ **Persistência:** Dados não são perdidos ao reiniciar o Docker  
✅ **Migração Automática:** Converte JSON antigos automaticamente  
✅ **Performance:** SQLite é mais rápido que arquivos JSON  
✅ **Integridade:** Relações entre usuários e carteiras garantidas  
✅ **Backup Fácil:** Apenas um arquivo para fazer backup  

## 🐛 Solução de Problemas

### Dados não aparecem após migração

```bash
# Verificar logs do container
docker logs robo-investimentos-app

# Deve aparecer:
# ✅ Banco de dados inicializado
# ✅ Usuários migrados de users.json para SQLite
# ✅ Carteiras migradas de user_portfolios.json para SQLite
```

### Resetar usuário admin

```bash
docker exec -it robo-investimentos-app bash
sqlite3 /app/data/robo_investimentos.db
DELETE FROM users WHERE username = 'admin';
INSERT INTO users (username, password, name) VALUES ('admin', 'investidor2026', 'Administrador');
.exit
exit
```

## 📚 Arquivos Modificados

- [`database.py`](database.py) - Novo módulo de banco de dados
- [`main.py`](main.py) - Atualizado para usar SQLite
- [`docker-compose.yml`](docker-compose.yml) - Adicionado volume persistente

---

**Agora seus dados estão seguros! 🎉**
