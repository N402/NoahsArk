from flask import Blueprint, render_template, jsonify, request
from flask.ext.login import login_required, current_user

from ark.utils.qiniu import gen_upload_token, hash_save_key, encodedEntryURI


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


@master_app.route('/uptoken/avatar/crop')
@login_required
def uptoken_avatar_crop():
    hash_key = hash_save_key(current_user.id, 'avatar')
    x = request.args.get('x', 0)
    y = request.args.get('y', 0)
    w = request.args.get('w', 0)
    h = request.args.get('h', 0)
    tw = request.args.get('tw', 0)
    th = request.args.get('th', 0)
    save_as = encodedEntryURI(hash_key)
    persistentOps = ('thumbnail/%sx%s|c2rop/!%sx%sa%sa%s|saveas/%s' %
                     (tw, th, w, h, x, y, save_as))
    data = {
        'saveKey': hash_key,
        'persistentOps': persistentOps,
    }
    uptoken = gen_upload_token(data)
    return jsonify(uptoken=uptoken)
