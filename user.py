from pydoc import describe
from colorama import Cursor
from flask_restful import reqparse
import pymysql
from flask import jsonify
import util
from flask_apispec import doc, use_kwargs, MethodResource, marshal_with
from user_route_model import UserGetResponse,UserOtherResponse,UserPostRequest,UserPatchRequest,LoginReqest
from flask_jwt_extended import create_access_token,jwt_required
from datetime import timedelta

def db_init():
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        db='cartproject'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)#傳參，輸出結果為字典
    return db, cursor

def get_access_token(username):
    token = create_access_token(
        identity={"username": username},
        expires_delta=timedelta(days=1)
    )
    return token

class Users(MethodResource):
    @doc(description="Get user info",tags=["User"])
    @marshal_with(UserGetResponse,code=200)
    @jwt_required()
    def get(self):
        db,cursor = db_init()

        sql="SELECT * FROM cartproject.user;"

        cursor.execute(sql)
        users = cursor.fetchall()#獲取所有行資料來源
        db.close()
        return util.success(users)
        
    @doc(description="Create user info",tags=["User"])
    @use_kwargs(UserPostRequest,location="json")
    @marshal_with(UserOtherResponse,code=200)
    def post(self,**kwargs):
        db,cursor = db_init()
        
        user = {
            'id': kwargs['id'],
            'username': kwargs['username'],
            'password': kwargs.get('password') ,
            'email': kwargs.get('email'),
        }
        sql = """

        INSERT INTO `cartproject`.`user` (`id`,`username`,`password`,`email`)
        VALUES ('{}','{}','{}','{}');

        """.format(
            user['id'], user['username'], user['password'], user['email'])

        

       
        
        result = cursor.execute(sql)


        db.commit()
        db.close()
        if result == 1:
            return util.success()
        
        return util.failure

     

class User(MethodResource):
    @doc(description="Post user info",tags=["User"])
    @use_kwargs(UserPatchRequest,location="json")
    @marshal_with(UserOtherResponse,code=200)
    def patch(self,id, **kwargs):
        db, cursor = db_init()
       
        user = {
            'username': kwargs.get('username'),
            'password': kwargs.get('password'),
            'email': kwargs.get('email'),
        }

        query = []
        print(user)
        '''{'username': None, 'password': 'Double', 'email': None}'''
        for key, value in user.items():
            if value is not None:
                query.append(f"{key} = '{value}'")
        query = ",".join(query)
        '''
        UPDATE table_name
        SET column1=value1, column2=value2, column3=value3···
        WHERE some_column=some_value;

        '''
        sql = """

        INSERT INTO `cartproject`.`user` (`username`,`password`,`email`)
        VALUES ('{}','{}','{}');

        """.format(
            user['username'], user['password'], user['email'])
            

        result = cursor.execute(sql)
        message = "success" if result == 1 else "failure"
        db.commit()
        db.close()
        
        if result == 1:
            return util.success()
        
        return util.failure()

    @doc(description="Delete user info",tags=["User"])
    @marshal_with(UserOtherResponse,code=200)
    def delete(self, id):
        db, cursor = db_init()
        sql = f'DELETE FROM `cartproject`.`user` WHERE id = {id};'
        result = cursor.execute(sql)
        message = "success" if result == 1 else "failure"
        db.commit()
        db.close()

        if result == 1:
            return util.success()
        
        return util.failure()

class Login(MethodResource):
    @doc(description='User Login', tags=['Login'])
    @use_kwargs(LoginReqest, location="json")
    # @marshal_with(user_router_model.UserGetResponse, code=200)
    def post(self, **kwargs):
        db, cursor = db_init()
        username, password = kwargs["username"], kwargs["password"]
        sql = f"SELECT * FROM cartproject.user WHERE username = '{username}' AND password = '{password}';"
        cursor.execute(sql)
        user = cursor.fetchall()
        db.close()

        if user != ():
            token = get_access_token(username)
            data = {
                "message": f"Welcome back {user[0]['username']}",
                "token": token}
            return util.success(data)
        
        return util.failure({"message":"Account or password is wrong"})