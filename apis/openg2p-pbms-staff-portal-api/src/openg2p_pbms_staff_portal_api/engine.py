from sqlalchemy.ext.asyncio import create_async_engine

from .config import Settings

_config = Settings.get_config()


def get_engine():
    if _config.db_datasource:
        return {
            "db_engine_bg_task": create_async_engine(_config.db_datasource),
        }
