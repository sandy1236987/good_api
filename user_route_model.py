from marshmallow import Schema, fields

# Parameter (Schema)
class UserPostRequest(Schema):
    id = fields.Str(doc="id", required=True)
    username = fields.Str(doc="username", required=True)
    password = fields.Str(doc="password", required=True)
    email = fields.Str(doc="email", required=True)
    

class UserPatchRequest(Schema):
    id = fields.Str(doc="id", required=True)
    username = fields.Str(doc="username", required=True)
    password = fields.Str(doc="password", required=True)
    email = fields.Str(doc="email", required=True)
    

class LoginReqest(Schema):
    username = fields.Str(doc="username", required=True)
    password = fields.Str(doc="password", required=True)

# Get 定義資料格式型態
class UserGetResponse(Schema):
    message = fields.Str(example="success")
    data = fields.List(
        fields.Dict(), 
        example={
            "id": 1,
            "username": "name",
            "email": "amy123@gmail.com",
            
        }
    )
    datetime = fields.Str()

class UserOtherResponse(Schema):
    message = fields.Str(example="success")

class Productlistrequest(Schema):
    goods_name = fields.Str(doc="goods_name")
    
#response
class ProductGetResponse(Schema):
    data = fields.List(fields.Dict())



class CartListRequest(Schema):
    goods_name = fields.Str(example="string") 

class CartPostRequest(Schema):
    goods_name = fields.Str(doc="goods_name", example="string", required=True)
    number = fields.Str(doc="number", example="string", required=True)
    username = fields.Str(doc="username", example="string", required=True)




class CartDeleteRequest(Schema):
    goods_name = fields.Str(example="string", required=True)

#response
class CartGetResponse(Schema):
    data = fields.List(fields.Dict())