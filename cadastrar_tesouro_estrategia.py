"""
Script para cadastrar títulos do Tesouro Direto com estratégia de venda inteligente
===================================================================================
Analisa a carteira e define estratégias específicas para cada título.
"""

import sqlite3
import json
import os
from datetime import datetime
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'robo_investimentos.db')

# Estratégias baseadas na análise realizada
ESTRATEGIAS = {
    # TÍTULOS SELIC - Alta liquidez, excelente rentabilidade
    "Tesouro Selic 2026": {
        "acao": "VENDA_PARCIAL_SE_NECESSARIO",
        "percentual_venda": 30,
        "gatilho": "Liquidez necessária ou rentabilidade atingir 40%",
        "motivo": "Rentabilidade de +34.72%. Manter 70% até vencimento, pode vender 30% se precisar de liquidez.",
        "prioridade": 3,
        "risco": "BAIXO"
    },
    "Tesouro Selic 2027": {
        "acao": "MANTER_ATE_VENCIMENTO",
        "percentual_venda": 0,
        "gatilho": "Só vender em emergência extrema",
        "motivo": "MELHOR PERFORMANCE (+70.25%)! Maior posição da carteira. Manter até vencimento para maximizar ganhos.",
        "prioridade": 1,
        "risco": "BAIXO"
    },
    "Tesouro Selic 2029": {
        "acao": "MANTER",
        "percentual_venda": 0,
        "gatilho": "N/A",
        "motivo": "Rentabilidade de +34.22%. Posição pequena, manter como reserva de longo prazo.",
        "prioridade": 2,
        "risco": "BAIXO"
    },
    
    # PREFIXADOS POSITIVOS - Avaliar cenário de juros
    "Tesouro Prefixado 2026": {
        "acao": "VENDER_SE_JUROS_SUBIREM",
        "percentual_venda": 100,
        "gatilho": "Se Selic subir para 12%+",
        "motivo": "Vence em 1 mês. Rentabilidade +27.28%. Liquidar para realocar se juros subirem.",
        "prioridade": 4,
        "risco": "BAIXO"
    },
    "Tesouro Prefixado 2028": {
        "acao": "MANTER_MONITORAR",
        "percentual_venda": 50,
        "gatilho": "Se Selic > 13% ou rentabilidade < 0%",
        "motivo": "Rentabilidade baixa (+6.49%). Vender 50% se juros subirem muito, manter 50% até vencimento.",
        "prioridade": 6,
        "risco": "MEDIO"
    },
    "Tesouro Prefixado 2029": {
        "acao": "MANTER",
        "percentual_venda": 0,
        "gatilho": "N/A",
        "motivo": "Rentabilidade boa (+26.29%). Posição pequena, manter.",
        "prioridade": 3,
        "risco": "MEDIO"
    },
    
    # PREFIXADO NEGATIVO - Manter até vencimento
    "Tesouro Prefixado com Juros Semestrais 2033": {
        "acao": "MANTER_ATE_VENCIMENTO",
        "percentual_venda": 0,
        "gatilho": "NÃO VENDER",
        "motivo": "Rentabilidade negativa (-6.51%) é marcação a mercado. Vender cristaliza prejuízo. MANTER até vencimento + receber cupons semestrais.",
        "prioridade": 1,
        "risco": "MEDIO",
        "cupons": True
    },
    
    # IPCA+ NEGATIVOS - Manter até vencimento para proteção inflação
    "Tesouro IPCA+ 2045": {
        "acao": "MANTER_ATE_VENCIMENTO",
        "percentual_venda": 0,
        "gatilho": "NÃO VENDER",
        "motivo": "Proteção contra inflação longo prazo. Rentabilidade +2.27%, posição pequena.",
        "prioridade": 2,
        "risco": "ALTO"
    },
    "Tesouro IPCA+ com Juros Semestrais 2035": {
        "acao": "MANTER_ATE_VENCIMENTO",
        "percentual_venda": 0,
        "gatilho": "NÃO VENDER",
        "motivo": "Rentabilidade negativa (-1.17%) é marcação a mercado. Receber cupons semestrais + correção IPCA.",
        "prioridade": 1,
        "risco": "MEDIO",
        "cupons": True
    },
    "Tesouro IPCA+ com Juros Semestrais 2040": {
        "acao": "MANTER_ATE_VENCIMENTO",
        "percentual_venda": 0,
        "gatilho": "NÃO VENDER",
        "motivo": "Rentabilidade negativa (-7.26%) é marcação a mercado. Vender cristaliza prejuízo de R$ 700+. Manter até vencimento + receber cupons.",
        "prioridade": 1,
        "risco": "ALTO",
        "cupons": True
    },
    "Tesouro IPCA+ com Juros Semestrais 2055": {
        "acao": "MANTER_ATE_VENCIMENTO",
        "percentual_venda": 0,
        "gatilho": "NÃO VENDER",
        "motivo": "MAIOR PREJUÍZO MARCADO (-17.71% = -R$ 2.660). Vender seria erro fatal. Manter para recuperar + receber cupons semestrais por 29 anos.",
        "prioridade": 1,
        "risco": "ALTO",
        "cupons": True
    }
}

