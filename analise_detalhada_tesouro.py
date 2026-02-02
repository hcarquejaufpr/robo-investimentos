import pandas as pd
from datetime import datetime

file_path = r'c:\Users\BRHECAR1\Downloads\relatorio-consolidado-anual-2025.xlsx'

# Ler dados
df = pd.read_excel(file_path, sheet_name='Posição - Tesouro Direto')

# Remover linhas vazias (últimas 3 linhas são totais/vazias)
df = df.dropna(subset=['Produto'])

print('='*100)
print('ANÁLISE DETALHADA DA CARTEIRA DE TESOURO DIRETO')
print('='*100)
print(f'\nData da análise: {datetime.now().strftime("%d/%m/%Y %H:%M")}\n')

# Informações gerais
print('📊 RESUMO GERAL:')
print(f'   • Total de títulos diferentes: {len(df)}')
print(f'   • Quantidade total de papéis: {df["Quantidade"].sum():.2f}')
print(f'   • Valor total aplicado: R$ {df["Valor Aplicado"].sum():,.2f}')
print(f'   • Valor bruto atual: R$ {df["Valor bruto"].sum():,.2f}')
print(f'   • Valor líquido atual (após IR): R$ {df["Valor líquido"].sum():,.2f}')

# Calcular rentabilidade
rentabilidade_bruta = ((df["Valor bruto"].sum() / df["Valor Aplicado"].sum()) - 1) * 100
rentabilidade_liquida = ((df["Valor líquido"].sum() / df["Valor Aplicado"].sum()) - 1) * 100

print(f'\n💰 RENTABILIDADE:')
print(f'   • Rentabilidade bruta: {rentabilidade_bruta:+.2f}%')
print(f'   • Rentabilidade líquida: {rentabilidade_liquida:+.2f}%')
print(f'   • Impacto do IR: {rentabilidade_bruta - rentabilidade_liquida:.2f}%')

# Agrupar por indexador
print('\n📈 DIVERSIFICAÇÃO POR INDEXADOR:')
por_indexador = df.groupby('Indexador').agg({
    'Quantidade': 'sum',
    'Valor Aplicado': 'sum',
    'Valor líquido': 'sum'
}).round(2)

for idx in por_indexador.index:
    valor = por_indexador.loc[idx, 'Valor líquido']
    pct = (valor / df['Valor líquido'].sum()) * 100
    print(f'   • {idx}: R$ {valor:,.2f} ({pct:.1f}%)')

# Análise por vencimento
print('\n📅 CONCENTRAÇÃO POR PRAZO DE VENCIMENTO:')
df['Vencimento'] = pd.to_datetime(df['Vencimento'], format='%d/%m/%Y')
df['Anos_ate_vencimento'] = ((df['Vencimento'] - datetime.now()).dt.days / 365).round(1)

df_sorted = df.sort_values('Vencimento')
for _, row in df_sorted.iterrows():
    anos = row['Anos_ate_vencimento']
    valor = row['Valor líquido']
    pct = (valor / df['Valor líquido'].sum()) * 100
    rent = ((row['Valor bruto'] / row['Valor Aplicado']) - 1) * 100
    print(f'   • {row["Produto"]:<50} | {row["Vencimento"].strftime("%m/%Y")} ({anos:.1f} anos) | R$ {valor:>10,.2f} ({pct:>5.1f}%) | Rent: {rent:+6.2f}%')

# Títulos com melhor e pior performance
print('\n🏆 MELHORES PERFORMANCES:')
df['Rentabilidade'] = ((df['Valor bruto'] / df['Valor Aplicado']) - 1) * 100
top3 = df.nlargest(3, 'Rentabilidade')
for i, (_, row) in enumerate(top3.iterrows(), 1):
    print(f'   {i}. {row["Produto"]}: {row["Rentabilidade"]:+.2f}%')

print('\n⚠️  PIORES PERFORMANCES:')
bottom3 = df.nsmallest(3, 'Rentabilidade')
for i, (_, row) in enumerate(bottom3.iterrows(), 1):
    print(f'   {i}. {row["Produto"]}: {row["Rentabilidade"]:+.2f}%')

# Análise de risco (duration aproximada)
print('\n⏰ ANÁLISE DE DURATION (SENSIBILIDADE A JUROS):')
curto_prazo = df[df['Anos_ate_vencimento'] <= 3]
medio_prazo = df[(df['Anos_ate_vencimento'] > 3) & (df['Anos_ate_vencimento'] <= 10)]
longo_prazo = df[df['Anos_ate_vencimento'] > 10]

