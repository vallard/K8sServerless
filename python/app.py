from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json, sys
import datetime
import pymongo
from bson.json_util import dumps as bdumps

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


def upload_image(request):
    mongo, minio = setup()
    #fn = request.form["filename"] 
    ufile = request.files['file'] # get the FileStorage object from the form
    ufile.seek(0, 2) # go to the end of the file pointer
    file_length = ufile.tell() # get the length of the file
    ufile.seek(0, 0) # set the file pointer back to the beginniong
    
    # store the image in minio
    try:
        minio.put_object("uploads", ufile.filename, ufile ,file_length, ufile.content_type)
    except ResponseError as err:
        print(err, file=sys.stderr)
        return json.dumps({"error" : str(err)}), 500

    # store the file metadata in mongo
    collection = mongo["photos"]["entries"]

    photo = {
        "name" : ufile.filename,
        "date" : datetime.datetime.utcnow(),
        "url" : "http://10.93.140.130:9000/uploads/" + ufile.filename
    }
    # put object information into database. 
    img_id = collection.insert_one(photo).inserted_id
    return bdumps({"id": img_id }), 200


def get_images():
    mongo, minio = setup()
    collection = mongo["photos"]["entries"]
    photos = [x for x in collection.find({})]
    result = bdumps({"photos" : photos})
    return result, 200
    
@app.route('/images', methods=["GET", "POST"])
@cross_origin()
def index():
    """
    Get the todo lists
    """
    if request.method == 'GET':
        return get_images()
        return json.dumps({"status": "ok"}), 200
    if request.method == 'POST':
        # want to store in database the name of the file. 
        print(request.form['filename'], file=sys.stderr)
        return upload_image(request)
        
    else:
        print(response.body)
        return json.dumps({"status": request.method}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
