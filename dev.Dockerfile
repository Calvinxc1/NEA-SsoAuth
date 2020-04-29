FROM python:3-slim

RUN apt-get update \
    && apt-get install -y git \
    && python -m pip install --upgrade pip

WORKDIR /srv/app

COPY ./ ./NEA-SsoAuth/
RUN python -m pip install --no-cache-dir ./NEA-SsoAuth \
    && rm -rf ./NEA-SsoAuth

VOLUME /srv/app/config.py
VOLUME /srv/app/gunicorn.py

EXPOSE 8000/tcp

CMD ["gunicorn", "-c", "./config/gunicorn.py", "nea_ssoAuth:app"]