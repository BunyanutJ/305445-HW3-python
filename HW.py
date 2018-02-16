Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> import pymongo
from datetime import datetime,date
from flask import Flask,request
from flask_restful import Resource ,Api ,reqparse

client = pymongo.MongoClient('localhost',27017)

app= Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('firstname')
parser.add_argument('lastname')
parser.add_argument('employeeNumber')

db = client.db_example1

work = db.work
class HistoryWork(Resource):
        def get(self):
                args = parser.parse_args()
                id = args['id']
                data = work.find_one({"user.employeeNumber":id})
                if(data):
                        firstname = data['user']['firstname']
                        lastname = data['user']['lastname']
                        list_work = data['list_work']
                        return {"firstname":firstname,"lastname":lastname,"list_work":list_work}
                return {}
class Registration(Resource):
        def post(self):
                args = parser.parse_args()
                id = args['employeeNumber']
                firstname = args['firstname']
                lastname = args['lastname']
                password = args['password']
                data = work.find_one({"user.employeeNumber":id})
                if(data):
                        return {"err":"has this id"}
                work.insert({"user":{"employeeNumber":id,"firstname":firstname,"lastname":lastname,"pastword":password},"list_work":[]})
                return {"firstname":firstname,"lastname":lastname,"employeeNumber":id,"password":password}
class Login(Resource):
        def post(self):
                args = parser.parse_args()
                username = args['username']
                password = args['password']
                data = work.find_one({"user.employeeNumber":username,"user.pastword":password})
                if(data):
                        firstname = data['user']['firstname']
                        lastname = data['user']['lastname']
                        datetime_login = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        work.update({"user.employeeNumber":username},{"$push":{"list_work":{"datetime":datetime_login}}})
                        return {"firstname":firstname,"lastname":lastname,"datetime":datetime_login}
                return {}
api.add_resource(Registration,'/api/register')
api.add_resource(Login,'/api/login')
api.add_resource(HistoryWork,'/api/list_work')

if __name__ == '__main__':
        app.run(host='0.0.0.0',port=5000)
