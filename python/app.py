from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json, sys
import datetime
from datetime import timedelta
import pymongo
from bson.json_util import dumps as bdumps
from bson.objectid import ObjectId # for deleting records

from minio import Minio
from minio.error import ResponseError

import io

app = Flask(__name__)
CORS(app)


def setup():
    mongo = setup_mongo()
    minio = setup_minio()
    return mongo, minio

def setup_minio():
    minio = Minio("10.93.140.130:9000",
                access_key="AKIAIOSFODNN7EXAMPLE",
                secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                secure=False)
    return minio

def setup_mongo():
    
    mongo = pymongo.MongoClient("mongodb://{0}:{1}@{2}".format("root",
                                                              "MVhPiLqIvh",
                                                              "10.93.140.132" ))
    return mongo

def get_file_length(filepointer):
    filepointer.seek(0, 2) # go to the end of the file pointer
    file_length = filepointer.tell() # get the length of the file
    filepointer.seek(0, 0) # set the file pointer back to the beginning
    return file_length
    

def upload_image(request):
    mongo, minio = setup()
    #fn = request.form["filename"] 
    f = request.files['file'] # get the FileStorage object from the form
    file_length = get_file_length(f)
    # store the image in minio
    try:
        minio.put_object("uploads", f.filename, f ,file_length, f.content_type)
    except ResponseError as err:
        print(err, file=sys.stderr)
        return json.dumps({"error" : str(err)}), 500

    # store the file metadata in mongo
    collection = mongo["photos"]["entries"]

    photo = {
        "name" : f.filename,
        "date" : datetime.datetime.utcnow(),
        "url" : minio.presigned_get_object('uploads', f.filename, expires=timedelta(days=5))
    }
    
    # put object information into database. 
    img_id = collection.insert_one(photo).inserted_id
    #return bdumps({"id": img_id }), 200
    return get_images()


def get_images():
    mongo, minio = setup()
    collection = mongo["photos"]["entries"]
    photos = [x for x in collection.find({})]
    result = bdumps({"photos" : photos})
    return result, 200

def get_image(iid):
    mongo, minio = setup()
    collection = mongo["photos"]["entries"]
    images = [i for i in collection.find({"_id": ObjectId(iid)})]
    return images[0]
     

def del_image(iid):
    """
    Remove photo from mongodb and from minio
    """
    mongo, minio = setup()
    print("deleting id: ", iid)
    # remove from database
    collection = mongo["photos"]["entries"]
    image = get_image(iid)
    result = collection.delete_one({'_id' : ObjectId(iid)})
    print(result,file=sys.stderr)
    # now remove from object storage
    try:
        minio.remove_object("uploads", image["name"])
    except ResponseError as err:
        print(err, file=sys.stderr)
        return json.dumps({"error" : str(err)}), 500
    
    return get_images()
    
@app.route('/images', methods=["GET", "POST", "DELETE"])
@cross_origin()
def index():
    """
    Get the todo lists
    """
    if request.method == 'GET':
        return get_images()
    if request.method == 'POST':
        # want to store in database the name of the file. 
        print(request.form['filename'], file=sys.stderr)
        return upload_image(request)
    if request.method == 'DELETE':
        print(request.json, file=sys.stderr)
        return del_image(request.json['id']) 
    else:
        print(response.body)
        return json.dumps({"status": request.method}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
