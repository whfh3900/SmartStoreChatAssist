# domain/faq_handler.py

# FAQ 데이터 처리와 관련된 서비스 로직을 다룹니다. 예를 들어, FAQ 데이터를 검색하고 답변을 반환하는 로직이 포함됩니다.
from faq_bot.infrastructure.rag import FAQRetriever

class FAQService:
    def __init__(self, faq_data):
        self.faq_data = faq_data
        # FAQ 데이터 벡터화 준비
        self.faq_retriever = FAQRetriever(faq_data)

    def get_answer(self, processed_question: str) -> str:
        """
        전처리된 질문을 FAQ 데이터와 비교하여 가장 유사한 질문을 찾고, 그에 대한 답변을 반환합니다.
        """
        # FAQRetriever를 사용하여 가장 적합한 질문과 유사도 점수 가져오기
        best_match, score = self.faq_retriever.find_best_match(processed_question)
        return best_match, score
