from flask import Flask
from file_handler.app import file_handler
import pytest
import os

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(file_handler)
    return app.test_client()

def test_upload(client):
    with open(os.path.join("file_handler","msbadge.jpg"),"rb") as reader:
        img_bytes = reader.read()
    
    response = client.post("/files/upload",data=img_bytes,headers={"Content-Type":"image/jpeg"})
    assert response.status_code == 200