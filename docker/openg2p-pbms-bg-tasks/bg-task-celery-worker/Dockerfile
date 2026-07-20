FROM python:3.12.11-alpine3.22

# External OpenG2P library refs (not part of this repo). Override via build-arg /
# workflow input. The PBMS bg-task code (models, workers) and the registry
# adapter extensions are installed from LOCAL source (build context = repo root).
ARG FASTAPI_COMMON_REF=develop
ARG G2P_BRIDGE_REF=develop

RUN apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers make \
 && apk add --no-cache bash git gettext libpq-dev libffi-dev openssl-dev

WORKDIR /app

# External libs (openg2p-fastapi-common family + g2p-bridge models)
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir jinja2 && \
    pip install --no-cache-dir \
        "git+https://github.com/openg2p/openg2p-fastapi-common@${FASTAPI_COMMON_REF}#subdirectory=openg2p-fastapi-common" \
        "git+https://github.com/openg2p/openg2p-fastapi-common@${FASTAPI_COMMON_REF}#subdirectory=openg2p-fastapi-auth" \
        "git+https://github.com/openg2p/openg2p-fastapi-common@${FASTAPI_COMMON_REF}#subdirectory=openg2p-fastapi-auth-models" \
        "git+https://gitlab.com/openg2p/g2p-bridge/g2p-bridge@${G2P_BRIDGE_REF}#subdirectory=core/models"

# Local source: PBMS + bg-task models, the celery workers, and the registry
# adapter extensions. Remaining deps resolve from PyPI via each pyproject.
COPY core/openg2p-pbms-models /src/openg2p-pbms-models
COPY core/openg2p-bg-task-models /src/openg2p-bg-task-models
COPY core/openg2p-bg-task-celery-workers /src/openg2p-bg-task-celery-workers
COPY extensions/openg2p-bg-task-registry-adapters /src/openg2p-bg-task-registry-adapters
RUN pip install --no-cache-dir \
        /src/openg2p-pbms-models \
        /src/openg2p-bg-task-models \
        /src/openg2p-bg-task-celery-workers \
        /src/openg2p-bg-task-registry-adapters

RUN apk del --no-network .build-deps

ENV PYTHONUNBUFFERED=1

# Use module path for Celery app (no local main.py)
CMD ["celery", "-A", "openg2p_bg_task_celery_workers.main.celery_app", "worker", "-Q", "bg_task_worker_queue", "--loglevel=debug"]
