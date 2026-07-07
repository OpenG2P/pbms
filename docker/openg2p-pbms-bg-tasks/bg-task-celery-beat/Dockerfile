FROM python:3.12.11-alpine3.22

# External OpenG2P library refs (not part of this repo). Override via build-arg /
# workflow input. The PBMS bg-task code is installed from LOCAL source
# (build context = repo root).
ARG FASTAPI_COMMON_REF=develop

RUN apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers make \
 && apk add --no-cache bash git gettext libpq-dev libffi-dev openssl-dev

WORKDIR /app

# External libs (openg2p-fastapi-common family)
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir \
        "git+https://github.com/openg2p/openg2p-fastapi-common@${FASTAPI_COMMON_REF}#subdirectory=openg2p-fastapi-common" \
        "git+https://github.com/openg2p/openg2p-fastapi-common@${FASTAPI_COMMON_REF}#subdirectory=openg2p-fastapi-auth" \
        "git+https://github.com/openg2p/openg2p-fastapi-common@${FASTAPI_COMMON_REF}#subdirectory=openg2p-fastapi-auth-models"

# Local source: PBMS + bg-task models and the celery beat producers.
COPY core/openg2p-pbms-models /src/openg2p-pbms-models
COPY core/openg2p-bg-task-models /src/openg2p-bg-task-models
COPY core/openg2p-bg-task-celery-beat-producers /src/openg2p-bg-task-celery-beat-producers
RUN pip install --no-cache-dir \
        /src/openg2p-pbms-models \
        /src/openg2p-bg-task-models \
        /src/openg2p-bg-task-celery-beat-producers

RUN apk del --no-network .build-deps

ENV PYTHONUNBUFFERED=1

# Use module path for Celery beat app
CMD ["celery", "-A", "openg2p_bg_task_celery_beat_producers.main.celery_app", "worker", "--beat", "--loglevel=info", "--schedule=/tmp/celery-beat-schedule.db"]
