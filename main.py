from fastapi import FastAPI, Request
from faq_bot.faq_data_load import load_faq_data
from faq_bot.rag import FAQRetriever
from faq_bot.openai_api import generate_response
from faq_bot.stopword_processor import get_custom_stopwords, preprocess_text
import json
import os
from pydantic import BaseModel


# 요청 및 응답 모델 정의
class ChatRequest(BaseModel):
    user_id: str  # 사용자 ID
    question: str  # 사용자가 입력한 질문

class ChatResponse(BaseModel):
    answer: str  # 챗봇의 응답
    suggest: str  # 관련 질문 제안

# 대화 기록 저장 파일 경로 지정
conversation_history_file = "./data/conversation_history.json"

# 대화 기록을 JSON 파일에서 로드
def load_conversation_history():
    """
    대화 기록을 파일에서 읽어 딕셔너리로 반환합니다.
    파일이 없거나 JSON 파싱 오류가 발생하면 빈 딕셔너리를 반환합니다.
    """
    if os.path.exists(conversation_history_file):
        with open(conversation_history_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)  # JSON 파일 로드
            except json.JSONDecodeError:
                return {}  # JSON 파싱 오류 시 빈 딕셔너리 반환
    return {}

# 대화 기록을 JSON 파일로 저장
def save_conversation_history():
    """
    대화 기록을 JSON 파일로 저장합니다.
    """
    with open(conversation_history_file, "w", encoding="utf-8") as f:
        json.dump(conversation_history, f, ensure_ascii=False, indent=4)

# 초기 대화 기록 로드
conversation_history = load_conversation_history()

# FastAPI 애플리케이션 초기화
app = FastAPI()

# FAQ 데이터 로드 (pickle 파일에서 데이터 읽기)
faq_data = load_faq_data("./data/final_result.pkl")

# FAQRetriever 인스턴스 생성 (질문 매칭을 위한 객체)
faqr = FAQRetriever(faq_data)

# 사용자 정의 불용어 목록 로드
custom_stopwords = get_custom_stopwords()

@app.post("/chat/", response_model=ChatResponse)
async def chat(request: Request):
    """
    사용자의 질문을 처리하는 API 엔드포인트.

    - `user_id`: 사용자 식별자.
    - `question`: 사용자가 입력한 질문.
    """
    # 요청 데이터 파싱
    data = await request.json()
    user_id = data.get("user_id")  # 사용자 ID
    question = data.get("question")  # 사용자 질문
    # 질문 텍스트 전처리 (불용어 제거)
    processed_query = preprocess_text(question, custom_stopwords)

    # 해당 사용자의 대화 기록 가져오기
    context = conversation_history.get(user_id, "")

    # 질문과 FAQ 데이터 간 유사도 계산 및 매칭
    best_question, score = faqr.find_best_match(processed_query)
    
    # 유사도가 낮은 경우 처리
    if score < 0.55:  # 유사도가 기준 이하인 경우
        _, suggest_response = await generate_response(score, processed_query, context, None)
        # 스마트스토어와 관련 없는 질문에 대해 응답
        return {
            "answer": "저는 스마트 스토어 FAQ를 위한 챗봇입니다. 스마트 스토어에 대한 질문을 부탁드립니다.",
            "suggest": suggest_response,
        }
    else:
        # 유사도가 높은 경우 관련 FAQ에서 답변 가져오기
        answer = faq_data[best_question]
        
        # 대화 기록 업데이트
        context += f"\nQ: {processed_query}\nA: {answer}"
        conversation_history[user_id] = context
        
        # OpenAI API를 사용해 답변 생성
        answer_response, suggest_response = await generate_response(score, processed_query, context, answer)
        
        # 대화 기록 저장
        save_conversation_history()
        
        # 응답 반환
        return {"answer": answer_response, "suggest": suggest_response}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )