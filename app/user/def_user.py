from ..Module import *
from ..db_setting import *


#使用者註冊
def usercreate(name,password,phone):
    select_phone_q = f"select phone from user.users where phone = '{phone}'"
    have_phone = mysql_engine.execute(select_phone_q).fetchone()
    if have_phone == None:
      while(True):
        user_id = random.randint(1000000000,9999999999)
        select_user_id_q = f"select user_id from user.users where user_id = '{user_id}'"
        have_user_id = mysql_engine.execute(select_user_id_q).fetchone()
        if have_user_id == None:
          hashpassword = hash_password(password)
          
          #建立商圈logo暫存區 以利qrcode生成
          if not os.path.isdir(shopping_area_data_path):
            os.makedirs(shopping_area_data_path)
          if not os.path.isdir(shopping_area_data_path + '/qrcode'):
            os.makedirs(shopping_area_data_path + '/qrcode')
          #生成使用者QRcode
          myqr.run(words = f'{user_id}', # 可放網址或文字(限英文)
            version = 5, # QR Code的邊長，越大圖案越清楚
            level = 'H', # 糾錯水平，預設是H(最高)
            save_name = shopping_area_data_path + '/qrcode' + f'/{user_id}_qrcode.png') # 儲存檔案名稱
          with open(shopping_area_data_path + '/qrcode' + f'/{user_id}_qrcode.png', "rb") as image_file:
            qrcode_base64 = base64.b64encode(image_file.read())
          qrcode_base64 = 'data:image/png;base64,' + qrcode_base64.decode('utf-8')
          #-----------------------------

          sql_cmd = f"INSERT INTO user.users (name, password, phone, user_id, user_qrcode) VALUES ('{name}','{hashpassword}','{phone}','{user_id}','{qrcode_base64}')"
          mysql_engine.execute(sql_cmd)

          #清空暫存資料夾
          shutil.rmtree(shopping_area_data_path + '/qrcode')
          os.mkdir(shopping_area_data_path + '/qrcode')

          #自動增加run_level_number
          sql_cmd = "SHOW COLUMNS FROM user.run_level_number;"
          df = pd.read_sql(sql_cmd,con=mysql_engine)
          area_list = list(df['Field'].tolist()[2:])
          columns = ''
          zero = ''
          print(area_list,len(area_list))
          for num in range(len(area_list)):
            columns += f',{area_list[num]}'
            zero += ",'0'"
          sql_cmd = f"INSERT INTO user.run_level_number (user_id{columns}) VALUES ('{user_id}'{zero})"
          mysql_engine.execute(sql_cmd)

          token = make_token(phone)
          return {'code':200,'user_id':user_id,'token':token,'message':'已完成註冊'}, 200
    else:
      return {'code':400,'message':'電話已被註冊'}, 400

#使用者登入
def user_login_f(phone,password):
    bcrypt = Bcrypt()
    select_phone_q = f"select * from user.users where phone = '{phone}'"
    have_phone = mysql_engine.execute(select_phone_q).fetchone()
    if have_phone != None:
      sql_password = have_phone['password']
      if bcrypt.check_password_hash(sql_password, str(password)):
        token = make_token(phone)
        name = have_phone['name']
        user_id = have_phone['user_id']
        return {'code':200, 'name':name, 'user_id':user_id, 'token':token,'message':'登入成功'}, 200
      else:
        return {'code':400, 'message':'密碼錯誤'}, 400
    else:
      return {'code':400, 'message':'號碼未被註冊'}, 400
      
      
