from bson.objectid import ObjectId
from datetime import datetime as dt, timedelta as td
from flask import request
from flask_restful import Resource
from jose import jwt
import pymongo as pm
import requests as rq

from ..tools import TokenProcessor

class OAuthCatcher(Resource):
    url = 'https://login.eveonline.com/v2/oauth/token'
    data_base = {
        'grant_type': 'authorization_code',
    }
    headers_base = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'login.eveonline.com',
    }
    database = 'EveSsoAuth'
    collections = {
        'pending': 'PendingAuths',
        'active': 'ActiveAuths',
    }
    
    def __init__(self, mongo_params, sso_auth):
        self.conn = pm.MongoClient(**mongo_params)
        self.data = {
            **self.data_base,
            'client_id': sso_auth['client_id'],
        }
        self.headers = {
            **self.headers_base,
        }
        
    def get(self):
        code_verifier = self.conn[self.database][self.collections['pending']].find_one(
            {'_id': ObjectId(request.args['state'])},
            {'_id': 0, 'code': 1},
        )['code']
        
        data = {
            **self.data,
            'code': request.args['code'],
            'code_verifier': code_verifier,
        }
        
        headers = {
            **self.headers,
        }
        
        resp = rq.post(self.url, data=data, headers=headers)
        token_rcd = TokenProcessor.process_token(resp.json())
        
        self.conn[self.database][self.collections['active']].update_one(
            {'_id': token_rcd['_id']},
            {'$set': token_rcd},
            upsert=True,
        )
        
        self.conn[self.database][self.collections['pending']].delete_one(
            {'_id': ObjectId(request.args['state'])}
        )
        
        return 'Complete'