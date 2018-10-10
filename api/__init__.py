from api import input
from settings import default_settings

def _handlers():
    return [
        (r'(?P<registry_obj>.+)/input$', input.RegistryHandler),
    ]


api_handlers = _handlers()