from typing import Callable


class InjectorException(Exception):
    pass


class ConstructorTypeError(TypeError):
    def __init__(self, constructor: Callable, constructor_error: TypeError):
        super(ConstructorTypeError, self).__init__("%s raised an error: %s" % (constructor, constructor_error))
