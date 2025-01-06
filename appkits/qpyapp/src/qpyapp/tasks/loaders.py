from __future__ import annotations

import importlib
import inspect
from pathlib import Path
from typing import List, Dict, Callable, Hashable, Any


class LoaderError(Exception):
    pass


def to_package_format(path: Path) -> str:
    module_fs_path = ".".join(path.parts)
    module = module_fs_path.replace(".py", "")
    if module.endswith(".__init__"):
        return module.replace(".__init__", "")

    return module


def discover(path: Path, app_path: str):
    dirs: list[Path] = [path]
    while dirs:
        module = dirs.pop(0)
        for sub_module in module.iterdir():
            if sub_module.is_dir():
                dirs.append(sub_module)
            else:
                if sub_module.name.endswith(".py"):
                    try:
                        mod = to_package_format(sub_module)
                        if mod not in app_path:
                            importlib.import_module(mod)
                    except ModuleNotFoundError as e:
                        raise LoaderError(str(e))


def autodiscover_modules(modules: List[str], app_path: str):
    """Utility to automatically import the app's modules so there is
    no need to manual importing controllers, services, etc, to provide
    the necessary registry for DI

    Args:
        modules:
        app_path:

    Returns:
        None

    """

    for module in modules:
        app_root = Path(module)

        if not app_root.is_dir():
            raise LoaderError(
                f"{app_root.resolve()} is not a dir. Autodiscovery must be called on a dir."
            )

        discover(app_root, app_path)


def load_class_to_method_lookup_table(service: Any) -> Dict[Hashable, Callable]:
    result: Dict[Hashable, Callable] = {}
    for member in dir(service):
        member_instance = getattr(service, member)
        if inspect.ismethod(member_instance):
            result[".".join([type(service).__name__, member])] = member_instance
    return result


def load_module_to_method_lookup_table(module: str | type) -> (Dict[Hashable, Callable], Dict[Hashable, Callable]):
    module_mapping: Dict[Hashable, Callable] = {}
    method_mapping: Dict[Hashable, Callable] = {}
    if not inspect.ismodule(module):
        module_for_lookup = importlib.import_module(module)
    else:
        module_for_lookup = module
    module_mapping[module_for_lookup.__name__] = module_for_lookup

    for member in dir(module_for_lookup):
        member_instance = getattr(module_for_lookup, member)
        if inspect.isclass(member_instance):
            if not inspect.isabstract(member_instance):
                method_mapping.update(load_class_to_method_lookup_table(member_instance()))
    return module_mapping, method_mapping
