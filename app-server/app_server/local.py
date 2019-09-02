import os

from dotenv import load_dotenv
from flask import Blueprint, request, render_template

from gc_form.main import process_form


bp = Blueprint('local', __name__, template_folder='templates')

load_dotenv()

GC_FORM_URL = os.getenv('GC_FORM_URL', '/')
GOOGLE_MAPS_KEY = os.getenv('GOOGLE_MAPS_KEY')

@bp.route("/", methods=('GET', 'POST'))
def price_check():
    if request.method == 'POST':
        return process_form(request)
    else:
        return render_template(
            'index.html',
            GOOGLE_MAPS_KEY=GOOGLE_MAPS_KEY,
            GC_FORM_URL=GC_FORM_URL)
