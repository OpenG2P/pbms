# One Celery image for the worker and the beat producer.
# CELERY_APP selects the Python app. CELERY_OPTS selects worker or worker --beat.
# pbms-connectors installs registry-adapters on top of this image.
FROM python:3.12.11-alpine3.22

ARG FASTAPI_COMMON_REF=develop
ARG G2P_BRIDGE_REF=develop

RUN apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers make \
 && apk add --no-cache bash git gettext libpq-dev libffi-dev openssl-dev

WORKDIR /app

RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir jinja2 && \
    pip install --no-cache-dir \
        "git+https://github.com/openg2p/openg2p-fastapi-common@${FASTAPI_COMMON_REF}#subdirectory=openg2p-fastapi-common" \
        "git+https://github.com/openg2p/openg2p-fastapi-common@${FASTAPI_COMMON_REF}#subdirectory=openg2p-fastapi-auth" \
        "git+https://github.com/openg2p/openg2p-fastapi-common@${FASTAPI_COMMON_REF}#subdirectory=openg2p-fastapi-auth-models" \
        "git+https://github.com/openg2p/g2p-bridge@${G2P_BRIDGE_REF}#subdirectory=core/models"

COPY core/openg2p-pbms-models /src/openg2p-pbms-models
COPY core/openg2p-bg-task-models /src/openg2p-bg-task-models
COPY core/openg2p-bg-task-celery-workers /src/openg2p-bg-task-celery-workers
COPY core/openg2p-bg-task-celery-beat-producers /src/openg2p-bg-task-celery-beat-producers
RUN pip install --no-cache-dir \
        /src/openg2p-pbms-models \
        /src/openg2p-bg-task-models \
        /src/openg2p-bg-task-celery-workers \
        /src/openg2p-bg-task-celery-beat-producers \
 && apk del --no-network .build-deps

COPY docker/openg2p-pbms-bg-tasks/celery/run_celery.py /app/run_celery.py

ENV PYTHONUNBUFFERED=1
ENV CELERY_APP=openg2p_bg_task_celery_workers.main.celery_app
ENV CELERY_OPTS="worker -Q bg_task_worker_queue --loglevel=info"

CMD ["python3", "/app/run_celery.py"]
