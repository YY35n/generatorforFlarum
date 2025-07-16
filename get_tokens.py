import requests
import json
import time

BASE_URL = "https://cnnewyorker.com"  # ← 你的 Flarum 域名，无斜杠
INPUT_FILE = "accounts1.txt"          # ← 每行格式: email,password
OUTPUT_FILE = "accounts.json"         # ← 输出为 list 格式

def get_token(email, password):
    url = f"{BASE_URL}/api/token"
    payload = {
        "identification": email,
        "password": password
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "username": email,
            "userId": data.get("userId"),
            "token": data.get("token")
        }
    except Exception as e:
        print(f"[❌] 登录失败：{email} → {e}")
        return None

def main():
    result = []
    seen = set()

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or ',' not in line:
            continue

        email, password = [part.strip() for part in line.split(',', 1)]
        if email in seen:
            continue
        seen.add(email)

        print(f"🔐 登录中: {email}")
        token_data = get_token(email, password)
        if token_data:
            result.append(token_data)
        time.sleep(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✅ 共 {len(result)} 个 token 已保存到 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
