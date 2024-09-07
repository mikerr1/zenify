import logging
import sys
import hashlib
from datetime import datetime


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


def get_timestamp(format: str = "%Y%m%d_%H%M%S"):
    dt = datetime.now()
    timestamp = dt.strftime(format)

    return timestamp


def hash_url(url: str):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()
