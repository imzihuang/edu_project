#coding:utf-8

from api import input, update, infos, delete, action, wx_action, combination_input, combination_infos
from settings import default_settings

def _handlers():
    return [
        (r'/(?P<registry_obj>.+)/input$', input.RegistryHandler),
        (r'/(?P<update_obj>.+)/update$', update.UpdateHandler),
        (r'/(?P<infos_obj>.+)/infos$', infos.InfosHandler),
        (r'/(?P<delete_obj>.+)/delete', delete.DeleteHandler),
        (r'/(?P<action>.+)/action$', action.ActionHandler, default_settings),
        (r'/(?P<action>.+)/wx_action$', wx_action.WXActionHandler),
        (r'/(?P<combination>.+)/combination_input$', combination_input.CombinationHandler),
        (r'/(?P<combination>.+)/combination_infos$', combination_infos.CombinationHandler)
    ]

api_handlers = _handlers()