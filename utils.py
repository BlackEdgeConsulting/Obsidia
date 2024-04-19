import json
import os
# from pymongo import MongoClient
from obsidia.settings import DATABASES

def get_test_database():
    dbconfig = DATABASES["mongodb"]
    return _get_db_handle_mongodb(
        host=dbconfig["HOST"],
        port=dbconfig["PORT"],
        username=dbconfig["USER"],
        password=dbconfig["PASSWORD"]
    )

def get_dev_database():
    dbconfig = DATABASES["default"]

def get_db_handle():
    environment = os.environ.get("OBSIDIA_ENVIRONMENT")
    if environment == "dev":
        pass
    elif environment == "test":
        return get_test_database()
    else:
        raise NotImplementedError("Haven't implemented that database yet")


def _get_db_handle_mongodb(host, port, username, password):
    client = MongoClient(host=host,
                      port=int(port),
                      username=username,
                      password=password
                     )
    db_handle = client['db_name']
    return db_handle, client