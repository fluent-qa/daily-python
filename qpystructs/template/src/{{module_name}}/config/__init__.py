import os

from dynaconf import Dynaconf
from pydantic import BaseModel

settings = Dynaconf(
    settings_file=[
        "configs/settings.toml",
        "configs/.secrets.toml",
        "settings.toml",
        ".secrets.toml",
    ],
    environment=True,
    load_dotenv=True,
    envvar_prefix=False,
    includes=["../config/custom_settings.toml"],
)

settings.validators.validate()


def ensure_env_settings(conf: Dynaconf, env_name: str):
    env_switcher_key = conf.ENV_SWITCHER_FOR_DYNACONF
    os.environ[env_switcher_key] = env_name
    conf.reload()


def setting_to_model(setting: Dynaconf, model_type: type[BaseModel]):
    model_value = model_type()
    for model_field in model_type.model_fields:
        setattr(model_value, model_field, getattr(setting, model_field))
    return model_value
