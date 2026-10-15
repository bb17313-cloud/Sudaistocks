import sys
import time
import pandas as pd
import yfinance as yf

# ==========================================
# إعدادات الأسهم وقائمة المتابعة
# ==========================================
# ضع هنا جميع الأسهم التي ترغب بفحصها (بما في ذلك سهم نما 2210.SR)
TICKERS = [
    '2210.SR',  # نما للكيماويات
    '2030.SR',  # مثال لسهم آخر
    # أضف باقي الأسهم هنا...
]

PERIOD = "30d"        # فترة البيانات المطلوبة
MAX_RETRIES = 5       # عدد محاولات إعادة الجلب عند الفشل
RETRY_DELAY = 6       # الانتظار بالثواني بين كل محاولة وأخرى


def fetch_stock_data_strict(ticker, period=PERIOD, max_retries=MAX_RETRIES, delay=RETRY_DELAY):
    """
    دالة صارمة لجلب بيانات السهم مع محاولات متعددة.
    تتوقف وترفض إكمال التشغيل (تمنع التخطي الصامت) إذا فشل السهم نهائياً،
    لضمان عدم تفويت أي سهم موجود في القائمة.
    """
    for attempt in range(1, max_retries + 1):
        try:
            print(f"[{ticker}] جاري محاولة الجلب (محاولة {attempt}/{max_retries})...")
            
            # جلب البيانات من yfinance
            data = yf.download(ticker, period=period, progress=False, timeout=15)
            
            # معالجة تنسيق الأعمدة الحديث في yfinance إذا لزم الأمر
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
                
            # التحقق من وجود بيانات صالحة وغير فارغة
            if data is not None and not data.empty and 'Close' in data.columns:
                print(f"[{ticker}] تم بنجاح جلب البيانات وصحتها.")
                return data
            else:
                print(f"[{ticker}] تنبيه: البيانات المُسترجعة فارغة أو غير مكتملة.")
                
        except Exception as e:
            print(f"[{ticker}] خطأ في الاتصال أو استثناء (محاولة {attempt}): {e}")
        
        if attempt < max_retries:
            print(f"الانتظار لمدة {delay} ثوانٍ قبل إعادة محاولة السهم {ticker}...")
            time.sleep(delay)
            
    # في حال استنفاد جميع المحاولات، يتم إيقاف السكربت بالكامل لعدم تجاوز السهم
    raise RuntimeError(
        f"فشل ذريع: تعذر نهائياً جلب بيانات السهم الأساسي ({ticker}) بعد {max_retries} محاولات. "
        f"تم إيقاف التشغيل لمنع تخطي أي سهم."
    )


def main():
    print("=" * 50)
    print("بدء تشغيل سكربت فحص الأسهم مع حماية كاملة ضد التخطي...")
    print("=" * 50)
    
    market_data = {}
    
    # حلقة مروره على الأسهم تضمن معالجة كل سهم على حدة
    for ticker in TICKERS:
        try:
            df = fetch_stock_data_strict(ticker)
            market_data[ticker] = df
            
            # مثال بسيط لتحليل آخر إغلاق (يمكنك استبداله بمنطق السكربت الخاص بك)
            last_close = df['Close'].iloc[-1]
            print(f"-> السهم {ticker} | آخر سعر إغلاق: {last_close}\n")
            
            # فاصل زمني قصير بين الأسهم لتقليل الضغط على المصدر وتجنب الحظر
            time.sleep(2)
            
        except Exception as err:
            print(f"\n[خطأ حرج]: {err}")
            # إيقاف التنفيذ بالكامل بناءً على طلبك بعدم تخطي أي سهم
            sys.exit(1)

    print("=" * 50)
    print("تمت معالجة جميع الأسهم بنجاح تام ودون أي تخطي!")
    print("=" * 50)
    
    # ضع هنا باقي كود الاستراتيجية، إرسال التنبيهات لـ Telegram، إلخ...


if __name__ == "__main__":
    main()
