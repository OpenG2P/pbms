import logging
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from fastapi_cache.decorator import cache
from openg2p_bg_task_models.models import BeneficiaryListDetails

_logger = logging.getLogger("app")
from openg2p_bg_task_models.schemas import (
    BeneficiarySearchResponsePayload,
    RegistrantDetails,
)
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from ..cache import beneficiary_count_key_builder
from ..interface import RegistryInterface
from ..models import (
    BeneficiaryListSummaryHousehold as BeneficiaryListSummaryHouseholdModel,
)
from ..models import G2PRegisterHousehold
from ..schema import (
    BeneficiaryListSummary,
    BeneficiaryListSummaryHousehold,
    BeneficiaryListSummaryHouseholdPayload,
    G2PRegisterHouseholdPayload,
)


class RegisterHousehold(RegistryInterface):
    """Fetches household data and computes summary statistics"""

    # ===================
    # Summary API Methods
    # ===================
    async def get_summary(
        self,
        beneficiary_list_id: str,
        bg_task_session: AsyncSession,
        formated: bool = False,
    ) -> BeneficiaryListSummaryHouseholdPayload:
        result = await bg_task_session.execute(
            select(BeneficiaryListSummaryHouseholdModel).where(
                BeneficiaryListSummaryHouseholdModel.beneficiary_list_id
                == beneficiary_list_id
            )
        )
        summary_row = result.scalars().first()
        return self._build_summary_payload(summary_row)

    def get_summary_sync(
        self, beneficiary_list_id: str, bg_task_session: Session
    ) -> BeneficiaryListSummaryHouseholdPayload:
        summary_row = (
            bg_task_session.query(BeneficiaryListSummaryHouseholdModel)
            .filter_by(beneficiary_list_id=beneficiary_list_id)
            .first()
        )
        return self._build_summary_payload(summary_row)

    def _build_summary_payload(
        self, row
    ) -> BeneficiaryListSummaryHouseholdPayload:
        def fmt(value, units):
            return f"{value} {units}" if value is not None else None

        return BeneficiaryListSummaryHouseholdPayload(
            beneficiary_list_summary=BeneficiaryListSummary(
                id=row.id,
                program_id=row.program_id,
                program_mnemonic=row.program_mnemonic,
                target_registry=row.target_registry,
                beneficiary_list_id=row.beneficiary_list_id,
                number_of_registrants=row.number_of_registrants,
                date_created=row.date_created,
                total_disbursement_quantity=row.total_disbursement_quantity,
                average_entitlement_per_registrant=row.average_entitlement_per_person,
            ),
            registry_summary=BeneficiaryListSummaryHousehold(
                size_children_u5_mean=fmt(row.size_children_u5_mean, row.size_children_u5_units),
                size_children_u5_q1=fmt(row.size_children_u5_q1, row.size_children_u5_units),
                size_children_u5_q2=fmt(row.size_children_u5_q2, row.size_children_u5_units),
                size_children_u5_q3=fmt(row.size_children_u5_q3, row.size_children_u5_units),
                size_elderly_mean=fmt(row.size_elderly_mean, row.size_elderly_units),
                size_elderly_q1=fmt(row.size_elderly_q1, row.size_elderly_units),
                size_elderly_q2=fmt(row.size_elderly_q2, row.size_elderly_units),
                size_elderly_q3=fmt(row.size_elderly_q3, row.size_elderly_units),
                rooms_count_mean=fmt(row.rooms_count_mean, row.rooms_count_units),
                rooms_count_q1=fmt(row.rooms_count_q1, row.rooms_count_units),
                rooms_count_q2=fmt(row.rooms_count_q2, row.rooms_count_units),
                rooms_count_q3=fmt(row.rooms_count_q3, row.rooms_count_units),
                overcrowding_indicator_mean=fmt(
                    row.overcrowding_indicator_mean, row.overcrowding_indicator_units
                ),
                overcrowding_indicator_q1=fmt(
                    row.overcrowding_indicator_q1, row.overcrowding_indicator_units
                ),
                overcrowding_indicator_q2=fmt(
                    row.overcrowding_indicator_q2, row.overcrowding_indicator_units
                ),
                overcrowding_indicator_q3=fmt(
                    row.overcrowding_indicator_q3, row.overcrowding_indicator_units
                ),
                entitlement_amount_q1=row.entitlement_amount_q1,
                entitlement_amount_q2=row.entitlement_amount_q2,
                entitlement_amount_q3=row.entitlement_amount_q3,
            ),
        )

    # ==============================
    # Beneficiary Search API Methods
    # ==============================
    async def search_beneficiaries(
        self,
        bg_task_session: AsyncSession,
        sr_session: AsyncSession,
        beneficiary_list_id: str,
        target_registry: str,
        search_query,
        page: int = 1,
        page_size: int = 10,
        order_by: str = "internal_record_id asc",
    ) -> Tuple[BeneficiarySearchResponsePayload, int]:
        registrant_details_result = await bg_task_session.execute(
            select(BeneficiaryListDetails.registrant_details).where(
                BeneficiaryListDetails.beneficiary_list_id == beneficiary_list_id
            )
        )
        registrant_details = registrant_details_result.scalars().all()
        _logger.info("search_beneficiaries: beneficiary_list_id=%r registrant_details row_count=%d", beneficiary_list_id, len(registrant_details))
        registrant_ids = []
        for registrant_detail in registrant_details:
            for registrant in registrant_detail:
                registrant_ids.append(registrant["registrant_id"])

        _logger.info("search_beneficiaries: registrant_ids count=%d ids=%r", len(registrant_ids), registrant_ids)
        _logger.info("search_beneficiaries: search_query=%r order_by=%r page=%r page_size=%r", search_query, order_by, page, page_size)

        (
            household_search_query,
            household_search_params,
        ) = self.construct_beneficiary_search_sql_query(
            registrant_ids,
            target_registry,
            search_query,
            order_by,
            page_size,
            page,
        )
        _logger.info("search_beneficiaries: sql=%r params=%r", str(household_search_query), household_search_params)

        household_search_results = (
            (await sr_session.execute(household_search_query, household_search_params))
            .mappings()
            .all()
        )
        _logger.info("search_beneficiaries: result_count=%d", len(household_search_results))

        total_beneficiary_count: int = await self._get_total_beneficiary_count(
            sr_session, beneficiary_list_id, registrant_ids, search_query
        )
        _logger.info("search_beneficiaries: total_beneficiary_count=%d", total_beneficiary_count)

        beneficiaries = []
        if household_search_results:
            beneficiaries = [
                G2PRegisterHouseholdPayload(
                    internal_record_id=row["internal_record_id"],
                    functional_record_id=row["functional_record_id"],
                    household_head_name=row["household_head_name"],
                    headship_type=row["headship_type"],
                    size_total=row["size_total"],
                    size_children_u5=row["size_children_u5"],
                    size_elderly=row["size_elderly"],
                    number_of_female_members=row["number_of_female_members"],
                    number_of_male_members=row["number_of_male_members"],
                    dwelling_type=row["dwelling_type"],
                    tenure_status=row["tenure_status"],
                    rooms_count=row["rooms_count"],
                    overcrowding_indicator=float(row["overcrowding_indicator"])
                    if row["overcrowding_indicator"] is not None
                    else None,
                    water_source_type=row["water_source_type"],
                    sanitation_type=row["sanitation_type"],
                    lighting_source=row["lighting_source"],
                    cooking_fuel_type=row["cooking_fuel_type"],
                    address_line_1=row["address_line_1"],
                    address_line_2=row["address_line_2"],
                    postal_code=row["postal_code"],
                    country_code=row["country_code"],
                )
                for row in household_search_results
            ]

        response_payload = BeneficiarySearchResponsePayload(
            beneficiary_count=len(beneficiaries),
            beneficiaries=beneficiaries,
        )

        return response_payload, total_beneficiary_count

    @cache(expire=120, key_builder=beneficiary_count_key_builder)
    async def _get_total_beneficiary_count(
        self,
        sr_session: AsyncSession,
        beneficiary_list_id: str,
        registrant_ids: List[str],
        search_query: Optional[str] = None,
    ) -> int:
        _logger.info("_get_total_beneficiary_count: registrant_ids count=%d search_query=%r", len(registrant_ids), search_query)
        (
            beneficiary_count_query,
            beneficiary_count_params,
        ) = self.construct_beneficiary_search_count_sql_query(
            registrant_ids, "households", search_query
        )
        _logger.info("_get_total_beneficiary_count: count_sql=%r params=%r", str(beneficiary_count_query), beneficiary_count_params)
        total_beneficiary_count = (
            await sr_session.execute(beneficiary_count_query, beneficiary_count_params)
        ).scalar_one()
        _logger.info("_get_total_beneficiary_count: result=%d", total_beneficiary_count)
        return total_beneficiary_count

    # =================================
    # Eligibility Celery Worker Methods
    # =================================
    def compute_eligibility_statistics(
        self,
        beneficiary_list_details: List[BeneficiaryListDetails],
        base_summary,
        sr_session: Session,
        bg_task_session: Session,
    ):
        household_summary = BeneficiaryListSummaryHouseholdModel(
            program_id=base_summary.program_id,
            program_mnemonic=base_summary.program_mnemonic,
            target_registry=base_summary.target_registry,
            beneficiary_list_id=base_summary.beneficiary_list_id,
            number_of_registrants=base_summary.number_of_registrants,
            date_created=base_summary.date_created,
        )

        size_children_u5: List[int] = []
        size_elderly: List[int] = []
        rooms_count: List[int] = []
        overcrowding_indicator: List[float] = []

        for beneficiary_list_detail in beneficiary_list_details:
            registrant_ids = []
            for registrant_detail in beneficiary_list_detail.registrant_details:
                registrant_detail = RegistrantDetails(**registrant_detail)
                registrant_ids.append(registrant_detail.registrant_id)

            registrants = self.get_registrants_by_ids(registrant_ids, sr_session)
            for household in registrants:
                if household.size_children_u5 is not None:
                    size_children_u5.append(household.size_children_u5)
                if household.size_elderly is not None:
                    size_elderly.append(household.size_elderly)
                if household.rooms_count is not None:
                    rooms_count.append(household.rooms_count)
                if household.overcrowding_indicator is not None:
                    overcrowding_indicator.append(float(household.overcrowding_indicator))

        self._apply_quartiles(household_summary, "size_children_u5", size_children_u5)
        self._apply_quartiles(household_summary, "size_elderly", size_elderly)
        self._apply_quartiles(household_summary, "rooms_count", rooms_count)
        self._apply_quartiles(
            household_summary, "overcrowding_indicator", overcrowding_indicator
        )

        bg_task_session.add(household_summary)

    @staticmethod
    def _apply_quartiles(summary_obj, prefix: str, values: List[float]) -> None:
        if not values:
            return
        arr = np.array(values)
        setattr(summary_obj, f"{prefix}_mean", round(float(np.mean(arr)), 2))
        setattr(
            summary_obj,
            f"{prefix}_q1",
            round(float(np.percentile(arr, 25, method="midpoint")), 2),
        )
        setattr(
            summary_obj,
            f"{prefix}_q2",
            round(float(np.percentile(arr, 50, method="midpoint")), 2),
        )
        setattr(
            summary_obj,
            f"{prefix}_q3",
            round(float(np.percentile(arr, 75, method="midpoint")), 2),
        )

    def get_registrants_by_ids(
        self, registrant_ids, sr_session
    ) -> List[G2PRegisterHousehold]:
        households = sr_session.query(G2PRegisterHousehold).filter(
            G2PRegisterHousehold.internal_record_id.in_(registrant_ids)
        )
        return list(households.yield_per(500))

    # =================================
    # Entitlement Celery Worker Methods
    # =================================
    def get_is_registant_entitled(
        self, registrant_id: str, sql_query: str, sr_session: Session
    ) -> bool:
        sql_query_with_registrant_id = (
            self.construct_get_is_registrant_entitled_sql_query(
                registrant_id, "households", sql_query
            )
        )
        result = sr_session.execute(sql_query_with_registrant_id).fetchone()
        return result is not None

    def get_entitlement_multiplier(
        self, multiplier: str, registrant_id: str, sr_session: Session
    ) -> int:
        if not multiplier or multiplier == "none":
            return 1

        sql_query = self.construct_multiplier_sql_query(
            multiplier, target_registry="households"
        )
        params = {"registrant_id": registrant_id}
        result = sr_session.execute(sql_query, params).fetchone()
        multiplier_value: int = (
            int(result[0]) if result and result[0] is not None else 1
        )
        return multiplier_value

    def compute_entitlement_statistics(
        self, beneficiary_list_id: str, bg_task_session: Session, sr_session: Session
    ):
        beneficiary_list_details = (
            bg_task_session.query(BeneficiaryListDetails)
            .filter_by(beneficiary_list_id=beneficiary_list_id)
            .all()
        )

        entitlements: Dict[Any, List[float]] = {}

        for beneficiary_list_detail in beneficiary_list_details:
            for registrant_detail in beneficiary_list_detail.registrant_details:
                registrant_detail = RegistrantDetails(**registrant_detail)
                for benefit_code_id, value in registrant_detail.entitlement.items():
                    entitlements.setdefault(benefit_code_id, []).append(value)

        entitlement_stats = self.compute_stats_dict(entitlements)

        bg_task_session.execute(
            update(BeneficiaryListSummaryHouseholdModel)
            .where(
                BeneficiaryListSummaryHouseholdModel.beneficiary_list_id
                == beneficiary_list_id
            )
            .values(
                total_disbursement_quantity=dict(entitlement_stats["total"]),
                average_entitlement_per_person=dict(entitlement_stats["average"]),
                entitlement_amount_q1=dict(entitlement_stats["q1"]),
                entitlement_amount_q2=dict(entitlement_stats["q2"]),
                entitlement_amount_q3=dict(entitlement_stats["q3"]),
            )
        )

    def compute_stats_dict(
        self, entitlements_dict: Dict[Any, List[float]]
    ) -> Dict[str, Dict[Any, float]]:
        stats: Dict[str, Dict[Any, float]] = {
            "average": {},
            "q1": {},
            "q2": {},
            "q3": {},
            "total": {},
        }
        for benefit_code_id, values in entitlements_dict.items():
            if not values:
                stats["average"][benefit_code_id] = 0.0
                stats["q1"][benefit_code_id] = 0.0
                stats["q2"][benefit_code_id] = 0.0
                stats["q3"][benefit_code_id] = 0.0
                stats["total"][benefit_code_id] = 0.0
            else:
                arr = np.array(values)
                stats["average"][benefit_code_id] = round(float(np.mean(arr)), 2)
                stats["q1"][benefit_code_id] = round(
                    float(np.percentile(arr, 25, method="midpoint")), 2
                )
                stats["q2"][benefit_code_id] = round(
                    float(np.percentile(arr, 50, method="midpoint")), 2
                )
                stats["q3"][benefit_code_id] = round(
                    float(np.percentile(arr, 75, method="midpoint")), 2
                )
                stats["total"][benefit_code_id] = float(np.sum(arr))
        return stats
