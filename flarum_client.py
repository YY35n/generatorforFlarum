# flarum_client.py
import requests
import json
import random
from config import FLARUM_URL, ACCOUNTS_PATH

def load_accounts():
    with open(ACCOUNTS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)  
def choose_random_account():
    return random.choice(load_accounts())

def post_to_flarum(title, content, account, tag_id):
    url = f"{FLARUM_URL}/api/discussions"
    headers = {
        "Authorization": f"Token {account['token']}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.api+json"
    }
    payload = {
        "data": {
            "type": "discussions",
            "attributes": {"title": title, "content": content},
            "relationships": {
                "tags": {"data": [{"type": "tags", "id": str(tag_id)}]}
            }
        }
    }
    res = requests.post(url, headers=headers, json=payload)
    print("发帖状态：", res.status_code, res.text)

def reply_to_discussion(discussion_id, content, account):
    url = f"{FLARUM_URL}/api/posts"
    headers = {
        "Authorization": f"Token {account['token']}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.api+json"
    }
    payload = {
        "data": {
            "type": "posts",
            "attributes": {"content": content},
            "relationships": {
                "discussion": {"data": {"type": "discussions", "id": str(discussion_id)}}
            }
        }
    }
    res = requests.post(url, headers=headers, json=payload)
    print("回帖状态：", res.status_code, res.text)
