from flask_restful import Resource, reqparse
import pymysql
from flask import jsonify, Response
import traceback
from collections import OrderedDict
import json
from dotenv import load_dotenv
import os
load_dotenv()

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('account_number')
parser.add_argument('user_id')
parser.add_argument('balance')
parser.add_argument('deleted')

# 為 GET 方法創建 parser
get_parser = reqparse.RequestParser()
get_parser.add_argument('gender', location='args')


class Accounts(Resource):
    def db_init(self):
        db = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWD'),
            database=os.getenv('DB_SCHEMA')
            )
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self,user_id):
        db, cursor = self.db_init()
        arg = get_parser.parse_args()
        sql = f"""SELECT * FROM api_flask.accounts WHERE user_id = '{user_id}' AND deleted IS NOT True"""
        cursor.execute(sql)
        db.commit()
        accounts = cursor.fetchall()
        db.close()

        return jsonify({'data':accounts})
    
    def post(self,user_id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
                    "id": arg["id"],
                    "account_number": arg["account_number"],
                    "balance": arg["balance"],
                    "user_id": arg["user_id"],
                    "deleted": arg["deleted"] or False
                  }
        sql = """INSERT INTO `api_flask`.`accounts` (`id`, `account_number`, `balance`, `user_id`) VALUES ('{}', '{}', '{}', '{}');
        """.format(arg["id"],arg['account_number'],arg["balance"],arg["user_id"])

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'succuss'

        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        
        db.commit()
        db.close()
        return jsonify(response)
    

class Account(Resource):
    def db_init(self):
        db = pymysql.connect(
            
            )
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self, user_id, id):
        db, cursor = self.db_init()
        sql = f"""SELECT * FROM api_flask.accounts WHERE deleted IS NOT True AND id = '{id}'"""
        cursor.execute(sql)
        db.commit()
        account = cursor.fetchone()
        db.close()

        # 按順序重新組織資料
        ordered_data = OrderedDict([
                                    ("id", account["id"]),
                                    ("account_number", account["account_number"]),
                                    ("balance",account["balance"]),
                                    ("user_id",account["user_id"]),
        ])

        response_data = json.dumps({"data": ordered_data}, ensure_ascii=False)

        # 返回 JSON 字串，並指定 Content-Type
        return Response(response_data, content_type="application/json")
    
    def patch(self,user_id,id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
                    "id": arg["id"],
                    "account_number": arg["account_number"],
                    "balance": arg["balance"],
                    "user_id": arg["user_id"],
                  }        
        query = []
        for key, value in account.items():
            if value is not None:
                query.append(key + " = "+ f"'{value}'")

        query =", ".join(query)
        
        sql = f"""UPDATE api_flask.accounts SET {query} WHERE id ='{id}'"""

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'succuss'

        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        
        db.commit()
        db.close()
        return jsonify(response)
        
    def delete(self, user_id,id):
        db, cursor = self.db_init()

        sql = f"""UPDATE `api_flask`.`accounts` SET deleted = True WHERE (`id` = '{id}');
        """
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'succuss'

        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        
        db.commit()
        db.close()
        return jsonify(response)




