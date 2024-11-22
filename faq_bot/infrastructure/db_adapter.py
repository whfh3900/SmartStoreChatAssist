# infrastructure/db_adapter.py

# MongoDB와의 상호작용을 담당합니다. FAQ 데이터를 DB에서 가져오거나 업데이트하는 로직을 처리합니다.
from pymongo import MongoClient

class MongoDBAdapter:
    def __init__(self, connection_uri= "mongodb://localhost:27017", database_name= "faq_chatbot"):
        self.client = MongoClient(connection_uri)
        self.db = self.client[database_name]

    def get_collection(self, collection_name:str):
        return self.db[collection_name]

    def find_one(self, collection_name:str, query:dict, sort=None):
        collection = self.get_collection(collection_name)
        document = collection.find_one(query, sort=sort)
        return document
    
    def find_all(self, collection_name:str, limit=0):
        """
        컬렉션 내 모든 데이터를 가져옵니다.

        :param collection_name: 컬렉션 이름
        :param limit: 가져올 문서 수 제한 (기본값: 0, 즉 무제한)
        :return: 문서 리스트
        """
        collection = self.get_collection(collection_name)
        cursor = collection.find({})  # 전체 문서 검색
        if limit > 0:
            cursor = cursor.limit(limit)
        return list(cursor)  # cursor를 리스트로 변환하여 반환
    
        
    