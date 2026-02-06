"""
Módulo de Análise de Bitcoin
Fornece análise técnica, tendência e sinais de compra/venda
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import ssl
import os

# Desabilita verificação SSL (necessário em algumas redes corporativas)
ssl._create_default_https_context = ssl._create_unverified_context

# Configurações adicionais para yfinance
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['CURL_CA_BUNDLE'] = ''

def obter_dados_bitcoin(periodo="3mo"):
    """
    Obtém dados históricos do Bitcoin
    
    Args:
        periodo: Período de dados ('1mo', '3mo', '6mo', '1y', '2y')
    
    Returns:
        DataFrame com dados históricos ou None em caso de erro
    """
    try:
        btc = yf.Ticker("BTC-USD")
        
        # Configura sessão para desabilitar verificação SSL
        import curl_cffi.requests
        session = curl_cffi.requests.Session(verify=False)
        btc.session = session
        
        df = btc.history(period=periodo)
        return df
    except ImportError:
        # Se curl_cffi não estiver disponível, usa método padrão
        try:
            btc = yf.Ticker("BTC-USD")
            df = btc.history(period=periodo)
            return df
        except Exception as e:
            print(f"Erro ao obter dados do Bitcoin: {e}")
            return None
    except Exception as e:
        print(f"Erro ao obter dados do Bitcoin: {e}")
        return None

def calcular_rsi(df, periodo=14):
    """
    Calcula o RSI (Relative Strength Index)
    
    Args:
        df: DataFrame com coluna 'Close'
        periodo: Período para cálculo do RSI
    
    Returns:
        Series com valores do RSI
    """
    delta = df['Close'].diff()
    ganho = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
    perda = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
    
    rs = ganho / perda
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calcular_macd(df, rapido=12, lento=26, sinal=9):
    """
    Calcula o MACD (Moving Average Convergence Divergence)
    
    Args:
        df: DataFrame com coluna 'Close'
        rapido: Período EMA rápida
        lento: Período EMA lenta
        sinal: Período da linha de sinal
    
    Returns:
        Tupla (macd_line, signal_line, histogram)
    """
    exp1 = df['Close'].ewm(span=rapido, adjust=False).mean()
    exp2 = df['Close'].ewm(span=lento, adjust=False).mean()
    
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=sinal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram

def calcular_medias_moveis(df, periodos=[20, 50, 200]):
    """
    Calcula médias móveis simples
    
    Args:
        df: DataFrame com coluna 'Close'
        periodos: Lista de períodos para calcular
    
    Returns:
        Dicionário com as médias móveis
    """
    medias = {}
    for periodo in periodos:
        if len(df) >= periodo:
            medias[f'SMA_{periodo}'] = df['Close'].rolling(window=periodo).mean().iloc[-1]
        else:
            medias[f'SMA_{periodo}'] = None
    return medias

def calcular_bandas_bollinger(df, periodo=20, num_std=2):
    """
    Calcula as Bandas de Bollinger
    
    Args:
        df: DataFrame com coluna 'Close'
        periodo: Período para média móvel
        num_std: Número de desvios padrão
    
    Returns:
        Tupla (banda_superior, banda_media, banda_inferior)
    """
    sma = df['Close'].rolling(window=periodo).mean()
    std = df['Close'].rolling(window=periodo).std()
    
    banda_superior = sma + (std * num_std)
    banda_media = sma
    banda_inferior = sma - (std * num_std)
    
    return banda_superior, banda_media, banda_inferior

def analisar_tendencia(df):
    """
    Analisa a tendência do Bitcoin baseado em múltiplos indicadores
    
    Args:
        df: DataFrame com dados históricos
    
    Returns:
        Dicionário com análise completa
    """
    if df is None or len(df) < 50:
        return None
    
    # Preço atual e variações
    preco_atual = df['Close'].iloc[-1]
    preco_ontem = df['Close'].iloc[-2] if len(df) > 1 else preco_atual
    var_dia = ((preco_atual - preco_ontem) / preco_ontem) * 100
    
    preco_semana = df['Close'].iloc[-7] if len(df) > 7 else preco_atual
    var_semana = ((preco_atual - preco_semana) / preco_semana) * 100
    
    preco_mes = df['Close'].iloc[-30] if len(df) > 30 else preco_atual
    var_mes = ((preco_atual - preco_mes) / preco_mes) * 100
    
    # Indicadores técnicos
    rsi = calcular_rsi(df).iloc[-1]
    macd_line, signal_line, histogram = calcular_macd(df)
    macd_atual = macd_line.iloc[-1]
    sinal_atual = signal_line.iloc[-1]
    hist_atual = histogram.iloc[-1]
    
    # Médias móveis
    medias = calcular_medias_moveis(df)
    
    # Bandas de Bollinger
    bb_superior, bb_media, bb_inferior = calcular_bandas_bollinger(df)
    bb_sup_atual = bb_superior.iloc[-1]
    bb_inf_atual = bb_inferior.iloc[-1]
    
    # Volatilidade (desvio padrão dos últimos 30 dias)
    volatilidade = df['Close'].tail(30).std()
    volatilidade_pct = (volatilidade / preco_atual) * 100
    
    # Volume
    volume_medio = df['Volume'].tail(20).mean()
    volume_atual = df['Volume'].iloc[-1]
    volume_relativo = (volume_atual / volume_medio) * 100 if volume_medio > 0 else 100
    
    # Análise de sinais
    sinais = []
    score = 0  # Score de -100 (forte venda) a +100 (forte compra)
    
    # Análise RSI
    if rsi < 30:
        sinais.append({"indicador": "RSI", "sinal": "COMPRA", "forca": "FORTE", "valor": f"{rsi:.1f}"})
        score += 30
    elif rsi < 40:
        sinais.append({"indicador": "RSI", "sinal": "COMPRA", "forca": "MODERADA", "valor": f"{rsi:.1f}"})
        score += 15
    elif rsi > 70:
        sinais.append({"indicador": "RSI", "sinal": "VENDA", "forca": "FORTE", "valor": f"{rsi:.1f}"})
        score -= 30
    elif rsi > 60:
        sinais.append({"indicador": "RSI", "sinal": "VENDA", "forca": "MODERADA", "valor": f"{rsi:.1f}"})
        score -= 15
    else:
        sinais.append({"indicador": "RSI", "sinal": "NEUTRO", "forca": "NEUTRO", "valor": f"{rsi:.1f}"})
    
    # Análise MACD
    if macd_atual > sinal_atual and hist_atual > 0:
        sinais.append({"indicador": "MACD", "sinal": "COMPRA", "forca": "MODERADA", "valor": f"{hist_atual:.2f}"})
        score += 20
    elif macd_atual < sinal_atual and hist_atual < 0:
        sinais.append({"indicador": "MACD", "sinal": "VENDA", "forca": "MODERADA", "valor": f"{hist_atual:.2f}"})
        score -= 20
    else:
        sinais.append({"indicador": "MACD", "sinal": "NEUTRO", "forca": "NEUTRO", "valor": f"{hist_atual:.2f}"})
    
    # Análise Médias Móveis
    if medias.get('SMA_50') and medias.get('SMA_200'):
        if medias['SMA_50'] > medias['SMA_200'] and preco_atual > medias['SMA_50']:
            sinais.append({"indicador": "Médias Móveis", "sinal": "COMPRA", "forca": "FORTE", "valor": "Golden Cross"})
            score += 25
        elif medias['SMA_50'] < medias['SMA_200'] and preco_atual < medias['SMA_50']:
            sinais.append({"indicador": "Médias Móveis", "sinal": "VENDA", "forca": "FORTE", "valor": "Death Cross"})
            score -= 25
        elif preco_atual > medias['SMA_50']:
            sinais.append({"indicador": "Médias Móveis", "sinal": "COMPRA", "forca": "MODERADA", "valor": "Acima MM50"})
            score += 10
        elif preco_atual < medias['SMA_50']:
            sinais.append({"indicador": "Médias Móveis", "sinal": "VENDA", "forca": "MODERADA", "valor": "Abaixo MM50"})
            score -= 10
    
    # Análise Bandas de Bollinger
    if preco_atual < bb_inf_atual:
        sinais.append({"indicador": "Bollinger", "sinal": "COMPRA", "forca": "FORTE", "valor": "Abaixo banda inferior"})
        score += 25
    elif preco_atual > bb_sup_atual:
        sinais.append({"indicador": "Bollinger", "sinal": "VENDA", "forca": "FORTE", "valor": "Acima banda superior"})
        score -= 25
    
    # Análise de Volume
    if volume_relativo > 150:
        sinais.append({"indicador": "Volume", "sinal": "ATENÇÃO", "forca": "ALTA", "valor": f"{volume_relativo:.0f}% da média"})
        # Volume alto intensifica o sinal atual
        score = score * 1.2 if score != 0 else score
    
    # Determinar recomendação final
    if score > 40:
        recomendacao = "COMPRA FORTE"
        emoji = "🟢🟢"
    elif score > 15:
        recomendacao = "COMPRA"
        emoji = "🟢"
    elif score < -40:
        recomendacao = "VENDA FORTE"
        emoji = "🔴🔴"
    elif score < -15:
        recomendacao = "VENDA"
        emoji = "🔴"
    else:
        recomendacao = "NEUTRO"
        emoji = "🟡"
    
    # Determinar tendência
    if var_mes > 10 and var_semana > 5:
        tendencia = "ALTA FORTE"
        emoji_tendencia = "📈📈"
    elif var_mes > 0 and var_semana > 0:
        tendencia = "ALTA"
        emoji_tendencia = "📈"
    elif var_mes < -10 and var_semana < -5:
        tendencia = "BAIXA FORTE"
        emoji_tendencia = "📉📉"
    elif var_mes < 0 and var_semana < 0:
        tendencia = "BAIXA"
        emoji_tendencia = "📉"
    else:
        tendencia = "LATERAL"
        emoji_tendencia = "➡️"
    
    # Máxima e mínima do período
    maxima_52w = df['High'].tail(252).max() if len(df) >= 252 else df['High'].max()
    minima_52w = df['Low'].tail(252).min() if len(df) >= 252 else df['Low'].min()
    dist_maxima = ((preco_atual - maxima_52w) / maxima_52w) * 100
    dist_minima = ((preco_atual - minima_52w) / minima_52w) * 100
    
    return {
        "preco_atual": preco_atual,
        "var_dia": var_dia,
        "var_semana": var_semana,
        "var_mes": var_mes,
        "rsi": rsi,
        "macd": macd_atual,
        "sinal_macd": sinal_atual,
        "histogram_macd": hist_atual,
        "medias_moveis": medias,
        "bollinger_superior": bb_sup_atual,
        "bollinger_inferior": bb_inf_atual,
        "volatilidade": volatilidade_pct,
        "volume_relativo": volume_relativo,
        "sinais": sinais,
        "score": score,
        "recomendacao": recomendacao,
        "emoji_recomendacao": emoji,
        "tendencia": tendencia,
        "emoji_tendencia": emoji_tendencia,
        "maxima_52w": maxima_52w,
        "minima_52w": minima_52w,
        "dist_maxima": dist_maxima,
        "dist_minima": dist_minima,
        "ultima_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

def obter_analise_completa():
    """
    Obtém análise completa do Bitcoin
    
    Returns:
        Dicionário com todos os dados e análises
    """
    df = obter_dados_bitcoin(periodo="1y")
    if df is None:
        return None
    
    analise = analisar_tendencia(df)
    if analise:
        analise['dataframe'] = df
    
    return analise
