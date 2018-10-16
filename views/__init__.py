
from tornado.web import URLSpec, StaticFileHandler, Application
from settings import default_settings
from views import input
def _handlers():
    prefix = "edu"
    return [
        URLSpec('/pre/', input.RegistryViewHandler, default_settings),
        (prefix + r'(.*\.(css|png|gif|jpg|js|ttf|woff|woff2))', StaticFileHandler, {'path': default_settings.get('static_path')}),
        ]

views_handlers = _handlers()