import logging
import sys
import hashlib
from datetime import datetime
import requests
import os
import platform
from zenify.settings import Settings


def initiate_logger(name,
                    enable_debug=False):
    # logging.basicConfig()
    if enable_debug:
        logging.root.setLevel(logging.NOTSET)
        level = logging.NOTSET
    else:
        logging.root.setLevel(logging.INFO)
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        stream=sys.stdout)

    name = name + " " * (6 - len(name))

    return logging.getLogger(name)

logger = initiate_logger("utils")

def get_timestamp(format: str = "%Y%m%d_%H%M%S"):
    dt = datetime.now()
    timestamp = dt.strftime(format)

    return timestamp


def hash_url(url: str):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def get_auth(s, retries=5):
    PROXY_PAYLOAD = s.PROXY_PAYLOAD
    PROXY_HEADERS = s.PROXY_HEADERS
    PROXY_LOGIN_URL = s.PROXY_LOGIN_URL

    response = requests.request("POST",
                                PROXY_LOGIN_URL,
                                data=PROXY_PAYLOAD,
                                headers=PROXY_HEADERS,
                                timeout=30)
    while retries > 0:
        if response.status_code != 200:
            retries -= 1
        else:
            token = response.json()
            access_token = token["access_token"]
            access_type = str(token["token_type"]).title()
            auth_string = " ".join([access_type, access_token])
            auth_header = {"Authorization": auth_string}
            return auth_header

def get_proxy(auth_header, s: Settings) -> dict:
    PROXY_PROXY_URL = s.PROXY_PROXY_URL
    try:
        headers = auth_header
        payload = {}

        resp = requests.request(method="GET",
                                url=PROXY_PROXY_URL,
                                headers=headers,
                                data=payload)

        if resp.status_code != 200:
            logger.info(f"Response code {resp.status_code}")
            return None
        http = "http://" + resp.json()["ip_address"] + ":" + resp.json()["port"]
        https = "http://" + resp.json()["ip_address"] + ":" + resp.json()["port"]
        proxy_dict = {"http": http, "https": https}
        return proxy_dict

    except Exception as e:
        # print(e)
        raise e


