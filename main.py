
from flask import Flask
from initial.database_table_ceate import run as datebase_create
from app.base.views import *
from app.user.views import *
from app.token.views import *
from app.shopping_area.views import *
from app.admin.views import *

try:
    datebase_create()  # 基本資料庫建置
except:
    pass

app = Flask(__name__)

app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False
app.config['SWAGGER'] = {
    "title": "Uninn API",
    "description": "Uninn API",
    "version": "1.0.0",
    "termsOfService": "",
    "hide_top_bar": True
}
CORS(app)
Swagger(app)

app.register_blueprint(base, url_prefix='/')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(token, url_prefix='/token')
app.register_blueprint(shopping_area, url_prefix='/shopping_area')

if __name__ == '__main__':
    print(app.url_map)
    app.run('0.0.0.0', debug=True)
