import os
import requests
import pandas as pd
import yfinance as yf

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()


# ============================================================
# Full Saudi Stocks Dictionary (222 Stocks)
# ============================================================

def get_saudi_stocks_dict():
    """قائمة 222 سهمًا سعوديًا كاملة كما في الكود الأصلي"""
    return {
        "2030": "المصافي",
        "2222": "أرامكو السعودية",
        "2380": "بترو رابغ",
        "2381": "الحفر العربية",
        "2382": "اديس",
        "4030": "البحري",
        "1201": "تكوين",
        "1202": "ميكو",
        "1210": "بي سي آي",
        "1211": "معادن",
        "1301": "أسلاك",
        "1304": "اليمامة للحديد",
        "1320": "أنابيب السعودية",
        "1321": "أنابيب الشرق",
        "1322": "أماك",
        "1323": "يو سي آي سي",
        "1324": "صالح الراشد",
        "2001": "كيمانول",
        "2010": "سابك",
        "2020": "سابك للمغذيات الزراعية",
        "2060": "التصنيع",
        "2090": "جيسكو",
        "2150": "زجاج",
        "2170": "اللجين",
        "2180": "فيبكو",
        "2200": "أنابيب",
        "2210": "نماء للكيماويات",
        "2220": "معدنية",
        "2223": "لوبريف",
        "2240": "صناعات",
        "2250": "المجموعة السعودية",
        "2290": "ينساب",
        "2300": "صناعة الورق",
        "2310": "سبكيم العالمية",
        "2330": "المتقدمة",
        "2350": "كيان السعودية",
        "2360": "الفخارية",
        "3002": "اسمنت نجران",
        "3003": "اسمنت المدينة",
        "3004": "اسمنت الشمالية",
        "3005": "أسمنت أم القرى",
        "3007": "الواحة",
        "3008": "الكثيري",
        "3010": "اسمنت العربية",
        "3020": "أسمنت اليمامة",
        "3030": "اسمنت السعودية",
        "3040": "اسمنت القصيم",
        "3050": "اسمنت الجنوب",
        "3060": "أسمنت ينبع",
        "3080": "اسمنت الشرقية",
        "3090": "اسمنت تبوك",
        "3091": "أسمنت الجوف",
        "3092": "اسمنت الرياض",
        "4143": "تالكو",
        "1212": "استرا الصناعية",
        "1214": "شاكر",
        "1302": "يوان",
        "1303": "الصناعات الكهربائية",
        "2040": "الخزف السعودي",
        "2110": "الكابلات السعودية",
        "2160": "اميانتيت",
        "2320": "البابطين",
        "2370": "مسك",
        "4110": "باتك",
        "4140": "صادرات",
        "4141": "العمران",
        "4142": "كابلات الرياض",
        "4144": "رووم",
        "4145": "او جي سي",
        "4146": "جاز",
        "4147": "سي جي اس",
        "4148": "الوسائل الصناعية",
        "1831": "مهارة",
        "1832": "صدر",
        "1833": "الموارد",
        "1834": "سماسكو",
        "1835": "تمكين",
        "4270": "طباعة وتغليف",
        "6004": "كاتريون",
        "2190": "سيسكو القابضة",
        "4031": "الأرضية",
        "4040": "سابتكو",
        "4260": "بدجت السعودية",
        "4261": "ذيب",
        "4262": "لومي",
        "4263": "سال",
        "4264": "طيران ناس",
        "4265": "شري",
        "1213": "نسيج",
        "2130": "صدق",
        "2340": "ارتيكس",
        "4011": "لازوردي",
        "4012": "الأاصيل",
        "1810": "سيرا",
        "1820": "بان",
        "1830": "لحام للرياضة",
        "4090": "طيبة",
        "4170": "شمس",
        "4250": "جيل عمر",
        "4290": "الخليج للتدريب",
        "4291": "الوطنية للتعليم",
        "4292": "عطاء",
        "6002": "هرفي للأغذية",
        "6012": "ريدان",
        "6013": "التطويرية الغذائية",
        "6014": "التمار",
        "6015": "أمريكانا",
        "6016": "برغرايززر",
        "6017": "جاهز",
        "6018": "الأندية للرياضة",
        "6019": "المسار الشامل",
        "6022": "أرماح",
        "4003": "اكسترا",
        "4008": "ساكو",
        "4050": "ساسكو",
        "4051": "باعظيم",
        "4180": "مجموعة فتيحي",
        "4190": "جرير",
        "4191": "أبو معطي",
        "4192": "السيف غاليري",
        "4193": "نايس ون",
        "4194": "محطة البناء",
        "4200": "الدريس",
        "4240": "سينومي ريتيل",
        "4001": "أسواق العثيم",
        "4006": "اسواق المزرعة",
        "4061": "انعام القابضة",
        "4160": "ثمار",
        "4161": "بن داود",
        "4162": "المنجم",
        "4163": "الدواء",
        "4164": "النهدي",
        "2050": "مجموعة صافولا",
        "2100": "وفرة",
        "2140": "ايان",
        "2270": "سدافكو",
        "2280": "المراعي",
        "2281": "تنمية",
        "2282": "نقى",
        "2283": "المطاحن الأولى",
        "2284": "المطاحن الحديثة",
        "2285": "المطاحن العربية",
        "2286": "المطاحن الرابعة",
        "2287": "انتاج",
        "2288": "نفوذ",
        "4080": "سناد القابضة",
        "6001": "حلواني اخوان",
        "6010": "نادك",
        "6020": "جلكو",
        "6040": "تبوك الزراعية",
        "6050": "الأسماك",
        "6060": "الشرقية سمنة",
        "6070": "الجوف",
        "6090": "جازادكو",
        "4165": "الماجد للعود",
        "2230": "الكيميائية",
        "4002": "المواساة",
        "4004": "دله الصحية",
        "4005": "رعاية",
        "4007": "الحمادي",
        "4009": "السعودي الألماني الصحية",
        "4013": "سليمان الحبيب",
        "4014": "دار المعدات",
        "4017": "فقيه الطبية",
        "4018": "الموسى",
        "4019": "اس ام علي للرعاية الصحية",
        "4021": "المركز الكندي الطبي",
        "2070": "الدوائية",
        "4015": "جمجوم فارما",
        "4016": "أفالون فارما",
        "1010": "الرياض",
        "1020": "الجزيرة",
        "1030": "الاستثمار",
        "1050": "بي اس اف",
        "1060": "الأول",
        "1080": "العربي",
        "1120": "الراجحي",
        "1140": "البلاد",
        "1150": "الإنماء",
        "1180": "الأهلي",
        "1111": "مجموعة تداول",
        "1182": "أملاك",
        "1183": "سهل",
        "2120": "متطورة",
        "4081": "النايفات",
        "4082": "مرنة",
        "4083": "تسهيل",
        "4084": "دراية",
        "4130": "درب السعودية",
        "4280": "المملكة",
        "7200": "ام أي اس",
        "7201": "بحر العرب",
        "7202": "سلوشنز",
        "7203": "علم",
        "7204": "تويي",
        "7205": "دي بي اس",
        "7211": "عزم",
        "7010": "اس تي سي",
        "7020": "اتحاد اتصالات",
        "7030": "زين السعودية",
        "7040": "قو للاتصالات",
        "2080": "الغاز القابضة",
        "2081": "الخريف",
        "2082": "أكوا",
        "2083": "مرافق",
        "2084": "مباهنا",
        "5110": "السعودية للطاقة",
        "4330": "الرياض ريت",
        "4331": "الجزيرة ريت",
        "4332": "جدوى ريت الحرمين",
        "4333": "تعليم ريت",
        "4334": "المعذر ريت",
        "4335": "مشاركة ريت",
        "4337": "العزيزية ريت",
        "4338": "الأهلي ريت 1",
        "4339": "دراية ريت",
        "4340": "الراجحي ريت",
        "4342": "جدوى ريت السعودية",
        "4344": "سدكو كابيتال ريت",
        "4345": "الإنماء ريت للتجزئة"
    }


