# infrastructure/db_adapter.py

# MongoDB와의 상호작용을 담당합니다. FAQ 데이터를 DB에서 가져오거나 업데이트하는 로직을 처리합니다.
from pymongo import MongoClient

class DBAdapter:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="faq_chatbot"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["faq_data"]

    def load_faq_data(self):
        faq_data = {}
        for document in self.collection.find():
            question = document.get("question")
            answer = document.get("answer")
            faq_data[question] = answer
        return faq_data
