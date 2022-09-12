from lib2to3.pgen2 import token

from flask import request
from flask import Blueprint
from .def_token import *

token=Blueprint('token',__name__)

@token.route('/')
def index():
    return 'token.hello'

#token驗證
@token.route('/verify' ,methods=['POST'])
def token_verify():
    """
        
    ---
    tags:
      - token
    produces: application/json,
    parameters:
    - name: Authorize
      in: body
      type: string
    responses:
      400:
       description: Token過期
       schema:
         id: TokenError
         properties:
           code:
             type: number
             description: code
             example: 400
           message:
             type: string
             description: 失敗訊息
             example: "token已過期"
      200:
       description: 驗證成功
       schema:
         id: TokenSuccess
         properties:
           code:
             type: number
             description: code
             example: 200
           message:
             type: string
             description: 成功訊息
    """
    if request.method == 'POST':
        body_json = request.get_json()
        if body_json == None:
          return {'code':401,'message':'無附帶token'},401
        if 'Authorize' in body_json.keys():
            try:
                decode_jwt = jwt.decode(body_json['Authorize'], 'mindnode', algorithms=['HS256'])
                username = decode_jwt['username']
                return {'code':200,'message':f'{username}歡迎登入'},200
            except:
                return {'code':401,'message':'token已過期'},401
        else:
            return {'code':401,'message':'無附帶token'},401