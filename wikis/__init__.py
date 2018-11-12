from flask import (
    g, redirect, render_template, request, session
)

import os

db = None

def signin_required(view):
    def wrapped_view(**kwargs):
        if session.get("account_username") is None:
            return redirect("/")
        else:
            return view(**kwargs)
    wrapped_view.__name__ = view.__name__

    return wrapped_view

def main_partial():
    return "wikis/main_partial.html"

def initialize_module(app, app_db):
    global db
    db = app_db

    from wikis import wiki
    app.register_blueprint(wiki.bp)

# This section for standalone development/testing only
# We switch on the environment variable of the FLASK_APP because
# that's the most reliable piece of information (that I could find),
# but this has the downside that you have to boot the standarlone
# with the command:
#
#    $ FLASK_APP=wikis flask run
#
# or as a standalone script
if __name__ == "__main__" or os.environ["FLASK_APP"] == "wikis":
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate

    app = Flask(__name__)

    try:
        app.config.from_object('config')
    except:
        raise RuntimeError("No config.py found")

    app.config["SECRET_KEY"] = "dev"
    app_db = SQLAlchemy(app)
    migrate = Migrate(app, app_db)

    @app.before_request
    def set_standalone():
        g.standalone = True

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

    if __name__ == "__main__":
        app.run(host='0.0.0.0')

    initialize_module(app, app_db)
