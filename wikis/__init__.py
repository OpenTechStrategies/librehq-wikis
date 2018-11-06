from flask import (
    Blueprint, render_template
)

bp = Blueprint('wikis', __name__, url_prefix='/wikis/', template_folder='templates')

@bp.route('')
def index():
    return render_template("upload.html");

def main_partial():
    return "main_partial.html"

# This section for standalone development/testing only
if __name__ == "__main__" or __name__ == "wikis":
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://librehq@localhost/librehq_wikis';
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    @app.route('/')
    def standalone_index():
        return render_template("standalone_index.html")

    app.register_blueprint(bp)
    if __name__ == "__main__":
        app.run(host='0.0.0.0')

from wikis import create

