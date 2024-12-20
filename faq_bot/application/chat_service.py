# application/chat_service.py

# 사용자의 요청을 처리하고, 도메인 계층의 로직을 호출하는 서비스 클래스입니다. 이 계층은 도메인 계층과 외부 인터페이스(어댑터) 간의 중간 역할을 합니다.
from faq_bot.domain.conversation import ConversationHistory
from faq_bot.domain.question_handler import QuestionHandler
from faq_bot.domain.faq_service import FAQService

class ChatService:
    def __init__(self, faq_service: FAQService, question_handler: QuestionHandler, conversation_history: ConversationHistory):
        self.faq_service = faq_service  # 이미 벡터화된 faq_service 전달
        self.question_handler = question_handler
        self.conversation_history = conversation_history

        
    def handle_chat(self, user_id: str, question: str):
        """
        사용자의 질문을 처리하고 적절한 답변을 반환.

        :param user_id: 사용자 식별자
        :param question: 사용자의 질문
        :return: (답변, 컨텍스트)
        """
        # 1. 질문 전처리
        processed_question = self.question_handler.preprocess(question)

        # 2. FAQ 서비스에서 답변 검색
        answer, score = self.faq_data.get_answer(processed_question)

        # 3. 점수가 0.55 이상인 경우에만 대화 이력 저장 및 결과 context 반환
        if score >= 0.55:
            context = self.conversation_history.save(user_id, question, answer)
        else:
            context = self.conversation_history.get_context(user_id)

        return answer, context