from model_for_test import DemoModel, DemoModelAlias


def test_modelize_camel_naming():
    result = DemoModel.parse_file("./structured-data/camel.json")
    print(result)


def test_modelize_alias_naming():
    result = DemoModelAlias.parse_file("./structured-data/camel-alias.json")
    print(result.k_index)
    print(result.model_dump_json(by_alias=True))
    print(result.to_json())
