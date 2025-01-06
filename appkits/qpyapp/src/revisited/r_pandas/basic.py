import pandas as pd

df_cr = pd.DataFrame({
    "Name": ["Braund, Mr. Owen Harris",
             "Allen, Mr. William Henry",
             "Bonnell, Miss. Elizabeth", ],
    "Age": [22, 35, 58],
    "Sex": ["male", "male", "female"],
})


def dataframe_demo():
    print("go through dataframe")
    ## DataFrame Col/Row

    print(df_cr)
    ## let's how in excel or csv
    df_cr.to_excel("user.xlsx")
    df_cr.to_csv("user.csv")


def dataframe_series_feature_demo():
    print(df_cr['Age'])
    ages = pd.Series([22, 35, 58], name="Age")
    print(ages)

    ## series features
    print(df_cr['Age'].max())
    print(df_cr['Age'].min())
    print(df_cr['Age'].mean())
    print(df_cr.describe())


dataframe_demo()
dataframe_series_feature_demo()
