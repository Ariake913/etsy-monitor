import requests
import os
import json

# ===== 環境変数 =====
ETSY_API_KEY = os.environ["ETSY_API_KEY"]
SHOP_ID = os.environ["SHOP_ID"]

PUSHOVER_TOKEN = os.environ["PUSHOVER_TOKEN"]
PUSHOVER_USER = os.environ["PUSHOVER_USER"]

STATE_FILE = "state.json"


# ===== Etsy 訪問者数取得 =====
#def get_visits():
#    url = f"https://openapi.etsy.com/v3/application/shops/{SHOP_ID}/stats"
#    headers = {
#        "x-api-key": ETSY_API_KEY
#    }
#
#    r = requests.get(url, headers=headers)
#    data = r.json()
#
#    # visits を取得（API仕様によりキー名変わる場合あり）
#    return data["results"]["visits"]

def get_visits():
    url = f"https://openapi.etsy.com/v3/application/shops/{SHOP_ID}/stats"
    headers = {
        "x-api-key": ETSY_API_KEY
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    print(data)   # ← これ追加（超重要）

    return 0

# ===== 前回値読み込み =====
def load_previous():
    if not os.path.exists(STATE_FILE):
        return 0
    with open(STATE_FILE, "r") as f:
        return json.load(f)["visits"]


# ===== 保存 =====
def save_current(visits):
    with open(STATE_FILE, "w") as f:
        json.dump({"visits": visits}, f)


# ===== Pushover通知 =====
def send_push(message):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "message": message,
        },
    )


# ===== メイン処理 =====
def main():
    current = get_visits()
    previous = load_previous()

    if current > previous:
        diff = current - previous
        send_push(f"Etsy visits increased +{diff} (Total: {current})")

    save_current(current)


if __name__ == "__main__":
    main()
