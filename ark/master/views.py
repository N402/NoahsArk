from flask import Blueprint, render_template, jsonify
from flask.ext.login import login_required

from ark.utils.qiniu import gen_upload_token


master_app = Blueprint('master', __name__)


@master_app.route('/')
def index():
    return render_template('index.html')


@master_app.route('/uptoken')
@login_required
def uptoken():
    uptoken = gen_upload_token()
    return jsonify(uptoken=uptoken)
