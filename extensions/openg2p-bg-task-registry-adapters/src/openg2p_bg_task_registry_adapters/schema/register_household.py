from typing import Optional

from .registry import G2PRegistryPayload


class G2PRegisterHouseholdPayload(G2PRegistryPayload):
    functional_record_id: Optional[str] = None
    household_head_name: Optional[str] = None
    headship_type: Optional[str] = None
    size_total: Optional[int] = None
    size_children_u5: Optional[int] = None
    size_elderly: Optional[int] = None
    number_of_female_members: Optional[int] = None
    number_of_male_members: Optional[int] = None
    dwelling_type: Optional[str] = None
    tenure_status: Optional[str] = None
    rooms_count: Optional[int] = None
    overcrowding_indicator: Optional[float] = None
    water_source_type: Optional[str] = None
    sanitation_type: Optional[str] = None
    lighting_source: Optional[str] = None
    cooking_fuel_type: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    postal_code: Optional[str] = None
    country_code: Optional[str] = None
