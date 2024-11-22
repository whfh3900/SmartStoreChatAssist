# domain/question_handler.py
# 사용자의 질문을 처리하고 FAQ 데이터와 매칭하는 로직을 담당합니다.
import re

class QuestionHandler:
    def __init__(self, additional_stopwords=None):
        # 기본 불용어 리스트 (스마트스토어 관련 단어 포함)
        default_stopwords = ['스마트스토어', '스마트', '스토어', '쇼핑몰']
        # 입력된 추가 불용어가 있다면 업데이트
        if additional_stopwords:
            default_stopwords.update(additional_stopwords)
        self.custom_stopwords = default_stopwords

    def preprocess(self, question: str) -> str:
        """
        사용자 질문을 전처리합니다.
        - 불용어를 제거하고 소문자로 변환하여 필터링된 단어들만 반환합니다.
        """
        # 정규표현식으로 텍스트에서 단어만 추출
        words = re.findall(r'\b\w+\b', question.lower())  # 소문자 변환하여 일관성 있게 비교
        # 불용어가 아닌 단어들만 필터링 (정규표현식으로 제거)
        filtered_words = [word for word in words if word not in self.custom_stopwords]
        # 필터링된 단어들을 공백으로 결합하여 반환
        return ' '.join(filtered_words)