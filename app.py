from flask import Flask
from flask_restful import Api
from user import Users, User,Login
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager
from cart import cart
from goods import goods


app = Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ALGORITHM"] = "HS256"
jwt = JWTManager(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)


api.add_resource(Users, '/user')
docs.register(Users)
api.add_resource(User, '/user/<int:id>')
docs.register(User)
api.add_resource(Login,'/login')
docs.register(Login)
api.add_resource(cart, "/cart")
docs.register(cart)
api.add_resource(goods, "/goods")
docs.register(goods)

if __name__ == '__main__':
    jwt = JWTManager().init_app(app)
    app.run(debug=True)