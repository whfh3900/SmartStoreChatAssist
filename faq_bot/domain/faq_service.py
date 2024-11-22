# domain/faq_handler.py

# FAQ 데이터 처리와 관련된 서비스 로직을 다룹니다. 예를 들어, FAQ 데이터를 검색하고 답변을 반환하는 로직이 포함됩니다.
import os
os.environ['TRANSFORMERS_CACHE'] = "./models"
from sentence_transformers import SentenceTransformer, util

class FAQService:
    def __init__(self, faq_data):
        self.faq_data = faq_data
        model_name = "nlpai-lab/KoE5"
        self.model = SentenceTransformer(model_name)

        # FAQ 데이터 질문 벡터화
        self.faq_embeddings = self.vectorize_faq_data(faq_data)

    def vectorize_faq_data(self, faq_data):
        """
        FAQ 데이터의 질문들을 벡터화합니다.
        """
        questions = [faq['question'] for faq in faq_data]
        embeddings = self.model.encode(questions)  # 모든 FAQ 질문을 벡터화
        return embeddings

    def vectorize(self, processed_question: str) -> str:
        return self.model.encode(processed_question, convert_to_tensor=True)

    def get_answer(self, processed_question: str) -> str:
        question_embedding = self.vectorize(processed_question)
        # FAQ 데이터와 코사인 유사도 계산
        scores = util.pytorch_cos_sim(question_embedding, self.faq_embeddings)
        
        # 가장 높은 유사도를 가진 FAQ 질문의 인덱스 및 점수 반환
        best_idx = scores.argmax().item()
        return self.faq_questions[best_idx], scores[0][best_idx].item()
