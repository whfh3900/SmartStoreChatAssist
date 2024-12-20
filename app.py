# main.py
from fastapi import FastAPI, Depends, Request
from faq_bot.infrastructure.db_adapter import MongoDBAdapter
from faq_bot.infrastructure.openai_adapter import OpenAIAdapter
from faq_bot.application.chat_service import ChatService
from faq_bot.domain.faq_service import FAQService
from faq_bot.domain.question_handler import QuestionHandler
from faq_bot.domain.conversation import ConversationHistory
import os
from dotenv import load_dotenv

load_dotenv("./.env")

app = FastAPI()

# # 의존성 주입을 위한 함수
# def get_faq_data(db_adapter: MongoDBAdapter):
#     db_adapter_instance = db_adapter()  # MongoDBAdapter 인스턴스 생성
#     return db_adapter_instance.find_all(collection_name="faq_data")


def get_faq_data(db_adapter: MongoDBAdapter):
    # db_adapter는 MongoDBAdapter 클래스의 인스턴스여야 하므로, 클래스에서 인스턴스를 생성해야 합니다.
    db_adapter_instance = db_adapter()  # 클래스 인스턴스를 생성해야 합니다.
    # db_adapter_instance를 사용하여 데이터를 가져오는 로직을 작성합니다.
    return db_adapter_instance.get_faq_data()


def get_faq_service(faq_data: list):
    return FAQService(faq_data)

def get_question_handler():
    question_handler = QuestionHandler()
    return question_handler

def get_conversation_history(db_adapter: MongoDBAdapter):
    conversation_history = ConversationHistory(db_adapter)
    return conversation_history

def get_openai_adapter():
    openai_adapter = OpenAIAdapter(api_key=os.environ.get("OPENAI_API_KEY"))
    return openai_adapter

# 서버 시작 시 FAQService 초기화 및 벡터화
@app.on_event("startup")
async def startup():
    global faq_service_instance
    db_adapter_instance = MongoDBAdapter()  # DB 연결 어댑터 생성
    faq_data = get_faq_data(db_adapter_instance)  # DB에서 FAQ 데이터 가져오기
    faq_service_instance = get_faq_service(faq_data)  # FAQService에 데이터 로드

    # FAQ 데이터를 벡터화하여 저장 (한 번만 실행)
    faq_service_instance.vectorize_faq_data()


@app.post("/chat/")
async def chat(request: Request, 
               faq_service: FAQService = Depends(lambda: faq_service_instance),  # 초기화된 faq_service 전달
               question_handler: QuestionHandler = Depends(get_question_handler),
               conversation_history: ConversationHistory = Depends(lambda: get_conversation_history(MongoDBAdapter)),
               openai_adapter: OpenAIAdapter = Depends(get_openai_adapter)):


    data = await request.json()
    user_id = data["user_id"]
    question = data["question"]

    # 서비스 객체 생성
    chat_service = ChatService(faq_service, question_handler, conversation_history)

    # 채팅 처리
    answer, context, score = chat_service.handle_chat(user_id, question)

    # openai 사용하여 답변 강화
    answer_response, suggest_response = await openai_adapter.generate_response(score, question, context, answer)
    if score < 0.55:
        return {"answer": "저는 스마트 스토어 FAQ를 위한 챗봇입니다. 스마트 스토어에 대한 질문을 부탁드립니다.", "suggest": suggest_response}
    else:
        return {"answer": answer_response, "suggest": suggest_response}