def cadastrar_tesouro_com_estrategia():
    """Cadastra todos os títulos do Tesouro com suas estratégias no banco de dados."""
    
    print('='*100)
    print('CADASTRANDO TESOURO DIRETO COM ESTRATÉGIAS DE VENDA')
    print('='*100)
    
    # Ler CSV gerado
    df = pd.read_csv('tesouro_para_importar.csv')
    
    # Conectar ao banco
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Buscar carteira do usuário admin
    cursor.execute('''
        SELECT us_stocks, br_fiis, tesouro_direto, asset_quantities, parametros, 
               individual_multipliers, operations_history, portfolio_snapshots
        FROM portfolios WHERE username = ? ORDER BY updated_at DESC LIMIT 1
    ''', ('admin',))
    result = cursor.fetchone()
    
    if result:
        portfolio = {
            "US_STOCKS": json.loads(result[0]) if result[0] else [],
            "BR_FIIS": json.loads(result[1]) if result[1] else [],
            "TESOURO_DIRETO": json.loads(result[2]) if result[2] else {},
            "ASSET_QUANTITIES": json.loads(result[3]) if result[3] else {},
            "PARAMETROS": json.loads(result[4]) if result[4] else {},
            "INDIVIDUAL_MULTIPLIERS": json.loads(result[5]) if result[5] else {},
            "OPERATIONS_HISTORY": json.loads(result[6]) if result[6] else [],
            "PORTFOLIO_SNAPSHOTS": json.loads(result[7]) if result[7] else []
        }
        print('✓ Carteira existente carregada')
    else:
        portfolio = {
            "US_STOCKS": [],
            "BR_FIIS": [],
            "TESOURO_DIRETO": {},
            "ASSET_QUANTITIES": {},
            "PARAMETROS": {},
            "INDIVIDUAL_MULTIPLIERS": {},
            "OPERATIONS_HISTORY": [],
            "PORTFOLIO_SNAPSHOTS": []
        }
        print('✓ Nova carteira criada')
    
    # Preparar dados do Tesouro Direto
    tesouro_dict = {}
    estrategias_resumo = []
    
    print('\n📊 CADASTRANDO TÍTULOS COM ESTRATÉGIAS:\n')
    
    for idx, row in df.iterrows():
        nome = row['Nome']
        data_compra = row['Data Compra']
        valor_investido = float(row['Valor Investido'])
        quantidade = float(row['Quantidade'])
        
        # Buscar estratégia
        estrategia = ESTRATEGIAS.get(nome, {
            "acao": "ANALISAR",
            "percentual_venda": 0,
            "gatilho": "Avaliar caso a caso",
            "motivo": "Título sem estratégia definida",
            "prioridade": 5,
            "risco": "MEDIO"
        })
        
        # Adicionar ao dicionário
        tesouro_dict[nome] = {
            "data_compra": data_compra,
            "valor_investido": valor_investido,
            "quantidade": quantidade,
            "estrategia": estrategia['acao'],
            "percentual_venda": estrategia['percentual_venda'],
            "gatilho_venda": estrategia['gatilho'],
            "motivo_estrategia": estrategia['motivo'],
            "prioridade": estrategia['prioridade'],
            "risco": estrategia['risco'],
            "tem_cupons": estrategia.get('cupons', False)
        }
        
        # Preparar resumo
        icone_acao = {
            "MANTER_ATE_VENCIMENTO": "✋",
            "MANTER": "👍",
            "MANTER_MONITORAR": "👀",
            "VENDA_PARCIAL_SE_NECESSARIO": "⚠️",
            "VENDER_SE_JUROS_SUBIREM": "📈",
            "ANALISAR": "❓"
        }.get(estrategia['acao'], "📋")
        
        icone_risco = {
            "BAIXO": "🟢",
            "MEDIO": "🟡",
            "ALTO": "🔴"
        }.get(estrategia['risco'], "⚪")
        
        print(f"{icone_acao} {nome[:45]:<45} | P{estrategia['prioridade']} {icone_risco}")
        print(f"   └─ Estratégia: {estrategia['acao']}")
        print(f"   └─ {estrategia['motivo'][:90]}")
        print()
        
        estrategias_resumo.append({
            'nome': nome,
            'acao': estrategia['acao'],
            'prioridade': estrategia['prioridade'],
            'risco': estrategia['risco']
        })
    
    # Atualizar portfolio
    portfolio['TESOURO_DIRETO'] = tesouro_dict
    
    # Adicionar metadados da estratégia
    if 'ESTRATEGIA_TESOURO' not in portfolio:
        portfolio['ESTRATEGIA_TESOURO'] = {}
    
    portfolio['ESTRATEGIA_TESOURO'] = {
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_titulos": len(tesouro_dict),
        "resumo": estrategias_resumo,
        "diretrizes_gerais": {
            "1": "NUNCA vender títulos negativos (cristaliza prejuízo)",
            "2": "Títulos com cupons são fonte de renda - manter",
            "3": "Tesouro Selic tem alta liquidez - pode usar como reserva",
            "4": "Prefixados são sensíveis a juros - monitorar Selic",
            "5": "IPCA+ protege contra inflação - manter longo prazo"
        }
    }
    
    # Salvar no banco
    tesouro_json = json.dumps(portfolio['TESOURO_DIRETO'], ensure_ascii=False)
    estrategia_json = json.dumps(portfolio.get('ESTRATEGIA_TESOURO', {}), ensure_ascii=False)
    
    try:
        # Verificar se já existe registro
        cursor.execute('SELECT id FROM portfolios WHERE username = ?', ('admin',))
        existing = cursor.fetchone()
        
        if existing:
            # Atualizar registro existente
            cursor.execute('''
                UPDATE portfolios 
                SET tesouro_direto = ?,
                    parametros = ?,
                    updated_at = ?
                WHERE username = ?
            ''', (tesouro_json, estrategia_json, datetime.now(), 'admin'))
            print('✓ Registro atualizado')
        else:
            # Inserir novo registro
            cursor.execute('''
                INSERT INTO portfolios (username, us_stocks, br_fiis, tesouro_direto, 
                                      asset_quantities, parametros, individual_multipliers,
                                      operations_history, portfolio_snapshots, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('admin', 
                  json.dumps(portfolio['US_STOCKS']),
                  json.dumps(portfolio['BR_FIIS']),
                  tesouro_json,
                  json.dumps(portfolio['ASSET_QUANTITIES']),
                  estrategia_json,
                  json.dumps(portfolio['INDIVIDUAL_MULTIPLIERS']),
                  json.dumps(portfolio['OPERATIONS_HISTORY']),
                  json.dumps(portfolio['PORTFOLIO_SNAPSHOTS']),
                  datetime.now()))
            print('✓ Novo registro criado')
        
        conn.commit()
        print('='*100)
        print('✅ TÍTULOS E ESTRATÉGIAS CADASTRADOS COM SUCESSO NO BANCO DE DADOS!')
        print('='*100)
    except Exception as e:
        print(f'❌ Erro ao salvar: {e}')
        import traceback
        traceback.print_exc()
        conn.rollback()
    
    # Gerar relatório de estratégias
    print('\n📋 RESUMO DAS ESTRATÉGIAS POR PRIORIDADE:\n')
    
    for prioridade in sorted(set(s['prioridade'] for s in estrategias_resumo)):
        titulos_prioridade = [s for s in estrategias_resumo if s['prioridade'] == prioridade]
        print(f'🎯 PRIORIDADE {prioridade} ({len(titulos_prioridade)} título(s)):')
        for t in titulos_prioridade:
            print(f'   • {t["nome"]}: {t["acao"]} ({t["risco"]})')
        print()
    
    # Estatísticas
    print('📊 ESTATÍSTICAS DAS ESTRATÉGIAS:\n')
    manter = sum(1 for s in estrategias_resumo if 'MANTER' in s['acao'])
    vender = sum(1 for s in estrategias_resumo if 'VENDER' in s['acao'] or 'VENDA' in s['acao'])
    
    print(f'   • Manter até vencimento: {manter} títulos')
    print(f'   • Considerar venda: {vender} títulos')
    print(f'   • Risco BAIXO: {sum(1 for s in estrategias_resumo if s["risco"] == "BAIXO")} títulos')
    print(f'   • Risco MÉDIO: {sum(1 for s in estrategias_resumo if s["risco"] == "MEDIO")} títulos')
    print(f'   • Risco ALTO: {sum(1 for s in estrategias_resumo if s["risco"] == "ALTO")} títulos')
    
    conn.close()
    
    print('\n' + '='*100)
    print('✅ Agora você pode acessar o dashboard e ver todos os títulos com suas estratégias!')
    print('='*100)

if __name__ == '__main__':
    cadastrar_tesouro_com_estrategia()
