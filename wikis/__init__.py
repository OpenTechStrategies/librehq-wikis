from flask import (
    Blueprint, render_template, request
)

bp = Blueprint('wikis', __name__, url_prefix='/wikis/')

@bp.route('')
def index():
    return render_template("upload.html");

@bp.route('uploadcsv', methods=(["POST"]))
def upload():
    print(request.files["csv"])
    print(request.files["config"])
    return "Uploaded"

# This section for standalone development/testing only
if __name__ == "wikis":
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.run(host='0.0.0.0')
