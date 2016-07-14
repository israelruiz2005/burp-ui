# -*- coding: utf8 -*-
"""
.. module:: burpui.api
    :platform: Unix
    :synopsis: Burp-UI api module.

.. moduleauthor:: Ziirish <hi+burpui@ziirish.me>


"""
import os
import sys
import logging

from flask import Blueprint, Response, request, current_app as bui
from flask_restplus import Api as ApiPlus
from flask_login import current_user
from importlib import import_module
from functools import wraps

from ..exceptions import BUIserverException

EXEMPT_METHODS = set(['OPTIONS'])


def cache_key():
    return '{}-{}-{}'.format(current_user.get_id(), request.path, request.values)


def api_login_required(func):
    """Custom login decorator that is able to parse Basic credentials as well as
    Cookies set with the traditional login.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        """decorator"""
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        try:
            name = func.func_name
        except:  # pragma: no cover
            name = func.__name__
        if (bui.auth != 'none' and
                name not in api.LOGIN_NOT_REQUIRED and
                not bui.config.get('LOGIN_DISABLED', False)):
            if not current_user.is_authenticated:
                if request.headers.get('X-From-UI', False):
                    return Response('Access denied', 403)
                return Response(
                    'Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return func(*args, **kwargs)
    return decorated_view


class Api(ApiPlus):
    """Wrapper class around :class:`flask_restplus.Api`"""
    db = None
    cache = None
    logger = logging.getLogger('burp-ui')
    loaded = False
    celery = None
    app_cli = None
    release = None
    __doc__ = None
    __url__ = None
    LOGIN_NOT_REQUIRED = []
    CELERY_REQUIRED = ['async']

    def load_all(self):
        """hack to automatically import api modules"""
        if not self.loaded:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            self.loaded = True
            for f in os.listdir(__path__[0]):
                name, ext = os.path.splitext(f)
                if (os.path.isfile(os.path.join(__path__[0], f)) and
                        ext == '.py' and
                        name not in ['__init__', '.', '..']):
                    mod = '.' + name
                    if name not in self.CELERY_REQUIRED or self.celery:
                        self.logger.debug('Loading API module: {}'.format(mod))
                        import_module(mod, __name__)
                    else:
                        self.logger.warning('Skipping API module: {}'.format(mod))


apibp = Blueprint('api', __name__, url_prefix='/api')
api = Api(apibp, title='Burp-UI API', description='Burp-UI API to interact with burp', doc='/doc', decorators=[api_login_required])


@api.errorhandler(BUIserverException)
def handle_bui_server_exception(error):
    """Forward a BUIserverException to the final user

    :param error: Custom exception
    :type error: :class:`burpui.exceptions.BUIserverException`
    """
    return {'message': error.description}, error.code
