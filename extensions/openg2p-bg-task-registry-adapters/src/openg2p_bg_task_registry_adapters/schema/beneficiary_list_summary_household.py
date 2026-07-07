from typing import Optional

from pydantic import BaseModel

from .beneficiary_list_summary import BeneficiaryListSummaryPayload


class BeneficiaryListSummaryHousehold(BaseModel):
    size_children_u5_mean: Optional[str] = None
    size_children_u5_q1: Optional[str] = None
    size_children_u5_q2: Optional[str] = None
    size_children_u5_q3: Optional[str] = None

    size_elderly_mean: Optional[str] = None
    size_elderly_q1: Optional[str] = None
    size_elderly_q2: Optional[str] = None
    size_elderly_q3: Optional[str] = None

    rooms_count_mean: Optional[str] = None
    rooms_count_q1: Optional[str] = None
    rooms_count_q2: Optional[str] = None
    rooms_count_q3: Optional[str] = None

    overcrowding_indicator_mean: Optional[str] = None
    overcrowding_indicator_q1: Optional[str] = None
    overcrowding_indicator_q2: Optional[str] = None
    overcrowding_indicator_q3: Optional[str] = None

    entitlement_amount_q1: Optional[dict] = None
    entitlement_amount_q2: Optional[dict] = None
    entitlement_amount_q3: Optional[dict] = None


class BeneficiaryListSummaryHouseholdPayload(BeneficiaryListSummaryPayload):
    registry_summary: BeneficiaryListSummaryHousehold
