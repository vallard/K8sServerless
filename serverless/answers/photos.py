import pymongo
import json, os, time, base64
import datetime
from datetime import timedelta

from bson.json_util import dumps as bdumps
from bson.objectid import ObjectId

from kubernetes import client, config # to get kubernetes secrets to access mongo and minio

from minio import Minio
from minio.error import ResponseError


MONGODB_HOST = os.environ.get("MONGODB_HOST") or "fonkdb-mongodb"
MONGODB_PORT = os.environ.get("MONGODB_PORT") or 27017
MONGODB_COLLECTION = os.environ.get("MONGODB_COLLECTION") or "entries"
MONGODB_SECRETS = os.environ.get("MONGODB_SECRETS") or "fonkdb-mongodb"

MINIO_HOST = os.environ.get("MINIO_HOST") #or "fonkfe:9000"
MINIO_SECRETS = os.environ.get("MINIO_SECRETS") or "fonkfe"
MINIO_BUCKET = os.environ.get("MINIO_BUCKET") or "uploads"
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


def get_image(iid):
    """
    Get just one image entry from the database.
    """
    minio, mongo = setup()
    collection = mongo[mgo_database][MONGODB_COLLECTION]
    images = [i for i in collection.find({"_id": ObjectId(iid)})]
    return images[0]

def delete(event, context):
    """
    Remove photo from mongodb and from minio
    """
    print("Event data: ", event["data"])
    iid = event["data"]["id"]
    print("Image ID to delete: ", iid)
    try: 
        minio, mongo = setup()
    except Exception as err:
        return json.dumps({"setup error": str(err)})

    # remove from mongo db    
    try:
        collection = mongo[mgo_database][MONGODB_COLLECTION]
        image = get_image(iid)
        result = collection.delete_one({'_id' : ObjectId(iid)})
        print(result)
    except Exception as err:
        return json.dumps({"error": str(err)})

    # remove from minio
    try:
        minio.remove_object(MINIO_BUCKET, image["name"])
    except ResponseError as err:
        print(err)
        return json.dumps({"error" : str(err)})

    return list("", "")

    
def get_file_length(filepointer):
    filepointer.seek(0, 2) # go to the end of the file pointer
    file_length = filepointer.tell() # get the length of the file
    filepointer.seek(0, 0) # set the file pointer back to the beginning
    return file_length


def upload(event, context):
    try:
        minio, mongo = setup()
    except Exception as err:
        return json.dumps({"setup error": str(err)})
    print("Get data file")
    f = event['files']['file'] # get the FileStorage object from the form
    print("bottle file object: ", f)
    print("bottle file name: ", f.filename)
    print("bottle file type: ", f.content_type)
    print("bottle file: ", f.file) 
    file_size = get_file_length(f.file)
    print("bottle file size: ", file_size)
     
    # store the image in minio
    try:
        print("putting minio")
        minio.put_object("uploads", f.filename, f.file , file_size, f.content_type)
    except ResponseError as err:
        print(err)
        return json.dumps({"error" : str(err)}), 500

    # store the file metadata in mongo
    collection = mongo[mgo_database][MONGODB_COLLECTION]

    # upload image
    url = minio.presigned_get_object('uploads', f.filename, expires=timedelta(days=5)) 
    print(url)
    print("MINIO_HOST IS: ", MINIO_HOST)
    url = url.replace("fonkfe:9000", MINIO_HOST)
    print(url)
    photo = {
        "name" : f.filename,
        "date" : datetime.datetime.utcnow(),
        "url" : url
    }
    # put object information into database.
    img_id = collection.insert_one(photo).inserted_id
    #return bdumps({"id": img_id }), 200
    return list("", "")
