from openg2p_fastapi_common.config import Settings as BaseSettings
from pydantic_settings import SettingsConfigDict

from . import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="staff_portal_api_", env_file=".env", extra="allow"
    )

    openapi_title: str = "OpenG2P PBMS Staff Portal API"
    openapi_description: str = """
        FastAPI Service for OpenG2P PBMS Staff Portal
        ***********************************
        Further details goes here
        ***********************************
        """
    openapi_version: str = __version__

    # Social Registry
    db_username_sr: str = "postgres"
    db_password_sr: str = "password"
    db_hostname_sr: str = "localhost"
    db_port_sr: int = 5432
    db_dbname_sr: str = "socialregistrydb"
