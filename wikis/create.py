from io import StringIO
from flask import (
    redirect, request, session
)

import csv2wiki, subprocess

from wikis import bp, db, signin_required

def create_wiki():
    new_wiki = Wiki(username=session.get("account_username"),
                    wikiname=request.form["name"])
    db.session.add(new_wiki)
    db.session.commit()

    wiki_db_name = "librehq_wikis_" + str(new_wiki.id)

    # Let this error if the script isn't here, since we're in prototype mode
    # TODO: Replace by ansible call
    subprocess.call(['addWiki.sh', request.form["name"], wiki_db_name])

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

    return redirect("/wikis/")

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

    return redirect("/wikis/")

@bp.route('uploadcsv', methods=(["POST"]))
@signin_required
def create_with_csv():
    create_wiki()

    config = csv2wiki.parse_config_string(request.files["config"].read().decode("utf-8"))

    # Override config options with our known parameters
    config["wiki_url"] = "http://" + request.form["name"] + ".otswiki.net/"
    # These are set in the addWiki.sh script, and should come from user federation later
    config["username"] = "test"
    config["password"] = "mdpwiki8chars"

    csv_in = csv2wiki.CSVInput(StringIO(request.files["csv"].read().decode('utf-8')), config)
    output = StringIO()
    wiki_sess = csv2wiki.WikiSession(config, csv_in, False, output)
    wiki_sess.make_pages(None, "size")
    return ("<pre>" + output.getvalue() + "</pre>" +
            "<a href='http://" +
            request.form["name"] +
            ".otswiki.net'>New wiki: " +
            request.form["name"] + "</a>")

class Wiki(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    wikiname = db.Column(db.String(128))
