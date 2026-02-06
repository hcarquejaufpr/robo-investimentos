# Sistema de Backup - Google Sheets

## ✅ Status: IMPLEMENTADO E TESTADO

### Configuração Realizada

- ✅ **Service Account**: `robo-investimentos-backup@gen-lang-client-0919671346.iam.gserviceaccount.com`
- ✅ **Planilha**: `RoboInvestimentos_Backup`
- ✅ **Credenciais**: `gen-lang-client-0919671346-30ffdbafba47.json`
- ✅ **Integração**: Backup automático ao salvar carteira

### Como Funciona

1. **Backup Automático**: Executado automaticamente ao salvar carteira via `save_user_portfolio()`
2. **Backup por Usuário**: Cada usuário tem abas separadas (`Carteira_username`, `Historico_username`)
3. **Persistência Dupla**: Dados salvos tanto no SQLite local quanto no Google Sheets

### Estrutura da Planilha

```
RoboInvestimentos_Backup/
├── Carteira_admin          # Carteira do usuário admin
├── Historico_admin         # Histórico de operações do admin
├── Carteira_<usuario>      # Carteira de cada usuário
└── Historico_<usuario>     # Histórico de cada usuário
```

### Campos Salvos na Carteira

| Campo      | Descrição                    |
|------------|------------------------------|
| Tipo       | US_STOCK, BR_FII, etc        |
| Ativo      | Ticker do ativo              |
| Quantidade | Quantidade de ativos         |

### Testes Executados

✅ **test_backup.py**: Testa conexão e operações básicas do BackupManager
```bash
python test_backup.py
```

✅ **test_integration.py**: Testa integração completa Database + Backup
```bash
python test_integration.py
```

### Arquivos do Sistema

```
backup_manager.py       # Classe BackupManager e funções auxiliares
database.py            # Integração com backup automático
test_backup.py         # Testes unitários do backup
test_integration.py    # Testes de integração
```

### Recuperação de Dados

Se precisar restaurar dados manualmente:

```python
from backup_manager import BackupManager

backup = BackupManager()
df = backup.carregar_carteira('admin')
print(df)
```

### Segurança

- ⚠️ Arquivo `gen-lang-client-0919671346-30ffdbafba47.json` está no `.gitignore`
- ⚠️ **NUNCA** commitar credenciais no repositório
- ✅ Service account tem acesso APENAS à planilha compartilhada
- ✅ Credenciais criptografadas pelo Google Cloud

### Logs de Backup

O sistema exibe logs detalhados:

```
🔍 [DEBUG] Executando backup para admin...
✅ Conectado: RoboInvestimentos_Backup
✅ Backup admin: 5 ativos
✅ [BACKUP] Backup executado para admin
```

### Troubleshooting

**Erro: "cannot import BackupManager"**
- Solução: `pip install gspread google-auth`

**Erro: "Credenciais não encontradas"**
- Solução: Verificar se arquivo `.json` está no diretório raiz

**Erro: "Permission denied"**
- Solução: Compartilhar planilha com o email da service account

### Próximos Passos (Opcional)

- [ ] Implementar versionamento de carteiras
- [ ] Adicionar backup de configurações do sistema
- [ ] Criar dashboard de auditoria no Sheets
- [ ] Notificações por email em caso de falha no backup

---

**Última atualização**: 05/02/2026  
**Testado por**: Sistema automatizado  
**Status**: ✅ Produção