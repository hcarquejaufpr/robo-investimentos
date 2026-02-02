import pandas as pd
import sys

file_path = r'c:\Users\BRHECAR1\Downloads\relatorio-consolidado-anual-2025.xlsx'

try:
    # Ler todas as abas
    xls = pd.ExcelFile(file_path)
    print('='*80)
    print('ABAS DISPONÍVEIS NO ARQUIVO:')
    print('='*80)
    for i, sheet in enumerate(xls.sheet_names, 1):
        print(f'{i}. {sheet}')
    
    print('\n' + '='*80)
    print('CONTEÚDO DAS ABAS:')
    print('='*80)
    
    for sheet in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)
        print(f'\n>>> ABA: {sheet}')
        print(f'>>> Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas')
        print(f'>>> Colunas: {list(df.columns)}')
        print('\n--- Primeiras 15 linhas ---')
        print(df.head(15).to_string(index=False))
        print('\n' + '-'*80)
        
except Exception as e:
    print(f'Erro ao ler arquivo: {e}')
    import traceback
    traceback.print_exc()
