import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from importlib import reload
import ssl
import hashlib
import config  # Importa suas configurações do config.py
import plotly.graph_objects as go
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Desabilita verificação SSL (necessário em algumas redes corporativas)
ssl._create_default_https_context = ssl._create_unverified_context

# --- Funções de Notificação por Email ---
def enviar_email_alerta(destinatario, assunto, conteudo_html):
    """
    Envia email usando Gmail SMTP
    Credenciais carregadas de st.secrets
    """
    try:
        # Carrega credenciais do Streamlit secrets
        sender_email = st.secrets.get("EMAIL_SENDER", "casamentojuliaehenrique2017@gmail.com")
        sender_password = st.secrets.get("EMAIL_PASSWORD", "")
        
        if not sender_password:
            return False, "❌ Configure EMAIL_PASSWORD no secrets.toml"
        
        # Cria mensagem
        msg = MIMEMultipart('alternative')
        msg['Subject'] = assunto
        msg['From'] = sender_email
        msg['To'] = destinatario
        
        # Anexa conteúdo HTML
        html_part = MIMEText(conteudo_html, 'html')
        msg.attach(html_part)
        
        # Conecta ao servidor Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Envia email
        server.send_message(msg)
        server.quit()
        
        return True, "✅ Email enviado com sucesso!"
    
    except Exception as e:
        return False, f"❌ Erro ao enviar email: {str(e)}"

