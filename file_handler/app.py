from flask import Blueprint,request,make_response,jsonify
import uuid
import os

file_handler = Blueprint("file_handler",__name__,url_prefix="/files")

STORED_FILES = []

ALLOWED_CONTENT_TYPES = [
    "application/octet-stream",
    "application/pdf",
    "image/jpeg",
    "image/png"
]

@file_handler.route("/upload",methods=["POST"])
def uploader():
    request_content_type = request.headers.get("Content-Type",None)
    if request_content_type == None:
        return make_response(jsonify({"message":"please provide content-type"}),400)

    if request_content_type not in ALLOWED_CONTENT_TYPES or not request_content_type.startswith("multipart/form-data"):
        make_response(jsonify({"message":f"we are currently not supporting {request_content_type} content-type",
                              "supported_content_types":ALLOWED_CONTENT_TYPES}),404)
    
    if request_content_type.startswith("multipart/form-data"):
        form_data = dict(request.form.lists())
        file_data = dict(request.files.lists())
        field_keys = set(form_data.keys()).union(set(file_data.keys()))
        
        id = uuid.uuid4().hex
        message = {"id":id,"content":{field_key:[] for field_key in field_keys}}
        
        for each_key in field_keys:
            if each_key in form_data:
                key_values = form_data[each_key]
                for each_val in key_values:
                     message["content"][each_key].append({"type":"string","value":each_val})
            if each_key in file_data:
                key_values = file_data[each_key]
                for each_file in key_values:
                    filename = each_file.filename
                    stream = each_file.stream.read()
                    
                    filestorepath = os.path.join("file_handler","STORE",filename)
                    with open(filestorepath,"wb") as filewriter:
                        filewriter.write(stream)
                    
                    message["content"][each_key].append({"type":"file","value":filestorepath})
        
        STORED_FILES.append(message)
        return make_response(jsonify(message),200)
    else:
        stream = request.data
        id = uuid.uuid4().hex
        if stream is None:
            return make_response(jsonify({"message":"file not uploaded","error":True}),400)
        
        filestorepath = os.path.join("file_handler","STORE","score.pdf")
        with open(filestorepath,"wb") as filewriter:
            filewriter.write(stream)
        
        message = {"id":id,"content":filestorepath}
        STORED_FILES.append(message)
        return make_response(jsonify(message),200)