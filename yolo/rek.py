import pymongo
import json, os, time, base64
import datetime
from datetime import timedelta
import urllib2 # python2
#import urllib.request #python3

from bson.json_util import dumps as bdumps
from bson.objectid import ObjectId

from kubernetes import client, config # to get kubernetes secrets to access mongo and minio

from minio import Minio
from minio.error import ResponseError


#MONGODB_HOST = os.environ.get("MONGODB_HOST") or "10.10.20.210"
MONGODB_HOST = os.environ.get("MONGODB_HOST") or "fonkdb-mongodb"
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION") or "entries"
MONGODB_SECRETS = os.environ.get("MONGODB_SECRETS") or "fonkdb-mongodb"
MONGODB_DB = "photos"

MINIO_HOST = os.environ.get("MINIO_HOST") or "fonkfe:9000" 
MINIO_SECRETS = os.environ.get("MINIO_SECRETS") or "fonkfe"
MINIO_BUCKET = os.environ.get("MINIO_BUCKET") or "uploads"


def setup():
    """
    get the mongo credentials then connect to them
    """
    # get kubernetes info
    config.load_incluster_config()
    v1=client.CoreV1Api()
    mgo_user = "root"
    mgo_password = ""
    access_key = ""
    secret_key = ""
    # connect to Kubernetes to get secrets
    # get the secrets to connect to the services.  Make sure your service account can do this or
    # this will fail. 
    for secrets in v1.list_secret_for_all_namespaces().items:
        if secrets.metadata.name == MINIO_SECRETS:
            access_key = base64.b64decode(secrets.data['accesskey'])
            secret_key = base64.b64decode(secrets.data['secretkey'])
        if secrets.metadata.name == MONGODB_SECRETS:
            mgo_password = base64.b64decode(secrets.data['mongodb-root-password'])

    mongo = pymongo.MongoClient("mongodb://{0}:{1}@{2}".format(mgo_user,
                                                              mgo_password, 
                                                               MONGODB_HOST))
    # try to connect to minio
    minio = Minio(MINIO_HOST,
                access_key=access_key,
                secret_key=secret_key,
                secure=False)
    return minio, mongo
        
def process_event(event, context):
    """
    Get the image and run through the image recognition application then 
    update
    """
    print("Data received: ", event['data'])
    wfile = event['data']['Key']
    bucket = os.path.dirname(wfile) 
    filename = os.path.basename(wfile) 
    print("uploaded object: ", filename)
    # wait a few minutes for it to actually complete
    time.sleep(10)
    # log into minio and mongo
    minio, mongo = setup()
    # get presigned link so that detection can access the file.
    # https://docs.minio.io/docs/python-client-api-reference.html#presigned_get_object
    wfile = minio.presigned_get_object(bucket, filename, expires=timedelta(minutes=2))
    print("shareable link to file: ", wfile)
    # get contents of file
    data = recognize(wfile)
    # write contents to database
    update_db(mongo, filename, data)
    

def update_db(mongo, filename, data):
    """
    Connect to the database, find the matching image and update the 
    data to show there are objects in it. 
    """
    # connect to the mongoDB to find the image
    collection = mongo[MONGODB_DB][MONGODB_COLLECTION]
    images = [i for i in collection.find({"name": filename})]
    ident = images[0]["_id"]
    print(ident)
    resp = collection.update({"_id": ident}, {'$set': {"objects" : data}})
    print(resp)
    

def recognize(file_url):
    """
    Connect to the detector service get the objects that are detected in it
    """
    #file_url = "http://{0}/{1}".format(MINIO_HOST, filename)
    #print("file url: ", file_url)
    
    jsonD = json.dumps({"url": file_url})
    detectorAPI = "http://yolo:5005/detect"
    #detectorAPI = "http://10.10.20.209:5005/detect"
    # file headers
    header = {
        "Content-Type": "application/json"
    }
    # construct request
    request = urllib2.Request(detectorAPI, jsonD, header)
    request.get_method = lambda: 'GET'

    # open the request
    response = urllib2.urlopen(request)
    print("Return code: ", response.getcode())
    print("info: ", response.info())
    if response.getcode() != 200:
        print("Error with object detection!")
    # get the data from the json response 
    data = json.load(response)
    print("recevied response of data: ",  data)
    return data
    
