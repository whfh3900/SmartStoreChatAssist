from fastapi import FastAPI, Request
from faq_bot.faq_data_load import load_faq_data
from faq_bot.rag import FAQRetriever
from faq_bot.openai_api import generate_response
from faq_bot.stopword_processor import get_custom_stopwords, preprocess_text
import json
import os
from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    question: str

class ChatResponse(BaseModel):
    answer: str
    
# 파일 경로 지정
conversation_history_file = "./data/conversation_history.json"

# 대화 기록을 JSON 파일에서 로드
def load_conversation_history():
    if os.path.exists(conversation_history_file):
        with open(conversation_history_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}  # JSON 파싱 오류가 나면 빈 딕셔너리로 반환
    return {}

# 대화 기록을 JSON 파일로 저장
def save_conversation_history():
    with open(conversation_history_file, "w", encoding="utf-8") as f:
        json.dump(conversation_history, f, ensure_ascii=False, indent=4)

# 초기 대화 기록 로드
conversation_history = load_conversation_history()

app = FastAPI()
faq_data = load_faq_data("./data/final_result.pkl")
faqr = FAQRetriever(faq_data)
# 불용어 리스트 가져오기
custom_stopwords = get_custom_stopwords()

@app.post("/chat/", response_model=ChatResponse)
async def chat(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    question = data.get("question")
    processed_query = preprocess_text(question, custom_stopwords)

    # 대화 기록 가져오기
    context = conversation_history.get(user_id, "")
    
    # 질문 매칭
    best_question, score = faqr.find_best_match(processed_query)
    
    # 기준 유사도 이하인 경우, 스마트스토어와 관련 없는 질문 처리
    if score < 0.55:  # 유사도가 낮으면 관련 없는 질문으로 판단
        openai_response = await generate_response(score, processed_query, context, None)
        return {"answer": "저는 스마트 스토어 FAQ를 위한 챗봇입니다. 스마트 스토어에 대한 질문을 부탁드립니다.\n%s"%openai_response}
    
    else:
        # FAQ 데이터에서 관련된 답변 찾기
        answer = faq_data[best_question]
        # 대화 기록 업데이트 (FAQ에서 찾은 답변을 context에 추가)
        context += f"\nQ: {processed_query}\nA: {answer}"

        # 대화 기록 업데이트
        conversation_history[user_id] = context + f"\nQ: {processed_query}\nA: {answer}"
        # OpenAI를 통한 답변 생성 (generate_response)
        openai_response = await generate_response(score, processed_query, context, answer)
    
        # 응답 후 대화 기록 파일에 저장
        save_conversation_history()
        
        return {"answer": openai_response}
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )