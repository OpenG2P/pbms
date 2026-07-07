import logging
import math
from datetime import datetime

from openg2p_bg_task_models.schemas import (
    BeneficiarySearchRequest,
    BeneficiarySearchResponse,
    BeneficiarySearchResponseBody,
    BeneficiarySearchResponsePayload,
)
from openg2p_bg_task_registry_adapters.factory import RegistryFactory
from openg2p_bg_task_registry_adapters.interface import RegistryInterface
from openg2p_fastapi_common.schemas import (
    G2PPaginationResponse,
    G2PResponseHeader,
    G2PResponseStatus,
)
from openg2p_fastapi_common.service import BaseService
from sqlalchemy.ext.asyncio import async_sessionmaker

from ..config import Settings
from ..engine import get_engine

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)
_engine = get_engine()


class BeneficiarySearchService(BaseService):
    async def search_beneficiaries(
        self, beneficiary_search_request: BeneficiarySearchRequest
    ) -> BeneficiarySearchResponse:
        beneficiary_search_request_payload = (
            beneficiary_search_request.request_body.request_payload
        )
        pagination_request = beneficiary_search_request.request_body.pagination_request

        session_maker = async_sessionmaker(
            bind=_engine.get("db_engine_bg_task"), expire_on_commit=False
        )
        sr_session_maker = async_sessionmaker(
            bind=_engine.get("db_engine_sr"), expire_on_commit=False
        )

        async with session_maker() as session, sr_session_maker() as sr_session:
            try:
                registry_interface: RegistryInterface = (
                    RegistryFactory.get_registry_class(
                        beneficiary_search_request_payload.target_registry
                    )
                )
                (
                    beneficiary_search_response_payload,
                    total_count,
                ) = await registry_interface.search_beneficiaries(
                    session,
                    sr_session,
                    beneficiary_search_request_payload.beneficiary_list_id,
                    beneficiary_search_request_payload.target_registry,
                    pagination_request.search_text,
                    pagination_request.current_page,
                    pagination_request.page_size,
                    pagination_request.sort_by,
                )

                # Build pagination response
                page_size = pagination_request.page_size if pagination_request else 10
                number_of_pages = (
                    math.ceil(total_count / page_size) if page_size > 0 else 0
                )
                pagination_response = G2PPaginationResponse(
                    number_of_items=total_count,
                    number_of_pages=number_of_pages,
                )

                return BeneficiarySearchResponse(
                    response_header=G2PResponseHeader(
                        request_id=beneficiary_search_request.request_header.request_id,
                        response_timestamp=datetime.now(),
                        response_status=G2PResponseStatus.SUCCESS,
                    ),
                    response_body=BeneficiarySearchResponseBody(
                        pagination_response=pagination_response,
                        response_payload=beneficiary_search_response_payload,
                    ),
                )

            except Exception as e:
                _logger.exception("Error searching for beneficiaries.")
                raise e

    async def construct_beneficiary_search_error_response(
        self,
        beneficiary_search_request: BeneficiarySearchRequest,
        error_code: str,
    ) -> BeneficiarySearchResponse:
        response = BeneficiarySearchResponse(
            response_header=G2PResponseHeader(
                request_id=beneficiary_search_request.request_header.request_id,
                response_timestamp=datetime.now(),
                response_status=G2PResponseStatus.ERROR,
                response_error_code=error_code,
            ),
            response_body=BeneficiarySearchResponseBody(
                response_payload=BeneficiarySearchResponsePayload(
                    beneficiary_count=0, beneficiaries=[]
                ),
            ),
        )

        return response
