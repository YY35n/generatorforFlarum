import requests
import json
import time

BASE_URL = "https://cnnewyorker.com"  # 替换成你的域名，无斜杠
INPUT_FILE = "accounts1.txt"
OUTPUT_FILE = "accounts.json"

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
            "userId": data.get("userId"),
            "token": data.get("token")
        }
    except Exception as e:
        print(f"[❌] {email} 登录失败: {e}")
        return None

def main():
    tokens = {}
    with open(INPUT_FILE, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line or ',' not in line:
            continue
        email, password = line.split(',', 1)
        print(f"🔑 正在获取: {email}")
        result = get_token(email.strip(), password.strip())
        if result:
            tokens[email] = result
        time.sleep(1)  # 可选：避免触发防火墙限制

    with open(OUTPUT_FILE, "w") as f:
        json.dump(tokens, f, indent=2)
    print(f"\n✅ 所有 token 已保存到 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
