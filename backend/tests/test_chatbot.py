import pytest
from app.services.chatbot import ChatbotService
from app.core.exceptions import ModelNotFoundError

def test_chatbot_initialization():
    chatbot = ChatbotService()
    assert chatbot is not None
    assert chatbot.model is not None

def test_process_query():
    chatbot = ChatbotService()
    response = chatbot.process_query("cho tôi xem menu")
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0

def test_invalid_query():
    chatbot = ChatbotService()
    with pytest.raises(ValueError):
        chatbot.process_query("")

def test_model_not_found():
    chatbot = ChatbotService()
    chatbot.model = None
    with pytest.raises(ModelNotFoundError):
        chatbot.process_query("test") 