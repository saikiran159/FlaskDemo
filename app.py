from flask import Flask
from message_handler.app import message_handler

app = Flask(__name__)
app.register_blueprint(message_handler)

if __name__ == "__main__":
    app.run()
