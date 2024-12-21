from flask import Flask
from message_handler.app import message_handler
from file_handler.app import file_handler

app = Flask(__name__)
app.register_blueprint(message_handler)
app.register_blueprint(file_handler)

if __name__ == "__main__":
    app.run()
