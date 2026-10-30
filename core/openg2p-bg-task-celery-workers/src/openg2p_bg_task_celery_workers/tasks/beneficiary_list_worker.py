import json
import logging
from datetime import datetime, timezone
from typing import List

from openg2p_bg_task_models.models import BeneficiaryListDetails, BeneficiaryListSummary
from openg2p_bg_task_models.schemas import RegistrantDetails
from openg2p_bg_task_registry_adapters.factory import RegistryFactory
from openg2p_bg_task_registry_adapters.interface import RegistryInterface
from openg2p_pbms_models.models import (
    G2PBeneficiaryList,
    G2PEligibilityRuleDefinition,
    G2PPriorityRuleDefinition,
    G2PProgramDefinition,
    ListStageEnum,
    ListWorkflowStatusEnum,
    StatusEnum,
)
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from ..app import celery_app, get_engine
from ..config import Settings

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)
_engine = get_engine()


@celery_app.task(name="beneficiary_list_worker")
def beneficiary_list_worker(id: int):
    _logger.info("Starting eligibility list generation for beneficiary list id: %s", id)
    bg_task_session_maker = sessionmaker(
        bind=_engine.get("db_engine_bg_task"), expire_on_commit=False
    )
    pbms_session_maker = sessionmaker(
        bind=_engine.get("db_engine_pbms"), expire_on_commit=False
    )

    with bg_task_session_maker() as bg_task_session, pbms_session_maker() as pbms_session:
        beneficiary_list = None
        try:
            beneficiary_list = (
                pbms_session.query(G2PBeneficiaryList)
                .filter(G2PBeneficiaryList.id == id)
                .first()
            )
            g2p_program_definition = (
                pbms_session.query(G2PProgramDefinition)
                .filter(G2PProgramDefinition.id == beneficiary_list.program_id)
                .first()
            )
            registry: RegistryInterface = RegistryFactory.get_registry_class(
                g2p_program_definition.target_registry
            )
            enrollment_rules = _enrollment_rules(
                pbms_session, beneficiary_list.program_id
            )

            if beneficiary_list.list_stage == ListStageEnum.ENROLLMENT.value:
                id_batches = registry.iter_eligible_ids(
                    enrollment_rules, _config.batch_size
                )
            elif beneficiary_list.list_stage == ListStageEnum.DISBURSEMENT.value:
                id_batches = registry.iter_priority_ids(
                    _priority_domains(pbms_session, beneficiary_list),
                    _enrolled_ids(pbms_session, bg_task_session, beneficiary_list),
                    enrollment_rules,
                    _config.batch_size,
                )
            else:
                raise ValueError(
                    f"Invalid list stage {beneficiary_list.list_stage} for beneficiary list id {id}"
                )

            total_number_of_registrants = 0
            beneficiary_list_details: List[BeneficiaryListDetails] = []
            for registrant_ids in id_batches:
                if not registrant_ids:
                    continue
                registrant_details = [
                    RegistrantDetails(
                        registrant_id=registrant_id,
                        entitlement={},
                        compute_elements={},
                    ).model_dump(mode="json")
                    for registrant_id in registrant_ids
                ]
                total_number_of_registrants += len(registrant_ids)
                beneficiary_list_details.append(
                    BeneficiaryListDetails(
                        beneficiary_list_id=beneficiary_list.beneficiary_list_id,
                        registrant_details=registrant_details,
                        entitlement_process_status=StatusEnum.pending.value
                        if beneficiary_list.list_stage
                        == ListStageEnum.DISBURSEMENT.value
                        else StatusEnum.not_applicable.value,
                        number_of_registrants=len(registrant_ids),
                    )
                )

            beneficiary_list.number_of_registrants = total_number_of_registrants
            bg_task_session.add_all(beneficiary_list_details)

            base_summary = BeneficiaryListSummary(
                program_id=beneficiary_list.program_id,
                program_mnemonic=g2p_program_definition.program_mnemonic,
                target_registry=g2p_program_definition.target_registry,
                beneficiary_list_id=beneficiary_list.beneficiary_list_id,
                number_of_registrants=total_number_of_registrants,
                date_created=datetime.now(timezone.utc),
            )
            registry.compute_eligibility_statistics(
                beneficiary_list_details, base_summary, bg_task_session
            )

            beneficiary_list.eligibility_process_status = StatusEnum.complete.value
            if beneficiary_list.list_stage == ListStageEnum.DISBURSEMENT.value:
                beneficiary_list.entitlement_process_status = StatusEnum.pending.value
            beneficiary_list.processed_date = datetime.now(timezone.utc)

            bg_task_session.commit()
            pbms_session.commit()

        except Exception as e:
            _logger.error(
                "Error during processing eligibility request for beneficiary list id %s: %s",
                id,
                e,
            )
            pbms_session.rollback()
            bg_task_session.rollback()

            beneficiary_list.eligibility_number_of_attempts += 1
            beneficiary_list.eligibility_processed_date = datetime.now(timezone.utc)
            beneficiary_list.eligibility_process_status = (
                StatusEnum.pending.value
                if beneficiary_list.eligibility_number_of_attempts
                < _config.worker_max_attempts
                else StatusEnum.failed.value
            )
            beneficiary_list.eligibility_latest_error_code = str(e)
            pbms_session.commit()
            raise e

        _logger.info(
            "Completed processing eligibility request for beneficiary list id: %s", id
        )


def _enrollment_rules(pbms_session, program_id) -> list[tuple[str, str]]:
    rows = pbms_session.execute(
        select(
            G2PEligibilityRuleDefinition.pbms_domain,
            G2PEligibilityRuleDefinition.set_operator,
        )
        .where(G2PEligibilityRuleDefinition.program_id == program_id)
        .order_by(G2PEligibilityRuleDefinition.rule_number.asc())
    ).all()
    return [(domain, operator) for domain, operator in rows]


def _priority_domains(pbms_session, beneficiary_list) -> list[str]:
    return list(
        pbms_session.execute(
            select(G2PPriorityRuleDefinition.pbms_domain).where(
                G2PPriorityRuleDefinition.disbursement_cycle_id
                == beneficiary_list.disbursement_cycle_id
            )
        )
        .scalars()
        .all()
    )


def _enrolled_ids(pbms_session, bg_task_session, beneficiary_list) -> list[str]:
    latest = (
        pbms_session.query(G2PBeneficiaryList.beneficiary_list_id)
        .filter(
            G2PBeneficiaryList.program_id == beneficiary_list.program_id,
            G2PBeneficiaryList.list_stage == ListStageEnum.ENROLLMENT.value,
            G2PBeneficiaryList.list_workflow_status
            == ListWorkflowStatusEnum.APPROVED_FINAL_ENROLMENT.value,
        )
        .order_by(G2PBeneficiaryList.creation_date.desc())
        .first()
    )
    if not latest:
        return []
    blocks = (
        bg_task_session.execute(
            select(BeneficiaryListDetails.registrant_details).where(
                BeneficiaryListDetails.beneficiary_list_id == latest[0]
            )
        )
        .scalars()
        .all()
    )
    registrant_ids = []
    for block in blocks:
        if isinstance(block, str):
            block = json.loads(block)
        for registrant in block or []:
            registrant_ids.append(registrant["registrant_id"])
    return registrant_ids
