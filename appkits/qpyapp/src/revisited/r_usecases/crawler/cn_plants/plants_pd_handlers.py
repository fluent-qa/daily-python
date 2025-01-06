import re

import pandas as pd
from pandas import DataFrame


#
# df = pd.read_excel("your_file.xlsx")
#
# # 方法1：使用 tolist()
# column_list = df['列名'].tolist()
#
# # 方法2：使用 values.tolist()
# column_list = df['列名'].values.tolist()
#
# # 方法3：使用 list() 转换
# column_list = list(df['列名'])
#
# # 方法4：使用 to_numpy()
# column_list = df['列名'].to_numpy().tolist()
#
# # 处理空值的方法
# # 方法5：排除 NaN 值
# column_list = df['列名'].dropna().tolist()
#
# # 方法6：将 NaN 替换为特定值后转换
# column_list = df['列名'].fillna('').tolist()
#
# # 方法7：使用列表推导式（可以添加条件）
# column_list = [x for x in df['列名'] if pd.notna(x)]


def read_excel_to_df(excel_path: str, file_type="csv") -> DataFrame | None:
    """
    读取Excel文件并转换为PlantData模型列表
    """
    try:
        # 获取字段别名映射
        # field_aliases = {
        #     field.alias: field_name  # 反转映射：中文 -> 英文字段名
        #     for field_name, field in PlantData.model_fields.items()
        #     if field.alias
        # }

        # 读取Excel文件
        if file_type == "xlsx":
            df = pd.read_excel(excel_path)
        elif file_type == "csv":
            df = pd.read_csv(excel_path, encoding="utf-8")
        # 重命名列（从中文到英文字段名）
        # df = df.rename(columns=field_aliases)

        return df
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        return None


# 完整的处理函数
# def get_clean_column_list(df: pd.DataFrame,
#                           column_name: str,
#                           drop_na: bool = True,
#                           drop_duplicates: bool = True,
#                           strip_spaces: bool = True) -> list:
#     """
#     获取清理后的列数据列表
#
#     Parameters:
#         df: DataFrame
#         column_name: 列名
#         drop_na: 是否删除空值
#         drop_duplicates: 是否删除重复值
#         strip_spaces: 是否去除空格
#     """
#     try:
#         # 获取列数据
#         series = df[column_name].copy()
#
#         # 去除空格
#         if strip_spaces:
#             series = series.apply(lambda x: x.strip() if isinstance(x, str) else x)
#
#         # 删除空值
#         if drop_na:
#             series = series.dropna()
#
#         # 删除空字符串
#         series = series[series != '']
#
#         # 删除重复值
#         if drop_duplicates:
#             series = series.unique()
#
#         return series.tolist()
#
#     except Exception as e:
#         print(f"处理列数据时出错: {e}")
#         return []


