from openg2p_bg_task_models.models import BeneficiaryListSummary
from sqlalchemy import JSON, Float, String
from sqlalchemy.orm import mapped_column


class BeneficiaryListSummaryHousehold(BeneficiaryListSummary):
    __tablename__ = "beneficiary_list_summary_household"

    size_children_u5_q1 = mapped_column(Float, nullable=True, default=0)
    size_children_u5_q2 = mapped_column(Float, nullable=True, default=0)
    size_children_u5_q3 = mapped_column(Float, nullable=True, default=0)
    size_children_u5_mean = mapped_column(Float, nullable=True, default=0)
    size_children_u5_units = mapped_column(String, nullable=False, default="persons")

    size_elderly_q1 = mapped_column(Float, nullable=True, default=0)
    size_elderly_q2 = mapped_column(Float, nullable=True, default=0)
    size_elderly_q3 = mapped_column(Float, nullable=True, default=0)
    size_elderly_mean = mapped_column(Float, nullable=True, default=0)
    size_elderly_units = mapped_column(String, nullable=False, default="persons")

    rooms_count_q1 = mapped_column(Float, nullable=True, default=0)
    rooms_count_q2 = mapped_column(Float, nullable=True, default=0)
    rooms_count_q3 = mapped_column(Float, nullable=True, default=0)
    rooms_count_mean = mapped_column(Float, nullable=True, default=0)
    rooms_count_units = mapped_column(String, nullable=False, default="rooms")

    overcrowding_indicator_q1 = mapped_column(Float, nullable=True, default=0)
    overcrowding_indicator_q2 = mapped_column(Float, nullable=True, default=0)
    overcrowding_indicator_q3 = mapped_column(Float, nullable=True, default=0)
    overcrowding_indicator_mean = mapped_column(Float, nullable=True, default=0)
    overcrowding_indicator_units = mapped_column(String, nullable=False, default="ratio")

    entitlement_amount_q1 = mapped_column(JSON, nullable=True)
    entitlement_amount_q2 = mapped_column(JSON, nullable=True)
    entitlement_amount_q3 = mapped_column(JSON, nullable=True)
    entitlement_units = mapped_column(JSON, nullable=True)
