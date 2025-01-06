from pydantic import BaseModel, Field
from typing import Optional


class PlantData(BaseModel):
    chinese_name: Optional[str] = Field(default=None, alias="中文名")
    latin_name: Optional[str] = Field(default=None, alias="拉丁名")
    collector: Optional[str] = Field(default=None, alias="采集人")
    collection_number: Optional[str] = Field(default=None, alias="采集号")
    collection_date: Optional[str] = Field(default=None, alias="采集时间")
    collection_location: Optional[str] = Field(default=None, alias="采集地")
    elevation: Optional[str] = Field(default=None, alias="海拔")
    habitat: Optional[str] = Field(default=None, alias="生境")
    occurrence_remarks: Optional[str] = Field(default=None, alias="习性")
    reproductive_condition: Optional[str] = Field(default=None, alias="物候期")
    image_url: Optional[str] = Field(default=None, alias="图片链接")
    local_image_path: Optional[str] = Field(default=None, alias="本地图片链接")

    class Config:
        populate_by_name = True
