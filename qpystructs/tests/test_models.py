from model_for_test import DemoModel, DemoModelAlias
from qpystructs import models


def test_modelize_camel_naming():
    result = DemoModel.parse_file("./structured-data/camel.json")
    print(result)


def test_modelize_alias_naming():
    result = DemoModelAlias.parse_file("./structured-data/camel-alias.json")
    print(result.k_index)
    print(result.model_dump_json(by_alias=True))
    print(result.to_json())


def test_parse_as():
    result = DemoModelAlias.parse_file("./structured-data/camel-alias.json")
    json_str = result.model_dump_json(by_alias=True)
    obj_model = models.parse_as(json_str, DemoModelAlias)
    dict_obj = result.to_dict(by_alias=True)
    print(obj_model)
    dict_model = models.parse_as(dict_obj, DemoModelAlias)
    assert dict_model.key == "v1"
