import os
from pathlib import Path
from qpydao import databases, db, init_database

from primary import pd_ext, cleanup
from primary.cleanup import csv_ext, first_cell_empty_handler
from primary.collectors.loc_gov_bonds import download_bonds
from primary.collectors.loc_gov_bonds.enitity import BondProjectDetail
from .contants import *

filter_year = None
filter_province = None
col_filters = {}
filtered_file_name = None
cleanup_filtered_file_name = None
source_file_path = None
download_dir = None
for_cleanup_file = None
cleanuped_file = None


def set_parameters(year: str, province: str):
    global filter_year, filter_province, col_filters, filtered_file_name, cleanup_filtered_file_name, source_file_path, download_dir, for_cleanup_file, cleanuped_file
    filter_year = year
    filter_province = province
    col_filters = {"年份": filter_year, "地区名称": filter_province}
    filtered_file_name = str(filter_year) + "-" + filter_province + ".csv"
    cleanup_filtered_file_name = "cleanup-" + str(filter_year) + "-" + filter_province + ".csv"
    source_file_path = Path(REWORKSPACE) / filtered_file_name
    download_dir = Path(REWORKSPACE) / filter_province / filter_year / "项目清单"
    # download_dir = Path(REWORKSPACE) / filter_province / filter_year
    for_cleanup_file = Path(REWORKSPACE) / filter_province / filtered_file_name
    cleanuped_file = Path(REWORKSPACE) / filter_province / cleanup_filtered_file_name


def test_refresh_parameters():
    set_parameters("2021", "广东省")
    print(cleanuped_file)


def test_download_all_bonds():
    for year in range(2024, 2014, -1):
        # provinces = get_province_list(["广东省", "黑龙江省","山东省","福建省","辽宁省","云南省","吉林省","四川省/2020"，'内蒙古自治区'])
        # DONE_PROVINCE = [""]
        ## '西藏自治区','海南省','青海省','宁夏回族自治区','江苏省','陕西省',
        # DONE provinces = ["吉林省","云南省","四川省","内蒙古自治区"]
        # provinces = ["宁夏回族自治区","安徽省","山东省","山西省"]
        # provinces = ["广西壮族自治区", "江苏省", "江西省", "河北省"]
        # -----------------------------------------------------
        # provinces = ["河南省", "浙江省", "海南省", "湖北省"]
        # provinces = ["湖南省", "甘肃省", "福建省", "西藏自治区"]
        # provinces = ["贵州省", "辽宁省", "陕西省", "青海省"]
        provinces = ["陕西省", "安徽省"]
        ## 河南省/山东省/福建省
        for province in provinces:
            set_parameters(str(year), province)
            pd_ext.filter_table_file(Path(REWORKSPACE + "/overall.csv"), col_filters,
                                     REWORKSPACE + "/" + filtered_file_name)
            os.makedirs(download_dir, exist_ok=True)
            download_bonds(source_file_path, download_dir)


def test_unzip_all_files():
    """
    Extract all zip files in the directory
    """

    set_parameters("2022", "辽宁省")
    target_dir = download_dir
    flat_extract_dir = target_dir / "all_files"  # Directory for flat extraction

    # First, extract each zip to its own directory (hierarchical)
    print("\nExtracting files hierarchically (each zip to its own directory):")
    for zip_file in target_dir.glob("*.zip"):
        cleanup.zip_ext.extract_zip_with_encoding(zip_file)

    # Then, extract all files to a single directory (flat)
    print("\nExtracting all files to a single directory:")
    flat_extract_dir.mkdir(exist_ok=True)
    for zip_file in target_dir.glob("*.zip"):
        cleanup.zip_ext.extract_zip_with_encoding(
            zip_file,
            extract_path=flat_extract_dir,
            flat_extract=True
        )


FIELD_MAPPINGS = {
    '债券期数': "债券名称",
    '所属地区（市区县）': "地区", '项目名称': "项目名称", '金额（万元）': "金额"
}


def fileter_first_cell_name(row):
    return row[0] == "其中：用作资本金" or row[0] == "合计"


def test_import_project_detail_data():
    """
    1. manual check and collect first raw data
    2. cleanup data for csv project
    :return:
    """
    set_parameters("2015", "宁夏回族自治区")
    cleanup_source_file_path = cleanuped_file
    cleaned_df = pd_ext.read_to_df(cleanup_source_file_path)

    models = pd_ext.read_to_models_by_field_mapping(cleaned_df, model_class=BondProjectDetail
                                                    , field_mappings=FIELD_MAPPINGS)
    for model in models:
        try:
            value = csv_ext.replace_dots_except_last(model.amount)
            # if float(value)>1000:
            model.amount = float(value) / 10000
        except Exception as e:
            model.amount = model.amount
        db.save(model)


def test_cleanup_import():
    set_parameters("2010", "安徽省")
    source_file_path = for_cleanup_file
    cleanup_source_file_path = cleanuped_file
    cleanup.clean_csv_rows(source_file_path, cleanup_source_file_path,
                           row_handlers=[first_cell_empty_handler, fileter_first_cell_name])
    cleaned_df = pd_ext.read_to_df(cleanup_source_file_path,
                                   # use_cols=range(5)
                                   )
    models = pd_ext.read_to_models_by_field_mapping(cleaned_df, model_class=BondProjectDetail
                                                    , field_mappings=FIELD_MAPPINGS)
    for model in models:
        try:
            value = csv_ext.replace_dots_except_last(model.amount)
            # if float(value)>100:
            model.amount = float(value) / 10000
        except Exception as e:
            model.amount = model.amount
        # model.amount = '未披露'
        if model.bond_period != '债券名称' or model.bond_period != '债券品种' or len(model.region)==0:
            db.save(model)
