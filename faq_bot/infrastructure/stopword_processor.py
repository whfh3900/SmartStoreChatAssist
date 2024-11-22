# infrastructure/steopword_processor.py
import re

# 불용어 리스트에 추가할 단어를 입력으로 받는 함수
def get_custom_stopwords(additional_stopwords=None):
    # 기본 불용어 리스트 (스마트스토어 관련 단어 포함)
    default_stopwords = ['스마트스토어', '스마트', '스토어', '쇼핑몰']
    
    # 입력된 추가 불용어가 있다면 업데이트
    if additional_stopwords:
        default_stopwords.update(additional_stopwords)
    
    # 최종 불용어 리스트 반환
    return default_stopwords

# 불용어 처리 함수
def preprocess_text(text, custom_stopwords):
    # 정규표현식으로 텍스트에서 단어만 추출
    words = re.findall(r'\b\w+\b', text.lower())  # 소문자 변환하여 일관성 있게 비교
    
    # 불용어가 아닌 단어들만 필터링 (정규표현식으로 제거)
    filtered_words = [word for word in words if word not in custom_stopwords]
    
    # 필터링된 단어들을 공백으로 결합하여 반환
    return ' '.join(filtered_words)