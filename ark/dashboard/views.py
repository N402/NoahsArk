from flask import Flask, Blueprint, render_template, request, jsonify

from ark.exts import db
from ark.exts.login import su_required
from ark.account.models import Account
from ark.dashboard.forms import EditAccountForm


dashboard_app = Blueprint('dashboard', __name__)


@dashboard_app.route('/dashboard/')
@su_required
def index():
    return render_template('dashboard/index.html')


@dashboard_app.route('/dashboard/accounts')
@su_required
def accounts():
    accounts = Account.query.all()
    return render_template('dashboard/accounts.html', accounts=accounts)


@dashboard_app.route('/dashboard/accounts/<uid>',
                     methods=['GET', 'PATCH', 'DELETE'])
def account(uid):
    account = Account.query.get_or_404(uid)
    form = EditAccountForm(obj=account)
    if request.method == 'PATCH':
        if form.validate_on_submit():
            if form.data.get('username'):
                account.username = form.data.get('username')
            if form.data.get('gender'):
                account.change_gender(gender)
            if form.data.get('password'):
                account.change_password(form.data.get('password'))
            db.session.add(account)
            db.session.commit()
            return jsonify(success=True)

        if form.errors:
            return jsonify(success=False, messages=form.errors)

    elif request.method == 'DELETE':
        account.delete()

    return render_template('dashboard/account.html',
                           account=account, form=form)


@dashboard_app.route('/dashboard/goals')
@su_required
def goals():
    return render_template('dashboard/goals.html')
