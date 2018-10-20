
from tornado.web import URLSpec, StaticFileHandler, Application
from settings import default_settings
from views import input

def _handlers():
    prefix = default_settings.get('view_prefix', '/edu')
    if prefix[-1] != '/':
        prefix += '/'
    return [
        URLSpec('/', input.DefaultHandler, default_settings),
        URLSpec(prefix+'login.html', input.LoginViewHandler, default_settings),
        URLSpec(prefix+'(?P<manage_obj>.+).html', input.ManageViewHandler, default_settings),
        (prefix + r'(.*\.(css|png|gif|jpg|js|ttf|woff|woff2))', StaticFileHandler, {'path': default_settings.get('static_path')}),
        ]

views_handlers = _handlers()