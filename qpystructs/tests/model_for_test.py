from typing import Any, Annotated

from qpystructs.models import GenericDataModel
from pydantic import Field


#
# {
#   "key": "v1",
#   "kList": [
#     "test",
#     "t2"
#   ],
#   "kObj": {
#     "k1": "v1",
#     "k2": "v2"
#   },
#   "kBool": true,
#   "kNum": 4.3
# }

class DemoModel(GenericDataModel):
    key: str
    k_list: []
    k_obj: Any
    k_bool: bool
    k_num: float


class DemoModelAlias(GenericDataModel):
    key: str
    k_list: []
    k_obj: Any
    k_bool: bool
    # k_index: float = Field(alias='k_num')
    k_index: Annotated[float, Field(alias='kNum')]
