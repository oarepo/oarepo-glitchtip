import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

def initialize_glitchtip(dsn=None, deployment_version=None):
    if dsn is None:
        dsn = os.environ.get("INVENIO_GLITCHTIP_DSN", "")
    if not dsn:
        return

    sentry_sdk.init(
        dsn=dsn,
        integrations=[FlaskIntegration()],
        # send details about current user. Note: glitchtip should be run on-premises
        # and we need to remove these records after 12-18 months to comply with CESNET
        # data retention policy
        send_default_pii=True
    )

    if deployment_version is None:
        deployment_version = os.environ.get("DEPLOYMENT_VERSION", "")
    if deployment_version:
        sentry_sdk.set_tag("release", deployment_version)
