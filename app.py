import flask
from flask_restful import Api
from resource.brand import Google,Trip,China,Pixnet
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_jwt_extended import JWTManager

# Flask setting
app = flask.Flask(__name__)

# Flask restful setting
api = Api(app)

app.config["DEBUG"] = True # Able to reload flask without exit the process
app.config["JWT_SECRET_KEY"] = "secret_key" #JWT token setting 

# Swagger setting
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='python一條龍_王品集團資料',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

# URL(router)
api.add_resource(Google, "/googlemap/<brand>")
docs.register(Google)
api.add_resource(Trip, "/tripadvisor/<brand>")
docs.register(Trip)
api.add_resource(China, "/chinatimes/<brand>")
docs.register(China)
api.add_resource(Pixnet, "/pixnet/<brand>")
docs.register(Pixnet)

if __name__ == '__main__':
    # JWT token setting
    jwt = JWTManager().init_app(app)
    app.run(host='0.0.0.0', port=10011)
