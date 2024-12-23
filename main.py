from flask import Flask, request, jsonify
from flask_restful import Api
from resources.user import Users, User
from resources.account import Accounts, Account
import pymysql, traceback, jwt, time
from server import app
from dotenv import load_dotenv
import os

load_dotenv()

# app = Flask(__name__)
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')
api.add_resource(Accounts, '/user/<user_id>/accounts')
api.add_resource(Account, '/user/<user_id>/account/<id>')


@app.errorhandler(Exception)
def handle_error(error):
    status_code = 500
    if type(error).__name__ == "NotFound":
        status_code = 404
    elif type(error).__name__ == "TypeError":
        status_code = 500
    return jsonify({'msg':type(error).__name__}), status_code 


# @app.before_request
# def auth():
#     token = request.headers.get('auth')
#     user_id = request.get_json()['user_id']
#     client_timestamp = request.get_json().get('timestamp')
#     SECRET_KEY = "my_secret_key"

#     valid_token = jwt.encode({'user_id':user_id, 'timestamp':client_timestamp}, SECRET_KEY, algorithm = 'HS256')
#     if token == valid_token:
#         pass
#     else:
#         return {'msg':'invalid token'}

@app.route('/')
def home():

    return "Bello World"


@app.route('/user/<user_id>/account/<id>/withdrew', methods = ['POST'])
def withdrew(user_id, id):
    db,cursor,account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] - int(money)
    response = {}
    if balance < 0:
        response['msg'] = 'You dont have enough money'
    else:
        sql = """UPDATE api_flask.accounts SET balance = {} WHERE id = {} and deleted IS NOT True""".format(balance,id)
        try:
            cursor.execute(sql)
            response['msg'] = 'succuss'

        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        
        db.commit()
        db.close()
    return jsonify(response)    

def get_account(id):
    db = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWD'),
            database=os.getenv('DB_SCHEMA')
            )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = f"""SELECT * FROM api_flask.accounts WHERE id = '{id}' and deleted IS NOT True"""
    cursor.execute(sql)
    return db, cursor, cursor.fetchone()


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)

