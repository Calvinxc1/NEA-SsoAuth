from multiprocessing.dummy import Pool
import pymongo as pm
import requests as rq

from . import TokenProcessor

class TokenRefresher:
    url = 'https://login.eveonline.com/v2/oauth/token'
    data_base = {
        'grant_type': 'refresh_token',
    }
    headers_base = {
        'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'login.eveonline.com'
    }
    database = 'EveSsoAuth'
    collection = 'ActiveAuths'
    pool_workers = 12
    
    def __init__(self, mongo_params, sso_auth, verbose=False):
        self.conn = pm.MongoClient(**mongo_params)
        self.data = {
            **self.data_base,
            'client_id': sso_auth['client_id'],
        }
        self.headers = {
            **self.headers_base,
        }
        self.verbose = verbose
        
    def refresh_tokens(self):
        tokens = [token for token in self.conn[self.database][self.collection].find()]
        with Pool(self.pool_workers) as P:
            output = P.imap_unordered(self._refresh_func, tokens)
            if self.verbose: output = tqdm(output, total=len(tokens), leave=False)
            output = list(output)
            
    def _refresh_func(self, token):
        data = {
            **self.data,
            'refresh_token': token['refresh_token'],
        }
        headers = {
            **self.headers,
        }

        resp = rq.post(self.url, data=data, headers=headers)
        token_rcd = TokenProcessor.process_token(resp.json())

        if token_rcd['_id'] != token['_id']:
            raise Exception('ID mismatch')

        self.conn[self.database][self.collection].update_one(
            {'_id': token_rcd['_id']},
            {'$set': token_rcd},
            upsert=True,
        )