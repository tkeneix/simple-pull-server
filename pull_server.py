from flask import Flask, render_template, request
from flask_restful import Resource, Api
from flask_cors import CORS
import yaml
import json
import requests
import os
import re
import datetime
import logging
import traceback
import copy
from pprint import pprint
import git

### global parameters
# ENV = None

### global variables
app = Flask(
    __name__, static_folder="frontend/build/static", template_folder="frontend/build"
)
CORS(app)
api = Api(app)
logging.basicConfig(level=logging.ERROR)


def notify_discord(message):
    env_discord = ENV.get('DISCORD')
    discord_webhook = env_discord.get("NOTIFY_WEBHOOK")
    
    if discord_webhook is not None:
        user_name = env_discord.get("NOTIFY_USERNAME")
        discord_headers = {'content-type': 'application/json'}

        payload_json = {
            "username": user_name,
            "content": "@everyone\n"
        }

        payload_json["content"] += message

        requests.post(
            discord_webhook,
            data=json.dumps(payload_json),
            headers=discord_headers)
    else:
        print(message)

# routing section
@app.route("/")
def index():
    return render_template("index.html")

class GitPull(Resource):

    def post(self):
        json = request.get_json(force = True)
        repo_name = json['repository']['name']
        repo_url = json['repository']['html_url']
        message = f"Push {repo_name}\n<{repo_url}>"

        env_repo = ENV.get('REPOSITORIES')
        repo_path = env_repo.get("PATH")
        repo = git.Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()        

        notify_discord(message)
        return

# main section
if __name__ == "__main__":

    base_dir = os.getcwd()
    envfile_path = os.path.join(base_dir, 'conf/pull_server.yaml')
    with open(envfile_path) as file:
        global ENV
        ENV = yaml.safe_load(file)

    api.add_resource(GitPull, "/api/v1/pull")
    app.run(host="0.0.0.0", port=6000, debug=True)
