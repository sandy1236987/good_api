import pymysql
from user_route_model import *
import util
from flask_apispec import doc, use_kwargs, MethodResource, marshal_with 
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


class cart(MethodResource):
    @doc(description='查詢購物車內容', tags=['Cart'])
    @use_kwargs(CartListRequest, location="json") 
    # @marshal_with(CartGetResponse, code=200)
    @jwt_required() 
    def get(self,**kwargs):
        db, cursor = db_init()

        goods_name=kwargs.get("goods_name")
        number=kwargs.get("number")
        username=kwargs.get("username")

        sql1="SELECT*FROM cartproject.cart"
        cursor.execute(sql1)
        result = cursor.fetchall()

        sql2=f"SELECT SUM(`cart`.`number` * `goods`.`price`) AS total_price FROM `cart` LEFT JOIN `goods` ON `cart`.`goods_name` = `goods`.`goods_name`;"
        cursor.execute(sql2)
        result1 = cursor.fetchall()
        db.close()
        return util.success(result+result1)

    @doc(description="添加或更新購物車商品", tags=["Cart"])
    @use_kwargs(CartPostRequest, location="json")
    @marshal_with(CartGetResponse, code=200)
    @jwt_required()
    def post(self,**kwargs):
        db, cursor = db_init()

        goods_name=kwargs.get("goods_name")
        number=kwargs.get("number")
        username=kwargs.get("username")

        sql = """
            INSERT INTO cartproject.cart (goods_name,number,username)
            VALUES ('{}','{}','{}')
            """.format(goods_name,number,username)

        result = cursor.execute(sql)
        db.commit()
        db.close()
        
        if result == 1:
            return util.success()
        else:
            return util.failure()
   
    @doc(description='刪除購物車商品', tags=['Cart']) 
    @use_kwargs(CartDeleteRequest, location="json")
    # @marshal_with(CartGetResponse, code=200) 
    @jwt_required() 
    def delete(self,name):
        db, cursor = db_init()
        
        sql = "DELETE FROM cartproject.cart WHERE goods_name = '{}';".format(name)
        cursor.execute(sql)
        db.commit()
        db.close()
        return util.success()
