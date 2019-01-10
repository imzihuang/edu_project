#!/usr/bin/python
# -*- coding: utf-8 -*-

import six

class ExpressException(Exception):
    """Base Cinder Exception
    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = "An unknown exception occurred."
    code = 500
    headers = {}
    safe = False
    key = ""

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        self.kwargs['message'] = message

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        for k, v in self.kwargs.items():
            if isinstance(v, Exception):
                # NOTE(tommylikehu): If this is a cinder exception it will
                # return the msg object, so we won't be preventing
                # translations.
                self.kwargs[k] = six.text_type(v)

        if self._should_format():
            try:
                _message = ""
                for k, v in kwargs.items():
                    _message += '{k}:{v};'.format(v=v, k=k)
                #message = self.message % kwargs
                message = self.message % {"message": _message}
                message = message.decode('utf-8')

            except Exception:
                # NOTE(melwitt): This is done in a separate method so it can be
                # monkey-patched during testing to make it a hard failure.
                #self._log_exception()
                message = self.message
        elif isinstance(message, Exception):
            # NOTE(tommylikehu): If this is a cinder exception it will
            # return the msg object, so we won't be preventing
            # translations.
            message = six.text_type(message)

        # NOTE(luisg): We put the actual message in 'msg' so that we can access
        # it, because if we try to access the message via 'message' it will be
        # overshadowed by the class' message attribute
        self.msg = message
        super(ExpressException, self).__init__(message)
        # Oslo.messaging use the argument 'message' to rebuild exception
        # directly at the rpc client side, therefore we should not use it
        # in our keyword arguments, otherwise, the rebuild process will fail
        # with duplicate keyword exception.
        self.kwargs.pop('message', None)

    def _log_exception(self):
        pass

    def _should_format(self):
        return self.kwargs['message'] is None and '%(message)' in self.message

    # NOTE(tommylikehu): self.msg is already an unicode compatible object
    # as the __init__ method ensures of it, and we should not be modifying
    # it in any way with str(), unicode(), or six.text_type() as we would
    # be preventing translations from happening.
    def __unicode__(self):
        return self.msg

class NotFound(ExpressException):
    message = u"Resource could not be found. %(message)s"
    code = 404
    safe = True

class ParamExist(ExpressException):
    message = "Params Exist. %(message)s"
    code = 408
    safe = True

class FormalError(ExpressException):
    message = "Formal Error. %(message)s"
    code = 409
    safe = True

class ParamNone(ExpressException):
    message = "Param is none. %(message)s"
    code = 410
    safe = True
