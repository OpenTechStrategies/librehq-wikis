from flask import (
    Blueprint, render_template, request
)

from io import StringIO

import csv2wiki

bp = Blueprint('wikis', __name__, url_prefix='/wikis/')

@bp.route('')
def index():
    return render_template("upload.html");

@bp.route('uploadcsv', methods=(["POST"]))
def upload():
    config = csv2wiki.parse_config_string(request.files["config"].read().decode("utf-8"))
    csv_in = csv2wiki.CSVInput(StringIO(request.files["csv"].read().decode('utf-8')), config)
    output = StringIO()
    wiki_sess = csv2wiki.WikiSession(config, csv_in, False, output)
    wiki_sess.make_pages(None, "size")
    return "<pre>" + output.getvalue() + "</pre>"

# This section for standalone development/testing only
if __name__ == "wikis":
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.run(host='0.0.0.0')
