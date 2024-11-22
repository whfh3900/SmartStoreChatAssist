# infrastruncture/rag.py
import os
os.environ['TRANSFORMERS_CACHE'] = "./models"
from sentence_transformers import SentenceTransformer, util


class FAQRetriever():
    
    def __init__(self, faq_data):
        model_name = "nlpai-lab/KoE5"
        self.model = SentenceTransformer(model_name)

        # FAQ 데이터 질문 벡터화
        # - faq_questions: FAQ 데이터의 질문 리스트
        # - faq_embeddings: FAQ 질문들을 벡터로 변환 (한 번만 수행됨)
        self.faq_questions = list(faq_data.keys())
        self.faq_embeddings = self.model.encode(self.faq_questions, convert_to_tensor=True)

    def find_best_match(self, query):
        """
        사용자 질문(query)과 FAQ 질문 간의 유사도를 계산하여 가장 적합한 질문을 반환합니다.
        """
        # 사용자 질문을 벡터로 변환
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        
        # FAQ 데이터와 코사인 유사도 계산
        scores = util.pytorch_cos_sim(query_embedding, self.faq_embeddings)
        
        # 가장 높은 유사도를 가진 FAQ 질문의 인덱스 및 점수 반환
        best_idx = scores.argmax().item()
        return self.faq_questions[best_idx], scores[0][best_idx].item()