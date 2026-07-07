set_default_env_vars(){
  export ODOO_PORT_NUMBER=${ODOO_PORT_NUMBER:-8069}
  export ODOO_LONGPOLLING_PORT_NUMBER=${ODOO_LONGPOLLING_PORT_NUMBER:-8072}
  export ODOO_PASSWORD=${ODOO_PASSWORD:-admin}
  export ODOO_PROXY_MODE=${ODOO_PROXY_MODE:-True}  # Odoo should always be running in proxy mode

  export ODOO_VOLUME_DIR=${ODOO_VOLUME_DIR:-/bitnami/odoo}
  export ODOO_VOLUME_DIR=${ODOO_VOLUME_DIR%/}
  export ODOO_DATA_DIR=${ODOO_DATA_DIR:-${ODOO_VOLUME_DIR}/data}
  # export ODOO_ADDONS_DIR="" # This will be set by set_addons_dir_env command

  export ODOO_DATABASE_MAXCONN=${ODOO_DATABASE_MAXCONN:-64}
  export ODOO_DATABASE_SSLMODE=${ODOO_DATABASE_SSLMODE:-prefer}
  export ODOO_DATABASE_TEMPLATE=${ODOO_DATABASE_TEMPLATE:-template1}
  export ODOO_DATABASE_FILTER_OVERRIDE=${ODOO_DATABASE_FILTER_OVERRIDE:-^${ODOO_DATABASE_NAME}$}

  export ODOO_SMTP_HOST=${ODOO_SMTP_HOST:-${OPENG2P_SMTP_HOST}}  # For helm chart compat
  export ODOO_SMTP_PORT_NUMBER=${ODOO_SMTP_PORT_NUMBER:-${OPENG2P_SMTP_PORT}}  # For helm chart compat
  export ODOO_SMTP_USER=${ODOO_SMTP_USER:-False}
  export ODOO_SMTP_PASSWORD=${ODOO_SMTP_PASSWORD:-False}
  if [ "$ODOO_SMTP_PROTOCOL" = "ssl" ] || [ "$ODOO_SMTP_PROTOCOL" = "tls" ]; then
    export ODOO_SMTP_SSL=${ODOO_SMTP_SSL:-True}
  else
    export ODOO_SMTP_SSL=${ODOO_SMTP_SSL:-False}
  fi

  if [ "$BITNAMI_DEBUG" = "yes" ]; then
    export ODOO_DEBUG_MODE=${ODOO_DEBUG_MODE:-True}
  else
    export ODOO_DEBUG_MODE=${ODOO_DEBUG_MODE:-False}
  fi
  export ODOO_LIST_DB=${ODOO_LIST_DB:-${LIST_DB:-False}}  # For helm chart compat

  export ODOO_LOG_DB=${ODOO_LOG_DB:-${LOG_DB:-False}}  # For helm chart compat
  export ODOO_LOG_HANDLER=${ODOO_LOG_HANDLER:-${LOG_HANDLER:-"':INFO'"}}  # For helm chart compat

  export ODOO_LIMIT_TIME_CPU=${ODOO_LIMIT_TIME_CPU:-${LIMIT_TIME_CPU:-90}}  # For helm chart compat
  export ODOO_LIMIT_TIME_REAL=${ODOO_LIMIT_TIME_REAL:-${LIMIT_TIME_REAL:-150}}  # For helm chart compat

  export ODOO_MAX_CRON_THREADS=${ODOO_MAX_CRON_THREADS:-1}
  export ODOO_WORKERS=${ODOO_WORKERS:-0}

  export ODOO_WITHOUT_DEMO=${ODOO_WITHOUT_DEMO:-${WITHOUT_DEMO:-False}}  # For helm chart compat
  export ODOO_SERVER_WIDE_MODULES=${ODOO_SERVER_WIDE_MODULES:-${SERVER_WIDE_MODULES:-base,web}}

  export ODOO_UPDATE_MODULES=${ODOO_UPDATE_MODULES:-all}
  export ODOO_BOOTSTRAP_MODULES=${ODOO_BOOTSTRAP_MODULES:-base}

  export WAIT_FOR_POSTGRES=${WAIT_FOR_POSTGRES:-60}
}

set_default_env_vars
