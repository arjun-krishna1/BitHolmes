from flask import *
import data
import os

app = Flask(__name__)


@app.route('/', methods = ["GET", "POST"])
def index():
    pressed = lambda x : x in request.form
    fraud_level = 0
    if pressed('public-key-submit'): #if submit button is pressed
        public_key = request.form['public-key-input']

    #function that outputs -1 0 1 2 or 3

    fraud_value = data.fraud_level_to_value.get(fraud_level, -1)

    return render_template("base.html", output_value = fraud_value)





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