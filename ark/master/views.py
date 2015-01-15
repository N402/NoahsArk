from flask import Blueprint, render_template, jsonify
from flask.ext.login import login_required, current_user

from ark.utils.qiniu import gen_upload_token, hash_save_key


master_app = Blueprint('master', __name__)


@master_app.route('/')
def index():
    return render_template('index.html')


@master_app.route('/uptoken')
@login_required
def uptoken():
    data = {
        'saveKey': hash_save_key(current_user.id),
    }
    uptoken = gen_upload_token(data)
    return jsonify(uptoken=uptoken)


@master_app.route('/uptoken/avatar')
@login_required
def uptoken_avatar():
    data = {
        'saveKey': hash_save_key(current_user.id, 'avatar'),
    }
    uptoken = gen_upload_token(data)
    return jsonify(uptoken=uptoken)
