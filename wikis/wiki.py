from io import StringIO
from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)

import csv2wiki, subprocess

from wikis import db, signin_required

bp = Blueprint('wikis', __name__, url_prefix='/wikis/', template_folder='templates')

def create_wiki():
    new_wiki = Wiki(username=session.get("account_username"),
                    wikiname=request.form["name"])
    db.session.add(new_wiki)
    db.session.commit()

    wiki_db_name = "librehq_wikis_" + str(new_wiki.id)

    # Let this error if the script isn't here, since we're in prototype mode
    # TODO: Replace by ansible call
    session.get("account_username")
    subprocess.call([
        'addWiki.sh',
        request.form["name"],
        wiki_db_name,
        session.get("account_username"),
        session.get("account_password")
    ])

@bp.route('')
@signin_required
def dashboard():
    wikis = Wiki.query.filter_by(username=session.get("account_username")).all()
    return render_template("wikis/dashboard.html", wikis=wikis)

@bp.route('createwiki', methods=(["POST"]))
@signin_required
def create_plain():
    create_wiki()

    return ("<a href='http://" +
        request.form["name"] +
        ".otswiki.net'>New wiki: " +
        request.form["name"] + "</a>")

@bp.route('deletewiki', methods=(["POST"]))
@signin_required
def delete_wiki():
    wiki = Wiki.query.get(request.form["wiki_id"])
    wiki_db_name = "librehq_wikis_" + str(wiki.id)

    db.session.delete(wiki)
    db.session.commit()

    # TODO: Replace by ansible call
    subprocess.call(['deleteWiki.sh', wiki.wikiname, wiki_db_name])

    return redirect(url_for(".dashboard"))

@bp.route('renamewiki', methods=(["POST"]))
@signin_required
def rename_wiki():
    wiki = Wiki.query.get(request.form["wiki_id"])
    old_wiki_name = wiki.wikiname
    new_wiki_name = request.form["new_wiki_name"]

    wiki.wikiname = new_wiki_name
    db.session.add(wiki)
    db.session.commit()

    # TODO: Replace by ansible call
    subprocess.call(['renameWiki.sh', old_wiki_name, new_wiki_name])

    return redirect(url_for(".dashboard"))

@bp.route('uploadcsv', methods=(["POST"]))
@signin_required
def create_with_csv():
    if "name" in request.form:
        wikiname = request.form["name"]
        create_wiki()
    else:
        wiki = Wiki.query.get(request.form["wiki_id"])
        wikiname = wiki.wikiname

    config = csv2wiki.parse_config_string(request.files["config"].read().decode("utf-8"))

    # Override config options with our known parameters
    config["wiki_url"] = "http://" + wikiname + ".otswiki.net/"
    # These are set in the addWiki.sh script, and should come from user federation later
    config["username"] = session.get("account_username")
    config["password"] = session.get("account_password")

    csv_in = csv2wiki.CSVInput(StringIO(request.files["csv"].read().decode('utf-8')), config)
    output = StringIO()
    wiki_sess = csv2wiki.WikiSession(config, csv_in, False, output)
    wiki_sess.make_pages(None, "size")
    return ("<pre>" + output.getvalue() + "</pre>" +
            "<a href='http://" +
            wikiname +
            ".otswiki.net'>New wiki: " +
            wikiname + "</a>")

class Wiki(db.Model):
    __bind_key__ = "wikis"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    wikiname = db.Column(db.String(128))
