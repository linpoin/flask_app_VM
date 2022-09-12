import pandas as pd

from flask import request
from flask import Blueprint
from .def_user import *

user=Blueprint('user',__name__)

@user.route('/')
def index():
    return 'user.hello'

#使用者註冊
@user.route('/signup' ,methods=['POST'])
def user_signup():
    """
        
    ---
    tags:
      - User
    produces: application/json,
    parameters:
    - name: username
      in: body
      type: string
    - name: password
      in: body
      type: string
    - name: phone_number
      in: body
      type: string
    responses:
      400:
       description: 輸入資訊不完全
       schema:
         id: SignupInputError
         properties:
           code:
             type: number
             description: code
             example: 400
           message:
             type: string
             description: 失敗訊息
             example: "請輸入帳號、密碼及手機號碼"
      200:
       description: 註冊成功
       schema:
         id: SignupSuccess
         properties:
           code:
             type: number
             description: code
             example: 200
           message:
             type: string
             description: 成功訊息
             example: "註冊成功"
           token:
             type: string
             description: Token
    """
    if request.method == 'POST':
        body_json = request.get_json()
        if 'username' in body_json.keys() and 'password' in body_json.keys() and 'phone_number' in body_json.keys():
            name = body_json['username']
            password = body_json['password']
            phone = body_json['phone_number']
            
            return_me = usercreate(name,password,phone)
            return return_me
        else:
            error = {'code':400,
                    'message':'請輸入帳號、密碼及手機號碼',
            }
            return error, 400

#使用者登入
@user.route('/login' ,methods=['POST'])
def user_login():
    """
        
    ---
    tags:
      - User
    produces: application/json,
    parameters:
    - name: phone
      in: body
      type: string
    - name: password
      in: body
      type: string
    responses:
      400:
       description: 輸入資訊不完全
       schema:
         id: LoginInputError
         properties:
           code:
             type: number
             description: code
             example: 400
           message:
             type: string
             description: 失敗訊息
             example: "請確認帳號、密碼"
      200:
       description: 登入成功
       schema:
         id: LoginSuccess
         properties:
           code:
             type: number
             description: code
             example: 200
           message:
             type: string
             description: 成功訊息
             example: "登入成功"
           token:
             type: string
             description: Token
    """
    if request.method == 'POST':
        body_json = request.get_json()
        if body_json == None:
            return {'code':401,'message':'無附帶body'}
        if 'phone' in body_json.keys() and 'password' in body_json.keys():            
            phone = body_json['phone']
            password = body_json['password']
            return_me = user_login_f(phone,password)
            return return_me
        else:
            error = {'code':400,
                    'message':'請確認電話、密碼',
            }
            return error,400

#使用者資料
@user.route('/<en_name>/data' ,methods=['GET'])
def user_data(en_name):
    """
        
    ---
    tags:
      - User
    produces: application/json,
    parameters:
    - name: token
      in: header
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
           level_num:
             type: number
             description: code
             example: 0
           name:
             type: string
             description: code
             example: 200
           user_id:
             type: number
             description: code
             example: 0123456789
           user_qrcode:
             type: string
             description: code
             example: 200
           message:
             type: string
             description: 成功訊息
             example: 驗證成功
    """
    if request.method == 'GET':
        token = request.headers.get('Authorize')
        if token == None:
          return {'code':401,'message':'無附帶token'}
        if 'Authorize' in request.headers:
            try:
                phone = jwt.decode(token, 'mindnode', algorithms=['HS256'])['phone']
                return_me = user_data_f(phone,en_name)
                return return_me
            except:
                return {'code':401,'message':'token已過期'},401
        else:
          return {'code':401,'message':'無附帶token','123':request.headers},401

#使用者資料(指定因子)
@user.route('/<en_name>/data/<factor>' ,methods=['GET'])
def user_data_factor(en_name,factor):
    """
        
    ---
    tags:
      - User
    produces: application/json,
    parameters:
    - name: token
      in: header
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
         id: data_factor
         properties:
           code:
             type: number
             description: code
             example: 200
           factor(ex.level_num):
             type: number
             description: code
             example: 0
           message:
             type: string
             description: 成功訊息
             example: 驗證成功
    """
    if request.method == 'GET':
        token = request.headers.get('Authorize')
        if token == None:
          return {'code':401,'message':'無附帶token'}
        if 'Authorize' in request.headers:
            try:
                phone = jwt.decode(token, 'mindnode', algorithms=['HS256'])['phone']
                return_me = user_data_f(phone,en_name,factor)
                return return_me
            except:
                return {'code':401,'message':'token已過期'},401
        else:
          return {'code':401,'message':'無附帶token','123':request.headers},401

