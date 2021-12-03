import pandas as pd
import requests

"""
这是一个小工具，用于从网页获取数据，并保存到csv文件中
"""


def get_html_data(url, table_num=0):
    """
    Fetch data from a table in the database
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=header)
    return pd.read_html(r.text)[table_num]


def save_df_to_csv(df, filename):
    """
    Save a dataframe to a csv file
    """
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    save_df_to_csv(get_html_data(
        "https://www.gingersoftware.com/content/grammar-rules/verbs/list-of-phrasal-verbs/"), "data.csv")
