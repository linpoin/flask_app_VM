from flask import request
from flask import Blueprint
from .def_shopping_area import *

shopping_area=Blueprint('shopping_area',__name__)

@shopping_area.route('/')
def index():
    return 'shopping_area.hello'

#商圈註冊
@shopping_area.route('/signup' ,methods=['POST'])
def shopping_area_signup():
    """
        
    ---
    tags:
      - Shopping_Area
    produces: application/json,
    parameters:
    - name: shopping_area_name
      in: body
      type: string
    - name: shopping_area_eg_name
      in: body
      type: string
    - name: shopping_logo
      in: body
      type: string
    - name: shopping_banner
      in: body
      type: string
    - name: welcome_text
      in: body
      type: string
    - name: activity_rule
      in: body
      type: string
    - name: convert_prize_rule
      in: body
      type: string
    - name: lottery_level_num
      in: body
      type: integer
    - name: lottery_method
      in: body
      type: integer
    - name: shop_list
      in: body
      type: string
      example: [{'shop_name':abc,'shop_id':123456,'shop_address':XX市...,'shop_phone':0912345678}]
    responses:
      400:
       description: 輸入資訊不完全
       schema:
         id: ShopSignupInputError
         properties:
           code:
             type: number
             description: code
             example: 400
           message:
             type: string
             description: 失敗訊息
             example: "無此商圈名稱"
      200:
       description: 註冊成功
       schema:
         id: ShopSignupSuccess
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
        if 'shopping_area_name' in body_json.keys() and 'shopping_area_eg_name' in body_json.keys() and 'shopping_logo' in body_json.keys() and 'shopping_banner' in body_json.keys() and 'welcome_text' in body_json.keys() and 'activity_rule' in body_json.keys() and 'convert_prize_rule' in body_json.keys() and 'lottery_method' in body_json.keys() and 'shop_list' in body_json.keys() and 'lottery_level_num' in body_json.keys() and 'repeat_pass' in body_json.keys() and 'verification_method' in body_json.keys() and 'prize_list' in body_json.keys():
            name = body_json['shopping_area_name']
            eg_name = body_json['shopping_area_eg_name']
            logo = body_json['shopping_logo']
            banner = body_json['shopping_banner']
            welcome = body_json['welcome_text']
            activity_rule = body_json['activity_rule']
            convert_prize_rule = body_json['convert_prize_rule']
            lottery_method = body_json['lottery_method']
            shop_list = body_json['shop_list']
            lottery_level_num = body_json['lottery_level_num']
            repeat_pass = body_json['repeat_pass']
            verification_method = body_json['verification_method']
            prize_list = body_json['prize_list']
            
            return_me = shopping_area_create(name,eg_name,logo,banner,welcome,activity_rule,convert_prize_rule,lottery_method,shop_list,lottery_level_num,repeat_pass,verification_method,prize_list)
            return return_me
        else:
            error = {'code':400,
                    'message':'請輸入完整資訊',
            }
            return error, 400

#商圈列表
@shopping_area.route('/list' ,methods=['GET'])
def shopping_area_list():
    """
        
    ---
    tags:
      - Shopping_Area
    produces: application/json,
    responses:
      400:
       description: 輸入資訊不完全
       schema:
         id: ShopSignupInputError
         properties:
           code:
             type: number
             description: code
             example: 400
           message:
             type: string
             description: 失敗訊息
             example: "無此商圈名稱"
      200:
       description: 成功資訊
       schema:
         id: ShopSignupSuccess
         properties:
           shopping_area_name:
             type: string
             description: 成功訊息
             example: "範例"
           shopping_area_eg_name:
             type: string
             description: 成功訊息
             example: "test"
    """
    if request.method == 'GET':
      return_me = select_shopping_area_list()
      return return_me

#商圈資訊
@shopping_area.route('/<shop_area_en_name>' ,methods=['GET'])
def shopping_area_info(shop_area_en_name):
    """
        
    ---
    tags:
      - Shopping_Area
    produces: application/json,
    responses:
      400:
       description: 輸入資訊不完全
       schema:
         id: No_Shopping_Error
         properties:
           code:
             type: number
             description: code
             example: 400
           message:
             type: string
             description: 失敗訊息
             example: "無此商圈名稱"
      200:
       description: 商圈資訊
       schema:
         id: Shopping_shop_list_Success
         properties:
           shopping_area_name:
             type: string
             description: 成功訊息
             example: "shopping_area_name"
           shopping_area_eg_name:
             type: string
             description: 成功訊息
             example: "shopping_area_eg_name"
           shopping_logo:
             type: string
             description: 成功訊息
             example: "shopping_logo"
           shopping_banner:
             type: string
             description: 成功訊息
             example: "shopping_banner"
           welcome_html:
             type: string
             description: 成功訊息
             example: "welcome_text"
           activity_rule_html:
             type: string
             description: 成功訊息
             example: "activity_rule_html"
           convert_prize_rule_html:
             type: string
             description: 成功訊息
             example: "convert_prize_rule_html"
           activity_rule_text:
             type: string
             description: 成功訊息
             example: "activity_rule_text"
           convert_prize_rule_text:
             type: string
             description: 成功訊息
             example: "convert_prize_rule_text"
           lottery_level_num:
             type: string
             description: 成功訊息
             example: "lottery_level_num"
           lottery_method:
             type: string
             description: 成功訊息
             example: "lottery_method"
           shop_list:
             type: string
             description: 成功訊息
             example: "shop_list"
    """
    if request.method == 'GET':
      return_me = select_shopping_area_info(shop_area_en_name)
      return return_me