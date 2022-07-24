import pymysql
import util
from flask_apispec import doc, use_kwargs, MethodResource, marshal_with 
from user_route_model import *
from flask_jwt_extended import jwt_required 



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

##查看產品清單##
class goods(MethodResource):
    @doc(description='不輸入品名直接查詢全部產品清單', tags=['goodsList']) 
    @use_kwargs(Productlistrequest, location="json") 
    @marshal_with(ProductGetResponse, code=200)
    @jwt_required() 
    def get(self, **kwargs):
        db, cursor = db_init()

        goods_name = kwargs.get("goods_name") 
        if goods_name == None:
            sql = "SELECT * FROM cartproject.goods ;"
        else:
            sql = "SELECT * FROM cartproject.goods WHERE goods_name = '%{}%';".format(goods_name)          
 
        cursor.execute(sql)
        plist = cursor.fetchall()
        db.close()
        return util.success(plist)