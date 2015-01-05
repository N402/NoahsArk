from flask import Blueprint, render_template


account_app = Blueprint('account', __name__)


@account_app.route('/account/signin', methods=['GET', 'POST'])
def signin():
    pass


@account_app.route('/account/signup', methods=['GET', 'POST'])
def signup():
    pass
