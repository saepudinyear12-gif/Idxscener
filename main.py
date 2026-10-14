import os
import asyncio
import pandas as pd
import yfinance as yf
from telegram import Bot

# Langsung dimasukkan ke sini karena repositori Anda Private
TELEGRAM_BOT_TOKEN = "8986896789:AAHls6ixUUTFSOaotL4ATnKoYVt04yIW0"
TELEGRAM_CHAT_ID = "1768576462"

# Daftar emiten IDX yang ingin dipindai (bisa Anda tambah/kurangi)
WATCHLIST = [
    "TLKM.JK", "BBCA.JK", "BBRI.JK", "BMRI.JK", "ASII.JK", 
    "PGAS.JK", "UNVR.JK", "ADRO.JK", "ANTM.JK", "ICBP.JK"
]

def check_stock_signal(ticker_symbol):
    try:
        df = yf.download(ticker_symbol, period="60d", interval="1d", progress=False)
        if len(df) < 30:
            return None

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['Vol_MA20'] = df['Volume'].rolling(window=20).mean()

        # MACD (12, 26, 9)
        ema12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema26 = df['Close'].ewm(span=26, adjust=False).mean()
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = macd_line - signal_line

        # RSI (14)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0
                      
