# application/chat_service.py

# 사용자의 요청을 처리하고, 도메인 계층의 로직을 호출하는 서비스 클래스입니다. 이 계층은 도메인 계층과 외부 인터페이스(어댑터) 간의 중간 역할을 합니다.
from faq_bot.domain.faq_service import FAQService
from faq_bot.domain.conversation import ConversationHistory
from faq_bot.domain.question_handler import QuestionHandler
from faq_bot.infrastructure.db_adapter import DBAdapter
from faq_bot.infrastructure.openai_adapter import OpenAIAdapter

class ChatService:
    def __init__(self, faq_data, conversation_data, db_adapter: DBAdapter, openai_adapter: OpenAIAdapter):
        # 외부 의존성 주입
        self.faq_service = FAQService(faq_data)
        self.conversation_history = ConversationHistory(conversation_data)
        self.question_handler = QuestionHandler()
        self.db_adapter = db_adapter
        self.openai_adapter = openai_adapter

    def handle_chat(self, user_id: str, question: str):
        # 질문 전처리
        processed_question = self.question_handler.preprocess(question)
        
        # FAQService에서 질문에 대한 답변과 유사도 얻기
        answer, score = self.faq_service.get_answer(processed_question)
        
        # 대화 기록을 업데이트하고, 답변 및 유사도 반환
        context = self.conversation_history.get_context(user_id)
        context += f"\nQ: {processed_question}\nA: {answer}"
        self.conversation_history.update_context(user_id, context)

        return answer, context, score