#闖關
@user.route('/<en_name>/run_level' ,methods=['POST'])
def user_runlevel(en_name):
    """
        
    ---
    tags:
      - User
    produces: application/json,
    parameters:
    - name: shop_id
      in: body
      type: string
    - name: Authorize
      in: header
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
         id: run_level
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
        token = request.headers.get('Authorize')
        if token == None:
          return {'code':401,'message':'無附帶token'}
        if 'shop_id' in body_json.keys():
            try:
                decode_jwt = jwt.decode(token, 'mindnode', algorithms=['HS256'])
                phone = decode_jwt['phone']
                shop_id = body_json['shop_id']
                return_me = run_level_f(phone,en_name,shop_id)
                return return_me
            except:
                return {'code':401,'message':'token已過期'},401
        else:
            return {'code':401,'message':'無附帶shop_id'},401
         
#抽獎
@user.route('/<en_name>/get_prize' ,methods=['POST'])
def user_get_prize(en_name):
    """
        
    ---
    tags:
      - User
    produces: application/json,
    parameters:
    - name: shop_id
      in: body
      type: string
    - name: Authorize
      in: header
      type: string
    responses:
      401:
       description: Token過期
       schema:
         id: TokenError
         properties:
           code:
             type: number
             description: code
             example: 401
           message:
             type: string
             description: 失敗訊息
             example: "token已過期"
      202:
       description: 闖關未達5關
       schema:
         id: run_level_Error_0
         properties:
           code:
             type: number
             description: code
             example: 202
           message:
             type: string
             description: 失敗訊息
             example: "闖關未達5關"
      200:
       description: 抽獎成功
       schema:
         id: run_level_0
         properties:
           code:
             type: number 
             description: code
             example: 200
           get:
             type: number
             description: 抽獎結果
             example: 1
           prize:
             type: string
             description: 獎品
             example: "相機"
    """
    if request.method == 'POST':
        token = request.headers.get('Authorize')
        if token == None:
          return {'code':401,'message':'無附帶token'},401
        else:
            try:
                decode_jwt = jwt.decode(token, 'mindnode', algorithms=['HS256'])
                phone = decode_jwt['phone']

                #取得user_id
                select_phone_q = f"select * from user.users where phone = '{phone}'"
                have_phone = mysql_engine.execute(select_phone_q).fetchone()
                user_id = have_phone['user_id']
                name = have_phone['name']

                #取得level_num
                select_level_num_q = f"select {en_name}_num from user.run_level_number where user_id = '{user_id}'"
                level_num = mysql_engine.execute(select_level_num_q).fetchone()
                level_num = int(level_num[f'{en_name}_num'])


                #取得通關數及抽獎方式
                select_lottery_level_num_q = f"select lottert_method,lottery_level_num from shopping_area.shopping_area_infor where shopping_area_eg_name = '{en_name}'"
                lottery_level_num = mysql_engine.execute(select_lottery_level_num_q).fetchone()
                lottery_level_num = lottery_level_num['lottery_level_num']
                lottert_method = lottery_level_num['lottert_method']


                if level_num >= int(lottery_level_num):
                    level_num = 0
                    
                    level_up_q = f"UPDATE user.run_level_number SET {en_name}_num = '{level_num}'  WHERE user_id = '{user_id}'"
                    mysql_engine.execute(level_up_q)
                    
                    return_me = user_get_prize_f(lottert_method,en_name,name,phone)
                    return return_me
                else:
                    return {'code':202,'message':'闖關未達5關'},202
            except:
                return {'code':401,'message':'token已過期'},401

#使用者獎品列表              
@user.route('/prize' ,methods=['GET'])
def user_prize():
    """
        
    ---
    tags:
      - User
    produces: application/json,
    parameters:
    - name: token
      in: header
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
           level_num:
             type: number
             description: code
             example: 0
           name:
             type: string
             description: code
             example: 200
           user_id:
             type: number
             description: code
             example: 0123456789
           message:
             type: string
             description: 成功訊息
             example: 驗證成功
    """
    if request.method == 'GET':
        token = request.headers.get('Authorize')
        if token == None:
          return {'code':401,'message':'無附帶token'}
        if 'Authorize' in request.headers:
            try:
                phone = jwt.decode(token, 'mindnode', algorithms=['HS256'])['phone']
                return_me = user_get_all_prize_f(phone)
                return return_me
            except:
                return {'code':401,'message':'token已過期'},401
        else:
          return {'code':401,'message':'無附帶token','123':request.headers},401