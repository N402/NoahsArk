from flask import Blueprint, render_template


master_app = Blueprint('master', __name__)


@master_app.route('/')
def index():
    return render_template('index.html')