#使用者資料
def user_data_f(phone,shopping_area_en_name,factor=None):
    select_phone_q = f"select * from user.users where phone = '{phone}'"
    have_phone = mysql_engine.execute(select_phone_q).fetchone()
    if have_phone != None:
        name = have_phone['name']
        user_id = have_phone['user_id']
        user_qrcode = have_phone['user_qrcode'].decode('utf-8')
        select_level_num_q = f"select {shopping_area_en_name}_num from user.run_level_number where user_id = '{user_id}'"
        level_num = mysql_engine.execute(select_level_num_q).fetchone()
        level_num = level_num[f'{shopping_area_en_name}_num']
        if factor == None:
          return {'code':200, 'name':name, 'user_id':user_id,'level_num':level_num,'user_qrcode':user_qrcode,'message':'驗證成功'}, 200
        else:
          return {'code':200, factor:locals()[factor],'message':'驗證成功'}, 200

    else:
      return {'code':400, 'message':'號碼未被註冊'}, 400      
      
#闖關
def run_level_f(phone,shopping_area_en_name,shop_id):
    #取得通關數
    select_lottery_level_num_q = f"select lottery_level_num from shopping_area.shopping_area_infor where shopping_area_eg_name = '{shopping_area_en_name}'"
    lottery_level_num = mysql_engine.execute(select_lottery_level_num_q).fetchone()
    lottery_level_num = lottery_level_num['lottery_level_num']
    

    #以電話搜尋user_id
    select_phone_q = f"select * from user.users where phone = '{phone}'"
    have_phone = mysql_engine.execute(select_phone_q).fetchone()
    user_id = have_phone['user_id']
    
    #以user_id搜尋run_level
    select_run_level_q = f"select {shopping_area_en_name}_num from user.run_level_number where user_id = '{user_id}'"
    run_level = mysql_engine.execute(select_run_level_q).fetchone()
    level_num = run_level[f'{shopping_area_en_name}_num']#該商圈闖關次數
    
    #搜尋是否已闖過此商店
    select_level_q = f"select * from user.run_level where user_id = '{user_id}' AND shop_id = '{shop_id}'"
    select_level =mysql_engine.execute(select_level_q).fetchone()
    
    #到 商圈 資料庫搜尋是否存在此 商店
    select_shop_q = f"select * from ShopArea_{shopping_area_en_name}.shop where shop_id = '{shop_id}'"
    select_shop = mysql_engine.execute(select_shop_q).fetchone()
    if select_shop != None:
        if select_level == None:
            level_num = int(level_num) + 1
            name = select_shop['shop_name']
            introduction  = select_shop['shop_introduction']
            if level_num > int(lottery_level_num):
                return {'code':203, 'message':'趕緊去抽獎'}, 203
            
            if level_num == int(lottery_level_num):
                level_up_q = f"UPDATE user.run_level_number SET {shopping_area_en_name}_num = '{level_num}'  WHERE user_id = '{user_id}'"
                mysql_engine.execute(level_up_q)
                
                sql_cmd = f"INSERT INTO user.run_level (user_id, shop_id) VALUES ('{user_id}','{shop_id}')"
                mysql_engine.execute(sql_cmd)
                return {'code':200, 'name':name, 'introduction':introduction, 'message':f'累積達{lottery_level_num}次，趕緊抽獎去'}, 200
            else:
                level_up_q = f"UPDATE user.run_level_number SET {shopping_area_en_name}_num = '{level_num}'  WHERE user_id = '{user_id}'"
                mysql_engine.execute(level_up_q)
                
                sql_cmd = f"INSERT INTO user.run_level (user_id, shop_id) VALUES ('{user_id}','{shop_id}')"
                mysql_engine.execute(sql_cmd)
                return {'code':200, 'name':name, 'introduction':introduction, 'message':'闖關成功'}, 200
            
        else:
          return {'code':400, 'message':'此關已闖過'}, 400
    else:
        return {'code':400, 'message':'無此商店'}, 400


