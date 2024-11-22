# domain/conversation.py

# 대화 기록과 관련된 비즈니스 로직을 담당합니다.
class ConversationHistory:
    def __init__(self, conversation_data):
        self.conversation_data = conversation_data

    def get_context(self, user_id: str) -> str:
        return self.conversation_data.get(user_id, "")

    def update_context(self, user_id: str, context: str):
        self.conversation_data[user_id] = context
