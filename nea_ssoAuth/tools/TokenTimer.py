from datetime import datetime as dt, timedelta as td
from multiprocessing import Process
from time import sleep

from . import TokenRefresher

class TokenTimer:
    def __init__(self, mongo_params, sso_auth):
        self.mongo_params = mongo_params
        self.sso_auth = sso_auth
        self.active = True
        self.interval_minutes = 15
        
    def run(self):
        while self.active:
            self._sleep_until_next()
            TokenRefresher(self.mongo_params, self.sso_auth).refresh_tokens()
        
    def _sleep_until_next(self):
        now, sleep_until, sleep_for = self._next_sleep()
        sleep(sleep_for)
        while now < sleep_until:
            sleep(1)
            now = dt.utcnow()
            
    def _next_sleep(self):
        now = dt.utcnow()
        sleep_until = now.replace(second=0, microsecond=0)
        sleep_until += td(minutes=self.interval_minutes - (now.minute % self.interval_minutes))
        sleep_for = (sleep_until - now).total_seconds()
        return now, sleep_until, sleep_for