from flask import Flask,make_response,jsonify
from message_handler.app import message_handler
from file_handler.app import file_handler

app = Flask(__name__)
app.register_blueprint(message_handler)
app.register_blueprint(file_handler)

@app.route("/health",methods=["GET"])
def live():
    return make_response(jsonify({"statuscode":200,"islive":True}),200)

if __name__ == "__main__":
    app.run()
