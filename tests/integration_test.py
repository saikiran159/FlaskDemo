import pytest
from app import app

@pytest.fixture
def client():
    print("used this")
    return app.test_client()

from message_handler.test_cases import test_invalid_message,test_message_creation,test_messages