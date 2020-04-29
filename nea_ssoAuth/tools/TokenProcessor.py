from datetime import datetime as dt
from jose import jwt
import requests as rq

class TokenProcessor:
    url = 'https://login.eveonline.com/oauth/jwks'
    issuers = ['login.eveonline.com', 'https://login.eveonline.com']
    active_alg = 'RS256'
    
    def __init__(self):
        self._load_jwk()
        
    def _load_jwk(self):
        resp = rq.get(self.url)
        self.jwk_sets = {
            alg['alg']:alg 
            for alg in resp.json()['keys']
        }
        
    @classmethod
    def process_token(cls, token):
        token_class = cls()
        jwt_data = token_class._decode_token(token)
        token_rcd = token_class._map_record(token, jwt_data)
        return token_rcd
        
    def _decode_token(self, token):
        jwt_data = None
        for issuer in self.issuers:
            try:
                jwt_data = jwt.decode(
                    token['access_token'],
                    self.jwk_sets[self.active_alg],
                    algorithms=self.active_alg,
                    issuer=issuer
                )
                break
            except Exception as e:
                continue
                
        if issuer != jwt_data['iss']:
            raise Exception('Mismatch in issuer!')
        
        return jwt_data
    
    @staticmethod
    def _map_record(token, jwt_data):
        token_rcd = {
            'access_token': token['access_token'],
            'token_type': token['token_type'],
            'refresh_token': token['refresh_token'],
            'scopes': jwt_data['scp'],
            'character_name': jwt_data['name'],
            '_id': int(jwt_data['sub'].split(':')[2]),
            'expires_at': dt.utcfromtimestamp(jwt_data['exp']),
        }
        return token_rcd