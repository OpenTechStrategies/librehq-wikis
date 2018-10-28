from flask import Blueprint

bp = Blueprint('wikis', __name__, url_prefix='/wikis/')

@bp.route('')
def index():
    return "This is the wikis stub"
