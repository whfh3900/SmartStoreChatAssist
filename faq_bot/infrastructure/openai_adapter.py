# infrastructure/openai_adapter.py
from openai import AsyncOpenAI


class OpenAIAdapter:
    def __init__(self, api_key:str) -> str:
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_response(self, question:str, context:str, faq_answer=None):
        # 유사도가 낮을 경우 처리 (관련 질문을 두 개 제안)
        if not faq_answer:
            prompt = f"""
            You are the Naver Smart Store FAQ chatbot.
            Context: {context}
            The following answer was found in the FAQ: No relevant answer found.
            Question: {question}
            Please suggest two related questions that the user may be interested in, based on the context of the Naver Smart Store FAQ.

            ### Response Template:
            Related Questions:
            1. [Provide the first related question here]
            2. [Provide the second related question here]

            Ensure the questions are in Korean and relevant to the user's question and the Naver Smart Store context.
            """
        else:
            # 유사도가 높을 경우 처리 (정확한 답변과 관련 질문 제안)
            prompt = f"""
            You are the Naver Smart Store FAQ chatbot.
            Context: {context}
            The following answer was found in the FAQ: {faq_answer}
            Question: {question}
            Please provide the following:

            1. A concise and accurate response to the user's question based on the context and FAQ answer.
            2. Two related questions in Korean that the user may be interested in, based on the context. These questions should be relevant to the user's question and context.

            ### Response Template:
            Answer: [Provide the concise and accurate response here]

            Related Questions:
            1. [Provide the first related question here]
            2. [Provide the second related question here]

            Make sure the response adheres to this format.
            """
                
        response = await self.client.chat.completions.create(
            model="gpt-4o",  # 모델 이름을 gpt-4로 설정
            messages=[
                {"role": "system", "content": "You are a helpful assistant and a Naver Smart Store FAQ chatbot."},
                {"role": "user", "content": prompt}],
            stream=False  # 스트리밍 비활성화
        )
        
        response_content = response.choices[0].message.content
        # 템플릿에 맞게 자르기
        if not faq_answer:
            answer = ""
            suggest = response_content.split("Related Questions:")[1].strip()
        else:
            sections = response_content.split("Related Questions:")
            answer = sections[0].split("Answer:")[1].strip()
            suggest = sections[1].strip()
        
        return answer, suggest


