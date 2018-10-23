#coding:utf-8

from api import input, update, infos, action, wx_action

def _handlers():
    return [
        (r'/(?P<registry_obj>.+)/input$', input.RegistryHandler),
        (r'/(?P<update_obj>.+)/infos$', update.UpdateHandler),
        (r'/(?P<infos_obj>.+)/infos$', infos.InfosHandler),
        (r'/(?P<action>.+)/action$', action.ActionHandler),
        (r'/(?P<action>.+)/wx_action$', wx_action.WXActionHandler),
    ]

api_handlers = _handlers()