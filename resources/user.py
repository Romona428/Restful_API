from flask_restful import Resource, reqparse
import pymysql
from flask import jsonify, make_response
import traceback
from server import db
from models import UserModel
from dotenv import load_dotenv
import os
load_dotenv()


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

# 為 GET 方法創建 parser
get_parser = reqparse.RequestParser()
get_parser.add_argument('gender', location='args')


class User(Resource):
    def db_init(self):
        db = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWD'),
            database=os.getenv('DB_SCHEMA')
            )
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self,id):
        db, cursor = self.db_init()
        sql = f"Select * from api_flask.users Where id = '{id}' and deleted is not True"
        cursor.execute(sql)
        db.commit()
        user = cursor.fetchone()
        db.close()

        return jsonify({'data':user})

    def patch(self,id):
        # db, cursor = self.db_init()
        arg = parser.parse_args()
        # user = {
        #     'name':arg['name'],
        #     'gender':arg['gender'],
        #     'birth':arg['birth'],
        #     'note':arg['note']
        # }
        # query = []
        # for key, value in user.items():
        #     if value is not None:
        #         query.append(key + " = " + f"'{value}'")
        
        # query =", ".join(query)

        # sql =f"""UPDATE `api_flask`.`users` SET {query} WHERE (`id` = '{id}');
        # """
        user = UserModel.query.filter_by(id = id, deleted = None).first()
        if arg['name'] is not None:
            user.name = arg['name']
        response = {}
        try:
            # cursor.execute(sql)
            db.session.commit()
            response['msg'] = 'succuss'

        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        
        # db.commit()
        # db.close()
        return jsonify(response)
    
    def delete(self,id):
        # db, cursor = self.db_init()

        # sql = f"""UPDATE `api_flask`.`users` SET deleted = True WHERE (`id` = '{id}');
        # """
        user = UserModel.query.filter_by(id = id, deleted = None).first()
        response = {}
        try:
            # cursor.execute(sql)
            db.session.delete(user)
            db.session.commit()
            response['msg'] = 'succuss'

        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        
        # db.commit()
        # db.close()
        return jsonify(response)



class Users(Resource):
    def db_init(self):
        db = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWD'),
            database=os.getenv('DB_SCHEMA')
            )
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    
    def get(self):
        # db, cursor = self.db_init()
        # arg = get_parser.parse_args()
        # sql = 'Select * from api_flask.users Where deleted is not True'
        # if arg["gender"] is not None:
        #     sql += f""" and gender = '{arg['gender']}'"""
        # cursor.execute(sql)
        # db.commit()
        # users = cursor.fetchall()
        # db.close()
        # return jsonify({'data':users})


        users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        return jsonify({'data':list(map(lambda user: user.serialize(), users))})
    
    def post(self):
        # db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name':arg['name'],
            'gender':arg['gender'],
            'birth':arg['birth'],
            'note':arg['note']
        }

        # sql = """INSERT INTO `api_flask`.`users` (`name`, `gender`, `birth`, `note`) VALUES ('{}', '{}', '{}', '{}');
        #       """.format(user['name'],user['gender'],user['birth'],user['note'])
        
        response = {}
        status_code = 200
        try:
            # cursor.execute(sql)
            new_user = UserModel(name = user['name'], gender = user['gender'], birth = user['birth'], note = user['note'])
            db.session.add(new_user)
            db.session.commit()
            response['msg'] = 'succuss'

        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'failed'
        
        # db.commit()
        # db.close()
        return make_response(jsonify(response),status_code)
