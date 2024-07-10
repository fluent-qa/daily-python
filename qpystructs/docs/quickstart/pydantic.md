# Pydantic Model

在进行接口测试时,几乎无时无刻都在进行数据结构类型的转换：

1. json-> python object/dict
2. python object/dict -> json

为了方便进行这种转换,使用了pydantic 类进行简化操作，同时方便编写业务意义代码.

## 使用pydantic 好处

- 和直接使用dict比较
- 有什么额外的好处
- 有什么不方便的地方

## 使用pydantic遇到的一些问题

- 问题是:

1. 不同语言的命名规范不一样，以及enum问题怎么解决

* python: test_case
* java: testCase
* Go: TestCase
* ....

2. 嵌套的对象序列化问题

* 什么是序列化和发序列化？

- 解决方案

```python
class BaseDataModel(BaseModel):
  class Config:
    arbitrary_types_allowed = True  # 解决问题2
    # alias_generator = to_camel
    allow_population_by_field_name = True  # 解决问题1
    use_enum_values = True

  def to_json(self):
    return self.json(by_alias=True, exclude_none=True)

  def to_dict(self):
    return self.dict(by_alias=True, exclude_none=True)
```

## 使用例子

- model 定义:

```python
class DemoNum(Enum):
  Test = "Test"
  Dev = "dev"


class DemoJsonFile(models.BaseDataModel):
  test_case: str = Field(None, alias="testCase")
  demo_enum: DemoNum = Field(None, alias="demoEnum")

```

- 测试脚本

```python
def test_base_data_model():
  json_result = DemoJsonFile(test_case="testcase", demo_enum=DemoNum.Test).to_json()
  dict_result = DemoJsonFile(test_case="testcase", demo_enum=DemoNum.Test).to_dict()
  print(type(json_result))
  print(json_result)
  print(type(dict_result))
  print(dict_result)
```
