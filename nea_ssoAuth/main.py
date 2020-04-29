from flask import Flask
from flask_restful import Api

from config.config import sso_auth, mongo_params
from .resources import NewAuth, OAuthCatcher

app = Flask(__name__)
api = Api(app)

api.add_resource(
    NewAuth, '/new_auth',
    resource_class_kwargs={'mongo_params': mongo_params, 'sso_auth': sso_auth}
)
api.add_resource(
    OAuthCatcher, '/_oauth',
    resource_class_kwargs={'mongo_params': mongo_params, 'sso_auth': sso_auth}
)
