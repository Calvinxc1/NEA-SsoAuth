from multiprocessing import Process

from config.config import mongo_params, sso_auth
from nea_ssoAuth import app
from nea_ssoAuth.tools import TokenTimer

if __name__ == '__main__':
    refresh_process = Process(target=TokenTimer.run_from_process, args=(mongo_params, sso_auth))
    refresh_process.start()
    
    app.run(host='0.0.0.0', port=80, debug=True)