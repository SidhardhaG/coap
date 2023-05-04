import json
from os import environ as env
import os
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request
import pandas as pd
from werkzeug.utils import secure_filename
import seat

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__, template_folder='templates', static_folder='stylesheet')
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route('/upload', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
      # upload file flask
        f = request.files.get('file')
 
        # Extracting uploaded file name
        data_filename = secure_filename(f.filename)
 
        f.save(os.path.join(env.get("UPLOAD_FOLDER"),
                            data_filename))
 
        session['uploaded_data_file_path'] = os.path.join(env.get("UPLOAD_FOLDER"),data_filename)
 
        return render_template('index2.html')
    return render_template("index.html")
  
@app.route('/show_data')
def showData():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    uploaded_df = pd.read_csv(data_file_path,
                              encoding='unicode_escape')
    # changing the file
    modified_df = seat.seat_counselling(data_file_path).to_html()

    uploaded_df_html = uploaded_df.to_html()
    return render_template('show_csv_data.html',
                           data_var=modified_df)


@app.route('/api/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    data_filename = secure_filename(file.filename)
    file.save(os.path.join(env.get("UPLOAD_FOLDER"),data_filename))
    return '', 204

@app.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))