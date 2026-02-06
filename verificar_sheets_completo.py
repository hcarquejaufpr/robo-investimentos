"""
Verifica em detalhes o Google Sheets - todas as abas e dados do hcarqueja
"""
import gspread
from google.oauth2.service_account import Credentials
import json

print("="*80)
print("🔍 VERIFICAÇÃO DETALHADA DO GOOGLE SHEETS")
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
    print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
    
    # Listar todas as abas
    worksheets = spreadsheet.worksheets()
    print(f"\n📊 Total de abas: {len(worksheets)}")
    
    # Buscar abas do hcarqueja
    for ws in worksheets:
        if 'hcarqueja' in ws.title.lower():
            print(f"\n" + "="*80)
            print(f"📄 ABA: {ws.title}")
            print("="*80)
            
            # Pegar todos os valores
            all_values = ws.get_all_values()
            
            if len(all_values) == 0:
                print("   ⚠️ ABA VAZIA (sem dados)")
                continue
            
            print(f"\n📏 Total de linhas com dados: {len(all_values)}")
            
            # Mostrar cabeçalho
            if len(all_values) > 0:
                print(f"\n📋 Cabeçalho:")
                print(f"   {all_values[0]}")
            
            # Mostrar dados
            if len(all_values) > 1:
                print(f"\n📊 Dados ({len(all_values) - 1} registros):")
                for idx, row in enumerate(all_values[1:], start=2):
                    print(f"\n   Linha {idx}:")
                    for col_idx, value in enumerate(row):
                        if value:  # Só mostra colunas com valor
                            col_name = all_values[0][col_idx] if col_idx < len(all_values[0]) else f"Col{col_idx}"
                            print(f"      {col_name}: {value}")
            else:
                print(f"\n   ⚠️ SÓ TEM CABEÇALHO - Nenhum registro de dados!")
            
            # Verificar especificamente HGRE11.SA
            print(f"\n🔍 Procurando HGRE11.SA...")
            found = False
            for idx, row in enumerate(all_values[1:], start=2):
                # Procurar em todas as colunas pelo ticker
                if 'HGRE11.SA' in str(row):
                    print(f"   ✅ ENCONTRADO na linha {idx}: {row}")
                    found = True
            
            if not found:
                print(f"   ❌ HGRE11.SA NÃO ENCONTRADO nesta aba!")
    
    print(f"\n" + "="*80)
    print("📝 TODAS AS ABAS DA PLANILHA:")
    print("="*80)
    for ws in worksheets:
        row_count = ws.row_count
        col_count = ws.col_count
        all_vals = ws.get_all_values()
        data_rows = len([r for r in all_vals if any(r)])  # linhas não vazias
        print(f"   • {ws.title}: {data_rows} linhas com dados (de {row_count} total)")

except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
