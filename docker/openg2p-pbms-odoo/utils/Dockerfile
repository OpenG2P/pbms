ARG BASE_VERSION="17.0-20250807"
FROM odoo:$BASE_VERSION

ARG EXTRA_ADDONS_DIR=/opt/odoo/extraaddons
ARG MODULES_TO_REMOVE
ARG MODULES_TO_REMOVE_PATHS=/usr/lib/python3/dist-packages/odoo/addons,${EXTRA_ADDONS_DIR}/*
# External OpenG2P Odoo commons (not part of this repo); baked in at build time.
ARG ODOO_COMMONS_REF=v1.4.0

# Build context = repo root, so in-repo addons are copied straight from odoo/.

USER root

RUN ln -s $(which python3) /usr/bin/python

# --- Addons ---
# Each immediate sub-directory of EXTRA_ADDONS_DIR becomes one Odoo addons_path
# entry (see docker-entrypoint.d/00-gather-addons.sh). Local (in-repo) modules
# are copied straight from odoo/; the one external dependency is cloned.
COPY odoo/g2p_pbms                 ${EXTRA_ADDONS_DIR}/pbms-core/g2p_pbms
COPY odoo/g2p_pbms_program_access  ${EXTRA_ADDONS_DIR}/pbms-core/g2p_pbms_program_access
COPY odoo/requirements.txt         ${EXTRA_ADDONS_DIR}/pbms-core/requirements.txt
COPY odoo/extensions               ${EXTRA_ADDONS_DIR}/pbms-extensions
COPY odoo/community-addons         ${EXTRA_ADDONS_DIR}/community-addons

# External OpenG2P Odoo commons, baked in at build time.
RUN apt-get update && apt-get install -y --no-install-recommends git \
 && git clone --depth 1 -b ${ODOO_COMMONS_REF} \
      https://github.com/OpenG2P/openg2p-odoo-commons ${EXTRA_ADDONS_DIR}/openg2p-commons \
 && rm -rf ${EXTRA_ADDONS_DIR}/openg2p-commons/.git \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

ADD docker/openg2p-pbms-odoo/utils/odoo.conf.tpl /etc/odoo

ADD docker/openg2p-pbms-odoo/utils/docker-build.sh /
ADD docker/openg2p-pbms-odoo/utils/docker-build.d /docker-build.d
RUN chmod +x /docker-build.sh || true
RUN /docker-build.sh
RUN rm -rf /docker-build.sh /docker-build.d

ADD docker/openg2p-pbms-odoo/utils/docker-entrypoint.sh /entrypoint.sh
ADD docker/openg2p-pbms-odoo/utils/docker-entrypoint.d /docker-entrypoint.d
RUN chmod -R +x /docker-entrypoint.d /entrypoint.sh

USER odoo
