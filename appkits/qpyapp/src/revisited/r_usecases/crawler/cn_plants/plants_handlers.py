import re
from typing import List

from pandas import DataFrame

from datafarm.plants.models import PlantData
import pandas as pd


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


def read_excel_to_models(excel_path: str, file_type="csv") -> List[PlantData]:
    """
    读取Excel文件并转换为PlantData模型列表
    """
    try:
        # 获取字段别名映射
        field_aliases = {
            field.alias: field_name  # 反转映射：中文 -> 英文字段名
            for field_name, field in PlantData.model_fields.items()
            if field.alias
        }

        # 读取Excel文件
        if file_type == "xlsx":
            df = pd.read_excel(excel_path)
        elif file_type == "csv":
            df = pd.read_csv(excel_path, encoding="utf-8")

        # 重命名列（从中文到英文字段名）
        df = df.rename(columns=field_aliases)

        # 转换为模型列表
        models = []
        for index, row in df.iterrows():
            try:
                # 处理NaN值
                row_dict = row.where(pd.notna(row), None).to_dict()
                model = PlantData(**row_dict)
                models.append(model)
            except Exception as e:
                print(f"第 {index + 2} 行数据验证失败: {e}")  # Excel行号从1开始，还有标题行
                continue

        return models

    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        return []


# 更多实用功能示例
def process_plant_data(models: List[PlantData]):
    """处理植物数据的辅助函数"""

    # 1. 按采集地统计
    location_stats = {}
    for plant in models:
        location_stats[plant.collection_location] = location_stats.get(plant.collection_location, 0) + 1

    # 2. 检查数据完整性
    incomplete_records = []
    for plant in models:
        missing_fields = []
        for field_name, field in PlantData.model_fields.items():
            if not field.is_required:
                continue
            if not getattr(plant, field_name):
                missing_fields.append(field.alias)
        if missing_fields:
            incomplete_records.append({
                "chinese_name": plant.chinese_name,
                "missing_fields": missing_fields
            })

    # 3. 导出统计结果
    stats = {
        "total_records": len(models),
        "location_stats": location_stats,
        "incomplete_records": incomplete_records,
        "unique_collectors": len(set(plant.collector for plant in models))
    }

    return stats


# 数据验证和清理示例
def validate_and_clean_data(models: List[PlantData]) -> List[PlantData]:
    """验证和清理数据"""
    cleaned_models = []
    for model in models:
        # 1. 清理空白字符
        model.chinese_name = model.chinese_name.strip()
        model.latin_name = model.latin_name.strip()

        # 2. 标准化日期格式（如果需要）
        if model.collection_date:
            try:
                # 可以添加日期格式转换逻辑
                pass
            except:
                print(f"日期格式错误: {model.collection_date}")

        # 3. 验证海拔格式
        if model.elevation:
            if not model.elevation.endswith('m'):
                model.elevation = f"{model.elevation}m"

        cleaned_models.append(model)

    return cleaned_models


def create_dataframe_from_json(data_list: list) -> pd.DataFrame:
    # 获取字段别名映射
    field_aliases = {
        field_name: field.alias
        for field_name, field in PlantData.model_fields.items()
        if field.alias
    }

    # 创建DataFrame
    df = pd.DataFrame(data_list)

    # 重命名列名（从中文别名到英文字段名）
    df = df.rename(columns={v: k for k, v in field_aliases.items()})

    return df


def write_to_excel(df: pd.DataFrame, output_path: str):
    # 获取字段别名映射
    field_aliases = {
        field_name: field.alias
        for field_name, field in PlantData.model_fields.items()
        if field.alias
    }

    # 重命名列名（从英文字段名到中文别名）
    df_output = df.rename(columns=field_aliases)

    # 写入Excel
    df_output.to_excel(output_path, index=False)


def write_models_to_excel(models: List[PlantData], excel_path: str):
    """
    将模型列表写入Excel，使用别名作为表头
    """
    try:
        # 将模型列表转换为字典列表，使用别名作为键
        rows = []
        for model in models:
            row = {
                field.alias: getattr(model, field_name)
                for field_name, field in model.__class__.model_fields.items()
                if field.alias
            }
            rows.append(row)

        # 创建DataFrame
        df = pd.DataFrame(rows)

        # 写入Excel
        df.to_excel(excel_path, index=False)
        print(f"成功写入 {len(models)} 条记录到 {excel_path}")

    except Exception as e:
        print(f"写入Excel文件时出错: {e}")


# def select_three_locations_per_latin(df: pd.DataFrame,
#                                      latin_col: str = '拉丁名',
#                                      location_col: str = '采集地') -> pd.DataFrame:
#     """
#     为每个拉丁名选择3个不同的采集地记录
#
#     Parameters:
#         df: 输入DataFrame
#         latin_col: 拉丁名列名
#         location_col: 采集地列名
#     """
#     try:
#         # 1. 对拉丁名和采集地进行分组，获取第一条记录
#         df_grouped = df.groupby([latin_col, location_col]).first().reset_index()
#
#         # 2. 为每个拉丁名选择3个不同的采集地
#         result_df = df_grouped.groupby(latin_col).head(3)
#
#         print(f"原始记录数: {len(df)}")
#         print(f"处理后记录数: {len(result_df)}")
#         print(f"拉丁名数量: {len(result_df[latin_col].unique())}")
#
#         return result_df
#
#     except Exception as e:
#         print(f"处理数据时出错: {e}")
#         return pd.DataFrame()


def select_three_locations_per_latin(df: pd.DataFrame,
                                     latin_col: str = '拉丁名',
                                     location_col: str = '采集地') -> pd.DataFrame:
    """
    为每个拉丁名选择3个不同的采集地记录

    Parameters:
        df: 输入DataFrame
        latin_col: 拉丁名列名
        location_col: 采集地列名
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


def write_excel_safely(df: pd.DataFrame, output_path: str):
    """安全地写入Excel文件"""
    try:
        # 清理所有列的数据
        df_clean = df.copy()
        for column in df_clean.columns:
            df_clean[column] = df_clean[column].apply(clean_illegal_chars)

        # 写入Excel
        df_clean.to_excel(output_path, index=False, engine='openpyxl')
        print(f"成功写入到 {output_path}")

    except Exception as e:
        print(f"写入Excel时出错: {e}")


# 使用示例
if __name__ == "__main__":
    df = read_excel_to_df("./origin/11-12-植物合并.csv", "csv")
    # df = read_excel_to_df("./origin/11-12-植物合并.csv","csv")

    result_df = select_three_locations_per_latin(df)
    print(result_df)
    write_excel_safely(result_df, "11-12-植物合并-3个.xlsx")
    # result_df.to_excel("001 10月20日植物-3个.xlsx")
    # r2 = read_excel_to_models("./origin/002 10月20日植物 合并.csv","csv")
    # r3 = read_excel_to_models("./origin/003 10月20日植物 合并.csv","csv")
    # r4 = read_excel_to_models("./origin/11-12-植物合并.csv","csv")
    # result.extend(r2)
    # result.extend(r3)
    # result.extend(r4)
    # current_item_name = ""
    # current_index = 1
    # current_location=""
    # filtered_result = []
    # for item in result:
    #     if current_index==1:
    #         current_item_name = item.latin_name
    #         current_location =item.collection_location
    #         filtered_result.append(item)

    # write_models_to_excel(result, "all_before_filter.xlsx")
