import secrets
from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.secret_key = "supersekrit"
blueprint = make_google_blueprint(
    client_id = {{secrets.CLIENT_ID}},
    client_secret={{secrets.client_secret}},
    scope=["profile", "email"]

)

app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])

if __name__ == "__main__":
    app.run()