def gerar_relatorio_html(usuario, alertas_criticos, resumo_carteira):
    """
    Gera HTML formatado para o email de notificação
    """
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; background-color: #f4f4f4; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 28px; }}
            .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
            .content {{ padding: 30px; }}
            .alert {{ background: #fff3cd; border-left: 4px solid #ff9800; padding: 15px; margin: 15px 0; border-radius: 4px; }}
            .critical {{ background: #f8d7da; border-left: 4px solid #dc3545; }}
            .success {{ background: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 15px 0; border-radius: 4px; }}
            .metrics {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .metric {{ text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; flex: 1; margin: 0 5px; }}
            .metric-label {{ font-size: 12px; color: #666; text-transform: uppercase; margin-bottom: 5px; }}
            .metric-value {{ font-size: 24px; font-weight: bold; color: #333; }}
            .metric-delta {{ font-size: 14px; margin-top: 5px; }}
            .green {{ color: #28a745; }}
            .red {{ color: #dc3545; }}
            .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; font-size: 14px; }}
            .button {{ display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
            ul {{ padding-left: 20px; }}
            ul li {{ margin: 8px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Robô de Investimentos</h1>
                <p>Relatório Diário - {data_atual}</p>
            </div>
            
            <div class="content">
                <h2 style="color: #333;">👤 Olá, {usuario}!</h2>
                
                {'<div class="alert critical"><h3 style="margin-top:0;">⚠️ ALERTAS CRÍTICOS</h3><ul>' + ''.join([f'<li>{a}</li>' for a in alertas_criticos]) + '</ul></div>' if alertas_criticos else '<div class="success"><strong>✅ Sem Alertas</strong><p style="margin: 5px 0 0 0;">Todos os ativos estão dentro dos parâmetros normais.</p></div>'}
                
                <h3 style="color: #333; margin-top: 30px;">📊 Resumo da Carteira</h3>
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-label">Valor Total</div>
                        <div class="metric-value">${resumo_carteira['total']:,.2f}</div>
                    </div>
                </div>
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-label">Potencial de Ganho</div>
                        <div class="metric-value green">+${resumo_carteira['ganho']:,.2f}</div>
                        <div class="metric-delta green">Se atingir todos os alvos</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Risco de Perda</div>
                        <div class="metric-value red">-${resumo_carteira['perda']:,.2f}</div>
                        <div class="metric-delta red">Se acionar todos os stops</div>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="https://robo-investimentos.streamlit.app" class="button">📱 Acessar Painel Completo</a>
                </div>
            </div>
            
            <div class="footer">
                <p>Este é um email automático do seu Robô de Investimentos.</p>
                <p style="margin: 5px 0;">🤖 Sistema de Estratégia de Saída 2026</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

# --- Configuração da Página ---
st.set_page_config(
    page_title="Robô Estratégia de Saída",
    page_icon="📈",
    layout="wide"
)

# ============================================================================
# SISTEMA DE AUTENTICAÇÃO MULTI-USUÁRIO
# ============================================================================

import json
import os

# ============================================================================
# GERENCIAMENTO DE CARTEIRAS POR USUÁRIO
# ============================================================================

def load_user_portfolio(username):
    """Carrega a carteira específica do usuário."""
    portfolios_file = "user_portfolios.json"
    
    # Carteira padrão (vazia)
    default_portfolio = {
        "US_STOCKS": [],
        "BR_FIIS": [],
        "TESOURO_DIRETO": {},
        "PARAMETROS": {
            "MULTIPLIER_US": 1.2,
            "MULTIPLIER_BR": 1.0
        }
    }
    
    if os.path.exists(portfolios_file):
        with open(portfolios_file, 'r') as f:
            portfolios = json.load(f)
            return portfolios.get(username, default_portfolio)
    
    return default_portfolio

def save_user_portfolio(username, portfolio):
    """Salva a carteira específica do usuário."""
    portfolios_file = "user_portfolios.json"
    
    # Carrega todas as carteiras
    if os.path.exists(portfolios_file):
        with open(portfolios_file, 'r') as f:
            portfolios = json.load(f)
    else:
        portfolios = {}
    
    # Atualiza a carteira do usuário
    portfolios[username] = portfolio
    
    # Salva
    with open(portfolios_file, 'w') as f:
        json.dump(portfolios, f, indent=2)

def load_users():
    """Carrega usuários do arquivo ou secrets."""
    try:
        # Tenta carregar do Streamlit secrets primeiro
        users_json = st.secrets.get("users", None)
        if users_json:
            return json.loads(users_json)
    except:
        pass
    
    # Se não existir, carrega do arquivo local
    users_file = "users.json"
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return json.load(f)
    
    # Usuário padrão se não existir nada
    return {
        "admin": {
            "password": "investidor2026",
            "name": "Administrador"
        }
    }

def save_users(users):
    """Salva usuários no arquivo local."""
    with open("users.json", 'w') as f:
        json.dump(users, f, indent=2)

def login_register_page():
    """Tela de login e registro."""
    
    st.markdown("""
    # 🤖 Robô de Investimentos
    ## Estratégia de Saída - Análise de Carteira
    """)
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Cadastro"])
    
    # ========== ABA DE LOGIN ==========
    with tab1:
        st.subheader("Acesse sua conta")
        
        with st.form("login_form"):
            username = st.text_input("Usuário", key="login_username")
            password = st.text_input("Senha", type="password", key="login_password")
            submit = st.form_submit_button("Entrar", type="primary", use_container_width=True)
            
            if submit:
                users = load_users()
                
                if username in users and users[username]["password"] == password:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.session_state["user_name"] = users[username]["name"]
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos!")
    
    # ========== ABA DE CADASTRO ==========
    with tab2:
        st.subheader("Criar nova conta")
        
        with st.form("register_form"):
            new_username = st.text_input("Escolha um usuário", key="reg_username")
            new_name = st.text_input("Seu nome completo", key="reg_name")
            new_password = st.text_input("Escolha uma senha", type="password", key="reg_password")
            new_password2 = st.text_input("Confirme a senha", type="password", key="reg_password2")
            register = st.form_submit_button("Cadastrar", type="primary", use_container_width=True)
            
            if register:
                # Validações
                if not new_username or not new_name or not new_password:
                    st.error("❌ Preencha todos os campos!")
                elif new_password != new_password2:
                    st.error("❌ As senhas não coincidem!")
                elif len(new_password) < 6:
                    st.error("❌ A senha deve ter pelo menos 6 caracteres!")
                else:
                    users = load_users()
                    
                    if new_username in users:
                        st.error("❌ Este usuário já existe!")
                    else:
                        # Cria novo usuário
                        users[new_username] = {
                            "password": new_password,
                            "name": new_name
                        }
                        save_users(users)
                        st.success(f"✅ Conta criada com sucesso! Faça login com o usuário: {new_username}")
    
    st.markdown("---")
    st.caption("💡 **Usuário padrão:** admin | **Senha:** investidor2026")

def check_authentication():
    """Verifica se o usuário está autenticado."""
    
    # Se não estiver autenticado, mostra tela de login
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        login_register_page()
        return False
    
    return True

# Verifica autenticação antes de mostrar o app
if not check_authentication():
    st.stop()

# ============================================================================
# APP PRINCIPAL (só executa se autenticado)
# ============================================================================
# SISTEMA DE AUTENTICAÇÃO
# ============================================================================

def check_password():
    """Retorna True se o usuário está autenticado."""
    
    def password_entered():
        """Verifica se a senha está correta."""
        # Tenta pegar do secrets (Streamlit Cloud) ou usa padrão local
        try:
            correct_password = st.secrets["password"]
        except:
            # Senha padrão local: "investidor2026"
            # Hash SHA256 de "investidor2026"
            correct_password = "investidor2026"
        
        if st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Remove senha da sessão
        else:
            st.session_state["password_correct"] = False

    # Primeira execução, mostra tela de login
    if "password_correct" not in st.session_state:
        st.markdown("""
        # 🔒 Área Restrita
        ## Robô de Investimentos - Estratégia de Saída
        
        Digite a senha para acessar seu dashboard de investimentos.
        """)
        
        st.text_input(
            "Senha de Acesso",
            type="password",
            on_change=password_entered,
            key="password",
            help="Senha padrão local: investidor2026"
        )
        
        st.info("💡 **Dica:** Configure sua senha personalizada em Settings > Secrets no Streamlit Cloud")
        return False
    
    # Senha incorreta
    elif not st.session_state["password_correct"]:
        st.markdown("""
        # 🔒 Área Restrita
        ## Robô de Investimentos - Estratégia de Saída
        """)
        
        st.text_input(
            "Senha de Acesso",
            type="password",
            on_change=password_entered,
            key="password"
        )
        st.error("❌ Senha incorreta. Tente novamente.")
        return False
    
    # Senha correta
    else:
        return True

# Verifica autenticação antes de mostrar o app
if not check_authentication():
    st.stop()

# ============================================================================
# CARREGA CARTEIRA DO USUÁRIO LOGADO
# ============================================================================

# Obtém username do usuário logado
current_username = st.session_state.get("username", "admin")

# Carrega a carteira do usuário
user_portfolio = load_user_portfolio(current_username)

# Usa as configurações da carteira do usuário ao invés do config.py
US_STOCKS = user_portfolio.get("US_STOCKS", [])
BR_FIIS = user_portfolio.get("BR_FIIS", [])
TESOURO_DIRETO = user_portfolio.get("TESOURO_DIRETO", {})
PARAMETROS = user_portfolio.get("PARAMETROS", {"MULTIPLIER_US": 1.2, "MULTIPLIER_BR": 1.0})

# Multiplicadores individuais por ticker (opcional)
INDIVIDUAL_MULTIPLIERS = user_portfolio.get("INDIVIDUAL_MULTIPLIERS", {})

# Quantidades de ativos (para cálculo de ganho/perda)
ASSET_QUANTITIES = user_portfolio.get("ASSET_QUANTITIES", {})

# Histórico de operações (compras/vendas)
OPERATIONS_HISTORY = user_portfolio.get("OPERATIONS_HISTORY", [])

# Histórico de snapshots da carteira (para gráfico de evolução)
PORTFOLIO_SNAPSHOTS = user_portfolio.get("PORTFOLIO_SNAPSHOTS", [])

# ============================================================================
# APP PRINCIPAL (só executa se autenticado)
# ============================================================================

# Título e Cabeçalho com informações do usuário
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🤖 Painel de Estratégia de Saída (2026)")
with col2:
    st.markdown(f"### 👤 {st.session_state.get('user_name', 'Usuário')}")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown("""
**Objetivo:** Vender ações e títulos nas próximas 3-4 semanas com o máximo de retorno.
* **Renda Variável:** Usa Volatilidade (ATR) para definir o preço de saída (Stop Loss).
* **Tesouro Direto:** Analisa a tabela regressiva de IR para economizar impostos.
""")

# --- Sistema de Alertas ---
if US_STOCKS or BR_FIIS:
    # Pega dados para análise de alertas
    alerts = []
    
    try:
        if US_STOCKS:
            df_us_alerts = get_market_data(US_STOCKS, PARAMETROS.get("MULTIPLIER_US", 1.2), 
                                          individual_multipliers=INDIVIDUAL_MULTIPLIERS, 
                                          asset_quantities=ASSET_QUANTITIES)
            if not df_us_alerts.empty:
                # Verifica ativos perto do stop (distância < 5%)
                near_stop_us = df_us_alerts[df_us_alerts["Distância Stop (%)"] < 5.0]
                if not near_stop_us.empty:
                    alerts.append(f"🛑 **{len(near_stop_us)} ação(ões) americana(s) perto do stop (<5%)**")
                
                # Verifica ativos que atingiram alvo (potencial < 1%)
                at_target_us = df_us_alerts[df_us_alerts["Potencial"].str.contains("⚠️", na=False) == False]
                at_target_us = at_target_us[pd.to_numeric(at_target_us["Potencial"].str.replace("%", "").str.replace(" ⚠️", ""), errors='coerce') < 1.0]
                if not at_target_us.empty:
                    alerts.append(f"🎯 **{len(at_target_us)} ação(ões) americana(s) próxima(s) do alvo (<1%)**")
        
        if BR_FIIS:
            df_br_alerts = get_market_data(BR_FIIS, PARAMETROS.get("MULTIPLIER_BR", 1.0), 
                                          individual_multipliers=INDIVIDUAL_MULTIPLIERS, 
                                          asset_quantities=ASSET_QUANTITIES)
            if not df_br_alerts.empty:
                near_stop_br = df_br_alerts[df_br_alerts["Distância Stop (%)"] < 5.0]
                if not near_stop_br.empty:
                    alerts.append(f"🛑 **{len(near_stop_br)} FII(s) perto do stop (<5%)**")
    except:
        pass  # Ignora erros na análise de alertas
    
    if alerts:
        st.warning("⚠️ **ALERTAS:** " + " | ".join(alerts))
    else:
        st.success("✅ Nenhum alerta no momento. Todos os ativos estão dentro dos parâmetros.")

# --- Sidebar (Barra Lateral de Controles) ---
st.sidebar.header("⚙️ Painel de Controle")

# Mostra informações do usuário logado
st.sidebar.success(f"✅ Logado como: **{st.session_state.get('username', 'admin')}**")

# --- Sistema de Notificações ---
with st.sidebar.expander("📧 Notificações Diárias", expanded=False):
    st.markdown("""Configure para receber alertas automáticos:""")
    
    enable_notifications = st.checkbox(
        "Ativar notificações",
        value=user_portfolio.get("NOTIFICATIONS", {}).get("enabled", False),
        help="Receba resumo diário da carteira"
    )
    
    if enable_notifications:
        notification_email = st.text_input(
            "Email para alertas:",
            value=user_portfolio.get("NOTIFICATIONS", {}).get("email", ""),
            placeholder="seu@email.com"
        )
        
        notification_time = st.time_input(
            "Horário de envio:",
            value=datetime.strptime(user_portfolio.get("NOTIFICATIONS", {}).get("time", "09:00"), "%H:%M").time()
        )
        
        if st.button("💾 Salvar Configurações", use_container_width=True):
            if not user_portfolio.get("NOTIFICATIONS"):
                user_portfolio["NOTIFICATIONS"] = {}
            
            user_portfolio["NOTIFICATIONS"]["enabled"] = enable_notifications
            user_portfolio["NOTIFICATIONS"]["email"] = notification_email
            user_portfolio["NOTIFICATIONS"]["time"] = notification_time.strftime("%H:%M")
            save_user_portfolio(current_username, user_portfolio)
            st.success("✅ Configurações salvas!")
        
        st.info("""
        📱 **Funcionalidades futuras:**
        - ✉️ Email diário com resumo
        - 💬 WhatsApp via API (Twilio)
        - 🔔 Alertas instantâneos
        
        ⚠️ Requer configuração de servidor SMTP ou API externa.
        """)
    
    if st.button("🧪 Testar Notificação Agora", disabled=not enable_notifications, use_container_width=True):
        if not notification_email:
            st.error("❌ Configure um email para receber as notificações!")
        else:
            with st.spinner("Enviando email de teste..."):
                # Coleta dados para o email
                alertas_teste = []
                resumo_teste = {'total': 0, 'ganho': 0, 'perda': 0}
                
                try:
                    # Verifica alertas reais
                    if US_STOCKS:
                        df_us = get_market_data(US_STOCKS, PARAMETROS.get("MULTIPLIER_US", 1.2), 
                                              individual_multipliers=INDIVIDUAL_MULTIPLIERS, 
                                              asset_quantities=ASSET_QUANTITIES)
                        if not df_us.empty:
                            near_stop = df_us[df_us["Distância Stop (%)"] < 5.0]
                            if not near_stop.empty:
                                for _, row in near_stop.iterrows():
                                    alertas_teste.append(f"🛑 {row['Ticker']} está a {row['Distância Stop (%)']:.1f}% do stop loss")
                    
                    if BR_FIIS:
                        df_br = get_market_data(BR_FIIS, PARAMETROS.get("MULTIPLIER_BR", 1.0), 
                                              individual_multipliers=INDIVIDUAL_MULTIPLIERS, 
                                              asset_quantities=ASSET_QUANTITIES)
                        if not df_br.empty:
                            near_stop = df_br[df_br["Distância Stop (%)"] < 5.0]
                            if not near_stop.empty:
                                for _, row in near_stop.iterrows():
                                    alertas_teste.append(f"🛑 {row['Ticker']} está a {row['Distância Stop (%)']:.1f}% do stop loss")
                    
                    # Calcula resumo real da carteira
                    if PORTFOLIO_SNAPSHOTS:
                        ultimo_snapshot = PORTFOLIO_SNAPSHOTS[-1]
                        resumo_teste = {
                            'total': ultimo_snapshot.get('valor_total', 0),
                            'ganho': ultimo_snapshot.get('ganho_potencial', 0),
                            'perda': ultimo_snapshot.get('perda_potencial', 0)
                        }
                except:
                    # Se houver erro, usa dados de exemplo
                    alertas_teste = ["📊 Sistema de monitoramento ativo"]
                    resumo_teste = {'total': 10000, 'ganho': 500, 'perda': 300}
                
                # Gera HTML e envia
                html = gerar_relatorio_html(
                    st.session_state.get('user_name', 'Usuário'),
                    alertas_teste,
                    resumo_teste
                )
                
                sucesso, mensagem = enviar_email_alerta(
                    notification_email,
                    "🤖 Robô de Investimentos - Teste de Notificação",
                    html
                )
                
                if sucesso:
                    st.success(mensagem + f" Verifique sua caixa de entrada: {notification_email}")
                else:
                    st.error(mensagem)
                    if "EMAIL_PASSWORD" in mensagem:
                        st.info("""
                        📝 **Como configurar:**
                        
                        1. Vá em: https://myaccount.google.com/apppasswords
                        2. Crie uma senha de app para "E-mail"
                        3. No Streamlit Cloud: Settings → Secrets → Adicione:
                        ```
                        EMAIL_PASSWORD = "sua senha de 16 caracteres"
                        ```
                        """)

# Mostra hora da última atualização
st.sidebar.caption(f"🕒 Atualizado: {datetime.now().strftime('%H:%M:%S')}")

# Sliders usando os valores padrão do seu config.py
mult_us = st.sidebar.slider(
    "🇺🇸 Stop Ações EUA (x ATR)", 
    1.0, 3.0, 
    float(PARAMETROS['MULTIPLIER_US']), 
    0.1,
    help="""📊 **Multiplicador do ATR para Stop Loss**
    
    • **ATR** = Average True Range (volatilidade média)
    • **Valores menores** (1.0-1.5x) = Stops mais próximos do preço → Mais sensível, vende mais rápido
    • **Valores maiores** (2.0-3.0x) = Stops mais distantes → Aguenta mais volatilidade
    
    💡 Para saída estratégica em 3-4 semanas, recomenda-se 1.0-1.5x"""
)

mult_br = st.sidebar.slider(
    "🇧🇷 Stop FIIs Brasil (x ATR)", 
    1.0, 3.0, 
    float(PARAMETROS['MULTIPLIER_BR']), 
    0.1,
    help="""📊 **Multiplicador do ATR para Stop Loss (FIIs)**
    
    • FIIs são geralmente menos voláteis que ações
    • **Valores menores** (1.0x) = Stops mais próximos → Proteção conservadora
    • **Valores maiores** (1.5-2.0x) = Stops mais distantes → Permite mais oscilação
    
    💡 FIIs tendem a ter ATR menor, então 1.0-1.5x é adequado"""
)

if st.sidebar.button("🔄 Atualizar Cotações", help="Recarrega os dados do mercado e limpa o cache. Use após salvar configurações ou para obter cotações mais recentes."):
    # Limpa o cache das funções
    st.cache_data.clear()
    # Força atualização da página
    st.rerun()

# --- Editor de Ativos ---
st.sidebar.markdown("---")
st.sidebar.header("📝 Gerenciar Ativos")

with st.sidebar.expander("🇺🇸 Ações e ETFs (EUA)", expanded=False):
    us_stocks_text = st.text_area(
        "Um ticker por linha (ex: AAPL, SPY, QQQ)",
        value="\n".join(US_STOCKS),
        height=100,
        key="us_stocks",
        help="Digite os tickers de ações e ETFs americanos, um por linha. Exemplos de Ações: AAPL, MSFT, NVDA, GOOGL, TSLA. Exemplos de ETFs: SPY, QQQ, VTI, VOO"
    )

with st.sidebar.expander("🇧🇷 FIIs Brasileiros", expanded=False):
    br_fiis_text = st.text_area(
        "Um ticker por linha com .SA (ex: HGLG11.SA)",
        value="\n".join(BR_FIIS),
        height=100,
        key="br_fiis",
        help="Digite os códigos dos FIIs brasileiros com .SA no final. Exemplos: HGLG11.SA, MXRF11.SA, VISC11.SA, KNIP11.SA"
    )

with st.sidebar.expander("💰 Tesouro Direto", expanded=False):
    st.markdown("**Formato:** Nome | Data de Compra")
    st.caption("Exemplo: Tesouro Selic 2027 | 2024-02-15")
    
    tesouro_lines = []
    for nome, dados in TESOURO_DIRETO.items():
        tesouro_lines.append(f"{nome} | {dados['data_compra']}")
    
    tesouro_text = st.text_area(
        "Um título por linha",
        value="\n".join(tesouro_lines),
        height=100,
        key="tesouro",
        help="""💰 **Como preencher:**
        
        Formato: Nome do Título | Data de Compra (AAAA-MM-DD)
        
        Exemplos:
        • Tesouro Selic 2027 | 2024-02-15
        • Tesouro IPCA+ 2035 | 2023-01-10
        • Tesouro Prefixado 2029 | 2024-08-20
        
        O sistema calculará automaticamente a alíquota de IR e recomendará o melhor momento de venda."""
    )

# --- Ajustes Individuais de ATR ---
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Ajustes Individuais (Opcional)")

with st.sidebar.expander("🎯 Multiplicador ATR por Ativo", expanded=False):
    st.markdown("""
    **Personalize o stop de cada ativo individualmente!**
    
    Formato: `TICKER: multiplicador`
    
    Exemplos:
    ```
    AAPL: 1.5
    NVDA: 2.0
    HGLG11: 1.0
    ```
    
    Se não definir, usa o padrão (US ou BR).
    """)
    
    # Converte dicionário em texto editável
    individual_mult_lines = []
    for ticker, mult in INDIVIDUAL_MULTIPLIERS.items():
        individual_mult_lines.append(f"{ticker}: {mult}")
    
    individual_mult_text = st.text_area(
        "Multiplicadores personalizados",
        value="\n".join(individual_mult_lines),
        height=150,
        key="individual_mults",
        help="Deixe em branco para usar os multiplicadores padrão. Defina apenas os tickers que quer personalizar."
    )

# --- Quantidades de Ativos ---
with st.sidebar.expander("📊 Quantidade de Ativos (Opcional)", expanded=False):
    st.markdown("""
    **Cadastre quantas ações/cotas você possui!**
    
    Com isso você verá:
    - 💰 Valor total da posição
    - 🎯 Ganho potencial em $ (se atingir alvos)
    - 🛑 Perda potencial em $ (se acionar stops)
    
    Formato: `TICKER: quantidade`
    
    Exemplos:
    ```
    AAPL: 100
    NVDA: 50
    HGLG11: 200
    ```
    """)
    
    # Converte dicionário em texto editável
    quantity_lines = []
    for ticker, qty in ASSET_QUANTITIES.items():
        quantity_lines.append(f"{ticker}: {qty}")
    
    quantity_text = st.text_area(
        "Quantidades por ticker",
        value="\n".join(quantity_lines),
        height=150,
        key="asset_quantities",
        help="Deixe em branco se não quiser ver cálculos financeiros. Útil para análise de portfólio."
    )

# --- Registrar Operação ---
with st.sidebar.expander("📝 Registrar Operação (Compra/Venda)", expanded=False):
    st.markdown("**Registre suas transações para acompanhar o histórico!**")
    
    col1, col2 = st.columns(2)
    with col1:
        op_type = st.selectbox("Tipo", ["COMPRA", "VENDA"], key="op_type")
    with col2:
        op_ticker = st.text_input("Ticker", key="op_ticker", placeholder="Ex: AAPL").upper()
    
    col3, col4 = st.columns(2)
    with col3:
        op_quantity = st.number_input("Quantidade", min_value=1, value=10, key="op_quantity")
    with col4:
        op_price = st.number_input("Preço", min_value=0.01, value=100.0, step=0.1, key="op_price")
    
    op_date = st.date_input("Data", value=datetime.now(), key="op_date")
    op_notes = st.text_input("Observações (opcional)", key="op_notes", placeholder="Ex: Stop loss acionado")
    
    if st.button("➕ Adicionar Operação", type="primary", use_container_width=True):
        if op_ticker:
            new_operation = {
                "data": op_date.strftime("%Y-%m-%d"),
                "tipo": op_type,
                "ticker": op_ticker,
                "quantidade": op_quantity,
                "preco": op_price,
                "total": op_quantity * op_price,
                "observacoes": op_notes
            }
            
            OPERATIONS_HISTORY.append(new_operation)
            
            # Atualiza quantidade automaticamente
            if op_type == "COMPRA":
                ASSET_QUANTITIES[op_ticker] = ASSET_QUANTITIES.get(op_ticker, 0) + op_quantity
            else:  # VENDA
                ASSET_QUANTITIES[op_ticker] = max(0, ASSET_QUANTITIES.get(op_ticker, 0) - op_quantity)
            
            # Salva imediatamente
            user_portfolio["OPERATIONS_HISTORY"] = OPERATIONS_HISTORY
            user_portfolio["ASSET_QUANTITIES"] = ASSET_QUANTITIES
            save_user_portfolio(current_username, user_portfolio)
            
            st.success(f"✅ Operação registrada: {op_type} {op_quantity} {op_ticker} @ ${op_price:.2f}")
            st.rerun()
        else:
            st.error("❌ Ticker é obrigatório!")

if st.sidebar.button("💾 Salvar Configurações", type="primary", help="Salva sua carteira pessoal (ativos e parâmetros). Seus dados ficam separados de outros usuários."):
    try:
        # Processa ações americanas
        new_us_stocks = [line.strip() for line in us_stocks_text.split('\n') if line.strip()]
        
        # Processa FIIs brasileiros
        new_br_fiis = [line.strip() for line in br_fiis_text.split('\n') if line.strip()]
        
        # Processa Tesouro Direto
        new_tesouro = {}
        for line in tesouro_text.split('\n'):
            if '|' in line:
                parts = line.split('|')
                if len(parts) == 2:
                    nome = parts[0].strip()
                    data = parts[1].strip()
                    new_tesouro[nome] = {'data_compra': data}
        
        # Processa multiplicadores individuais do text area (mantido por compatibilidade)
        new_individual_multipliers = {}
        for line in individual_mult_text.split('\n'):
            line = line.strip()
            if ':' in line:
                try:
                    ticker, mult = line.split(':', 1)
                    ticker = ticker.strip().upper()
                    mult = float(mult.strip())
                    if mult > 0:  # Valida multiplicador positivo
                        new_individual_multipliers[ticker] = mult
                except ValueError:
                    st.sidebar.warning(f"⚠️ Linha ignorada (formato inválido): {line}")
        
        # Captura edições das tabelas (prioridade sobre text area)
        if "edited_us" in st.session_state:
            for _, row in st.session_state["edited_us"].iterrows():
                ticker = row["Ticker"]
                mult = row["ATR Mult."]
                if pd.notna(mult) and mult > 0:
                    new_individual_multipliers[ticker] = float(mult)
        
        if "edited_br" in st.session_state:
            for _, row in st.session_state["edited_br"].iterrows():
                ticker = row["Ticker"]
                mult = row["ATR Mult."]
                if pd.notna(mult) and mult > 0:
                    new_individual_multipliers[ticker] = float(mult)
        
        # Processa quantidades de ativos
        new_asset_quantities = {}
        for line in quantity_text.split('\n'):
            line = line.strip()
            if ':' in line:
                try:
                    ticker, qty = line.split(':', 1)
                    ticker = ticker.strip().upper()
                    qty = int(qty.strip())
                    if qty > 0:  # Valida quantidade positiva
                        new_asset_quantities[ticker] = qty
                except ValueError:
                    st.sidebar.warning(f"⚠️ Linha ignorada (formato inválido): {line}")
        
        # Cria o objeto de carteira do usuário
        user_portfolio = {
            "US_STOCKS": new_us_stocks,
            "BR_FIIS": new_br_fiis,
            "TESOURO_DIRETO": new_tesouro,
            "PARAMETROS": {
                "MULTIPLIER_US": mult_us,
                "MULTIPLIER_BR": mult_br
            },
            "INDIVIDUAL_MULTIPLIERS": new_individual_multipliers,
            "ASSET_QUANTITIES": new_asset_quantities
        }
        
        # Salva a carteira específica deste usuário
        save_user_portfolio(current_username, user_portfolio)
        
        st.sidebar.success("✅ Sua carteira foi salva!")
        st.sidebar.info("Clique em 'Atualizar Cotações' para ver os novos dados")
        
    except Exception as e:
        st.sidebar.error(f"❌ Erro ao salvar: {e}")

# --- Funções de Cálculo ---

@st.cache_data(ttl=300) # Cache de 5 minutos
def get_market_data(tickers, multiplier, individual_multipliers=None, asset_quantities=None):
    """Baixa dados, calcula ATR, RSI e define Stop Loss."""
    if not tickers:
        return pd.DataFrame()
    
    if individual_multipliers is None:
        individual_multipliers = {}
    
    if asset_quantities is None:
        asset_quantities = {}
    
    data_list = []
    errors = []
    
    # Barra de progresso visual
    bar = st.progress(0)
    status_text = st.empty()
    total = len(tickers)
    
    for i, ticker in enumerate(tickers):
        status_text.text(f"Baixando {ticker}... ({i+1}/{total})")
        try:
            # Usa Ticker.history() ao invés de yf.download()
            stock = yf.Ticker(ticker)
            df = stock.history(period="1y")
            
            if df.empty:
                errors.append(f"⚠️ {ticker}: Sem dados disponíveis (ticker inválido?)")
                bar.progress((i + 1) / total)
                continue
                
            # ================================================================
            # CÁLCULOS TÉCNICOS: ATR, SMA e RSI
            # ================================================================
            
            # 1. ATR (Average True Range) - Volatilidade
            df['High-Low'] = df['High'] - df['Low']
            df['High-PrevClose'] = abs(df['High'] - df['Close'].shift(1))
            df['Low-PrevClose'] = abs(df['Low'] - df['Close'].shift(1))
            df['TR'] = df[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)
            df['ATR'] = df['TR'].rolling(window=14).mean()
            
            # 2. SMA (Simple Moving Average) - Tendência
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            
            # 3. RSI (Relative Strength Index) - Força Relativa
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # Verifica se há dados suficientes
            if pd.isna(df['ATR'].iloc[-1]) or pd.isna(df['SMA_20'].iloc[-1]) or pd.isna(df['RSI'].iloc[-1]):
                errors.append(f"⚠️ {ticker}: Dados insuficientes para cálculo (precisa >20 dias)")
                bar.progress((i + 1) / total)
                continue
            
            # ================================================================
            # EXTRAÇÃO DOS VALORES FINAIS
            # ================================================================
            
            last_close = float(df['Close'].iloc[-1])
            last_atr = float(df['ATR'].iloc[-1])
            last_sma = float(df['SMA_20'].iloc[-1])
            last_rsi = float(df['RSI'].iloc[-1])
            
            # Usa multiplicador individual se existir (PRIORIDADE: ajuste manual prevalece sobre sliders)
            ticker_clean = ticker.replace(".SA", "")
            has_manual_adjustment = ticker_clean in individual_multipliers
            current_multiplier = individual_multipliers.get(ticker_clean, multiplier)
            
            # ================================================================
            # TRAVA DE SEGURANÇA AUTOMÁTICA - STOP LOSS INTELIGENTE
            # ================================================================
            # O sistema força automaticamente 1.0x ATR em situações de risco:
            # 1. RSI >= 70 (Sobrecompra/Topo)
            # 2. Tendência de Baixa (Preço < SMA 20)
            
            # Verifica condições de risco
            is_overbought = last_rsi >= 70  # Sobrecompra (possível topo)
            is_downtrend = last_close < last_sma  # Tendência de baixa
            
            # Define RSI Status
            if last_rsi >= 70:
                rsi_status = f"🔥 ALERTA: CARO ({last_rsi:.1f})"
            elif last_rsi <= 30:
                rsi_status = f"❄️ Barato ({last_rsi:.1f})"
            else:
                rsi_status = f"Neutro ({last_rsi:.1f})"
            
            # LÓGICA DE SEGURANÇA: Força 1.0x se houver risco
            if is_overbought or is_downtrend:
                stop_multiplier = 1.0
                
                # Identifica o motivo da proteção automática
                reasons = []
                if is_overbought:
                    reasons.append("RSI≥70")
                if is_downtrend:
                    reasons.append("Baixa")
                
                mult_display = f"1.0x 🛡️ ({', '.join(reasons)})"
            else:
                # Nenhum risco detectado: usa multiplicador configurado
                stop_multiplier = current_multiplier
                
                if has_manual_adjustment:
                    mult_display = f"{stop_multiplier:.1f}x ✏️"  # Ajuste manual
                else:
                    mult_display = f"{stop_multiplier:.1f}x"  # Slider padrão
            
            # ================================================================
            # CÁLCULO DE PREÇOS ESTRATÉGICOS
            # ================================================================
            
            # Stop Loss (Gatilho de Venda para limitar perdas)
            stop_price = last_close - (last_atr * stop_multiplier)
            
            # Take Profit / Alvo de Lucro (Projeção de alta baseada em volatilidade)
            # Usa 2.0x ATR para capturar movimentos significativos de alta
            gain_target = last_close + (last_atr * 2.0)
            
            # Potencial de Ganho até o alvo
            gain_potential_value = ((gain_target - last_close) / last_close) * 100
            
            # Tendência baseada na SMA
            tendencia = "🟢 Alta" if last_close > last_sma else "🔴 Baixa"
            
            # Aviso visual de contra-tendência (padrão do mercado)
            if last_close < last_sma:  # Tendência de baixa
                gain_potential_display = f"{gain_potential_value:.1f}% ⚠️"
            else:
                gain_potential_display = f"{gain_potential_value:.1f}%"
            
            # ATR como porcentagem do preço (mais prático para decisões)
            atr_percent = (last_atr / last_close) * 100
            
            # ================================================================
            # CÁLCULOS FINANCEIROS (se quantidade informada)
            # ================================================================
            
            quantity = asset_quantities.get(ticker_clean, 0)
            
            if quantity > 0:
                position_value = last_close * quantity
                gain_if_target = (gain_target - last_close) * quantity
                loss_if_stop = (last_close - stop_price) * quantity
            else:
                position_value = 0
                gain_if_target = 0
                loss_if_stop = 0
            
            # ================================================================
            # ADICIONA AO RESULTADO
            # ================================================================
            
            data_list.append({
                "Ticker": ticker_clean,
                "Qtd": quantity if quantity > 0 else "-",
                "Valor Posição": position_value if quantity > 0 else "-",
                "Preço Atual": last_close,
                "ATR %": atr_percent,  # Volatilidade percentual
                "RSI (Termômetro)": rsi_status,
                "Stop Loss Sugerido": stop_price,
                "Alvo (Gain)": gain_target,
                "Potencial": gain_potential_display,  # Com aviso visual
                "Ganho se Alvo": gain_if_target if quantity > 0 else "-",
                "Perda se Stop": loss_if_stop if quantity > 0 else "-",
                "Distância Stop (%)": ((last_close - stop_price) / last_close) * 100,
                "ATR Mult. ⚙️": mult_display,  # Mostra origem do multiplicador (Auto/Manual/Slider)
                "Tendência": tendencia,
                "Histórico": df['Close'], # Salva para o gráfico
                # DEBUG INFO
                "_RSI_Valor": last_rsi,
                "_ATR_Absoluto": last_atr,
                "_Mult_Config": current_multiplier,
                "_Mult_Usado_Stop": stop_multiplier,
                "_Stop_Calc": f"{last_close:.2f} - ({last_atr:.2f} × {stop_multiplier}) = {stop_price:.2f}"
            })
            
        except Exception as e:
            errors.append(f"❌ {ticker}: {str(e)}")
            
        bar.progress((i + 1) / total)
        
    bar.empty()
    status_text.empty()
    
    # Mostra erros se houver
    if errors:
        with st.expander(f"⚠️ Problemas ao baixar {len(errors)} ticker(s)", expanded=True):
            for error in errors:
                st.warning(error)
    
    return pd.DataFrame(data_list)

def analyze_taxes(carteira):
    """Analisa dias regressivos do IR."""
    results = []
    hoje = datetime.now()
    
    for titulo, dados in carteira.items():
        compra = datetime.strptime(dados['data_compra'], "%Y-%m-%d")
        dias = (hoje - compra).days
        
        # Tabela Regressiva
        if dias <= 180:
            aliq, prox_aliq, dias_muda = 22.5, 20.0, 181 - dias
        elif dias <= 360:
            aliq, prox_aliq, dias_muda = 20.0, 17.5, 361 - dias
        elif dias <= 720:
            aliq, prox_aliq, dias_muda = 17.5, 15.0, 721 - dias
        else:
            aliq, prox_aliq, dias_muda = 15.0, 15.0, 0
            
        msg = "✅ Venda Liberada"
        cor = "green"
        
        if dias_muda > 0 and dias_muda <= 30:
            msg = f"🚨 AGUARDE {dias_muda} DIAS (Imposto cai de {aliq}% para {prox_aliq}%)"
            cor = "red"
        
        results.append({
            "Título": titulo,
            "Dias Investidos": dias,
            "Alíquota Hoje": f"{aliq}%",
            "Status": msg,
            "Cor": cor
        })
    return pd.DataFrame(results)

# --- EXECUÇÃO DO LAYOUT ---

# 1. Análise de Ações e FIIs
st.header("📊 Renda Variável: Ações e FIIs")

# Explicação dos indicadores
with st.expander("❓ Como interpretar a tabela", expanded=False):
    st.markdown("""
    ### � Colunas da Tabela
    
    | Coluna | Significado |
    |--------|-------------|
    | **Ticker** | Código do ativo |
    | **Qtd** | Quantidade de ações/cotas que você possui |
    | **Valor Posição** | Valor total investido (Qtd × Preço Atual) |
    | **Preço Atual** | Último preço de fechamento |
    | **ATR %** | Volatilidade diária média (<2% estável, >5% volátil) |
    | **RSI** | 🔥 Caro (>70) / ❄️ Barato (<30) / Neutro (30-70) |
    | **Stop Loss 🛑** | Preço de saída para limitar perdas |
    | **Alvo (Gain) 🎯** | Meta de lucro projetada |
    | **Ganho $ 🎯** | Lucro em $ se atingir o alvo |
    | **Perda $ 🛑** | Perda em $ se acionar o stop |
    | **Potencial** | Ganho % até o alvo (⚠️ = contra tendência) |
    | **Tendência** | 🟢 Alta (acima SMA 20) / 🔴 Baixa (abaixo SMA 20) |
    | **ATR Mult.** | Ajuste individual do stop (editável) |
    
    ---
    
    ### 💡 Dicas Rápidas:
    - **RSI > 70 (Caro):** Sistema aplica automaticamente stop 1.0x ATR para proteger lucros
    - **Ajuste manual:** Clique duplo em "ATR Mult." para personalizar cada ativo
    - **Sliders do painel:** Não afetam ativos com ajuste manual
    """)

# Renda Variável EUA (Ações e ETFs)
st.subheader("🇺🇸 Renda Variável EUA (Ações e ETFs)")
st.caption("💡 **Dica:** RSI > 70 ativa stop 1.0x ATR automaticamente (salvo ajuste manual). Clique duplo em 'ATR Mult.' para personalizar.")
if US_STOCKS:
    st.caption(f"📊 Analisando {len(US_STOCKS)} ticker(s): {', '.join(US_STOCKS)}")
    
    # DEBUG: Mostra os tickers carregados
    with st.expander("🔍 Debug: Tickers Carregados", expanded=False):
        st.json({"US_STOCKS": US_STOCKS, "Total": len(US_STOCKS)})
    
    # BUSCA OS DADOS DO MERCADO
    df_us = get_market_data(US_STOCKS, mult_us, individual_multipliers=INDIVIDUAL_MULTIPLIERS, asset_quantities=ASSET_QUANTITIES)
    
    if not df_us.empty:
        # DEBUG COMPLETO: Mostra cálculos detalhados
        with st.expander("🐛 DEBUG COMPLETO: Cálculos RSI e Stop Loss", expanded=True):
            st.warning("**Esta seção mostra os cálculos internos para debug**")
            
            debug_df = df_us[["Ticker", "_RSI_Valor", "_ATR_Absoluto", "_Mult_Config", "_Mult_Usado_Stop", "_Stop_Calc"]].copy()
            debug_df.columns = ["Ticker", "RSI (número)", "ATR ($)", "Mult. Configurado", "Mult. Usado no Stop", "Cálculo do Stop"]
            
            st.dataframe(
                debug_df,
                use_container_width=True,
                hide_index=True
            )
            
            st.info("""
            **Legenda:**
            - **RSI (número):** Valor numérico do RSI (≥70 = CARO deve forçar 1.0x)
            - **ATR ($):** Valor absoluto do ATR em dólares
            - **Mult. Configurado:** Seu ajuste manual ou slider (o que você configurou)
            - **Mult. Usado no Stop:** O multiplicador realmente usado (deveria ser 1.0 se RSI ≥ 70)
            - **Cálculo do Stop:** Fórmula completa do cálculo
            
            🔍 **Verifique:** Se RSI ≥ 70 mas "Mult. Usado no Stop" não é 1.0, há um bug!
            """)
        
        # Define quais colunas mostrar (depende se tem quantidades cadastradas)
        has_quantities = any(df_us["Qtd"] != "-")
        
        if has_quantities:
            display_columns = ["Ticker", "Qtd", "Valor Posição", "Preço Atual", "ATR %", "RSI (Termômetro)", 
                             "Stop Loss Sugerido", "Alvo (Gain)", "Ganho se Alvo", "Perda se Stop", 
                             "Potencial", "Tendência", "ATR Mult. ⚙️"]
        else:
            display_columns = ["Ticker", "Preço Atual", "ATR %", "RSI (Termômetro)", 
                             "Stop Loss Sugerido", "Alvo (Gain)", "Potencial", "Distância Stop (%)", 
                             "Tendência", "ATR Mult. ⚙️"]
        
        # Configura colunas editáveis
        edited_df_us = st.data_editor(
            df_us[display_columns],
            use_container_width=True,
            column_config={
                "Ticker": st.column_config.TextColumn("Ticker", disabled=True),
                "Qtd": st.column_config.TextColumn("Qtd", disabled=True),
                "Valor Posição": st.column_config.NumberColumn(
                    "Valor Posição",
                    format="$%.0f",
                    help="Valor total investido neste ativo (Quantidade × Preço Atual)",
                    disabled=True
                ),
                "Preço Atual": st.column_config.NumberColumn(
                    "Preço Atual",
                    format="$%.1f",
                    disabled=True
                ),
                "ATR %": st.column_config.NumberColumn(
                    "Volatilidade (ATR) %",
                    format="%.1f%%",
                    help="Oscilação diária média. <2% = estável, 2-5% = moderado, >5% = volátil.",
                    disabled=True
                ),
                "RSI (Termômetro)": st.column_config.TextColumn("RSI (Termômetro)", disabled=True),
                "Stop Loss Sugerido": st.column_config.NumberColumn(
                    "Stop Loss 🛑",
                    format="$%.1f",
                    help="Preço de venda automática para limitar perdas. RSI > 70 ajusta para 1.0x ATR.",
                    disabled=True
                ),
                "Alvo (Gain)": st.column_config.NumberColumn(
                    "Alvo (Gain) 🎯",
                    format="$%.1f",
                    help="Preço alvo de lucro (2.0x ATR acima do preço atual). Meta de venda estratégica.",
                    disabled=True
                ),
                "Ganho se Alvo": st.column_config.NumberColumn(
                    "Ganho $ 🎯",
                    format="$%.0f",
                    help="Lucro em dólares se atingir o alvo (Quantidade × Diferença de preço)",
                    disabled=True
                ),
                "Perda se Stop": st.column_config.NumberColumn(
                    "Perda $ 🛑",
                    format="$%.0f",
                    help="Perda em dólares se acionar o stop (Quantidade × Diferença de preço)",
                    disabled=True
                ),
                "Potencial": st.column_config.TextColumn(
                    "Potencial 📈",
                    help="Ganho % se atingir o alvo. ⚠️ = Contra tendência de baixa (operação mais arriscada).",
                    disabled=True
                ),
                "Distância Stop (%)": st.column_config.NumberColumn(
                    "Risco (%)",
                    format="%.1f%%",
                    help="Distância percentual até o stop loss (quanto pode cair antes de vender).",
                    disabled=True
                ),
                "Tendência": st.column_config.TextColumn("Tendência", disabled=True),
                "ATR Mult. ⚙️": st.column_config.TextColumn(
                    "ATR Mult. ⚙️",
                    help="🛡️ 1.0x (RSI≥70, Baixa) = Proteção automática | ✏️ = Ajuste manual | Sem ícone = Slider padrão",
                    disabled=True
                ),
            },
            num_rows="fixed",
            hide_index=True,
            key="editor_us"
        )
        # Armazena no session_state para salvar depois
        st.session_state["edited_us"] = edited_df_us
    else:
        st.warning("Nenhum dado disponível para ações americanas")
else:
    st.info("Adicione tickers em config.py")

st.markdown("---")  # Separador visual

# FIIs Brasileiros
st.subheader("🇧🇷 FIIs Brasileiros")
st.caption("💡 **Dica:** RSI > 70 ativa stop automático em 1.0x ATR (proteção de lucro). Edite 'ATR Mult.' para personalizar.")
if BR_FIIS:
    st.caption(f"📊 Analisando {len(BR_FIIS)} ticker(s): {', '.join(BR_FIIS)}")
    df_br = get_market_data(BR_FIIS, mult_br, individual_multipliers=INDIVIDUAL_MULTIPLIERS, asset_quantities=ASSET_QUANTITIES)
    if not df_br.empty:
        # Define quais colunas mostrar (depende se tem quantidades cadastradas)
        has_quantities_br = any(df_br["Qtd"] != "-")
        
        if has_quantities_br:
            display_columns_br = ["Ticker", "Qtd", "Valor Posição", "Preço Atual", "ATR %", "RSI (Termômetro)", 
                                 "Stop Loss Sugerido", "Alvo (Gain)", "Ganho se Alvo", "Perda se Stop", 
                                 "Potencial", "Tendência", "ATR Mult. ⚙️"]
        else:
            display_columns_br = ["Ticker", "Preço Atual", "ATR %", "RSI (Termômetro)", 
                                 "Stop Loss Sugerido", "Alvo (Gain)", "Potencial", "Distância Stop (%)", 
                                 "Tendência", "ATR Mult. ⚙️"]
        
        # Configura colunas editáveis
        edited_df_br = st.data_editor(
            df_br[display_columns_br],
            use_container_width=True,
            column_config={
                "Ticker": st.column_config.TextColumn("Ticker", disabled=True),
                "Qtd": st.column_config.TextColumn("Qtd", disabled=True),
                "Valor Posição": st.column_config.NumberColumn(
                    "Valor Posição",
                    format="R$ %.0f",
                    help="Valor total investido neste ativo (Quantidade × Preço Atual)",
                    disabled=True
                ),
                "Preço Atual": st.column_config.NumberColumn(
                    "Preço Atual",
                    format="R$ %.1f",
                    disabled=True
                ),
                "ATR %": st.column_config.NumberColumn(
                    "Volatilidade (ATR) %",
                    format="%.1f%%",
                    help="Oscilação diária média. <2% = estável, 2-5% = moderado, >5% = volátil.",
                    disabled=True
                ),
                "RSI (Termômetro)": st.column_config.TextColumn("RSI (Termômetro)", disabled=True),
                "Stop Loss Sugerido": st.column_config.NumberColumn(
                    "Stop Loss 🛑",
                    format="R$ %.1f",
                    help="Preço de venda automática para limitar perdas. RSI > 70 ajusta para 1.0x ATR.",
                    disabled=True
                ),
                "Alvo (Gain)": st.column_config.NumberColumn(
                    "Alvo (Gain) 🎯",
                    format="R$ %.1f",
                    help="Preço alvo de lucro (2.0x ATR acima do preço atual). Meta de venda estratégica.",
                    disabled=True
                ),
                "Ganho se Alvo": st.column_config.NumberColumn(
                    "Ganho R$ 🎯",
                    format="R$ %.0f",
                    help="Lucro em reais se atingir o alvo (Quantidade × Diferença de preço)",
                    disabled=True
                ),
                "Perda se Stop": st.column_config.NumberColumn(
                    "Perda R$ 🛑",
                    format="R$ %.0f",
                    help="Perda em reais se acionar o stop (Quantidade × Diferença de preço)",
                    disabled=True
                ),
                "Potencial": st.column_config.TextColumn(
                    "Potencial 📈",
                    help="Ganho % se atingir o alvo. ⚠️ = Contra tendência de baixa (operação mais arriscada).",
                    disabled=True
                ),
                "Distância Stop (%)": st.column_config.NumberColumn(
                    "Risco (%)",
                    format="%.1f%%",
                    help="Distância percentual até o stop loss (quanto pode cair antes de vender).",
                    disabled=True
                ),
                "Tendência": st.column_config.TextColumn("Tendência", disabled=True),
                "ATR Mult. ⚙️": st.column_config.TextColumn(
                    "ATR Mult. ⚙️",
                    help="🛡️ 1.0x (RSI≥70, Baixa) = Proteção automática | ✏️ = Ajuste manual | Sem ícone = Slider padrão",
                    disabled=True
                ),
            },
            num_rows="fixed",
            hide_index=True,
            key="editor_br"
        )
        # Armazena no session_state para salvar depois
        st.session_state["edited_br"] = edited_df_br
    else:
        st.warning("Nenhum dado disponível para FIIs")
else:
    st.info("Adicione FIIs em config.py")

# --- Resumo Financeiro ---
if ASSET_QUANTITIES:
    st.markdown("---")
    st.header("💰 Resumo da Carteira")
    
    # Combina dataframes US e BR
    dfs_to_combine = []
    if US_STOCKS and 'df_us' in locals() and not df_us.empty:
        dfs_to_combine.append(df_us)
    if BR_FIIS and 'df_br' in locals() and not df_br.empty:
        dfs_to_combine.append(df_br)
    
    if dfs_to_combine:
        df_combined = pd.concat(dfs_to_combine, ignore_index=True)
        
        # Filtra apenas ativos com quantidade
        df_with_qty = df_combined[df_combined["Qtd"] != "-"].copy()
        
        if not df_with_qty.empty:
            # Calcula totais
            total_invested = df_with_qty["Valor Posição"].sum()
            total_gain_if_target = df_with_qty["Ganho se Alvo"].sum()
            total_loss_if_stop = df_with_qty["Perda se Stop"].sum()
            
            # Relação risco/retorno
            if total_loss_if_stop > 0:
                risk_reward_ratio = total_gain_if_target / total_loss_if_stop
            else:
                risk_reward_ratio = 0
            
            # Exibe resumo em colunas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="📊 Valor Total Investido",
                    value=f"${total_invested:,.0f}" if US_STOCKS else f"R$ {total_invested:,.0f}",
                    help="Soma do valor atual de todas as posições"
                )
            
            with col2:
                st.metric(
                    label="🎯 Ganho Potencial Total",
                    value=f"${total_gain_if_target:,.0f}" if US_STOCKS else f"R$ {total_gain_if_target:,.0f}",
                    delta=f"+{(total_gain_if_target/total_invested)*100:.1f}%",
                    help="Lucro se todos os ativos atingirem seus alvos"
                )
            
            with col3:
                st.metric(
                    label="🛑 Perda Máxima Total",
                    value=f"${total_loss_if_stop:,.0f}" if US_STOCKS else f"R$ {total_loss_if_stop:,.0f}",
                    delta=f"-{(total_loss_if_stop/total_invested)*100:.1f}%",
                    delta_color="inverse",
                    help="Perda se todos os stops forem acionados"
                )
            
            with col4:
                st.metric(
                    label="📈 Relação Risco/Retorno",
                    value=f"{risk_reward_ratio:.2f}:1",
                    help="Quanto você pode ganhar para cada R$1 de risco"
                )
            
            st.info("💡 **Dica:** Uma relação risco/retorno > 2:1 é considerada boa para swing trading.")
            
            # Salva snapshot da carteira para o gráfico de evolução
            today = datetime.now().strftime("%Y-%m-%d")
            snapshot_exists = any(s["data"] == today for s in PORTFOLIO_SNAPSHOTS)
            
            if not snapshot_exists:
                new_snapshot = {
                    "data": today,
                    "valor_total": float(total_invested),
                    "ganho_potencial": float(total_gain_if_target),
                    "perda_potencial": float(total_loss_if_stop)
                }
                PORTFOLIO_SNAPSHOTS.append(new_snapshot)
                user_portfolio["PORTFOLIO_SNAPSHOTS"] = PORTFOLIO_SNAPSHOTS
                save_user_portfolio(current_username, user_portfolio)

# --- Histórico de Operações ---
if OPERATIONS_HISTORY:
    st.markdown("---")
    st.header("📝 Histórico de Operações")
    
    df_operations = pd.DataFrame(OPERATIONS_HISTORY)
    df_operations = df_operations.sort_values("data", ascending=False)
    
    # Formata para exibição
    df_operations_display = df_operations.copy()
    df_operations_display["Data"] = pd.to_datetime(df_operations_display["data"]).dt.strftime("%d/%m/%Y")
    df_operations_display["Tipo"] = df_operations_display["tipo"]
    df_operations_display["Ticker"] = df_operations_display["ticker"]
    df_operations_display["Qtd"] = df_operations_display["quantidade"]
    df_operations_display["Preço"] = df_operations_display["preco"].apply(lambda x: f"${x:.2f}")
    df_operations_display["Total"] = df_operations_display["total"].apply(lambda x: f"${x:.2f}")
    df_operations_display["Observações"] = df_operations_display["observacoes"]
    
    st.dataframe(
        df_operations_display[["Data", "Tipo", "Ticker", "Qtd", "Preço", "Total", "Observações"]],
        use_container_width=True,
        hide_index=True
    )
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Limpar Histórico", help="Remove todas as operações registradas", type="secondary"):
            user_portfolio["OPERATIONS_HISTORY"] = []
            save_user_portfolio(current_username, user_portfolio)
            st.success("✅ Histórico limpo!")
            st.rerun()

# --- Gráfico de Evolução da Carteira ---
if PORTFOLIO_SNAPSHOTS and len(PORTFOLIO_SNAPSHOTS) >= 1:
    st.markdown("---")
    st.header("📈 Evolução da Carteira")
    
    if len(PORTFOLIO_SNAPSHOTS) == 1:
        st.info("💡 Primeiro registro salvo! Continue usando o sistema para acompanhar a evolução ao longo do tempo.")
    
    df_snapshots = pd.DataFrame(PORTFOLIO_SNAPSHOTS)
    df_snapshots["data"] = pd.to_datetime(df_snapshots["data"])
    df_snapshots = df_snapshots.sort_values("data")
    
    # Calcula valores projetados
    df_snapshots["Valor Alvo"] = df_snapshots["valor_total"] + df_snapshots["ganho_potencial"]
    df_snapshots["Valor Stop"] = df_snapshots["valor_total"] - df_snapshots["perda_potencial"]
    
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    # Linha principal - Valor atual
    fig.add_trace(go.Scatter(
        x=df_snapshots["data"],
        y=df_snapshots["valor_total"],
        mode='lines+markers',
        name='Valor Investido',
        line=dict(color='blue', width=3),
        marker=dict(size=8)
    ))
    
    # Linha de alvo
    fig.add_trace(go.Scatter(
        x=df_snapshots["data"],
        y=df_snapshots["Valor Alvo"],
        mode='lines',
        name='Se Atingir Alvos',
        line=dict(color='green', width=2, dash='dash')
    ))
    
    # Linha de stop
    fig.add_trace(go.Scatter(
        x=df_snapshots["data"],
        y=df_snapshots["Valor Stop"],
        mode='lines',
        name='Se Acionar Stops',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    # Marcadores de operações
    if OPERATIONS_HISTORY:
        df_ops = pd.DataFrame(OPERATIONS_HISTORY)
        df_ops["data"] = pd.to_datetime(df_ops["data"])
        
        # Merge com snapshots para pegar valor da carteira na data
        df_ops_plot = df_ops.merge(df_snapshots[["data", "valor_total"]], on="data", how="left")
        
        compras = df_ops_plot[df_ops_plot["tipo"] == "COMPRA"]
        vendas = df_ops_plot[df_ops_plot["tipo"] == "VENDA"]
        
        if not compras.empty:
            fig.add_trace(go.Scatter(
                x=compras["data"],
                y=compras["valor_total"],
                mode='markers',
                name='Compras',
                marker=dict(size=12, color='green', symbol='triangle-up', line=dict(width=2, color='darkgreen'))
            ))
        
        if not vendas.empty:
            fig.add_trace(go.Scatter(
                x=vendas["data"],
                y=vendas["valor_total"],
                mode='markers',
                name='Vendas',
                marker=dict(size=12, color='red', symbol='triangle-down', line=dict(width=2, color='darkred'))
            ))
    
    fig.update_layout(
        title="Evolução do Valor da Carteira ao Longo do Tempo",
        xaxis_title="Data",
        yaxis_title="Valor ($)",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("💡 **Dica:** O gráfico é atualizado automaticamente a cada acesso. Triângulos verdes = compras, vermelhos = vendas.")

# 2. Otimização Fiscal
st.header("💰 Tesouro Direto: Análise de IR")

# Explicação da tabela regressiva
with st.expander("❓ Como funciona a tributação do Tesouro Direto", expanded=False):
    st.markdown("""
    ### 📖 Tabela Regressiva de IR
    
    O Imposto de Renda sobre o Tesouro Direto **diminui com o tempo:**
    
    | Período Investido | Alíquota de IR |
    |-------------------|----------------|
    | Até 180 dias      | 22,5% 😰       |
    | 181 a 360 dias    | 20,0% 😐       |
    | 361 a 720 dias    | 17,5% 😊       |
    | Acima de 720 dias | 15,0% 😃       |
    
    ### 💡 Estratégia de Otimização
    
    - 🚨 **AGUARDE** → Se faltam menos de 30 dias para a próxima faixa, vale a pena esperar!
    - ✅ **Pode vender** → Se está longe da próxima mudança ou já está na menor alíquota (15%).
    
    **Exemplo:** Um título com 355 dias investidos está a apenas 6 dias de cair de 20% para 17,5%. 
    Esperar economiza 2,5% do rendimento!
    """)

if TESOURO_DIRETO:
    df_tesouro = analyze_taxes(TESOURO_DIRETO)
    
    for _, row in df_tesouro.iterrows():
        if row['Cor'] == 'red':
            st.error(f"**{row['Título']}** - {row['Status']}")
        else:
            st.success(f"**{row['Título']}** - {row['Status']}")
    
    st.dataframe(
        df_tesouro[["Título", "Dias Investidos", "Alíquota Hoje", "Status"]],
        use_container_width=True
    )
else:
    st.info("Adicione títulos do Tesouro Direto em config.py")

# 3. Rodapé
st.markdown("---")
st.caption("📅 Dados atualizados automaticamente. Cache de 5 minutos.")