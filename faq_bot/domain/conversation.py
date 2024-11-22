# domain/conversation.py
import datetime

# 대화 기록과 관련된 비즈니스 로직을 담당합니다.
class ConversationHistory:
    def __init__(self, db_adapter):
        """
        ConversationHistory 초기화.

        :param db_adapter: MongoDB와의 상호작용을 담당하는 어댑터
        """
        self.db_adapter = db_adapter

    def save(self, user_id: str, question: str, answer: str):
        collection_name = "user_contexts"
        context = self.get_context(user_id)

        if context:
            context += f"\nQ: {question}\nA: {answer}"
            self.db_adapter.get_collection(collection_name).update_one(
                {"user_id": user_id},  # 조건: user_id
                {"$set": {"conversation": context}}  # 새로운 context 저장
            )
        else:
            context = f"\nQ: {question}\nA: {answer}"
            # 새로운 문서 추가
            self.db_adapter.get_collection(collection_name).insert_one(
                {"user_id": user_id, "context": context}
            )
        return context

    def get_context(self, user_id: str):
        """
        특정 사용자의 대화 컨텍스트를 가져옴.

        :param user_id: 사용자 식별자
        :return: 사용자의 대화 이력 (str 타입)
        """
        query = {"user_id": user_id}
        result = self.db_adapter.find_one("user_contexts", query)
        
        # 만약 대화가 존재하면 그 대화 내용을 반환
        if result and "context" in result:
            context_list = result["context"]  # 'context' 필드를 가져옴
            # 리스트를 문자열로 변환 (예: 각 항목을 새로운 줄로 구분)
            return "\n".join(context_list)  # 리스트 항목들을 개행문자('\n')로 구분하여 하나의 문자열로 반환
        else:
            return ""
        