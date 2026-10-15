import os
import sys
import time
import pandas as pd
import yfinance as yf
import requests

# ==========================================
# إعدادات تيليجرام (سحبها من متغيرات البيئة تلقائياً)
# ==========================================
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    """دالة لإرسال الرسائل عبر تيليجرام مع التحقق من النجاح"""
    if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
        print("خطأ: توكن تيليجرام أو معرف المحادثة غير متاح في متغيرات البيئة.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        res_data = response.json()
        if response.status_code == 200 and res_data.get("ok"):
            print("تم إرسال التقرير إلى تيليجرام بنجاح.")
        else:
            print(f"فشل إرسال التنبيه لتيليجرام: {res_data}")
    except Exception as e:
        print(f"خطأ في الاتصال بتيليجرام: {e}")

# ==========================================
# إعدادات الأسهم وقائمة المتابعة
# ==========================================
TICKERS = [
    '2210.SR',  # نما للكيماويات
    '2030.SR',  # مثال لسهم آخر
]

PERIOD = "30d"        
MAX_RETRIES = 5       
RETRY_DELAY = 6       


def fetch_stock_data_strict(ticker, period=PERIOD, max_retries=MAX_RETRIES, delay=RETRY_DELAY):
    """دالة صارمة لجلب بيانات السهم مع محاولات متعددة لمنع التخطي"""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"[{ticker}] جاري محاولة الجلب (محاولة {attempt}/{max_retries})...")
            data = yf.download(ticker, period=period, progress=False, timeout=15)
            
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
                
            if data is not None and not data.empty and 'Close' in data.columns:
                print(f"[{ticker}] تم بنجاح جلب البيانات وصحتها.")
                return data
            else:
                print(f"[{ticker}] تنبيه: البيانات المُسترجعة فارغة.")
                
        except Exception as e:
            print(f"[{ticker}] خطأ في الاتصال (محاولة {attempt}): {e}")
        
        if attempt < max_retries:
            time.sleep(delay)
            
    raise RuntimeError(f"فشل ذريع: تعذر نهائياً جلب بيانات السهم الأساسي ({ticker}).")


def main():
    print("بدء تشغيل سكربت الفحص والإرسال...")
    
    signals_to_send = []
    
    for ticker in TICKERS:
        try:
            df = fetch_stock_data_strict(ticker)
            last_close = df['Close'].iloc[-1]
            
            # صياغة رسالة السهم
            msg = f"📈 *تحديث السهم:* `{ticker}`\n💰 *السعر الحالي:* `{last_close:.2f}`"
            signals_to_send.append(msg)
            
            time.sleep(2)
            
        except Exception as err:
            error_msg = f"❌ *خطأ حرج في السهم {ticker}:* {err}"
            print(error_msg)
            send_telegram_message(error_msg)
            sys.exit(1)

    # إرسال النتائج عبر تيليجرام دفعة واحدة
    if signals_to_send:
        full_report = "🚀 *تقرير فحص الأسهم اليومي*\n\n" + "\n\n".join(signals_to_send)
        send_telegram_message(full_report)

if __name__ == "__main__":
    main()