print(f'   • Curto prazo (até 3 anos): R$ {curto_prazo["Valor líquido"].sum():,.2f} ({(curto_prazo["Valor líquido"].sum()/df["Valor líquido"].sum()*100):.1f}%)')
print(f'   • Médio prazo (3-10 anos): R$ {medio_prazo["Valor líquido"].sum():,.2f} ({(medio_prazo["Valor líquido"].sum()/df["Valor líquido"].sum()*100):.1f}%)')
print(f'   • Longo prazo (>10 anos): R$ {longo_prazo["Valor líquido"].sum():,.2f} ({(longo_prazo["Valor líquido"].sum()/df["Valor líquido"].sum()*100):.1f}%)')

# Recomendações
print('\n💡 ANÁLISE E RECOMENDAÇÕES:')
print('\n1. DIVERSIFICAÇÃO:')
ipca_pct = (por_indexador.loc['IPCA', 'Valor líquido'] / df['Valor líquido'].sum() * 100) if 'IPCA' in por_indexador.index else 0
prefixado_pct = (por_indexador.loc['prefixado', 'Valor líquido'] / df['Valor líquido'].sum() * 100) if 'prefixado' in por_indexador.index else 0
selic_pct = (por_indexador.loc['SELIC', 'Valor líquido'] / df['Valor líquido'].sum() * 100) if 'SELIC' in por_indexador.index else 0

if selic_pct > 60:
    print('   ✓ Carteira muito conservadora (alta exposição ao Tesouro Selic)')
    print('   → Considere aumentar IPCA+ para proteção contra inflação')
elif ipca_pct > 60:
    print('   ✓ Boa proteção contra inflação (alta exposição ao IPCA+)')
    print('   → Mantenha diversificação ou aumente prefixados se juros caírem')
elif prefixado_pct > 60:
    print('   ⚠️  Alta exposição a prefixados - risco se juros subirem')
    print('   → Rebalanceie para IPCA+ e Selic para reduzir risco')
else:
    print('   ✓ Boa diversificação entre indexadores')

print('\n2. PRAZO DE VENCIMENTO:')
longo_pct = (longo_prazo["Valor líquido"].sum()/df["Valor líquido"].sum()*100)
if longo_pct > 40:
    print('   ⚠️  Alta concentração em prazos longos (>40%)')
    print('   → Maior volatilidade marcada a mercado')
    print('   → Ideal para quem pode manter até o vencimento')
else:
    print('   ✓ Boa distribuição de prazos')

print('\n3. TÍTULOS COM CUPONS:')
com_cupons = df[df['Produto'].str.contains('Juros Semestrais', case=False, na=False)]
if len(com_cupons) > 0:
    valor_cupons = com_cupons['Valor líquido'].sum()
    pct_cupons = (valor_cupons / df['Valor líquido'].sum() * 100)
    print(f'   • {len(com_cupons)} títulos com cupons: R$ {valor_cupons:,.2f} ({pct_cupons:.1f}%)')
    print('   ✓ Bom para gerar fluxo de caixa periódico')
else:
    print('   • Nenhum título com cupons semestrais')
    print('   → Considere adicionar se precisar de renda periódica')

print('\n4. TRIBUTAÇÃO:')
impacto_ir = df['Valor bruto'].sum() - df['Valor líquido'].sum()
print(f'   • Impacto atual do IR: R$ {impacto_ir:,.2f}')
print(f'   • Representa {(impacto_ir/df["Valor bruto"].sum()*100):.2f}% do lucro bruto')

# Verificar títulos próximos de 2 anos (alíquota cai de 15% para 15%)
proximos_2anos = df[(df['Anos_ate_vencimento'] < 2) & (df['Anos_ate_vencimento'] > 0)]
if len(proximos_2anos) > 0:
    print(f'   • {len(proximos_2anos)} título(s) próximo(s) a atingir menor alíquota de IR (15%)')

print('\n' + '='*100)
print('✅ CARTEIRA ANALISADA COM SUCESSO!')
print('='*100)

# Gerar CSV para importação no sistema
print('\n📋 GERANDO ARQUIVO CSV PARA IMPORTAÇÃO NO SISTEMA...')
df_export = df[['Produto', 'Vencimento', 'Valor Aplicado', 'Quantidade']].copy()
df_export['Vencimento'] = df_export['Vencimento'].dt.strftime('%Y-%m-%d')
df_export = df_export.rename(columns={
    'Produto': 'Nome',
    'Vencimento': 'Data Compra',
    'Valor Aplicado': 'Valor Investido'
})
df_export.to_csv('tesouro_para_importar.csv', index=False, encoding='utf-8-sig')
print('✓ Arquivo "tesouro_para_importar.csv" criado com sucesso!')
print('  Use este arquivo para importar todos os títulos no sistema.')
