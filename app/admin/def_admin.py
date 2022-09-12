from ..Module import *
from ..db_setting import *

#管理員登入
def admin_login_f(account,password):
    bcrypt = Bcrypt()
    select_account_q = f"select * from shopping_area.admin_member where shopping_area_en_name = '{account}'"
    have_account = mysql_engine.execute(select_account_q).fetchone()
    if have_account != None:
      sql_password = have_account['password']
      if bcrypt.check_password_hash(sql_password, str(password)):
        token = make_token(sql_password)
        name = have_account['shopping_area_en_name']
        return {'code':200, 'shopping_area_en_name':name, 'token':token,'message':'登入成功'}, 200
      else:
        return {'code':400, 'message':'密碼錯誤'}, 400
    else:
      return {'code':400, 'message':'商圈未被註冊'}, 400

#使用者兌獎
def user_redeem_f(en_name,name,user_id):
    select_lottery_user_q = f"select user_id from shoparea_{en_name}.lottery_user where user_id = '{user_id}'"
    select_lottery_user = mysql_engine.execute(select_lottery_user_q).fetchone()
    if select_lottery_user == None:
        while(True):
            #產生英數10位隨機數
            lottery_num = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8) )

            select_lottery_num_q = f"select lottery_num from shoparea_{en_name}.lottery_user where lottery_num = '{lottery_num}'"
            select_lottery_num = mysql_engine.execute(select_lottery_num_q).fetchone()
            if select_lottery_num == None:
                update_lottery = f"INSERT INTO shoparea_{en_name}.lottery_user (user_name, user_id, lottery_num) VALUES ('{name}','{user_id}','{lottery_num}')"
                mysql_engine.execute(update_lottery)
                return {'code':200,'name':name,'user_id':user_id,'lottery_num':lottery_num},200
    else:
        return {'code':403,'message':'此用戶已兌換過抽獎資格'},403
    
#已兌換列表
def user_redeem_list_f(en_name):
    select_lottery_q = f"select lottery_num,user_name,user_id from shoparea_{en_name}.lottery_user"
    select_lottery_list = mysql_engine.execute(select_lottery_q)
    return jsonify(execute_to_list(select_lottery_list))
      
# #使用者資料
# def user_data_f(phone,shopping_area_en_name,factor=None):
#     select_phone_q = "select * from user.users where phone = '{}'".format(phone)
#     have_phone = mysql_engine.execute(select_phone_q).fetchone()
#     if have_phone != None:
#         name = have_phone['name']
#         user_id = have_phone['user_id']
#         user_qrcode = have_phone['user_qrcode'].decode('utf-8')
#         select_level_num_q = "select {}_num from user.run_level_number where user_id = '{}'".format(shopping_area_en_name,user_id)
#         level_num = mysql_engine.execute(select_level_num_q).fetchone()
#         level_num = level_num['{}_num'.format(shopping_area_en_name)]
#         if factor == None:
#           return {'code':200, 'name':name, 'user_id':user_id,'level_num':level_num,'user_qrcode':user_qrcode,'message':'驗證成功'}, 200
#         else:
#           return {'code':200, factor:locals()[factor],'message':'驗證成功'}, 200

#     else:
#       return {'code':400, 'message':'號碼未被註冊'}, 400      
      
# #闖關
# def run_level_f(phone,shopping_area_en_name,shop_id):
#     #取得通關數
#     select_lottery_level_num_q = "select lottery_level_num from shopping_area.shopping_area_infor where shopping_area_eg_name = '{}'".format(shopping_area_en_name)
#     lottery_level_num = mysql_engine.execute(select_lottery_level_num_q).fetchone()
#     lottery_level_num = lottery_level_num['lottery_level_num']
    

#     #以電話搜尋user_id
#     select_phone_q = "select * from user.users where phone = '{}'".format(phone)
#     have_phone = mysql_engine.execute(select_phone_q).fetchone()
#     user_id = have_phone['user_id']
    
#     #以user_id搜尋run_level
#     select_run_level_q = "select {}_num from user.run_level_number where user_id = '{}'".format(shopping_area_en_name,user_id)
#     run_level = mysql_engine.execute(select_run_level_q).fetchone()
#     level_num = run_level['{}_num'.format(shopping_area_en_name)]#該商圈闖關次數
    
#     #搜尋是否已闖過此商店
#     select_level_q = "select * from user.run_level where user_id = '{}' AND shop_id = '{}'".format(user_id,shop_id)
#     select_level =mysql_engine.execute(select_level_q).fetchone()
    
#     #到 商圈 資料庫搜尋是否存在此 商店
#     select_shop_q = "select * from ShopArea_{}.shop where shop_id = '{}'".format(shopping_area_en_name,shop_id)
#     select_shop = mysql_engine.execute(select_shop_q).fetchone()
#     if select_shop != None:
#         if select_level == None:
#             level_num = int(level_num) + 1
            
            
#             if level_num > int(lottery_level_num):
#                 return {'code':203, 'message':'趕緊去抽獎'}, 203
            
#             if level_num == int(lottery_level_num):
#                 level_up_q = "UPDATE user.run_level_number SET {}_num = '{}'  WHERE user_id = '{}'".format(shopping_area_en_name,level_num,user_id)
#                 mysql_engine.execute(level_up_q)
                
