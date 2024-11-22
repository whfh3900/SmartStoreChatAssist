import json
import pickle
from pymongo import MongoClient
import uuid

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["faq_chatbot"]  # 데이터베이스 이름
collection_contexts = db["user_contexts"]  # 사용자 문맥 데이터 컬렉션
collection_faq = db["faq_data"]  # FAQ 데이터 컬렉션

# conversation_history.json 삽입
with open("data/conversation_history.json", "r", encoding="utf-8") as file:
    conversation_data = json.load(file)
    # 데이터를 MongoDB에 삽입하기 전에 확인
    # conversation_data가 비어 있지 않음을 확인
    if conversation_data:
        documents = [
            {"user_id": user_id, "conversation": conversation}
            for user_id, conversation in conversation_data.items()
        ]
        # MongoDB에 데이터 삽입
        collection_contexts.insert_many(documents)
    else:
        print("데이터가 비어 있습니다.")

print("`conversation_history.json` 데이터를 MongoDB의 `user_contexts` 컬렉션에 삽입 완료.")

# final_result.pkl 삽입
with open("data/final_result.pkl", "rb") as file:
    faq_data = pickle.load(file)

# faq_data가 딕셔너리 형태라고 가정 (key: 질문, value: 답변)
if isinstance(faq_data, dict):
    for question, answer in faq_data.items():
        # 각 질문/답변 쌍에 대해 고유 _id를 생성하여 삽입
        document = {
            "question": question,  # 질문
            "answer": answer       # 답변
        }
        collection_faq.insert_one(document)
else:
    print("FAQ 데이터 형식이 잘못되었습니다. 예상되는 형식은 딕셔너리입니다.")

print("`final_result.pkl` 데이터를 MongoDB의 `faq_data` 컬렉션에 삽입 완료.")
