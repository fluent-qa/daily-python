from pathlib import Path

from qpyconf import settings

REWORKSPACE = settings.REWORKSPACE

province_list = """
青海省
新疆维吾尔自治区
湖北省
深圳市
宁波市
山西省
云南省
河北省
广西壮族自治区
海南省
辽宁省
上海市
大连市
福建省
新疆生产建设兵团
陕西省
四川省
新疆兵团
贵州省
广东省
厦门市
青岛市
北京市
黑龙江省
江苏省
天津市
重庆市
山东省
内蒙古自治区
宁夏回族自治区
浙江省
西藏自治区
吉林省
安徽省
江西省
河南省
甘肃省
湖南省
"""



def get_province_list(filter_list: list = None):
    if filter_list is None:
        filter_list = []
    result = province_list.split("\n")
    result_new = [item for item in result if len(item) > 0 and item not in filter_list]
    return result_new