def get_duplicate_values(df: pd.DataFrame, column_name: str, min_count: int = 2):
    """
    获取列中的重复值

    Parameters:
        df: DataFrame
        column_name: 列名
        min_count: 最小重复次数
    """
    try:
        # 获取值计数
        value_counts = df[column_name].value_counts()

        # 获取重复的值
        duplicates = value_counts[value_counts >= min_count]

        # 创建结果字典：值 -> 出现次数
        result_dict = duplicates.to_dict()

        print(f"\n重复值统计 (最小重复次数: {min_count}):")
        print(f"总值数量: {len(df[column_name])}")
        print(f"重复值数量: {len(result_dict)}")

        # 按出现次数排序
        sorted_duplicates = sorted(
            result_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_duplicates

    except Exception as e:
        print(f"获取重复值时出错: {e}")
        return []


def compare_duplicate_methods(df: pd.DataFrame, column_name: str):
    """
    比较不同的重复值处理方法
    """
    # 1. series.drop_duplicates() - 保留唯一值
    unique_values = df[column_name].drop_duplicates().tolist()

    # 2. get_duplicate_values() - 获取重复的值
    value_counts = df[column_name].value_counts()
    duplicate_values = value_counts[value_counts >= 2].index.tolist()

    print(f"\n比较结果:")
    print(f"原始数据总数: {len(df[column_name])}")
    print(f"drop_duplicates 结果数量: {len(unique_values)}")  # 所有不重复的值
    print(f"get_duplicate_values 结果数量: {len(duplicate_values)}")  # 只有重复的值

    # 显示示例
    print("\n示例比较:")
    print("1. drop_duplicates 结果 (所有唯一值):")
    print(unique_values[:5])

    print("\n2. get_duplicate_values 结果 (只有重复值):")
    print(duplicate_values[:5])

    # 显示具体例子
    example_value = duplicate_values[0] if duplicate_values else None
    if example_value:
        print(f"\n具体例子 '{example_value}':")
        print(f"在原始数据中出现 {value_counts[example_value]} 次")
        print(f"在 drop_duplicates 结果中出现 1 次")
        print(f"在 get_duplicate_values 结果中出现 1 次")


def select_three_locations_per_latin(df: pd.DataFrame,
                                     key_counts=None,
                                     latin_col: str = '拉丁名',
                                     location_col: str = '采集地'
                                     ) -> pd.DataFrame:
    """
    为每个拉丁名选择3个不同的采集地记录

    Parameters:
        df: 输入DataFrame
        latin_col: 拉丁名列名
        location_col: 采集地列名
        :param key_counts:
    """
    try:
        # 1. 获取每个拉丁名的不同采集地
        df_unique_locations = df.drop_duplicates([latin_col, location_col])

        # 2. 为每个拉丁名选择最多3个不同的采集地
        result_dfs = []
        for latin_name, group in df_unique_locations.groupby(latin_col):
            # 如果有超过3个不同采集地，随机选择3个
            if len(group) > 3:
                selected_records = group.sample(n=3)
            else:
                selected_records = group
            if len(key_counts) > 0:
                if latin_name.strip() in key_counts.index:
                    # 方法1：直接修改值
                    key_counts[latin_name] += 1
                else:
                    continue
            result_dfs.append(selected_records)

        # 3. 合并结果
        result_df = pd.concat(result_dfs, ignore_index=True)

        print(f"原始记录数: {len(df)}")
        print(f"处理后记录数: {len(result_df)}")
        print(f"拉丁名数量: {len(result_df[latin_col].unique())}")

        # 4. 验证结果
        location_counts = result_df.groupby(latin_col)[location_col].nunique()
        print("\n采集地数量统计:")
        print(f"最大值: {location_counts.max()}")
        print(f"最小值: {location_counts.min()}")
        print(f"平均值: {location_counts.mean():.2f}")

        return result_df

    except Exception as e:
        print(f"处理数据时出错: {e}")
        return pd.DataFrame()


def clean_illegal_chars(text):
    """清理非法字符"""
    if not isinstance(text, str):
        return text

    # 移除或替换非法字符
    # ILLEGAL_CHARACTERS_RE = r'[\000-\010]|[\013-\014]|[\016-\037]'
    ILLEGAL_CHARACTERS_RE = r'[\000-\010]|[\013-\014]|[\016-\037]|[\x00-\x1f\x7f-\x9f]'
    return re.sub(ILLEGAL_CHARACTERS_RE, '', str(text))


def write_excel_safely(df: pd.DataFrame, output_path: str,output_type="xlsx"):
    """安全地写入Excel文件"""
    try:
        # 清理所有列的数据
        df_clean = df.copy()
        for column in df_clean.columns:
            df_clean[column] = df_clean[column].apply(clean_illegal_chars)

        # 写入Excel
        if output_type == "xlsx":
            df_clean.to_excel(output_path, index=False, engine='openpyxl')
        else:
            df_clean.to_csv(output_path, index=False)
        print(f"成功写入到 {output_path}")

    except Exception as e:
        print(f"写入Excel时出错: {e}")


if __name__ == '__main__':
    category_df = read_excel_to_df("./docs/删除重复.xlsx", "xlsx")
    unique_values = category_df["拉丁名"].str.strip().drop_duplicates()
    value_counts = unique_values.value_counts()
    print(value_counts[value_counts > 1])

    # current_df = None
    for file_name in ["./origin/001 10月20日植物 合并", "./origin/002 10月20日植物 合并",
                      "./origin/003 10月20日植物 合并", "./origin/11-12-植物合并"]:
        df = read_excel_to_df(file_name + ".csv", "csv")
        result_df = select_three_locations_per_latin(df, key_counts=value_counts)
        # if current_df is not None:
        #     current_df = pd.merge(current_df, result_df)
        # else:
        #     current_df = result_df
        write_excel_safely(result_df, file_name + "-3.csv",output_type="csv")
    # write_excel_safely(current_df, "all.xlsx")

    print(value_counts[value_counts > 1])
    print(len(value_counts[value_counts == 1]))
    value_df = value_counts.reset_index()
    value_df.columns = ["拉丁名", "数量"]
    value_df.to_excel("name_stats.xlsx", index=False)
    ignored_df = value_counts[value_counts == 1].reset_index()
    ignored_df.columns = ["拉丁名", "数量"]
    ignored_df.to_excel("name_ignore_stats.xlsx", index=False)
    # write_excel_safely(value_counts.to_frame(), "all_written.xlsx")
