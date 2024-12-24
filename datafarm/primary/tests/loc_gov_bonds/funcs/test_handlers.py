"""
1. read project detail
2. standard: write project details into database
3. read overview details
4. compose data into standard database or output
"""
from pathlib import Path

import pandas as pd
from qpyconf import settings
from qpydao import db

from primary import cleanup, pd_ext

WORKING_DIR = Path(settings.workspace)
BOND_BACH_NAME = ""
BOND_PROVINCE = ""

"""
1. 获取数据: 手工清理保存成csv
2. cleanup: cleanup.csv后缀
3. 进行数据标准化: 
"""


def cleanup_bond_file(province: str, batch_name: str, cleanup_flag=True) -> pd.DataFrame:
    source_file_name = batch_name + ".csv"
    cleanup_source_file_name = batch_name + "_cleanup.csv"
    source_file_path = WORKING_DIR / province / source_file_name
    cleanup_source_file_path = WORKING_DIR / province / cleanup_source_file_name
    if cleanup_flag:
        cleanup.clean_csv_empty_column(source_file_path, cleanup_source_file_path)
    df = pd_ext.read_to_df(cleanup_source_file_path, file_type="csv")
    cleanup_df = pd_ext.clean_unnamed_columns(df)
    return cleanup_df


STANDARD_COLUMNS = [
    '债券代码',
    '文件公告日期', '债券批次（可以为空）', '债券期数',
    '债券总金额（亿元）', '债券年限（年）',
    '所属地区（市区县）', '项目名称', '金额（万元）'
]

ANHUI_FIELD_MAPPING = {
    '债券代码': "债券编码",
    '文件公告日期': "发行日期", '债券批次（可以为空）': "", '债券期数': "债券全称",
    '债券总金额（亿元）': None, '债券年限（年）': "债券期限（年）",
    '所属地区（市区县）': "所属市县", '项目名称': "项目名称", '金额（万元）': "项目拟发行专项债券总金额"
}

BEIJING_FIELD_MAPPING = {
    '债券代码': "债券编码",
    '文件公告日期': "发行日期", '债券批次（可以为空）': "", '债券期数': "债券名称",
    '债券总金额（亿元）': "总金额", '债券年限（年）': "债券期限（年）",
    '所属地区（市区县）': "所属市县", '项目名称': "项目名称", '金额（万元）': None
}

DALIAN_FIELD_MAPPING = {
    '债券代码': "债券编码",
    '文件公告日期': "发行日期", '债券批次（可以为空）': "", '债券期数': "债券名称",
    '债券总金额（亿元）': "总金额", '债券年限（年）': "发债期限(年)",
    '所属地区（市区县）': "地区", '项目名称': "项目名称", '金额（万元）': "本批债券拟发行金额"
}
FUJIAN_FIELD_MAPPING = {
    '债券代码': "债券编码",
    '文件公告日期': "发行日期", '债券批次（可以为空）': "", '债券期数': "债券名称",
    '债券总金额（亿元）': "发行规模", '债券年限（年）': "债券期限（年）",
    '所属地区（市区县）': "项目单位", '项目名称': "项目名称", '金额（万元）': None
}

GANSU_FIELD_MAPPING = {
    '债券代码': "债券编码",
    '文件公告日期': "发行日期", '债券批次（可以为空）': "", '债券期数': "债券名称",
    '债券总金额（亿元）': "发行金额", '债券年限（年）': "债券期限（年）",
    '所属地区（市区县）': "项目单位", '项目名称': "项目名称", '金额（万元）': "None"
}
GUANGDONG_FIELD_MAPPING = {
    '债券代码': "债券编码",
    '文件公告日期': "发行日期", '债券批次（可以为空）': "", '债券期数': "债券名称",
    '债券总金额（亿元）': "发行规模", '债券年限（年）': "债券期限（年）",
    '所属地区（市区县）': "项目单位", '项目名称': "项目名称", '金额（万元）': ""
}

GUANGXI_FIELD_MAPPING = {
    '债券代码': "债券编码",
    '文件公告日期': "发行日期", '债券批次（可以为空）': "", '债券期数': "债券全称",
    '债券总金额（亿元）': "总金额", '债券年限（年）': "发债期限(年)",
    '所属地区（市区县）': "所属市县", '项目名称': "项目名称", '金额（万元）': "项目本次专项债券发行金额"
}

HEBEI_FIELD_MAPPING = {
    '债券代码': "债券编码",
    '文件公告日期': "发行日期", '债券批次（可以为空）': "债券名称", '债券期数': "债券名称",
    '债券总金额（亿元）': "发行规模", '债券年限（年）': "发债期限(年)",
    '所属地区（市区县）': "项目单位", '项目名称': "项目名称", '金额（万元）': "发行额度"
}

HEILONGJIA_FIELD_MAPPING = {
    '债券代码': "债券编码",
    '文件公告日期': "发行日期", '债券批次（可以为空）': "", '债券期数': "债券名称",
    '债券总金额（亿元）': "总金额", '债券年限（年）': "发债期限(年)",
    '所属地区（市区县）': "所属市县", '项目名称': "项目名称", '金额（万元）': "发行额度"
}

HUBEI_FIELD_MAPPING = {
    '债券代码': "债券编码",
    '文件公告日期': "发行日期", '债券批次（可以为空）': "债券名称", '债券期数': "债券名称",
    '债券总金额（亿元）': "发行规模", '债券年限（年）': "发债期限(年)",
    '所属地区（市区县）': "项目单位", '项目名称': "项目名称", '金额（万元）': "发行额度"
}


def test_standard_process():
    batch_name = "2024年湖北省政府债券第十三批"
    cleanup_df = cleanup_bond_file(province="hubei", batch_name=batch_name, cleanup_flag=True)
    print(cleanup_df)
    # overall_df = pd_ext.read_to_df(WORKING_DIR / "total-bond.xlsx", file_type="xlsx")
    bonds = []
    for index, row in cleanup_df.iterrows():
        row_dict = row.to_dict()
        ## TODO: Convert functions
        if ANHUI_FIELD_MAPPING:
            mapped_row_dict = {}
            for key, value in HUBEI_FIELD_MAPPING.items():
                if value:
                    mapped_row_dict[key] = row_dict.get(value, None)

            bond_data = BondProjectDetail(**mapped_row_dict)
            bond_data.bond_batch = batch_name
            bond_data.bond_years = "2024"
            bond_data.file_announcement_date = "2024-09-24"
            # bond_data.amount = str(float(bond_data.amount)*10000)
            db.save(bond_data)
            bonds.append(bond_data)


def test_read_project_detail():
    ## 1.cleanup project detail
    cleanup.clean_csv_empty_column(WORKING_DIR + "/templates/new_source.csv",
                                   WORKING_DIR + "/templates/source_cleanup.csv")
    df = pd_ext.read_to_df(WORKING_DIR + "/templates/source_cleanup.csv", file_type="csv")
    print(df)
    ## 2. remove all unnamed columns
    cleanup_df = pd_ext.clean_unnamed_columns(df)
    print(cleanup_df)
    ## 3. convert to standard format
