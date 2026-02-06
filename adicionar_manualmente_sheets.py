"""
Adiciona HGRE11.SA manualmente no Google Sheets
"""
import gspread
from google.oauth2.service_account import Credentials

print("="*80)
print("💾 ADICIONANDO HGRE11.SA NO GOOGLE SHEETS MANUALMENTE")
print("="*80)

# Configuração de autenticação
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'gen-lang-client-0919671346-30ffdbafba47.json'

try:
    # Autenticar
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    
    # Abrir planilha
    spreadsheet_id = '1m_D8SB1g-r2g6w96lzh5U9asrQfE4lFMwW3RXzDz9eE'
    spreadsheet = client.open_by_key(spreadsheet_id)
    
    print(f"\n✅ Conectado à planilha: {spreadsheet.title}")
    
    # Abrir aba do usuário
    worksheet_name = "Carteira_hcarqueja"
    worksheet = spreadsheet.worksheet(worksheet_name)
    
    print(f"✅ Aba encontrada: {worksheet_name}")
    
    # Limpar tudo
    worksheet.clear()
    
    print(f"\n🧹 Aba limpa")
    
    # Criar cabeçalho e dados
    dados = [
        ['Tipo', 'Ativo', 'Quantidade', 'Preço Entrada', 'Data Entrada', 'Observações'],
        ['BR_FII', 'HGRE11.SA', 83, 0.0, '2026-02-06', 'Cadastro inicial']
    ]
    
    # Adicionar dados
    worksheet.update('A1', dados)
    
    print(f"\n✅ DADOS ADICIONADOS COM SUCESSO!")
    print(f"\n📊 Dados inseridos:")
    print(f"   Tipo: BR_FII")
    print(f"   Ativo: HGRE11.SA")
    print(f"   Quantidade: 83")
    print(f"   Preço Entrada: 0.0")
    print(f"   Data Entrada: 2026-02-06")
    
    print(f"\n🔗 Verifique no Google Sheets:")
    print(f"   https://docs.google.com/spreadsheets/d/1m_D8SB1g-r2g6w96lzh5U9asrQfE4lFMwW3RXzDz9eE")
    print(f"   Aba: Carteira_hcarqueja")
    
    print(f"\n🎉 AGORA NO STREAMLIT CLOUD:")
    print(f"   1. Faça logout")
    print(f"   2. Faça login novamente com hcarqueja")
    print(f"   3. A quantidade 83 deve aparecer corretamente!")
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
