from pathlib import Path

from psycopg import IntegrityError
from qpydao import databases, db, init_database

from loc_gov_bonds.contants import REWORKSPACE
from primary import pd_ext
from primary.collectors.loc_gov_bonds.enitity import Bond


# ## why needed?


def test_init_db():
    """
    1. 初始化数据库
    :return:
    """
    print(db)
    dao = databases.get_db("default")
    init_database(db)
    print(dao)


def test_save_models_to_db():
    """
    1. import all data into database
    :return:
    """
    result = pd_ext.read_to_models(Path(REWORKSPACE + "/overall.csv"), Bond)
    print(result)
    for item in result:
        try:
            db.save(item)
        except IntegrityError as uv:
            print(uv)

