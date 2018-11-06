from flask import (
    Blueprint, redirect, render_template, request, session
)

bp = Blueprint('wikis', __name__, url_prefix='/wikis/', template_folder='templates')

def signin_required(view):
    def wrapped_view(**kwargs):
        if session.get("account_username") is None:
            return redirect("/")
        else:
            return view(**kwargs)

    return wrapped_view

@bp.route('')
@signin_required
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

    app.config["SECRET_KEY"] = "dev"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://librehq@localhost/librehq_wikis';
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    @app.route('/')
    def standalone_index():
        if session.get("account_username") is None:
            return render_template("standalone_index.html")
        else:
            return redirect("/wikis/")

    @app.route('/standalone_signin', methods=(["POST"]))
    def standalone_signin():
        session['account_username'] = request.form["username"]
        session['account_password'] = request.form["password"]
        return(redirect("/"))

    @app.route('/standalone_signout')
    def standalone_signout():
        session.clear()
        return(redirect("/"))

    app.register_blueprint(bp)
    if __name__ == "__main__":
        app.run(host='0.0.0.0')

from wikis import create

