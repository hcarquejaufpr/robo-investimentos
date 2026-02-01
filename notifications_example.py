"""
📧 EXEMPLO DE IMPLEMENTAÇÃO DE NOTIFICAÇÕES
============================================

Este arquivo mostra como implementar notificações por email e WhatsApp.
NÃO está integrado ao sistema principal - é apenas um guia de implementação.

REQUISITOS:
-----------
pip install python-dotenv
pip install twilio  # Para WhatsApp

CONFIGURAÇÃO:
-------------
1. Crie um arquivo .env ou adicione ao secrets.toml do Streamlit
2. Adicione as credenciais necessárias
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ========================================
# 1. NOTIFICAÇÕES POR EMAIL (Gmail/SMTP)
# ========================================

def enviar_email_alerta(destinatario, assunto, conteudo_html):
    """
    Envia email usando Gmail SMTP
    
    CONFIGURAÇÃO NECESSÁRIA em .env ou secrets.toml:
    - EMAIL_SENDER = "seu_email@gmail.com"
    - EMAIL_PASSWORD = "sua_senha_de_app"  # Senha de aplicativo do Gmail
    
    Como obter senha de app do Gmail:
    1. Vá em: https://myaccount.google.com/security
    2. Ative verificação em 2 etapas
    3. Vá em "Senhas de app"
    4. Gere uma senha para "Mail" ou "Outro"
    """
    
    # Credenciais (carregar de secrets.toml ou .env)
    sender_email = "seu_email@gmail.com"  # Configure no secrets.toml
    sender_password = "sua_senha_de_app"   # Configure no secrets.toml
    
    # Cria mensagem
    msg = MIMEMultipart('alternative')
    msg['Subject'] = assunto
    msg['From'] = sender_email
    msg['To'] = destinatario
    
    # Anexa conteúdo HTML
    html_part = MIMEText(conteudo_html, 'html')
    msg.attach(html_part)
    
    try:
        # Conecta ao servidor Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Envia email
        server.send_message(msg)
        server.quit()
        
        return True, "Email enviado com sucesso!"
    
    except Exception as e:
        return False, f"Erro ao enviar email: {str(e)}"


def gerar_relatorio_html(usuario, alertas_criticos, resumo_carteira):
    """
    Gera HTML formatado para o email
    """
    
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ background: #1f77b4; color: white; padding: 20px; text-align: center; }}
            .alert {{ background: #fff3cd; border-left: 4px solid #ff9800; padding: 15px; margin: 10px 0; }}
            .critical {{ background: #f8d7da; border-left: 4px solid #dc3545; }}
            .success {{ background: #d4edda; border-left: 4px solid #28a745; }}
            .metric {{ display: inline-block; margin: 10px 20px; }}
            .value {{ font-size: 24px; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #4CAF50; color: white; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 Robô de Investimentos</h1>
            <p>Relatório Diário - {data_atual}</p>
        </div>
        
        <div style="padding: 20px;">
            <h2>👤 Olá, {usuario}!</h2>
            
            {'<div class="alert critical">' if alertas_criticos else '<div class="success">'}
                <h3>{'⚠️ ALERTAS CRÍTICOS' if alertas_criticos else '✅ Sem Alertas'}</h3>
                {'<ul>' + ''.join([f'<li>{a}</li>' for a in alertas_criticos]) + '</ul>' if alertas_criticos else '<p>Todos os ativos estão dentro dos parâmetros normais.</p>'}
            </div>
            
            <h3>📊 Resumo da Carteira</h3>
            <div>
                <div class="metric">
                    <p>Valor Total Investido</p>
                    <p class="value">${resumo_carteira['total']:,.2f}</p>
                </div>
                <div class="metric">
                    <p>Potencial de Ganho</p>
                    <p class="value" style="color: green;">+${resumo_carteira['ganho']:,.2f}</p>
                </div>
                <div class="metric">
                    <p>Risco de Perda</p>
                    <p class="value" style="color: red;">-${resumo_carteira['perda']:,.2f}</p>
                </div>
            </div>
            
            <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
                📱 Acesse seu painel completo em: <a href="https://robo-investimentos.streamlit.app">robo-investimentos.streamlit.app</a>
            </p>
        </div>
    </body>
    </html>
    """
    
    return html


# ========================================
# 2. NOTIFICAÇÕES POR WHATSAPP (Twilio)
# ========================================

