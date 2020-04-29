from config.config import mongo_params, sso_auth
from nea_ssoAuth.tools import TokenTimer

if __name__ == '__main__':
    TokenTimer(mongo_params, sso_auth).run()