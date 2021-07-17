from flask import *
import data, os
import qrcodefunctions as qrfunc
from rq import check_addr
from crytpoaddrverification import verify_bitcoin
from datetime import timedelta

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

fraud_level = 0
app.secret_key = "7291"
app.permanent_session_lifetime = timedelta(minutes=10)


@app.route("/<address>", methods = ["GET"])
@app.route('/', methods = ["GET", "POST"])
def index(address = None):
    global fraud_level
    error_one = error_two = 0
    pressed = lambda x: x in request.form
    if address: #if address passed into the url
        if verify_bitcoin(address):
            fraud_level = check_addr(address)
        else:
            error_one = "That bitcoin public key was not found"
    elif pressed('public-key-submit-qr') and request.form['public-key-input-qr']:
        public_key_qr = request.form['public-key-input-qr']
        if verify_bitcoin(public_key_qr):
            return redirect("/qr/" + public_key_qr)
        else:
            error_two = "That bitcoin public key was not found"
    elif pressed('public-key-submit') and request.form['public-key-input']: #if submit button is pressed
        public_key = request.form['public-key-input']
        if verify_bitcoin(public_key):
            fraud_level = check_addr(public_key)
            return render_template("results.html", fraud_level = fraud_level)
        else:
            error_one = "That bitcoin public key was not found"

    return render_template("base.html", errors = [error_one, error_two])


@app.route("/qr/<address>", methods = ["GET"])
@app.route('/qr/', methods = ["GET"])
def qr(address = None):
    error_two = 0
    if address is None:
        return redirect("/")
    if verify_bitcoin(address):
        qrfunc.delete_old_files()
        qr_hash = qrfunc.make_website_link_qr(address)
        location = url_for('static', filename = qr_hash)
    else:
        error_two = "That public key was not found"
        return render_template("base.html", errors=[0, error_two])

    return render_template("qr.html", location = location)


@app.route("/reports/<address>", methods = ["GET"])
@app.route('/reports/', methods = ["GET", "POST"])
def reports(address = None):
    error_one = 0
    if 'report-btn-submit' in request.form and request.form['report-key-input']:
        reported_public_key = request.form['report-key-input']
        if verify_bitcoin(reported_public_key):
            #DATABASE ADDITION LOCATION
            return redirect("/")
        else:
            error_one = "That public key was not found"
    return render_template("reports.html", errors = [error_one])





@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get('filename', None)
        if filename:
            path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == "__main__":
    # app.run(host='localhost', debug=False, port=8000, threaded=True)
    app.run(debug=True)
