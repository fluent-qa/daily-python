
from qpydao import databases, db, init_database
# ## why needed?
from primary.collectors.loc_gov_bonds import enitity


def init_bond_app():
    init_database(db)

