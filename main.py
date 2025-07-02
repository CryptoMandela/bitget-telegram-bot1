import requests

BOT_TOKEN = "7721157216:AAFizSoWsqxKSYtHBcG_6wx4aD89glvT000"
CHAT_ID = "961904906"
SELL_PRICE = 1570  # Change to your current Telegram price

def fetch_bitget_price():
    url = "https://www.bitget.com/api/p2p/v2/merchantAdvert/page"
    payload = {
        "coin": "USDT",
        "currency": "NGN",
        "payType": "",
        "side": "BUY",
        "authType": "",
        "userType": "",
        "page": 1,
        "size": 1
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bitget.com",
        "Origin": "https://www.bitget.com"
    }

    res = requests.post(url, json=payload, headers=headers)
    if res.status_code != 200 or not res.text.startswith('{'):
        send_alert("❌ Bitget returned invalid data or blocked request.")
        return

    data = res.json()
    try:
        price = float(data["data"]["data"][0]["price"])
        profit = SELL_PRICE - price

        if profit >= 20:
            message = f"📊 Bitget P2P USDT Buy: ₦{price}\n💵 Your Sell Price: ₦{SELL_PRICE}\n💰 Profit/USDT: ₦{profit:.2f}"
            send_alert(message)
        else:
            print(f"No alert. Profit only ₦{profit:.2f}")
    except:
        send_alert("⚠️ Failed to parse Bitget price data.")

def send_alert(message):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(telegram_url, data=payload)

fetch_bitget_price()
