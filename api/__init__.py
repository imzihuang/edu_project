import input
from settings import default_settings

#express api
def _express_handlers():
    return [
        (r'(?P<registry_obj>.+)/input$', input.RegistryHandler),
    ]


api_handlers = []#_express_handlers()