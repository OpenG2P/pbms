import logging
from datetime import datetime, timezone
from typing import List

from openg2p_bg_task_models.models import BeneficiaryListDetails
from openg2p_bg_task_models.schemas import RegistrantDetails
from openg2p_bg_task_registry_adapters.factory import RegistryFactory
from openg2p_bg_task_registry_adapters.interface import RegistryInterface
from openg2p_pbms_models.models import (
    G2PBeneficiaryList,
    G2PEntitlementRuleDefinition,
    G2PProgramBenefitCodes,
    G2PProgramDefinition,
    StatusEnum,
)
from sqlalchemy.orm import sessionmaker

from ..app import celery_app, get_engine
from ..config import Settings

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)
_engine = get_engine()


@celery_app.task(name="entitlement_worker")
def entitlement_worker(id: str):
    _logger.info("Starting entitlement request for beneficiary list details id: %s", id)
    bg_task_session_maker = sessionmaker(
        bind=_engine.get("db_engine_bg_task"), expire_on_commit=False
    )
    pbms_session_maker = sessionmaker(
        bind=_engine.get("db_engine_pbms"), expire_on_commit=False
    )

    with bg_task_session_maker() as bg_task_session, pbms_session_maker() as pbms_session:
        beneficiary_list_details = None
        try:
            beneficiary_list_details = (
                bg_task_session.query(BeneficiaryListDetails)
                .filter(BeneficiaryListDetails.id == id)
                .first()
            )
            beneficiary_list = (
                pbms_session.query(G2PBeneficiaryList)
                .filter(
                    G2PBeneficiaryList.beneficiary_list_id
                    == beneficiary_list_details.beneficiary_list_id
                )
                .first()
            )

            target_registry = (
                pbms_session.query(G2PProgramDefinition.target_registry)
                .filter(G2PProgramDefinition.id == beneficiary_list.program_id)
                .one_or_none()
            )
            target_registry = target_registry[0]

            entitlement_rule_definitions: List[G2PEntitlementRuleDefinition] = (
                pbms_session.query(G2PEntitlementRuleDefinition)
                .filter(
                    G2PEntitlementRuleDefinition.program_id
                    == beneficiary_list.program_id
                )
                .all()
            )

            registrant_details: List[RegistrantDetails] = [
                RegistrantDetails(**item)
                for item in beneficiary_list_details.registrant_details
            ]
            registrant_ids = [item.registrant_id for item in registrant_details]
            registry_interface: RegistryInterface = RegistryFactory.get_registry_class(
                target_registry
            )

            for entitlement_rule_definition in entitlement_rule_definitions:
                benefit_code_id = entitlement_rule_definition.benefit_code_id
                program_benefit_code_max_quantity = (
                    pbms_session.query(G2PProgramBenefitCodes.max_quantity)
                    .filter(
                        G2PProgramBenefitCodes.program_id == beneficiary_list.program_id,
                        G2PProgramBenefitCodes.benefit_code_id == benefit_code_id,
                    )
                    .first()
                )
                max_quantity: float = (
                    program_benefit_code_max_quantity[0]
                    if program_benefit_code_max_quantity
                    else 0
                )
                multipliers = registry_interface.entitlement_multipliers(
                    registrant_ids,
                    entitlement_rule_definition.pbms_domain,
                    entitlement_rule_definition.multiplier,
                )
                for registrant_detail in registrant_details:
                    if (
                        registrant_detail.entitlement is not None
                        and benefit_code_id in registrant_detail.entitlement
                        and registrant_detail.entitlement[benefit_code_id] == max_quantity
                    ):
                        continue
                    multiplier_value = multipliers.get(str(registrant_detail.registrant_id))
                    is_registrant_entitled = multiplier_value is not None
                    if not is_registrant_entitled:
                        multiplier_value = 0
                        calculated_entitlement = 0
                    else:
                        calculated_entitlement = round(
                            multiplier_value * entitlement_rule_definition.quantity,
                            entitlement_rule_definition.decimal_places,
                        )
                    update_registrant_detail_json(
                        registrant_detail,
                        benefit_code_id,
                        max_quantity,
                        calculated_entitlement,
                        entitlement_rule_definition.multiplier,
                        multiplier_value,
                        is_registrant_entitled,
                    )

            _logger.info(
                "Updating beneficiary list details with calculated entitlements"
            )
            beneficiary_list_details.registrant_details = [
                registrant_detail.model_dump(mode="json")
                for registrant_detail in registrant_details
            ]

            beneficiary_list_details.entitlement_number_of_attempts += 1
            beneficiary_list_details.entitlement_processed_date = datetime.now(
                timezone.utc
            )
            beneficiary_list_details.entitlement_process_status = (
                StatusEnum.complete.value
            )

            bg_task_session.commit()
            pbms_session.commit()

        except Exception as e:
            _logger.error(
                f"Error during processing entitlement request for beneficiary list id {id}: {str(e)}"
            )
            bg_task_session.rollback()
            pbms_session.rollback()

            beneficiary_list_details.entitlement_number_of_attempts += 1
            beneficiary_list_details.entitlement_processed_date = datetime.now(
                timezone.utc
            )
            beneficiary_list_details.entitlement_process_status = (
                StatusEnum.pending.value
                if beneficiary_list_details.entitlement_number_of_attempts
                < _config.worker_max_attempts
                else StatusEnum.failed.value
            )
            beneficiary_list_details.entitlement_latest_error_code = str(e)
            bg_task_session.commit()

        _logger.info(
            f"Completed processing entitlements for beneficiary list details id: {id}"
        )


def compute_entitlement_statistics(
    id, bg_task_session, beneficiary_list_details, target_registry
):
    try:
        registry_interface: RegistryInterface = RegistryFactory.get_registry_class(
            target_registry
        )
        registry_interface.compute_entitlement_statistics(
            beneficiary_list_details.beneficiary_list_id,
            bg_task_session,
        )

        _logger.info(
            f"Entitlement summary statistics added successfully for beneficiary list id: {id}"
        )

    except Exception as e:
        raise Exception(
            f"Error computing entitlement summary statistics for beneficiary list id {id}: {e}"
        ) from e


def update_registrant_detail_json(
    registrant_detail,
    benefit_code_id,
    max_quantity,
    calculated_entitlement,
    entitlement_rule_multiplier,
    multiplier_value,
    is_registrant_entitled,
):
    if benefit_code_id in registrant_detail.entitlement:
        existing_entitlement = registrant_detail.entitlement[benefit_code_id]
        if max_quantity == 0:
            addl_entitlement = existing_entitlement + calculated_entitlement
        else:
            addl_entitlement = min(
                existing_entitlement + calculated_entitlement,
                max_quantity,
            )
        registrant_detail.entitlement[benefit_code_id] = addl_entitlement
    else:
        if max_quantity == 0:
            addl_entitlement = calculated_entitlement
        else:
            addl_entitlement = min(
                calculated_entitlement,
                max_quantity,
            )
        registrant_detail.entitlement[benefit_code_id] = addl_entitlement

    if benefit_code_id not in registrant_detail.compute_elements:
        registrant_detail.compute_elements[benefit_code_id] = {}

    if is_registrant_entitled and entitlement_rule_multiplier:
        registrant_detail.compute_elements[benefit_code_id][
            entitlement_rule_multiplier
        ] = multiplier_value


