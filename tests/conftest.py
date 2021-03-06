import json
from datetime import datetime as dt

from flask import (
    Flask,
    current_app,
    url_for,
)
import pytest

from flask_jsondash import charts_builder


URL_BASE = 'http://127.0.0.1:80'
app = Flask('test_flask_jsondash')
app.secret_key = '123'
app.debug = True
app.register_blueprint(charts_builder.charts)


def _username():
    return 'Username'


def _authtest(**kwargs):
    return False


@pytest.fixture()
def ctx(request):
    with app.test_request_context() as req_ctx:
        yield req_ctx


@pytest.fixture()
def client():
    app.config.update(
        JSONDASH_GLOBALDASH=False,
        JSONDASH_FILTERUSERS=False,
        JSONDASH_GLOBAL_USER='global-test',
    )
    app.config['JSONDASH'] = dict(
        metadata=dict(
            created_by=_username,
            username=_username,
        ),
        static=dict(
            js_path='js/vendor/',
            css_path='css/vendor/',
        ),
        auth=dict(
            edit_others=_authtest,
            edit_global=_authtest,
            create=_authtest,
            view=_authtest,
            clone=_authtest,
            delete=_authtest,
        )
    )
    return app, app.test_client()
