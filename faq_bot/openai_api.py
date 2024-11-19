from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
# .env 파일 경로 지정
dotenv_path = os.path.join("./", '.env')
# .env 파일 로드
load_dotenv(dotenv_path)

client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

async def generate_response(score, query, context, faq_answer=None):
    # 유사도가 낮을 경우 처리 (관련 질문을 두 개 제안)
    if score < 0.55:
        prompt = f"""
        You are the Naver Smart Store FAQ chatbot.
        Context: {context}
        The following answer was found in the FAQ: No relevant answer found.
        Question: {query}
        Please suggest two related questions that the user may be interested in, based on the context of the Naver Smart Store FAQ.
        These questions should be in Korean, and relevant to the user's question and the Naver Smart Store context.
        """
    else:
        # 유사도가 높을 경우 처리 (정확한 답변과 관련 질문 제안)
        prompt = f"""
        You are the Naver Smart Store FAQ chatbot.
        Context: {context}
        The following answer was found in the FAQ: {faq_answer}
        Question: {query}
        Please provide the following:
        1. A concise and accurate response to the user's question based on the context and FAQ answer.
        2. Two related questions in Korean that the user may be interested in, based on the context. These questions should be relevant to the user's question and context.

        Please make sure to format the response clearly, with each part labeled separately.
        """
            
    response = await client.chat.completions.create(
        model="gpt-4o",  # 모델 이름을 gpt-4로 설정
        messages=[
            {"role": "system", "content": "You are a helpful assistant and a Naver Smart Store FAQ chatbot."},
            {"role": "user", "content": prompt}],
        stream=False  # 스트리밍 비활성화
    )
    return response.choices[0].message.content
