from primary.collectors.loc_gov_bonds.models import BondData

from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal


class Bond(SQLModel, table=True):
    __tablename__ = "bonds"

    id: Optional[int] = Field(default=None, primary_key=True)

    file_name: str = Field(
        index=True,
        alias="文件名"
    )

    admin_region_code: str = Field(
        index=True,
        alias="行政区划代码"
    )

    year: int = Field(
        index=True,
        alias="年份"
    )

    region_name: str = Field(
        index=True,
        alias="地区名称"
    )

    bond_name: str = Field(
        index=True,
        alias="债券名称"
    )

    bond_code: str = Field(
        unique=True,
        index=True,
        alias="债券代码"
    )

    bond_short_name: str = Field(
        alias="债券简称"
    )

    bond_period: str = Field(
        alias="债券期限"
    )

    issue_amount: Decimal = Field(
        decimal_places=2,
        alias="发行金额"
    )

    new_bond_amount: Decimal = Field(
        decimal_places=2,
        alias="新增债券金额"
    )

    replacement_bond_amount: Decimal = Field(
        decimal_places=2,
        alias="置换债券金额"
    )

    refinancing_bond_amount: Decimal = Field(
        decimal_places=2,
        alias="再融资债券金额"
    )

    value_date: date = Field(
        alias="起息日期"
    )

    bond_type: str = Field(
        alias="债券类型"
    )

    interest_rate: Decimal = Field(
        decimal_places=4,
        alias="利率"
    )

    issue_date: date = Field(
        alias="发行日期"
    )

    interest_payment_method: str = Field(
        alias="付息方式"
    )

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True  # Allows using both alias and field names
        json_encoders = {
            Decimal: str  # Handle Decimal serialization
        }


class LocGovBond(SQLModel, BondData, table=True):
    __tablename__ = 'loc_gov_bonds'
    id: Optional[int] = Field(default=None, primary_key=True)
    # 地区代码（可能是更广义的编码，具体含义需根据业务场景确定）
    AD_CODE_GK: str = Field(None, alias='地区码_GK')
    # 设置年份（可能是与债券相关设置的年份，具体业务相关）
    SET_YEAR_GK: str = Field(None, alias='债券设定年份_GK')
    # 付息频次（广义，具体含义可能与债券付息频率相关业务场景有关，这里为空值可能表示未设置或暂无相关信息）
    FXPC_GK: str = Field(None, alias='付息频次_GK')
    # 债券批次代码（可能用于区分不同批次的债券，具体含义由业务规则定义）
    ZQ_PC_CODE: str = Field(None, alias='债券批次代码')
    # 付息频次名称（对应具体的付息频率名称，如“半年一次”等，这里为空可能表示未明确或暂无对应名称）
    FXPC_NAME: str = Field(None, alias='付息频次名称')
    # 地区代码（可能用于明确债券所属地区，比如省份代码等）
    AD_CODE: str = Field(None, alias='地区码')
    # 地区名称（与AD_CODE对应，明确债券所属地区的具体名称，如这里是“安徽省”）
    AD_NAME: str = Field(None, alias='地区名称')
    # 设置年份（可能涉及债券发行、相关设置等的年份）
    SET_YEAR: str = Field(None, alias='债券设定年份')
    # 债券名称（完整呈现债券的名称，包含年份、地区、债券类型及期数等信息）
    ZQ_NAME: str = Field(None, alias='债券名称')
    # 债券代码（用于唯一标识某一只债券的编码）
    ZQ_CODE: str = Field(None, alias='债券代码')
    # 债券简称（对债券名称的一种简略称呼，方便日常使用和识别）
    ZQ_JC: Optional[str] = Field(None, alias='债券简称')
    # 债券期限ID（可能用于在系统或业务流程中唯一标识债券的期限类型，具体数字含义由业务定义）
    ZQQX_ID: Optional[str] = Field(None, alias='债券期限ID')
    # 债券期限名称（明确债券的期限时长描述，如“7年”）
    ZQQX_NAME: str = Field(None, alias='债券期限名称')
    # 发行金额（债券本次发行的金额数量）
    FX_AMT: float = Field(0, alias='发行金额')
    # 新增债券金额（可能是在特定业务场景下新增发行债券的金额，这里为0可能表示此次无新增债券情况）
    XZZQ_AMT: float = Field(0, alias='新增债券金额')
    # 置换债券金额（可能涉及债券置换业务场景下的金额，这里为0可能表示未发生相关置换或暂无对应金额）
    ZHZQ_AMT: float = Field(0, alias='置换债券金额')
    # 再融资专项债券金额（明确是再融资专项债券的金额数量）
    ZRZZQ_AMT: float = Field(0, alias='再融资专项债券金额')
    # 起息日期（债券开始计算利息的日期）
    QX_DATE: str = Field(None, alias='起息日期')
    # 债券类型ID（用于在系统或业务流程中唯一标识债券类型，具体数字含义由业务定义）
    ZQLX_ID: str = Field(None, alias='债券类型ID')
    # 债券类型名称（明确债券所属的类型名称，如“专项债券”）
    ZQLX_NAME: str = Field(None, alias='债券类型名称')
    # 利率（债券的票面利率等相关利率数值）
    LL: float = Field(None, alias='利率')
    # 债券付息时间（明确债券进行付息操作的具体时间）
    ZQ_FXTIME: str = Field(None, alias='债券发行时间')
    # 利息方式ID（可能用于在系统或业务流程中唯一标识利息支付方式，具体数字含义由业务定义）
    LXFS_ID: str = Field(None, alias='利息方式ID')
    # 付息方式（明确债券利息的支付方式，如“1年一次”）
    FXFS: str = Field(None, alias='付息方式')
    # 剩余期限结构（可能是关于债券剩余期限的一种结构化描述，这里“7+0+0”具体含义需结合业务场景解读，可能表示剩余期限分段情况等）
    SHMS: str = Field(None, alias='剩余期限结构')
    DETAIL_URL: str = Field(None, alias='URL地址')
    download_url: str = Field(None, alias='披露下载地址')


class BondProjectDetail(SQLModel, table=True):
    __tablename__ = 'bond_projects'
    id: Optional[int] = Field(default=None, primary_key=True)
    bond_code: str = Field(alias="债券代码", description="债券代码", nullable=True)
    file_announcement_date: str = Field(alias="文件公告日期", description="文件公告日期", nullable=True)
    bond_batch: Optional[str] = Field(default=None, alias="债券批次（可以为空）", description="债券批次（可以为空）",
                                      nullable=True)
    bond_period: str = Field(alias="债券期数", description="债券期数", nullable=True)
    total_amount: str = Field(alias="债券总金额（亿元）", description="债券总金额（亿元）", nullable=True)
    region: str = Field(alias="所属地区（市区县）", description="所属地区（市区县）", nullable=True)
    project_name: str = Field(alias="项目名称", description="项目名称", nullable=True)
    amount: str = Field(alias="金额（万元）", description="金额（万元）", nullable=True)
    bond_years: int = Field(alias="债券年份", description="债券年份", nullable=True)



