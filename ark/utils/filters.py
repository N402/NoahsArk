from flask.ext.babel import lazy_gettext as _


def gender(is_male):
    return _('male') if is_male else _('female')
