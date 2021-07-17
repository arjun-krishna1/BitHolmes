from flask import *
import data, os
import qrcodefunctions as qrfunc
from rq import check_addr

app = Flask(__name__)

fraud_level = 0

@app.route("/<address>", methods = ["GET"])
@app.route('/', methods = ["GET", "POST"])
def index(address = None):
    global fraud_level
    pressed = lambda x : x in request.form
    if address: #if address passed into the url
        fraud_level = check_addr(address)
    elif pressed('public-key-submit') and request.form['public-key-input']: #if submit button is pressed
        public_key = request.form['public-key-input']

        fraud_level = check_addr(public_key)
        return render_template("results.html", fraud_level = fraud_level)

    fraud_value = data.fraud_level_to_value.get(fraud_level, 0)

    return render_template("base.html")


@app.route("/qr/<address>", methods = ["GET"])
@app.route('/qr/', methods = ["GET"])
def qr(address = None):
    if address is None:
        return redirect("/")
    qrfunc.delete_old_files()
    qr_hash = qrfunc.make_website_link_qr(address)
    location = url_for('static', filename = qr_hash)
    return render_template("qr.html", location = location)





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
