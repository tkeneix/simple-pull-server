from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
import os
import re
import datetime
import logging
import traceback
import copy
from pprint import pprint

### global parameters

### global variables
app = Flask(
    __name__, static_folder="frontend/build/static", template_folder="frontend/build"
)
CORS(app)
api = Api(app)
logging.basicConfig(level=logging.ERROR)


# routing section
@app.route("/")
def index():
    return render_template("index.html")

class GitPull(Resource):
    # curl -H "accept: application/json" -H "Content-Type: application/json" -d '{"comment": "Hello, World."}' -XGET http://localhost:5000/api/v1/healthcheck

    def get(self):
        args = self.reqparse.parse_args()
        pprint(args)
        ret_json = {"status": True}
        ret_json["comment"] = args["comment"]
        return ret_json

    def post(self):
        json = request.get_json(force = True)
        pprint(json)
        # repo = git.Repo('path/to/git_repo')
        # origin = repo.remotes.origin
        # origin.pull()        
        return { 'json_request': json }

# main section
if __name__ == "__main__":
    api.add_resource(GitPull, "/api/v1/pull")
    app.run(host="0.0.0.0", port=6000, debug=True)
