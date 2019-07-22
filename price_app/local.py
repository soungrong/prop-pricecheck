from flask import Flask, request, render_template
from .gcloud.main import process_form


app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def price_check():
    if request.method == 'POST':
        return process_form(request)
    else:
        return render_template('index.html')
