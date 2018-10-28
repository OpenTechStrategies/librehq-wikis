from flask import Blueprint

bp = Blueprint('wikis', __name__, url_prefix='/wikis/')

@bp.route('')
def index():
    return "This is the wikis stub"

# This section for standalone development/testing only
if __name__ == "wikis":
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.run(host='0.0.0.0')