#使用者抽獎
def user_get_prize_f(lottert_method,shopping_area_en_name,user_name,phone):
    select_phone_q = f"select * from user.users where phone = '{phone}'"
    have_phone = mysql_engine.execute(select_phone_q).fetchone()
    if have_phone != None:
        user_id = have_phone['user_id']
        if lottert_method == 1:
          select_prize_q = f"select * from shoparea_{shopping_area_en_name}.prize order by prize_probability asc"
          select_prize = mysql_engine.execute(select_prize_q)
          prize_list = []
          probability_list= [0,]
          for row in select_prize:
              prize_list.append(row['prize'])
              probability_list.append(int(row['prize_probability']))
          num = random.randint(0,100)
          f_num = 0
          for i in range(len(prize_list)):
            f_num += probability_list[i]
            l_num = f_num + probability_list[i+1]

            if num > f_num and num <= l_num:
              get_prize = prize_list[i]

              select_prize_q = f"select * from shoparea_{shopping_area_en_name}.prize where prize = '{get_prize}'"
              select_prize = mysql_engine.execute(select_prize_q).fetchone()
              last_num = int(select_prize['last_quantity']) + 1
              
              level_up_q = f"UPDATE shoparea_{shopping_area_en_name}.prize SET last_quantity = '{last_num}'  WHERE prize = '{get_prize}'"
              mysql_engine.execute(level_up_q)
              
              while(True):
                  #產生英數10位隨機數
                  prize_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10) )

                  select_prize_id_q = f"select prize_id from user.user_get_prize where prize_id = '{prize_id}'"
                  select_prize_id = mysql_engine.execute(select_prize_id_q).fetchone()
                  if select_prize_id == None:
                      sql_cmd = f"INSERT INTO user.user_get_prize (phone, shopping_area_en_name, prize, prize_id) VALUES ('{phone}','{shopping_area_en_name}','{get_prize}','{prize_id}')"
                      mysql_engine.execute(sql_cmd)
                      return {'code':200,'get':1,'prize':get_prize}
          return {'code':200,'get':0,'prize':'銘謝惠顧'}


        """if num < 7:
            get_prize = prize_list[random.randint(0,len(prize_list))]
            select_prize_q = "select * from prize where prize = '{}'".format(get_prize)
            select_prize = db.engine.execute(select_prize_q).fetchone()
            prize_num = select_prize['all_quantity']
            prize_num = int(prize_num) - 1
            last_num = 40 - prize_num
            
            level_up_q = "UPDATE prize SET all_quantity = '{}'  WHERE prize = '{}'".format(prize_num,get_prize)
            db.engine.execute(level_up_q)
            level_up_q = "UPDATE prize SET last_quantity = '{}'  WHERE prize = '{}'".format(last_num,get_prize)
            db.engine.execute(level_up_q)
            
            while(True):
                prize_id = random.randint(100000,999999)
                prize_id = 'SL' + str(prize_id)                
                select_prize_id_q = "select prize_id from user_get_prize where prize_id = '{}'".format(prize_id)
                select_prize_id = db.engine.execute(select_prize_id_q).fetchone()
                if select_prize_id == None:
                    sql_cmd = "INSERT INTO user_get_prize (phone, prize, prize_id) VALUES ('{}','{}','{}')".format(phone,get_prize,prize_id)
                    db.engine.execute(sql_cmd)
                    return {'code':200,'get':1,'prize':get_prize}
        else:
            return {'code':200,'get':0,'prize':'銘謝惠顧'}"""
            
        return {'123':num}
    else:
      return {'code':400, 'message':'號碼未被註冊'}, 400

#使用者獎品列表
def user_get_all_prize_f(phone):
    select_phone_q = f"select * from user.user_get_prize where phone = '{phone}'"
    have_phone = mysql_engine.execute(select_phone_q)
    prize_list = []
    if have_phone != None:
        for row in have_phone:
            prize_list.append({"img":"https://fakeimg.pl/100x100/?retina=1&text=%E5%84%AA%E6%83%A0%E5%8D%B7&font=noto","prize":row['prize'],"describe":f"{row['prize']}_{row['shopping_area_en_name']}","prize_id":row['prize_id']})
        return jsonify(prize_list),200
    else:
      return {'code':400,'message':'無獲得獎品紀錄'},400