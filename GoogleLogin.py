import flask
import requests_oauthlib
import os

CLIENT_ID = "94302061300-8mt0r2qhicblghvr12s7i5e10mlgo0p0.apps.googleusercontent.com"
CLIENT_SECRET = "eKwvQT9xuIKF9fv4EM5aPBDF"
redirect_uri = "http://localhost:5000/callback"

AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"
SCOPE_URL = "https://www.googleapis.com/auth/books"

# This allows us to use a plain HTTP callback
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = flask.Flask(__name__)


@app.route("/")
def index():
    return """
    <a href="/login">Login with Google</a> 
    """


@app.route("/login")
def login():
    simplelogin = requests_oauthlib.OAuth2Session(
        CLIENT_ID, redirect_uri=redirect_uri, scope=SCOPE_URL
    )
    authorization_url, _ = simplelogin.authorization_url(AUTHORIZATION_BASE_URL)

    return flask.redirect(authorization_url)


@app.route("/callback")
def callback():
    simplelogin = requests_oauthlib.OAuth2Session(CLIENT_ID, redirect_uri=redirect_uri)
    simplelogin.fetch_token(
        TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=flask.request.url
    )
    print(simplelogin)
    return f"""
    Ok
    """

if __name__ == "__main__":
    app.run(host="localhost", debug=True)