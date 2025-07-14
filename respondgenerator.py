# respond_generator.py
import requests
import random
from openai import OpenAI
from config import FLARUM_URL, DEEPSEEK_API_KEY
from flarum_client import choose_random_account, reply_to_discussion

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def fetch_discussion(discussion_id):
    url = f"{FLARUM_URL}/api/discussions/{discussion_id}"
    return requests.get(url).json()

def generate_reply(title, content):
    prompt = f"""你是一个论坛用户，正在回复这个话题：
标题：{title}
内容：{content}

请写一条有共鸣、有价值的中文回复，不少于30字。
"""
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个中文论坛用户，擅长高质量回帖。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=400
    )
    return resp.choices[0].message.content.strip()

def run_reply(discussion_id, num_replies=3):
    data = fetch_discussion(discussion_id)
    title = data["data"]["attributes"]["title"]
    content = data["data"]["attributes"]["firstPost"]["attributes"]["content"]

    for _ in range(num_replies):
        reply = generate_reply(title, content)
        account = choose_random_account()
        reply_to_discussion(discussion_id, reply, account)
