#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import logging

STATIC_PATH = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'static')
TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'templates')

default_settings = {
    'base_url': '/',
    'view_prefix': 'edu',
    'static_path': STATIC_PATH,
    'templates_path': TEMPLATES_PATH,
    'api_version': 'v1.0',
    'enabled_methods': ['get', 'post', 'put', 'patch', 'delete'],
    'exclude_namespaces': [],
    'log_path': "./log/edu.log",
    'model_checkpoint': './model/20180920-153747',
    'face_path': 'image/face/'
}

models = []

Debug = False

if Debug:
    logging.basicConfig(level=logging.DEBUG)
