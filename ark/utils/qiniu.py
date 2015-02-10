import os
import hmac
import json
import calendar
from uuid import uuid4
from hashlib import sha1, md5
from urlparse import urljoin
from base64 import urlsafe_b64encode
from datetime import datetime, timedelta


def hmac_sha1(data):
    access_secret = os.environ['ARK_QINIU_ACCESS_SECRET']
    hashed = hmac.new(access_secret, data, sha1)
    return hashed.digest()


def calc_ts(s):
    now = datetime.utcnow()
    deadline = now + timedelta(seconds=s)
    return calendar.timegm(deadline.timetuple())


def hash_save_key(uid=None, prefix=None):
    hash_uid = md5(str(uid)).hexdigest()
    key = uuid4().hex
    if prefix:
        key = '%s-%s' % (prefix, key)
    return '%s/%s$(ext)' % (hash_uid, key)


def encodedEntryURI(key, bucket=None):
    bucket = bucket or os.environ['ARK_QINIU_BUCKET']
    entry = '%s:%s' % (bucket, key)
    return urlsafe_b64encode(entry)


def gen_encoded_policy(data):
    scope = os.environ['ARK_QINIU_BUCKET']
    deadline = calc_ts(60 * 10)
    policy  = {
        'scope': scope,
        'deadline': deadline,
        'mimeLimit': 'image/*',
        'fsizeLimit': 1024 * 1024 * 3,
        'returnBody': '{"name": $(fname), "key": $(key)}',
    }
    policy.update(data)
    return urlsafe_b64encode(json.dumps(policy))


def gen_encoded_sign(policy):
    sign = hmac_sha1(policy)
    encoded_sign = urlsafe_b64encode(sign)
    return encoded_sign


def gen_upload_token(data):
    encoded_policy = gen_encoded_policy(data)
    encoded_sign = gen_encoded_sign(encoded_policy)
    return "%s:%s:%s" % (os.environ['ARK_QINIU_ACCESS_KEY'],
                         encoded_sign,
                         encoded_policy)


def get_url(key, base_url=None):
    base_url = base_url or os.environ['ARK_QINIU_BASE_URL']
    if not base_url.endswith('/'):
        base_url = '%s/' % base_url
    return urljoin(base_url, key)
