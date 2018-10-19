from api import input
from api import infos
from api import action
from settings import default_settings

def _handlers():
    return [
        (r'(?P<registry_obj>.+)/input$', input.RegistryHandler),
        (r'(?P<infos_obj>.+)/infos', infos.InfosHandler),
        (r'(?P<action>.+)/action', action.ActionHandler),
    ]


api_handlers = _handlers()