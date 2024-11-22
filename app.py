# main.py
from fastapi import FastAPI, Request
from faq_bot.infrastructure.db_adapter import DBAdapter
from faq_bot.infrastructure.openai_adapter import OpenAIAdapter
from faq_bot.application.chat_service import ChatService
import os
from dotenv import load_dotenv
load_dotenv("./.env")

app = FastAPI()

# MongoDB에서 FAQ 데이터를 불러옵니다.
db_adapter = DBAdapter()
faq_data = db_adapter.load_faq_data()

# OpenAI API 설정
openai_adapter = OpenAIAdapter(api_key=os.environ.get("OPENAI_API_KEY"))

# 서비스 객체 생성 (의존성 주입 방식으로 변경)
chat_service = ChatService(faq_data, {}, db_adapter, openai_adapter)

@app.post("/chat/")
async def chat(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    question = data["question"]

    # 채팅 처리
    answer, context, score = chat_service.handle_chat(user_id, question)

    answer_response, suggest_response = await openai_adapter.generate_response(score, question, context, answer)
    if score < 0.55:
        return {"answer": "저는 스마트 스토어 FAQ를 위한 챗봇입니다. 스마트 스토어에 대한 질문을 부탁드립니다.", "suggest": suggest_response}
    else:
        return {"answer": answer_response, "suggest": suggest_response}
    

