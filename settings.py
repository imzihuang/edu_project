#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import logging

STATIC_PATH = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'static')
TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'templates')

default_settings = {
    'base_url': '/',
    'static_path': STATIC_PATH,
    'templates_path': TEMPLATES_PATH,
    'api_version': 'v1.0',
    'api_key': '',
    'enabled_methods': ['get', 'post', 'put', 'patch', 'delete'],
    'exclude_namespaces': [],
    'log_path': "/var/log/express.log"
}

models = []

Debug = False

if Debug:
    logging.basicConfig(level=logging.DEBUG)