def enviar_whatsapp_alerta(numero_destinatario, mensagem):
    """
    Envia mensagem via WhatsApp usando Twilio API
    
    CONFIGURAÇÃO NECESSÁRIA em .env ou secrets.toml:
    - TWILIO_ACCOUNT_SID = "seu_account_sid"
    - TWILIO_AUTH_TOKEN = "seu_auth_token"
    - TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Número sandbox da Twilio
    
    Como configurar Twilio:
    1. Crie conta em: https://www.twilio.com/
    2. Vá em Console > WhatsApp > Sandbox
    3. Envie mensagem de ativação para o número sandbox
    4. Copie credenciais: Account SID e Auth Token
    
    CUSTO: ~$0.005 por mensagem (após período gratuito)
    """
    
    try:
        from twilio.rest import Client
        
        # Credenciais (carregar de secrets.toml ou .env)
        account_sid = "seu_account_sid"     # Configure no secrets.toml
        auth_token = "seu_auth_token"        # Configure no secrets.toml
        whatsapp_from = "whatsapp:+14155238886"  # Número Twilio
        
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            from_=whatsapp_from,
            body=mensagem,
            to=f"whatsapp:{numero_destinatario}"  # Ex: "whatsapp:+5511999999999"
        )
        
        return True, f"WhatsApp enviado! SID: {message.sid}"
    
    except ImportError:
        return False, "Biblioteca 'twilio' não instalada. Execute: pip install twilio"
    
    except Exception as e:
        return False, f"Erro ao enviar WhatsApp: {str(e)}"


def gerar_mensagem_whatsapp(usuario, alertas_criticos, resumo_carteira):
    """
    Gera mensagem formatada para WhatsApp (texto simples)
    """
    
    msg = f"""🤖 *Robô de Investimentos*
    
👤 Olá, {usuario}!

📅 {datetime.now().strftime("%d/%m/%Y %H:%M")}

"""
    
    if alertas_criticos:
        msg += "⚠️ *ALERTAS CRÍTICOS:*\n"
        for alerta in alertas_criticos:
            msg += f"• {alerta}\n"
        msg += "\n"
    else:
        msg += "✅ *Sem alertas* - Tudo dentro dos parâmetros!\n\n"
    
    msg += f"""📊 *Resumo da Carteira:*
• Valor Total: ${resumo_carteira['total']:,.2f}
• Potencial Ganho: +${resumo_carteira['ganho']:,.2f}
• Risco Perda: -${resumo_carteira['perda']:,.2f}

📱 Acesse: robo-investimentos.streamlit.app
"""
    
    return msg


# ========================================
# 3. AGENDAMENTO AUTOMÁTICO
# ========================================

def agendar_notificacoes_diarias():
    """
    Exemplo de agendamento usando APScheduler
    
    NOTA: Para funcionar no Streamlit Cloud, você precisaria:
    1. Usar um serviço externo (AWS Lambda, Google Cloud Functions)
    2. Ou configurar GitHub Actions para executar script diariamente
    
    Para teste local, instale: pip install APScheduler
    """
    
    from apscheduler.schedulers.background import BackgroundScheduler
    
    def job_diario():
        """Esta função seria executada todo dia no horário configurado"""
        print("Enviando notificações diárias...")
        
        # Aqui você carregaria os dados do usuário
        # e chamaria as funções acima
        
        # Exemplo:
        # usuario = carregar_usuario()
        # alertas = verificar_alertas(usuario)
        # resumo = calcular_resumo_carteira(usuario)
        
        # if usuario['NOTIFICATIONS']['enabled']:
        #     if usuario['NOTIFICATIONS']['email']:
        #         html = gerar_relatorio_html(usuario['name'], alertas, resumo)
        #         enviar_email_alerta(usuario['NOTIFICATIONS']['email'], 
        #                           "🤖 Relatório Diário", html)
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(job_diario, 'cron', hour=9, minute=0)  # Todo dia às 9h
    scheduler.start()


# ========================================
# 4. EXEMPLO DE USO
# ========================================

if __name__ == "__main__":
    """Teste das funções"""
    
    # Dados de exemplo
    alertas_exemplo = [
        "AAPL está 3% abaixo do stop loss",
        "NVDA atingiu 95% do alvo de gain"
    ]
    
    resumo_exemplo = {
        'total': 35505.50,
        'ganho': 1811.32,
        'perda': 1170.45
    }
    
    # Teste Email
    print("=" * 50)
    print("TESTE DE EMAIL")
    print("=" * 50)
    html = gerar_relatorio_html("Seu Nome", alertas_exemplo, resumo_exemplo)
    print(html[:200] + "...")
    print("\n⚠️ Para enviar realmente, configure as credenciais!")
    
    # Teste WhatsApp
    print("\n" + "=" * 50)
    print("TESTE DE WHATSAPP")
    print("=" * 50)
    msg = gerar_mensagem_whatsapp("Seu Nome", alertas_exemplo, resumo_exemplo)
    print(msg)
    print("\n⚠️ Para enviar realmente, configure Twilio!")
    
    print("\n" + "=" * 50)
    print("PRÓXIMOS PASSOS:")
    print("=" * 50)
    print("""
    1. Escolha o método de notificação (Email é mais simples)
    2. Configure credenciais em secrets.toml do Streamlit
    3. Integre ao main.py (botão "Testar Notificação")
    4. Para produção: Configure GitHub Actions para executar diariamente
    
    📚 Documentação:
    - Gmail SMTP: https://support.google.com/mail/answer/185833
    - Twilio WhatsApp: https://www.twilio.com/docs/whatsapp
    - GitHub Actions: https://docs.github.com/en/actions
    """)
