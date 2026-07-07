from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class G2PRegistryPayload(BaseModel):
    internal_record_id: str
