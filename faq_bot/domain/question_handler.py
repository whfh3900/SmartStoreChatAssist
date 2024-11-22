# domain/question_handler.py
# 사용자의 질문을 처리하고 FAQ 데이터와 매칭하는 로직을 담당합니다.
from faq_bot.infrastructure import stopword_processor

class QuestionHandler:
    def __init__(self):
        # 기본 불용어 리스트 가져오기
        self.custom_stopwords = stopword_processor.get_custom_stopwords()

    def preprocess(self, question: str) -> str:
        """
        사용자 질문을 전처리합니다.
        - 불용어를 제거하고 소문자로 변환하여 필터링된 단어들만 반환합니다.
        """
        return stopword_processor.preprocess_text(question, self.custom_stopwords)

