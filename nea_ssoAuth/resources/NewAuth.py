import base64 as b64
from datetime import datetime as dt
from flask import redirect
from flask_restful import Resource
import hashlib
import pymongo as pm
import random
from urllib.parse import urlencode

class NewAuth(Resource):
    url = 'https://login.eveonline.com/v2/oauth/authorize/'
    params_base = {
        'response_type': 'code',
        'code_challenge_method': 'S256',
    }
    database = 'EveSsoAuth'
    collection = 'PendingAuths'
    
    def __init__(self, mongo_params, sso_auth):
        self.conn = pm.MongoClient(**mongo_params)
        self.params = {
            **self.params_base,
            'redirect_uri': sso_auth['callback_url'],
            'client_id': sso_auth['client_id'],
            'scope': ' '.join(sso_auth['scopes']),
        }
        
    def get(self):
        pending_auth = {
            'code': b64.urlsafe_b64encode(bytearray(random.getrandbits(8) for _ in range(32))),
            'requested_at': dt.utcnow(),
        }
        state = str(self.conn[self.database][self.collection].insert_one(pending_auth).inserted_id)
        
        params = {
            **self.params,
            'code_challenge': self._gen_challenge(pending_auth['code']),
            'state': state,
        }
        
        url = '{url}?{params}'.format(url=self.url, params=urlencode(params))
        resp = redirect(url, code=302)
        return resp
        
    @staticmethod
    def _gen_challenge(code):
        code_challenge = hashlib.sha256(code).digest()
        code_challenge = b64.urlsafe_b64encode(code_challenge).decode().replace('=', '')
        return code_challenge