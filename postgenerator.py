# post_generator.py
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from config import DEEPSEEK_API_KEY, FLARUM_TAG_ID
from flarum_client import post_to_flarum, choose_random_account

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAISS_PATH = os.path.join(BASE_DIR, 'mitbbs', 'forum_posts_index.faiss')
TEXT_PATH = os.path.join(BASE_DIR, 'mitbbs', 'forum_posts_texts.json')

class PostGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.read_index(FAISS_PATH)
        with open(TEXT_PATH, 'r', encoding='utf-8') as f:
            self.texts = json.load(f)

    def clean(self, text):
        return ' '.join(text.split()).replace('"', '').replace('•', '-')

    def semantic_search_examples(self, keyword, top_k=3):
        vec = self.embed_model.encode([keyword])
        D, I = self.index.search(np.array(vec), top_k)
        return [self.texts[i] for i in I[0] if i < len(self.texts)]

    def generate_post(self, keyword):
        examples = self.semantic_search_examples(keyword)
        prompt = f"请根据以下示例生成关于“{keyword}”的中文论坛主贴：\n\n"
        for text in examples:
            parts = text.split('。\n', 1)
            title = parts[0] if parts else ""
            content = parts[1] if len(parts) > 1 else ""
            prompt += f"示例标题: {title}\n示例内容: {self.clean(content)}\n\n"
        prompt += "# 请仿照风格写一个中文主贴，标题用“# 标题”格式，不提及加米或一亩三分地。"

        resp = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是中文论坛发帖机器人，模仿真实语气。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.95,
            max_tokens=1000
        )
        return resp.choices[0].message.content.strip()

def run_post(keyword):
    gen = PostGenerator()
    full_content = gen.generate_post(keyword)
    if "# " in full_content:
        title, content = full_content.split("# ", 1)[1].split("\n", 1)
        account = choose_random_account()
        post_to_flarum(title.strip(), content.strip(), account, FLARUM_TAG_ID)
    else:
        print("格式错误，未能识别标题。")
