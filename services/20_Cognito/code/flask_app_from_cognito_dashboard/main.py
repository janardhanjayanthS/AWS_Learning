import os

from authlib.integrations.flask_client import OAuth
from flask import Flask, jsonify, redirect, session, url_for, abort

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a secure random key in production
oauth = OAuth(app)

oauth.register(
    name="oidc",
    authority="https://cognito-idp.us-east-1.amazonaws.com/us-east-1_6o9GaI28R",
    client_id="28v52oa4u6rlt08cl0mns3e48e",
    client_secret="<client secret>",
    server_metadata_url="https://cognito-idp.us-east-1.amazonaws.com/us-east-1_6o9GaI28R/.well-known/openid-configuration",
    client_kwargs={"scope": "phone openid email"},
)


@app.route("/")
def index():
    user = session.get("user")
    if user:
        return f'Hello, {user["email"]}. <a href="/logout">Logout</a>'
    else:
        return 'Welcome! Please <a href="/login">Login</a>.'


@app.route("/login")
def login():
    # Alternate option to redirect to /authorize
    # redirect_uri = url_for('authorize', _external=True)
    # return oauth.oidc.authorize_redirect(redirect_uri)
    return oauth.oidc.authorize_redirect("https://d84l1y8p4kdic.cloudfront.net")


@app.route("/authorize")
def authorize():
    token = oauth.oidc.authorize_access_token()
    user = token["userinfo"]
    session["user"] = user
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/secret")
def secret():
    if not session.get("user"):
        abort(401)
    return jsonify({"the secret secret ingredient of the secret soup is:": "nothing!"})


if __name__ == "__main__":
    app.run(debug=True)
