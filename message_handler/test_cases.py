import pytest
from message_handler.app import message_handler
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(message_handler)
    return app.test_client()


def test_message_creation(client):
    message = {"name":"saikiran","age":50}
    response = client.post("/messages/create",json=message,headers={"Content-Type":"application/json"})
    assert response.status_code == 200

def test_messages(client):
    # formdata
    form_data = {"name":"saikiran","age":52}
    response = client.post("/messages/create",data=form_data,headers={"Content-Type":"application/x-www-form-urlencoded"})
    assert response.status_code == 200

    id = response.json["id"]

    # get formdata
    response = client.get(f"/messages/get/{id}")
    assert response.status_code == 200

def test_invalid_message(client):
    response = client.post("/messages/create",data="my name i saikiran",headers={"Content-Type":"application/pdf"})
    assert response.status_code == 404