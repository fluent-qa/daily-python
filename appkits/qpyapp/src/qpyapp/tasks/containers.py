import abc
import inspect
import typing
from typing import Any

from box import Box

from . import loaders


class AbsContainer(abc.ABC):

    def __init__(self, *args, **kwargs):
        self.lookup_table = {}
        self.router = kwargs["router"]

    def register(self, registry: Any, identity: typing.Hashable):
        self.lookup_table[identity] = registry

    def export(self):
        return self.lookup_table

    def get(self, identity: Any):
        return self.lookup_table[identity]


class ProviderContainer(AbsContainer):

    def __init__(self, router="Provider"):
        super().__init__(router=router)


class ServiceContainer(AbsContainer):

    def __init__(self, router="Service"):
        super().__init__(router=router)
        self.services = Box()
        self.handlers = Box()

    def register(self, spell: Any, identity: typing.Hashable):
        if inspect.isclass(spell):
            self.services[spell.__name__] = spell  ## todo: remove
            self.handlers.update(loaders.load_class_to_method_lookup_table(spell.__init__(spell)))
        if inspect.ismodule(spell):
            modules, methods = loaders.load_module_to_method_lookup_table(spell)
            self.services.update(**modules)
            self.handlers.update(**methods)
        self.lookup_table[identity] = spell
        return self

    def get_spell(self, identity: Any):
        return self.handlers[identity]

    def add_handler(self, handler: Any):
        self.handlers[handler.__name__] = handler
        return self

    @staticmethod
    def __dynamic_call_func(func, http_json_model):
        t = inspect.signature(func)
        args = []
        for item in t.parameters.items():
            args.append(getattr(http_json_model, item[0]))
        return func(*args)

    def call_service(self, service_name: Any, request_data: Any):
        handler = self.handlers.get(service_name)
        return self.__dynamic_call_func(handler, request_data)


providers = ProviderContainer()
services = ServiceContainer()
