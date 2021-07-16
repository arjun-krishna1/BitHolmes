from flask import *
import data
import os
from rq import check_addr

app = Flask(__name__)


@app.route('/', methods = ["GET", "POST"])
def index():
    pressed = lambda x : x in request.form
    fraud_level = 0
    if pressed('public-key-submit'): #if submit button is pressed
        public_key = request.form['public-key-input']
        fraud_level = check_addr(public_key)

    fraud_value = data.fraud_level_to_value.get(fraud_level, 0)



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
