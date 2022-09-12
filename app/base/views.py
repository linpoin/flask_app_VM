# import sys
# sys.path.append("..")
from ..Module import *

from flask import request
from flask import Blueprint
from .def_base import *

base=Blueprint('base',__name__)

@base.route('/')
def index():
    return 'base.hello'

#解析圖片
@base.route("/image_parse", methods=["GET", "POST"])
def image_parse():
    if request.method == 'POST':
        img = request.files['file'].read()
        encoded = base64.b64encode(img).decode('utf-8')
        img_type = str(request.files['file'].mimetype)
        encoded = f'data:{img_type};base64,{encoded}'
        #sql_cmd = "INSERT INTO test (image) VALUES ('{}')".format(encoded)
        #test_engine.execute(sql_cmd)

        #img_type = str(request.files['file'].mimetype)
        #img = 'data:{};base64,{}'.format(img_type,encoded.decode('utf-8'))
    return encoded