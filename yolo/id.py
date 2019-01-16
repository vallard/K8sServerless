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


MONGODB_HOST = os.environ.get("MONGODB_HOST") or "10.10.20.210"
MONGODB_PORT = os.environ.get("MONGODB_PORT") or "27017"
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION") or "entries"
MONGODB_SECRETS = os.environ.get("MONGODB_SECRETS") or "fonkdb-mongodb"
MINIO_HOST = "http://minio.10.10.20.207.xip.io"
mgo_database = "photos"

def setup():
    # get kubernetes info
    config.load_incluster_config()
    v1=client.CoreV1Api()
    mgo_user = "root"
    mgo_password = ""
    # connect to Kubernetes to get secrets
    # get the secrets to connect to the services.  Make sure your service account can do this or
    # this will fail. 
    for secrets in v1.list_secret_for_all_namespaces().items:
        if secrets.metadata.name == MONGODB_SECRETS:
            mgo_password = base64.b64decode(secrets.data['mongodb-root-password'])

    mongo = pymongo.MongoClient("mongodb://{0}:{1}@{2}".format(mgo_user,
                                                              mgo_password, 
                                                               MONGODB_HOST))
    return mongo
        
def qsetup():
    mongo = pymongo.MongoClient("mongodb://{0}:{1}@{2}".format("root",
                                                              "oBfLXGFSZe",
                                                              "10.10.20.210:27017"))
    return mongo
    

def process_event(event, context):
    """
    Get the image and run through the image recognition application then 
    update
    """
    wfile = event['data']['Key']
    bucket = os.path.dirname(event['data']['Key'])
    filename = os.path.basename(event['data']['Key'])
    # get contents of file
    data = recognize(wfile)
    # write contents to database
    update_db(filename, data)
    



def update_db(filename, data):
    # connect to the mongoDB to find the image
    mongo = qsetup()
    collection = mongo[mgo_database][MONGODB_COLLECTION]
    images = [i for i in collection.find({"name": filename})]
    ident = images[0]["_id"]
    print(ident)
    resp = collection.update({"_id": ident}, {'$set': {"objects" : data}})
    print(resp)
    

def recognize(filename):
    file_url = "{0}/{1}".format(MINIO_HOST, filename)
    print("file url: ", file_url)
    jsonD = json.dumps({"url": file_url})
    detectorAPI = "http://10.10.20.209:5005/detect"
    # file headers
    header = {
        "Content-Type": "application/json"
    }
    # construct request
    request = urllib2.Request(detectorAPI, jsonD, header)
    request.get_method = lambda: 'GET'

    # open the request
    response = urllib2.urlopen(request)
    
    
    data = json.load(response)
    print(data)
    return data
    


img = "uploads/people.jpg"
event = { 
    "data" : {
        'Key' : img
    }
}
 	
process_event(event, "")
