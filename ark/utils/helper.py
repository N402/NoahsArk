from speaklater import is_lazy_string

from flask import jsonify


def jsonify_lazy(**kwargs):
    def _validate(var):
        if isinstance(var, (tuple, list)):
            for i, v in enumerate(var):
                var[i] = _validate(v)
        elif isinstance(var, dict):
            for k in var:
                var[k] = _validate(var[k])
        else:
            if is_lazy_string(var):
                return unicode(var)
            else:
                return var
        return var

    for k in kwargs:
        kwargs[k] = _validate(kwargs[k])

    return jsonify(**kwargs)
