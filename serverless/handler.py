import pymongo
import json, os, time, base64

from bson.json_util import dumps as bdumps
from bson.objectid import ObjectId

from kubernetes import client, config # to get kubernetes secrets to access mongo and minio

from minio import Minio
from minio.error import ResponseError


MONGODB_HOST = os.environ.get("MONGODB_HOST") or "fonkdb-mongodb"
MONGODB_PORT = os.environ.get("MONGODB_PORT") or 27017
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION") or "entries"
MONGODB_SECRETS = os.environ.get("MONGODB_SECRETS") or "fonkdb-mongodb"

MINIO_HOST = os.environ.get("MINIO_HOST") or "fonkfe:9000"
MINIO_SECRETS = os.environ.get("MINIO_SECRETS") or "fonkfe"
mgo_database = "photos"

def setup():
    # get kubernetes info
    config.load_incluster_config()
    v1=client.CoreV1Api()
    access_key = ""
    secret_key = ""
    mgo_user = "root"
    mgo_password = ""
    # connect to KUbernetes to get secrets
    # get the secrets to connect to the services.  Make sure your service account can do this or
    # this will fail. 
    for secrets in v1.list_secret_for_all_namespaces().items:
        if secrets.metadata.name == MINIO_SECRETS:
            access_key = base64.b64decode(secrets.data['accesskey'])
            secret_key = base64.b64decode(secrets.data['secretkey'])
        if secrets.metadata.name == MONGODB_SECRETS:
            #mgo_password = base64.b64decode(secrets.data['mongodb-password'])
            mgo_password = base64.b64decode(secrets.data['mongodb-root-password'])


    print(access_key, secret_key)
    print(mgo_password)
    # try to connect to minio
    minio = Minio(MINIO_HOST,
                access_key=access_key,
                secret_key=secret_key,
                secure=False)

    print(mgo_user, mgo_password, MONGODB_HOST)
    mongo = pymongo.MongoClient("mongodb://{0}:{1}@{2}".format(mgo_user,
                                                              mgo_password, 
                                                               MONGODB_HOST))
    return minio, mongo
        
def list(event, context):
    """
    List the photos with their meta data
    """
    try:
        minio, mongo = setup()
    except Exception as err:
        return json.dumps({"setup error": str(err)})
        
    try:
        collection = mongo[mgo_database][MONGODB_COLLECTION]
        photos = [x for x in collection.find({})]
        result = bdumps({"photos": photos})
        return result
    except Exception as err:
        return json.dumps({"error": str(err)})
