import pandas as pd

def test_read_to_objects():
   result: pd.DataFrame = pd.read_excel('unit_demo.xlsx')
   print(result)
