from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import json
import os
import webbrowser

# setting env variables
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

# getting the user info from the config files

with open("config.json") as f:
    config_data = json.load(f)

app = Flask(__name__)
# random thing
app.secret_key = "supersekrit"

# setting client id and client secret

client_id = config_data["client_id"]
client_secret = config_data["client_secret"]

print(client_id)
print(client_secret)
# another random thing
scope=["profile", "email"]

blueprint = make_google_blueprint(client_id, client_secret)

app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/login/google/authorized")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])

if __name__ == "__main__":
    app.run()