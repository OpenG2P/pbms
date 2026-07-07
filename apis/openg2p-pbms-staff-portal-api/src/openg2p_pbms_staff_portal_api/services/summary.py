import logging
from datetime import datetime

from openg2p_bg_task_models.errors import BGTaskErrorCodes, BGTaskException
from openg2p_bg_task_models.schemas import (
    SummaryRequest,
    SummaryRequestPayload,
    SummaryResponse,
    SummaryResponseBody,
    SummaryResponsePayload,
)
from openg2p_bg_task_registry_adapters.factory import RegistryFactory
from openg2p_bg_task_registry_adapters.interface import RegistryInterface
from openg2p_bg_task_registry_adapters.schema import (
    BeneficiaryListSummaryPayload,
)
from openg2p_fastapi_common.schemas import (
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


class SummaryService(BaseService):
    async def get_summary(
        self, summary_request_payload: SummaryRequestPayload
    ) -> SummaryResponsePayload:
        session_maker = async_sessionmaker(
            bind=_engine.get("db_engine_bg_task"), expire_on_commit=False
        )
        async with session_maker() as session:
            try:
                registry_interface: RegistryInterface = (
                    RegistryFactory.get_registry_class(
                        summary_request_payload.target_registry
                    )
                )
                beneficiary_list_summary_payload: BeneficiaryListSummaryPayload = (
                    await registry_interface.get_summary(
                        summary_request_payload.beneficiary_list_id,
                        session,
                        formated=True,
                    )
                )
                return SummaryResponsePayload(
                    beneficiary_list_id=summary_request_payload.beneficiary_list_id,
                    summary=beneficiary_list_summary_payload,
                )

            except Exception as e:
                _logger.error(f"Error fetching beneficiary list summary : {e}")
                raise BGTaskException(
                    message="Eligibility request invalid",
                    code=BGTaskErrorCodes.INVALID_REQUEST,
                ) from e

    async def construct_summary_success_response(
        self,
        summary_request: SummaryRequest,
        summary_response_payload: SummaryResponsePayload,
    ) -> SummaryResponse:
        response = SummaryResponse(
            response_header=G2PResponseHeader(
                request_id=summary_request.request_header.request_id,
                response_timestamp=datetime.now(),
                response_status=G2PResponseStatus.SUCCESS,
            ),
            response_body=SummaryResponseBody(
                response_payload=summary_response_payload,
            ),
        )
        return response

    async def construct_summary_error_response(
        self, summary_request: SummaryRequest, error_code: str
    ) -> SummaryResponse:
        response = SummaryResponse(
            response_header=G2PResponseHeader(
                request_id=summary_request.request_header.request_id,
                response_timestamp=datetime.now(),
                response_status=G2PResponseStatus.ERROR,
                response_error_code=error_code,
            ),
            response_body=SummaryResponseBody(
                response_payload=SummaryResponsePayload(
                    beneficiary_list_id=summary_request.request_body.request_payload.beneficiary_list_id,
                    summary=None,
                ),
            ),
        )

        return response
