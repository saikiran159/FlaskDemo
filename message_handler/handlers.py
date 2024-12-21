import json
import execjs
from lxml import etree
from bs4 import BeautifulSoup

def json_handler(bytes):
    content = bytes.decode("utf-8")
    try:
        return json.loads(content),0
    except Exception as e:
        return str(e),1

def javascript_handler(bytes):
    code = bytes.decode("utf-8")
    try:
        compile = execjs.compile(code)
        return code,0
    except Exception as e:
        return str(e),1

def xml_handler(bytes):
    xml_code = bytes.decode("utf-8")
    try:
        res = etree.fromstring(xml_code)
        return xml_code,0
    except Exception as e:
        return str(e),1

def html_handler(bytes):
    html_code = bytes.decode("utf-8")
    try:
        soup = BeautifulSoup(html_code, "html.parser")
        return html_code,0
    except Exception as e:
        return str(e),1

def form_handler(keyvals):
    return dict(keyvals.lists()),0

def text_handler(bytes):
    text = bytes.decode("utf-8")
    return text,0