#!/usr/bin/python
# -*- coding: utf-8 -*-

class Logic(object):
    def __init__(self):
        pass

    def input(self, *args, **kwargs):
        return True

    def update(self, id="", **kwargs):
        return True

    def infos(self, *args, **kwargs):
        return {}

    def delete(self, id="", **kwargs):
        return True

    def views(self, models):
        if isinstance(models, list):
            result = []
            for model in models:
                result.append(model.to_dict())
            return result
        return models.to_dict()