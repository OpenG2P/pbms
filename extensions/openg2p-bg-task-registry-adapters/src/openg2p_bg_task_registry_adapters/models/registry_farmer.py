from openg2p_pbms_models.models import G2PRegistry
from sqlalchemy import JSON, Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class G2PFarmerRegistry(G2PRegistry):
    __tablename__ = "g2p_register_farmer"

    # G2PRegister identity fields
    functional_record_id: Mapped[str] = mapped_column(String, nullable=True)
    link_internal_record_id: Mapped[str] = mapped_column(String, nullable=True)
    link_foundational_id: Mapped[str] = mapped_column(String, nullable=True)
    record_name: Mapped[str] = mapped_column(String, nullable=True)
    record_status: Mapped[str] = mapped_column(String, nullable=True)
    record_status_reason: Mapped[str] = mapped_column(String, nullable=True)

    # Person
    foundational_id: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    middle_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    given_name: Mapped[str] = mapped_column(String, nullable=True)
    prefix: Mapped[str] = mapped_column(String, nullable=True)
    suffix: Mapped[str] = mapped_column(String, nullable=True)
    gender: Mapped[str] = mapped_column(String, nullable=True)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=True)
    phone_numbers: Mapped[list] = mapped_column(JSON, nullable=True)
    emails: Mapped[list] = mapped_column(JSON, nullable=True)
    marital_status: Mapped[str] = mapped_column(String, nullable=True)
    occupation: Mapped[str] = mapped_column(String, nullable=True)
    income_level: Mapped[str] = mapped_column(String, nullable=True)
    language_code: Mapped[str] = mapped_column(String, nullable=True)
    registration_date: Mapped[Date] = mapped_column(Date, nullable=True)

    # Geo
    latitude: Mapped[str] = mapped_column(String, nullable=True)
    longitude: Mapped[str] = mapped_column(String, nullable=True)
    altitude: Mapped[str] = mapped_column(String, nullable=True)
    plus_code: Mapped[str] = mapped_column(String, nullable=True)
    address_line_1: Mapped[str] = mapped_column(String, nullable=True)
    address_line_2: Mapped[str] = mapped_column(String, nullable=True)
    postal_code: Mapped[str] = mapped_column(String, nullable=True)
    country_code: Mapped[str] = mapped_column(String, nullable=True)
    geo_lowest_level_value_id: Mapped[str] = mapped_column(String, nullable=True)
    geo_code_hierarchy_json: Mapped[dict] = mapped_column(JSON, nullable=True)

    # Farmer-specific
    estimated_age: Mapped[int] = mapped_column(Integer, nullable=True)
    has_personal_phone: Mapped[bool] = mapped_column(Boolean, nullable=True)
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=True)
    disability_type: Mapped[str] = mapped_column(String, nullable=True)
    disability_severity: Mapped[str] = mapped_column(String, nullable=True)
    source_of_income: Mapped[str] = mapped_column(String, nullable=True)
    source_of_income_other: Mapped[str] = mapped_column(String, nullable=True)
    language_spoken: Mapped[str] = mapped_column(String, nullable=True)
    education_level: Mapped[str] = mapped_column(String, nullable=True)
    national_id_masked: Mapped[str] = mapped_column(String, nullable=True)
