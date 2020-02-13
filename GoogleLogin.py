import flask
import requests_oauthlib
import os
import requests


CLIENT_ID = "clientid"
CLIENT_SECRET = "secretkey"
redirect_uri = "http://localhost:5000/callback"

AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"
SCOPE_URL = ["openid", "email", "profile"]


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
    ID_Token = simplelogin.token.get('id_token')
    URL = "https://oauth2.googleapis.com/tokeninfo?id_token=" + str(ID_Token)
    req = requests.get(url=URL)
    print(req.content)
    return """
    Ok
    """

if __name__ == "__main__":
    app.run(host="localhost", debug=True)