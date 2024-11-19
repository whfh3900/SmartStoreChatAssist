import requests

# FastAPI 서버 URL
BASE_URL = "http://127.0.0.1:8000"

def test_chat_api():
    """
    FastAPI의 /chat/ 엔드포인트를 테스트하는 함수
    """
    # 테스트 데이터
    test_data = [
        {"user_id": "user1", "question": "스마트스토어에서 상품 등록은 어떻게 하나요?"},
        {"user_id": "user2", "question": "스마트스토어 결제 수단은 어떻게 설정하나요?"},
        {"user_id": "user3", "question": "다음 월드컵 예선전 국가대표팀 경기는 언제인가요?"},
    ]

    for i, data in enumerate(test_data):
        print(f"\n[테스트 케이스 {i + 1}] 사용자 질문: {data['question']}")
        
        # POST 요청
        response = requests.post(f"{BASE_URL}/chat/", json=data, stream=True, timeout=60)
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    print("응답 청크:", chunk.decode('utf-8', errors='replace'))
        else:
            print("서버 오류:", response.status_code)

# 테스트 실행
if __name__ == "__main__":
    test_chat_api()