from typing import Optional

from .registry import G2PRegistryPayload


class G2PFarmerRegistryPayload(G2PRegistryPayload):
    functional_record_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    estimated_age: Optional[int] = None
    disabled: Optional[bool] = None
    source_of_income: Optional[str] = None
    education_level: Optional[str] = None
    country_code: Optional[str] = None
