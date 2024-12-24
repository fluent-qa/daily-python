from pathlib import Path

import loguru
from qpyconf import settings
from qpydao import db

from loc_gov_bonds.contants import REWORKSPACE
from loc_gov_bonds.test_standard_process import col_filters, filtered_file_name
from primary import pd_ext
from primary.collectors.loc_gov_bonds.enitity import LocGovBond
from primary.collectors.loc_gov_bonds.models import BondData

WORKING_DIR = settings.workspace


def test_read_to_models():
    result = pd_ext.read_to_models(Path(WORKING_DIR + "/total-bond.xlsx"), BondData, "xlsx")
    print(result)


def test_save_models_to_db():
    result = pd_ext.read_to_models(Path(WORKING_DIR + "/total-bond.xlsx"), BondData, "xlsx")
    for item in result:
        l = LocGovBond(**item.model_dump())
        db.save(l)


def test_split_bonds_info():
    """
    1. getting data for a given year and province
    :return:
    """
    pd_ext.filter_table_file(Path(REWORKSPACE + "/overall.csv"), col_filters, REWORKSPACE + "/" + filtered_file_name)
