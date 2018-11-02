from flask import (
    Blueprint, render_template
)

bp = Blueprint('wikis', __name__, url_prefix='/wikis/', template_folder='templates')

from wikis import create

@bp.route('')
def index():
    return render_template("upload.html");

def main_partial():
    return "main_partial.html"

# This section for standalone development/testing only
if __name__ == "__main__" or __name__ == "wikis":
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(bp)
    if __name__ == "__main__":
        app.run(host='0.0.0.0')
