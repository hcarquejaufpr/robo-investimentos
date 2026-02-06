"""
Script para enviar notificações diárias - Roda via GitHub Actions
"""
import os
import sys
import json
import sqlite3
from datetime import datetime
import yfinance as yf
import pandas as pd

# Adiciona o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(__file__))

import database as db
from main import enviar_email_alerta, get_market_data

def enviar_notificacoes_diarias():
    """Envia notificações para todos os usuários que ativaram"""
    print("="*80)
    print(f"🤖 EXECUTANDO NOTIFICAÇÕES DIÁRIAS - {datetime.now()}")
    print("="*80)
    
    # Carrega todos os portfolios
    conn = sqlite3.connect('data/robo_investimentos.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT username, us_stocks, br_fiis, asset_quantities, parametros, 
               individual_multipliers, operations_history
        FROM portfolios
    """)
    
    portfolios = cursor.fetchall()
    conn.close()
    
    usuarios_notificados = 0
    
    for row in portfolios:
        username = row[0]
        
        # Carrega portfolio completo
        portfolio = db.load_user_portfolio(username)
        
        if not portfolio:
            continue
        
        # Verifica se notificações estão ativadas
        notifications = portfolio.get('NOTIFICATIONS', {})
        
        if not notifications.get('enabled', False):
            print(f"⏭️  {username}: notificações desativadas")
            continue
        
        email = notifications.get('email')
        horario = notifications.get('time', '09:00')
        
        if not email:
            print(f"⚠️  {username}: email não configurado")
            continue
        
        print(f"\n📧 Enviando para {username} ({email})...")
        
        try:
            # Coleta dados
            US_STOCKS = portfolio.get('US_STOCKS', [])
            BR_FIIS = portfolio.get('BR_FIIS', [])
            PARAMETROS = portfolio.get('PARAMETROS', {})
            INDIVIDUAL_MULTIPLIERS = portfolio.get('INDIVIDUAL_MULTIPLIERS', {})
            ASSET_QUANTITIES = portfolio.get('ASSET_QUANTITIES', {})
            
            alertas = []
            resumo = {'total': 0, 'ganho': 0, 'perda': 0}
            
            # Verifica alertas US
            if US_STOCKS:
                try:
                    df_us = get_market_data(
                        US_STOCKS, 
                        PARAMETROS.get("MULTIPLIER_US", 1.2),
                        individual_multipliers=INDIVIDUAL_MULTIPLIERS,
                        asset_quantities=ASSET_QUANTITIES
                    )
                    
                    if not df_us.empty:
                        # Alertas de stop loss
                        near_stop = df_us[df_us["Distância Stop (%)"] < 5.0]
                        for _, row in near_stop.iterrows():
                            alertas.append(
                                f"🛑 {row['Ticker']} está a {row['Distância Stop (%)']:.1f}% do stop loss"
                            )
                        
                        # Calcula resumo
                        resumo['total'] += df_us['Valor Total (USD)'].sum()
                        resumo['ganho'] += df_us[df_us['Ganho/Perda (USD)'] > 0]['Ganho/Perda (USD)'].sum()
                        resumo['perda'] += df_us[df_us['Ganho/Perda (USD)'] < 0]['Ganho/Perda (USD)'].sum()
                
                except Exception as e:
                    print(f"   ⚠️ Erro ao processar US stocks: {e}")
            
            # Verifica alertas BR
            if BR_FIIS:
                try:
                    df_br = get_market_data(
                        BR_FIIS,
                        PARAMETROS.get("MULTIPLIER_BR", 1.0),
                        individual_multipliers=INDIVIDUAL_MULTIPLIERS,
                        asset_quantities=ASSET_QUANTITIES
                    )
                    
                    if not df_br.empty:
                        # Alertas de stop loss
                        near_stop = df_br[df_br["Distância Stop (%)"] < 5.0]
                        for _, row in near_stop.iterrows():
                            alertas.append(
                                f"🛑 {row['Ticker']} está a {row['Distância Stop (%)']:.1f}% do stop loss"
                            )
                        
                        # Calcula resumo (converte BRL para USD para somar)
                        resumo['total'] += df_br['Valor Total (R$)'].sum() / 5.0  # Aproximação
                        resumo['ganho'] += df_br[df_br['Ganho/Perda (R$)'] > 0]['Ganho/Perda (R$)'].sum() / 5.0
                        resumo['perda'] += df_br[df_br['Ganho/Perda (R$)'] < 0]['Ganho/Perda (R$)'].sum() / 5.0
                
                except Exception as e:
                    print(f"   ⚠️ Erro ao processar BR FIIs: {e}")
            
            # Monta HTML do email
            user_name = username.title()
            
            html = f"""
            <!DOCTYPE html>
            <html><head><meta charset="UTF-8"></head><body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
                <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h1 style="color: #2c3e50; margin-bottom: 10px;">🤖 Relatório Diário</h1>
                    <p style="color: #7f8c8d; margin-bottom: 30px;">Olá, {user_name}! Aqui está o resumo da sua carteira:</p>
                    
                    <div style="background-color: #ecf0f1; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <h2 style="color: #2c3e50; margin-top: 0;">📊 Resumo da Carteira</h2>
                        <p style="font-size: 18px; margin: 10px 0;">
                            <strong>Valor Total:</strong> ${resumo['total']:.2f}
                        </p>
                        <p style="font-size: 16px; margin: 10px 0; color: #27ae60;">
                            <strong>Ganhos:</strong> ${resumo['ganho']:.2f} ✅
                        </p>
                        <p style="font-size: 16px; margin: 10px 0; color: #e74c3c;">
                            <strong>Perdas:</strong> ${resumo['perda']:.2f} ❌
                        </p>
                    </div>
            """
            
            if alertas:
                html += """
                    <div style="background-color: #fff3cd; padding: 20px; border-radius: 8px; border-left: 4px solid #ffc107; margin-bottom: 20px;">
                        <h2 style="color: #856404; margin-top: 0;">⚠️ Alertas Importantes</h2>
                        <ul style="margin: 0; padding-left: 20px;">
                """
                for alerta in alertas:
                    html += f'<li style="margin: 8px 0; color: #856404;">{alerta}</li>'
                html += """
                        </ul>
                    </div>
                """
            else:
                html += """
                    <div style="background-color: #d4edda; padding: 20px; border-radius: 8px; border-left: 4px solid #28a745; margin-bottom: 20px;">
                        <p style="color: #155724; margin: 0;">✅ Nenhum alerta no momento. Tudo dentro dos parâmetros!</p>
                    </div>
                """
            
            html += f"""
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ecf0f1; text-align: center;">
                        <p style="color: #7f8c8d; font-size: 14px; margin: 5px 0;">
                            Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}
                        </p>
                        <p style="color: #7f8c8d; font-size: 12px; margin: 5px 0;">
                            <a href="https://robo-investimentos.streamlit.app" style="color: #3498db; text-decoration: none;">
                                🔗 Acessar Painel Completo
                            </a>
                        </p>
                    </div>
                </div>
            </div>
            </body></html>
            """
            
            # Envia email
            enviar_email_alerta(
                email,
                f"🤖 Relatório Diário - {datetime.now().strftime('%d/%m/%Y')}",
                html
            )
            
            print(f"   ✅ Email enviado com sucesso!")
            usuarios_notificados += 1
            
        except Exception as e:
            print(f"   ❌ Erro ao enviar para {username}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n" + "="*80)
    print(f"✅ Processo concluído: {usuarios_notificados} usuário(s) notificado(s)")
    print("="*80)

if __name__ == "__main__":
    enviar_notificacoes_diarias()
