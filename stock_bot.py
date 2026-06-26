import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

# ✅ 台股清單（先給你常見+流動性高）
stocks = [
      "2330.TW", "2317.TW", "2454.TW", "2308.TW", "2881.TW",
      "2882.TW", "1301.TW", "1303.TW", "2002.TW", "2603.TW",
      "2609.TW", "2615.TW", "3034.TW", "3711.TW", "2891.TW"
  ]

results = []

for ticker in stocks:
    try:  
          df = yf.download(ticker, period="3mo", progress=False)

        if df.empty or len(df) < 30:
              continue
          
        # === 指標 ===
        df['MA5'] = df['Close'].rolling(5).mean()
        df['MA20'] = df['Close'].rolling(20).mean()

        rsi = RSIIndicator(df['Close'], window=14)
        df['RSI'] = rsi.rsi()

        macd = MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['Signal'] = macd.macd_signal()

        last = df.iloc[-1]
        prev = df.iloc[-2]

        score = 0

        # ✅ 條件打分
        if last['RSI'] < 30:
            score += 2
        if last['MA5'] > last['MA20']:
            score += 2
        if last['Close'] > prev['Close']:
            score += 1
        if last['MACD'] > last['Signal']:
            score += 2

        results.append({
            "股票": ticker,
            "收盤價": round(last['Close'], 2),    
            "RSI": round(last['RSI'], 2),
            "分數": score  
        })   
    except Exception as e:
       print(f"{ticker} 錯誤: {e}")
# ✅ 排序
df_result = pd.DataFrame(results)
top10 = df_result.sort_values(by="分數", ascending=False).head(10)

print("🔥 今日最強10檔股票 🔥")
print(top10)
