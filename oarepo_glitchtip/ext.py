import sentry_sdk
from flask_login import current_user
from invenio_accounts.models import User
from invenio_files_rest.app import Flask

import logging
log = logging.getLogger(__name__)

class OARepoGlitchtipExt:
    def __init__(self, app=None, **kwargs):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions['oarepo-glitchtip'] = self


def finalize_app(app: Flask):
    app.before_request(add_user_to_glitchtip)


def add_user_to_glitchtip() -> None:
    """Add user to glitchtip."""
    try:
        if not current_user.is_authenticated:
            return
        u: User = current_user
        sentry_sdk.set_user({"id": u.id, "email": u.email, "username": u.email, "ip_address": "{{auto}}",
                             **u.user_profile})
    except:       # noqa
        log.exception("Failed to add user to glitchtip")