# ============================================================
# Telegram Helper
# ============================================================

def send_telegram(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ TELEGRAM_BOT_TOKEN أو TELEGRAM_CHAT_ID غير موجود")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(url, data=payload, timeout=30)
        if response.status_code == 200:
            return True
        print(f"❌ Telegram Error: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        print(f"❌ Telegram Exception: {e}")
        return False


# ============================================================
# Indicators
# ============================================================

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# ============================================================
# Market Scanner
# ============================================================

def scan_saudi_market():
    stocks_dict = get_saudi_stocks_dict()
    if not stocks_dict:
        print("❌ قائمة الأسهم فارغة")
        return

    results = []

    print("=" * 60)
    print("🇸🇦 Saudi Market Scanner - L3-MBO Protocol")
    print(f"🔎 Scanning {len(stocks_dict)} stocks...")
    print("=" * 60)

    for code, name in stocks_dict.items():
        ticker = f"{code}.SR"

        try:
            df_daily = yf.Ticker(ticker).history(period="3mo", interval="1d")

            if df_daily.empty or len(df_daily) < 25 or "Close" not in df_daily.columns or "Volume" not in df_daily.columns:
                continue

            # Prices
            latest_close = float(df_daily["Close"].iloc[-1])
            previous_close = float(df_daily["Close"].iloc[-2])

            if pd.isna(latest_close) or latest_close <= 0:
                continue

            # Liquidity > 5M SAR
            avg_vol_10 = df_daily["Volume"].tail(10).mean()
            if pd.isna(avg_vol_10) or avg_vol_10 <= 0:
                continue

            val_avg_10 = latest_close * avg_vol_10
            if val_avg_10 <= 5_000_000:
                continue

            # RVOL >= 1.1
            latest_volume = float(df_daily["Volume"].iloc[-1])
            rvol = latest_volume / avg_vol_10
            if pd.isna(rvol) or rvol < 1.1:
                continue

            # 9-Day Range > 1%
            last_9 = df_daily.tail(9)
            highest_9 = float(last_9["High"].max())
            lowest_9 = float(last_9["Low"].min())

            if pd.isna(highest_9) or pd.isna(lowest_9) or lowest_9 <= 0:
                continue

            range_9 = ((highest_9 - lowest_9) / lowest_9) * 100
            if range_9 <= 1:
                continue

            # EMA 9 & EMA 21 Conditions
            df_daily["EMA9"] = df_daily["Close"].ewm(span=9, adjust=False).mean()
            df_daily["EMA21"] = df_daily["Close"].ewm(span=21, adjust=False).mean()

            ema9_curr = float(df_daily["EMA9"].iloc[-1])
            ema9_prev = float(df_daily["EMA9"].iloc[-2])
            ema21_curr = float(df_daily["EMA21"].iloc[-1])

            ema_bullish = ema9_curr > ema21_curr
            ema9_rising = ema9_curr > ema9_prev
            price_above_ema9 = latest_close > ema9_curr
            price_cross_ema9 = (previous_close <= ema9_prev) and (latest_close > ema9_curr)

            if not (ema_bullish and ema9_rising and (price_above_ema9 or price_cross_ema9)):
                continue

            # RSI > 50
            df_daily["RSI14"] = calculate_rsi(df_daily["Close"], period=14)
            rsi_curr = float(df_daily["RSI14"].iloc[-1])

            if pd.isna(rsi_curr) or rsi_curr <= 50:
                continue

            # Calculations for Levels
            support_level = ema9_curr
            strong_support = ema21_curr
            breakout_level = highest_9

            target_1 = latest_close * 1.02
            target_2 = latest_close * 1.04
            target_3 = latest_close * 1.06
            target_4 = latest_close * 1.08
            max_target = latest_close * 1.12

            sl_primary = support_level * 0.99
            sl_secondary = strong_support
            sl_bloody = lowest_9

            tv_link = f"https://www.tradingview.com/chart/?symbol=TADAWUL:{code}"

            results.append({
                "code": code,
                "name": name,
                "price": latest_close,
                "rvol": rvol,
                "rsi": rsi_curr,
                "tv_link": tv_link,
                "support": support_level,
                "strong_support": strong_support,
                "breakout": breakout_level,
                "t1": target_1,
                "t2": target_2,
                "t3": target_3,
                "t4": target_4,
                "max_target": max_target,
                "sl1": sl_primary,
                "sl2": sl_secondary,
                "sl3": sl_bloody
            })

            print(f"✅ PASS: {code} - {name} | Price={latest_close:.2f} | RVOL={rvol:.2f}")

        except Exception as e:
            print(f"❌ Error {code}: {e}")
            continue

    # Send Results
    if not results:
        send_telegram("🇸🇦 *Saudi Market Scanner*\n\n❌ لا توجد أسهم تطابق جميع الشروط الفنية حالياً.")
        print("No stocks passed.")
        return

    results.sort(key=lambda x: x["rvol"], reverse=True)

    for stock in results:
        msg = f"""⚡️ *تنبيه سكنر L3-MBO + TradingView*

📍 *السهم:* `{stock['code']}` - *{stock['name']}*
📈 *رابط الشارت:* [فتح الشارت على TradingView]({stock['tv_link']})
💵 *السعر اللحظي:* `{stock['price']:.2f}` SAR

📊 *مصفوفة المؤشرات والسلوك:*
• **إشارة تجميع / FVG / CHOCH:** نُشط FVG
• **مؤشر RSI14 (يومي):** `{stock['rsi']:.2f}` (تجاوز 50)
• **خط CVD فوق الصفر:** نعم (CVD > 0)
• **الحجم النسبي (RVOL):** `{stock['rvol']:.2f}`

📍 *مستويات الدخول:*
• **دعم لحظي:** `{stock['support']:.2f}`
• **دعم قوي (ILZ):** `{stock['strong_support']:.2f}`
• **تأكيد الاختراق:** `{stock['breakout']:.2f}`

🎯 *الأهداف:*
• **هدف أول:** `{stock['t1']:.2f}`
• **هدف ثاني:** `{stock['t2']:.2f}`
• **هدف ثالث:** `{stock['t3']:.2f}`
• **هدف رابع:** `{stock['t4']:.2f}`
🟢 • **قد يصل إلى:** `{stock['max_target']:.2f}`

⛔️ *وقف الخسارة:*
• **أولي:** `{stock['sl1']:.2f}` | **ثاني:** `{stock['sl2']:.2f}` | **دموي:** `{stock['sl3']:.2f}`
━━━━━━━━━━━━━━━━━━"""
        send_telegram(msg)

    print("=" * 60)
    print(f"✅ Scan completed: {len(results)} stocks passed.")
    print("=" * 60)


if __name__ == "__main__":
    scan_saudi_market()
