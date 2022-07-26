import azure.functions as func
import pymongo
import os
import json
from bson.json_util import dumps


def main(req: func.HttpRequest) -> func.HttpResponse:
    # must enter ?id=idnumber to retrieve element with idnumber = n like 1, 5, etc...
    try:
        url = os.environ["MyDbConnection"] # Change the Variable name, as applicable to you
        client = pymongo.MongoClient(url)
        database = client['test'] # Change the MongoDB name
        collection = database['portalnotes']    # Change the collection name

        query = req.params.get('id')
        if not query:
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                query = req_body.get('id')

        if query:
            result = collection.find({'id':query})

            # for 12-byte input or a 24-character hex string id
            from bson.objectid import ObjectId
            query = {'_id': ObjectId(query)}
            result = collection.find_one(query)

            result = dumps(result)
            return func.HttpResponse(result, mimetype="application/json", charset='utf-8')
        else:
             return func.HttpResponse(
             "Please pass an id in the query string or in the request body to query a specific item.",
             status_code=200
        )


    except ConnectionError:
        print("could not connect to mongodb")
        return func.HttpResponse("could not connect to mongodb",
                                 status_code=400)
