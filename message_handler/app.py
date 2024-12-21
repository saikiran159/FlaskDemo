from flask import Blueprint,request,make_response,jsonify
from .handlers import json_handler,javascript_handler,xml_handler,html_handler,text_handler,form_handler
import uuid

message_handler = Blueprint("message_handler",__name__,url_prefix="/messages")

MESSSAGE_STORE = []

CONTENT_TYPE_MAPPINGS = {
    "application/json":"json_handler",
    "application/javascript":"javascript_handler",
    "application/xml":"xml_handler",
    "text/html":"html_handler",
    "text/plain":"text_handler",
    "application/x-www-form-urlencoded":"form_handler",
}

@message_handler.route("/create",methods=["POST"])
def create_message():
    headers = request.headers
    content_type = headers.get("Content-Type",None)
    if content_type == None:
        return make_response(jsonify({"message":"please provide content-type"}),400)
    
    store_type = CONTENT_TYPE_MAPPINGS.get(content_type,None)
    if store_type is None:
        store_type = "form_handler" if content_type.startswith("multipart/form-data") else None

    if store_type is None:
        return make_response(jsonify({"message":f"we are currently not supporting {content_type} content-type",
                              "supported_content_types":list(CONTENT_TYPE_MAPPINGS.keys())}),404)
    
    if store_type == "form_handler":
        content = request.form
    else:
        content = request.data
    
    processed_content,status = eval(store_type)(content)
    if status == 1:
        return make_response(jsonify({"message":processed_content,"error":True}),400)
    
    ID = uuid.uuid4().hex
    message = {"handler":store_type,"id":ID,"content":processed_content}

    MESSSAGE_STORE.append(message)

    return make_response(jsonify(message),200)

message_handler.route("/list")
def fetchall():
    return make_response(jsonify({"content":MESSSAGE_STORE}),200)

message_handler.route("/get/<id>")
def fetch(id):
    pick = [each_msg for each_msg in MESSSAGE_STORE if each_msg["id"] == id]
    if pick:
        return make_response(jsonify(pick),200)
    return make_response(jsonify({"message":"not found"}),404)