#                 sql_cmd = "INSERT INTO user.run_level (user_id, shop_id) VALUES ('{}','{}')".format(user_id,shop_id)
#                 mysql_engine.execute(sql_cmd)
#                 return {'code':200, 'message':'累積達5次，趕緊抽獎去'}, 200
#             else:
#                 level_up_q = "UPDATE user.run_level_number SET {}_num = '{}'  WHERE user_id = '{}'".format(shopping_area_en_name,level_num,user_id)
#                 mysql_engine.execute(level_up_q)
                
#                 sql_cmd = "INSERT INTO user.run_level (user_id, shop_id) VALUES ('{}','{}')".format(user_id,shop_id)
#                 mysql_engine.execute(sql_cmd)
#                 return {'code':200, 'message':'闖關成功'}, 200
            
#         else:
#           return {'code':400, 'message':'此關已闖過'}, 400
#     else:
#         return {'code':400, 'message':'無此商店'}, 400


# #使用者抽獎
# def user_get_prize_f(shopping_area_en_name,phone):
#     select_phone_q = "select * from user.users where phone = '{}'".format(phone)
#     have_phone = mysql_engine.execute(select_phone_q).fetchone()
#     if have_phone != None:
#         user_id = have_phone['user_id']

#         select_prize_q = "select * from shoparea_{}.prize order by prize_probability asc".format(shopping_area_en_name)
#         select_prize = mysql_engine.execute(select_prize_q)
#         prize_list = []
#         probability_list= [0,]
#         for row in select_prize:
#             prize_list.append(row['prize'])
#             probability_list.append(int(row['prize_probability']))
#         num = random.randint(0,100)
#         f_num = 0
#         for i in range(len(prize_list)):
#           f_num += probability_list[i]
#           l_num = f_num + probability_list[i+1]

#           if num > f_num and num <= l_num:
#             get_prize = prize_list[i]

#             select_prize_q = "select * from shoparea_{}.prize where prize = '{}'".format(shopping_area_en_name,get_prize)
#             select_prize = mysql_engine.execute(select_prize_q).fetchone()
#             last_num = int(select_prize['last_quantity']) + 1
            
#             level_up_q = "UPDATE shoparea_{}.prize SET last_quantity = '{}'  WHERE prize = '{}'".format(shopping_area_en_name,last_num,get_prize)
#             mysql_engine.execute(level_up_q)
            
#             while(True):
#                 #產生英數10位隨機數
#                 prize_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10) )

#                 select_prize_id_q = "select prize_id from user.user_get_prize where prize_id = '{}'".format(prize_id)
#                 select_prize_id = mysql_engine.execute(select_prize_id_q).fetchone()
#                 if select_prize_id == None:
#                     sql_cmd = "INSERT INTO user.user_get_prize (phone, shopping_area_en_name, prize, prize_id) VALUES ('{}','{}','{}','{}')".format(phone,shopping_area_en_name,get_prize,prize_id)
#                     mysql_engine.execute(sql_cmd)
#                     return {'code':200,'get':1,'prize':get_prize}
#         else:
#             return {'code':200,'get':0,'prize':'銘謝惠顧'}


#         """if num < 7:
#             get_prize = prize_list[random.randint(0,len(prize_list))]
#             select_prize_q = "select * from prize where prize = '{}'".format(get_prize)
#             select_prize = db.engine.execute(select_prize_q).fetchone()
#             prize_num = select_prize['all_quantity']
#             prize_num = int(prize_num) - 1
#             last_num = 40 - prize_num
            
#             level_up_q = "UPDATE prize SET all_quantity = '{}'  WHERE prize = '{}'".format(prize_num,get_prize)
#             db.engine.execute(level_up_q)
#             level_up_q = "UPDATE prize SET last_quantity = '{}'  WHERE prize = '{}'".format(last_num,get_prize)
#             db.engine.execute(level_up_q)
            
#             while(True):
#                 prize_id = random.randint(100000,999999)
#                 prize_id = 'SL' + str(prize_id)                
#                 select_prize_id_q = "select prize_id from user_get_prize where prize_id = '{}'".format(prize_id)
#                 select_prize_id = db.engine.execute(select_prize_id_q).fetchone()
#                 if select_prize_id == None:
#                     sql_cmd = "INSERT INTO user_get_prize (phone, prize, prize_id) VALUES ('{}','{}','{}')".format(phone,get_prize,prize_id)
#                     db.engine.execute(sql_cmd)
#                     return {'code':200,'get':1,'prize':get_prize}
#         else:
#             return {'code':200,'get':0,'prize':'銘謝惠顧'}"""
            
#         return {'123':num}
#     else:
#       return {'code':400, 'message':'號碼未被註冊'}, 400

# #使用者獎品列表
# def user_get_all_prize_f(phone):
#     select_phone_q = "select * from user.user_get_prize where phone = '{}'".format(phone)
#     have_phone = mysql_engine.execute(select_phone_q)
#     prize_list = []
#     if have_phone != None:
#         for row in have_phone:
#             prize_list.append({"img":"https://fakeimg.pl/100x100/?retina=1&text=%E5%84%AA%E6%83%A0%E5%8D%B7&font=noto","prize":row['prize'],"describe":"{}_{}".format(row['prize'],row['shopping_area_en_name']),"prize_id":row['prize_id']})
#         return jsonify(prize_list),200
#     else:
#       return {'code':400,'message':'無獲得獎品紀錄'},400