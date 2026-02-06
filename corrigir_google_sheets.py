"""
Corrige a quantidade no Google Sheets de 3 para 83
"""
import gspread
from google.oauth2.service_account import Credentials

print("="*80)
print("🔧 CORRIGINDO QUANTIDADE NO GOOGLE SHEETS")
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
    
    # Buscar todos os dados
    all_data = worksheet.get_all_records()
    
    print(f"\n📊 Total de registros: {len(all_data)}")
    
    # Procurar HGRE11.SA
    for idx, row in enumerate(all_data, start=2):  # start=2 porque linha 1 é cabeçalho
        if row.get('Ativo') == 'HGRE11.SA':
            quantidade_atual = row.get('Quantidade', 0)
            print(f"\n🔍 Encontrado na linha {idx}:")
            print(f"   Ativo: {row.get('Ativo')}")
            print(f"   Quantidade atual: {quantidade_atual}")
            
            if quantidade_atual != 83:
                print(f"\n🔧 Corrigindo: {quantidade_atual} → 83")
                
                # Atualizar célula (coluna C é Quantidade)
                col_letra = 'C'  # Assumindo que Quantidade está na coluna C
                cell = f"{col_letra}{idx}"
                worksheet.update(cell, 83)
                
                print(f"✅ Atualizado na célula {cell}!")
                print(f"\n🎉 CONCLUÍDO! Quantidade corrigida no Google Sheets.")
                print(f"\n📝 PRÓXIMOS PASSOS:")
                print(f"   1. No Streamlit Cloud, faça logout")
                print(f"   2. Faça login novamente")
                print(f"   3. A quantidade 83 deve aparecer corretamente")
            else:
                print(f"\n✅ Quantidade já está correta (83)")
            
            break
    else:
        print(f"\n⚠️ HGRE11.SA não encontrado na planilha")
        print(f"\nDados encontrados:")
        for row in all_data:
            print(f"   - {row.get('Ativo')}: {row.get('Quantidade')}")

except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
