import allure
import pandas as pd
from pydantic import BaseModel

from primary import pd_ext


class DemoPostModel(BaseModel):
    title: str
    link: str


@allure.feature("pydantic models to excel/csv")
def test_model_to_file():
    items = [
        DemoPostModel(title="title1", link="http://baidu.com"),
        DemoPostModel(title="title2", link="http://sina.com")
    ]
    pd_ext.models_to_file(items, "demo1.csv")
    pd_ext.models_to_file(items, "demo2.xlsx", "xlsx")


@allure.feature("get column data from excel")
def test_get_column_data():
    df = pd.read_csv("demo1.csv")
    print(df['link'])
    for item in df['link']:
        print(item)
