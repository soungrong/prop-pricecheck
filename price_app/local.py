import os

from flask import Blueprint, request, render_template

from .gcloud.main import process_form


bp = Blueprint('local', __name__, template_folder='templates')


@bp.route("/", methods=('GET', 'POST'))
def price_check():
    if request.method == 'POST':
        return process_form(request)
    else:
        return render_template('index.html')
