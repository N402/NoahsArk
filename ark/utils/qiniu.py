import os
import hmac
import json
import calendar
from uuid import uuid4
from hashlib import sha1, md5
from base64 import urlsafe_b64encode
from datetime import datetime, timedelta

from flask.ext.login import current_user


def hmac_sha1(data):
    access_secret = os.environ['ARK_QINIU_ACCESS_SECRET']
    hashed = hmac.new(access_secret, data, sha1)
    return hashed.digest()


def calc_ts(s):
    now = datetime.utcnow()
    deadline = now + timedelta(seconds=s)
    return calendar.timegm(deadline.timetuple())


def gen_key(uid=None, filename=None):
    uid = str(uid or current_user.id)
    hash_uid = md5(uid).hexdigest()
    key = filename.split('.', 1)[0] if filename else uuid4().hex
    return '%s/%s$(ext)' % (hash_uid, key)


def gen_encoded_policy(uid=None, filename=None):
    scope = os.environ['ARK_QINIU_BUCKET']
    deadline = calc_ts(60 * 10)
    returnBody = '{"name": $(fname), "key": $(key)}'
    data = {
        'scope': scope,
        'deadline': deadline,
        'saveKey': gen_key(uid, filename),
        'mimeLimit': 'image/*',
        'fsizeLimit': 1024 * 1024 * 3,
        'returnBody': returnBody,
    }
    return urlsafe_b64encode(json.dumps(data))


def gen_encoded_sign(policy):
    sign = hmac_sha1(policy)
    encoded_sign = urlsafe_b64encode(sign)
    return encoded_sign


def gen_upload_token(uid=None, filename=None):
    encoded_policy = gen_encoded_policy(uid, filename)
    encoded_sign = gen_encoded_sign(encoded_policy)
    return "%s:%s:%s" % (os.environ['ARK_QINIU_ACCESS_KEY'],
                         encoded_sign,
                         encoded_policy)
