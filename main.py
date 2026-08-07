from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from ai.characters import CHARACTERS
from ai.memory import MEMORY
import os


# .env読み込み
load_dotenv()

# APIキー確認（動作確認後は削除OK）
print("API KEY:", os.getenv("OPENAI_API_KEY"))

# OpenAI接続
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


app = FastAPI()


# 受け取るデータ形式
class ChatRequest(BaseModel):
    character: str
    message: str


# トップページ確認用
@app.get("/")
def home():
    return {
        "message": "AI Word Wolf Start!"
    }


# AI会話API
@app.post("/chat")
def chat(request: ChatRequest):

    # キャラクター取得
    personality = CHARACTERS.get(request.character)

    if personality is None:
        return {
            "error": "キャラクターが存在しません"
        }


    # 初回なら履歴作成
    if request.character not in MEMORY:
        MEMORY[request.character] = []


    # ユーザー発言を保存
    MEMORY[request.character].append(
        {
            "role": "user",
            "content": request.message
        }
    )


    # AIに渡すメッセージ
    messages = [
        {
            "role": "system",
            "content": personality["system_prompt"]
        }
    ]


    # 過去会話を追加
    messages.extend(
        MEMORY[request.character]
    )


    # AIへ送信
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )


    # AI回答取得
    answer = response.choices[0].message.content


    # AI回答を履歴保存
    MEMORY[request.character].append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    return {
        "character": request.character,
        "answer": answer
    }