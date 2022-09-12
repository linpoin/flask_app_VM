from flask import request
from flask import Blueprint
from .def_admin import *

admin=Blueprint('admin',__name__)

@admin.route('/')
def index():
    return 'admin.hello'

#管理者登入
@admin.route('/login' ,methods=['POST'])
def user_login():
    """
        
    ---
    tags:
      - Admin
    produces: application/json,
    parameters:
    - name: account
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
        if 'account' in body_json.keys() and 'password' in body_json.keys():            
            account = body_json['account']
            password = body_json['password']
            return_me = admin_login_f(account,password)
            return return_me
        else:
            error = {'code':400,
                    'message':'請確認帳號、密碼',
            }
            return error,400

#管理者掃描兌獎
@admin.route('/<en_name>/redeem' ,methods=['POST'])
def admin_redeem(en_name):
    """
        
    ---
    tags:
      - Admin
    produces: application/json,
    parameters:
    - name: user_id
      in: body
      type: string
    responses:
      400:
       description: body未帶user_id
       schema:
         id: BodyNoUserIdError
         properties:
           code:
             type: number
             description: code
             example: 400
           message:
             type: string
             description: 失敗訊息
             example: "請輸入user_id"
      401:
       description: 無附帶body
       schema:
         id: NoBodyError
         properties:
           code:
             type: number
             description: code
             example: 401
           message:
             type: string
             description: 失敗訊息
             example: "無附帶body"
      402:
       description: 無此user_id
       schema:
         id: NoHaveUserIdError
         properties:
           code:
             type: number
             description: code
             example: 402
           message:
             type: string
             description: 失敗訊息
             example: "無此user_id"
      403:
       description: 已兌換過抽獎資格
       schema:
         id: doneredeemError
         properties:
           code:
             type: number
             description: code
             example: 403
           message:
             type: string
             description: 失敗訊息
             example: "此用戶已兌換過抽獎資格"
      200:
       description: 兌換抽獎資格成功
       schema:
         id: lottery_done
         properties:
           code:
             type: number 
             description: code
             example: 200
           name:
             type: string
             description: 使用者姓名
             example: "陳XX"
           user_id:
             type: string
             description: 使用者編號
             example: "0123456789"
           lottery_num:
             type: string
             description: 抽獎券編號
             example: "Ah48b68z"
    """
    if request.method == 'POST':
        body_json = request.get_json()
        if body_json == None:
            return {'code':401,'message':'無附帶body'}
        if 'user_id' in body_json.keys():
            user_id = body_json['user_id']

            #取得user_name
            select_user_id_q = f"select * from user.users where user_id = '{user_id}'"
            have_user_id = mysql_engine.execute(select_user_id_q).fetchone()
            name = have_user_id['name']

            #取得level_num
            select_level_num_q = f"select {en_name}_num from user.run_level_number where user_id = '{user_id}'"
            level_num = mysql_engine.execute(select_level_num_q).fetchone()
            if level_num == None:
              return {'code':402,'message':'無此user_id'},402
            level_num = int(level_num[f'{en_name}_num'])


            #取得通關數及抽獎方式
            select_lottery_level_num_q = f"select lottery_method,lottery_level_num from shopping_area.shopping_area_infor where shopping_area_eg_name = '{en_name}'"
            lottery_level_num = mysql_engine.execute(select_lottery_level_num_q).fetchone()
            lottery_level_num = lottery_level_num['lottery_level_num']


            if level_num >= int(lottery_level_num):
                #level_num = 0
                
                #level_up_q = "UPDATE user.run_level_number SET {}_num = '{}'  WHERE user_id = '{}'".format(en_name,level_num,user_id)
                #mysql_engine.execute(level_up_q)
                
                return_me = user_redeem_f(en_name,name,user_id)
                return return_me
            else:
                return {'code':202,'message':f'闖關未達{lottery_level_num}關'},202
        else:
          return {'code':400,'message':'請輸入user_id'},400
          
#管理者已兌換列表
@admin.route('/<en_name>/redeem_list' ,methods=['GET'])
def admin_redeem_list(en_name):
    """
        
    ---
    tags:
      - Admin
    produces: application/json,
    responses:
      200:
       description: 成功
       schema:
         id: lottery_done
         properties:
           code:
             type: number 
             description: code
             example: 201
           name:
             type: string
             description: 使用者姓名
             example: "陳XX"
           user_id:
             type: string
             description: 使用者編號
             example: "0123456789"
           lottery_num:
             type: string
             description: 抽獎券編號
             example: "Ah48b68z"
    """
    if request.method == 'GET':
      return_me = user_redeem_list_f(en_name)
      return return_me

# #使用者資料
# @admin.route('/<en_name>/data' ,methods=['GET'])
# def user_data(en_name):
#     """
        
#     ---
#     tags:
#       - Admin
#     produces: application/json,
#     parameters:
#     - name: token
#       in: header
#       type: string
#     responses:
#       400:
#        description: Token過期
#        schema:
#          id: TokenError
#          properties:
#            code:
#              type: number
#              description: code
#              example: 400
#            message:
#              type: string
#              description: 失敗訊息
#              example: "token已過期"
#       200:
#        description: 驗證成功
#        schema:
#          id: TokenSuccess
#          properties:
#            code:
#              type: number
#              description: code
#              example: 200
#            level_num:
#              type: number
#              description: code
#              example: 0
#            name:
#              type: string
#              description: code
#              example: 200
#            user_id:
#              type: number
#              description: code
#              example: 0123456789
#            user_qrcode:
#              type: string
#              description: code
#              example: 200
#            message:
#              type: string
#              description: 成功訊息
#              example: 驗證成功
#     """
#     if request.method == 'GET':
#         token = request.headers.get('Authorize')
#         if token == None:
#           return {'code':401,'message':'無附帶token'}
#         if 'Authorize' in request.headers:
#             try:
#                 phone = jwt.decode(token, 'mindnode', algorithms=['HS256'])['phone']
#                 return_me = user_data_f(phone,en_name)
#                 return return_me
#             except:
#                 return {'code':401,'message':'token已過期'},401
#         else:
#           return {'code':401,'message':'無附帶token','123':request.headers},401

# #使用者資料(指定因子)
# @admin.route('/<en_name>/data/<factor>' ,methods=['GET'])
# def user_data_factor(en_name,factor):
#     """
        
#     ---
#     tags:
#       - Admin
#     produces: application/json,
#     parameters:
#     - name: token
#       in: header
#       type: string
#     responses:
#       400:
#        description: Token過期
#        schema:
#          id: TokenError
#          properties:
#            code:
#              type: number
#              description: code
#              example: 400
#            message:
#              type: string
#              description: 失敗訊息
#              example: "token已過期"
#       200:
#        description: 驗證成功
#        schema:
#          id: data_factor
#          properties:
#            code:
#              type: number
#              description: code
#              example: 200
#            factor(ex.level_num):
#              type: number
#              description: code
#              example: 0
#            message:
#              type: string
#              description: 成功訊息
#              example: 驗證成功
#     """
#     if request.method == 'GET':
#         token = request.headers.get('Authorize')
#         if token == None:
#           return {'code':401,'message':'無附帶token'}
#         if 'Authorize' in request.headers:
#             try:
#                 phone = jwt.decode(token, 'mindnode', algorithms=['HS256'])['phone']
#                 return_me = user_data_f(phone,en_name,factor)
#                 return return_me
#             except:
#                 return {'code':401,'message':'token已過期'},401
#         else:
#           return {'code':401,'message':'無附帶token','123':request.headers},401