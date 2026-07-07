FROM python:3.12.11-alpine3.22

# External OpenG2P library refs (not part of this repo). Override via build-arg /
# workflow input. The PBMS API code + registry adapter extensions are installed
# from LOCAL source (build context = repo root).
ARG FASTAPI_COMMON_REF=develop

RUN apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers make \
 && apk add --no-cache bash git gettext libpq-dev libmagic

WORKDIR /app

# External libs (openg2p-fastapi-common family)
RUN pip install --no-cache-dir \
        "git+https://github.com/openg2p/openg2p-fastapi-common@${FASTAPI_COMMON_REF}#subdirectory=openg2p-fastapi-common" \
        "git+https://github.com/openg2p/openg2p-fastapi-common@${FASTAPI_COMMON_REF}#subdirectory=openg2p-fastapi-auth" \
        "git+https://github.com/openg2p/openg2p-fastapi-common@${FASTAPI_COMMON_REF}#subdirectory=openg2p-fastapi-auth-models" \
 && pip install --no-cache-dir jinja2

# Local source: PBMS + bg-task models, the beneficiary portal API, and the
# registry adapter extensions.
COPY core/openg2p-pbms-models /src/openg2p-pbms-models
COPY core/openg2p-bg-task-models /src/openg2p-bg-task-models
COPY apis/openg2p-pbms-bene-portal-api /src/openg2p-pbms-bene-portal-api
COPY extensions/openg2p-bg-task-registry-adapters /src/openg2p-bg-task-registry-adapters
RUN pip install --no-cache-dir \
        /src/openg2p-pbms-models \
        /src/openg2p-bg-task-models \
        /src/openg2p-pbms-bene-portal-api \
        /src/openg2p-bg-task-registry-adapters

RUN apk del --no-network .build-deps

ENV PYTHONUNBUFFERED=1
ENV BG_TASK_WORKER_TYPE=gunicorn
ENV BG_TASK_HOST=0.0.0.0
ENV BG_TASK_PORT=8000
ENV BG_TASK_NO_OF_WORKERS=8

# Use module path for migrate and Gunicorn WSGI app
CMD python3 -m openg2p_pbms_bene_portal_api.main migrate; \
    ${BG_TASK_WORKER_TYPE} "openg2p_pbms_bene_portal_api.main:app" --workers ${BG_TASK_NO_OF_WORKERS} --worker-class uvicorn.workers.UvicornWorker --bind ${BG_TASK_HOST}:${BG_TASK_PORT}
