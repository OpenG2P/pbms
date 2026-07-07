if ! [ -e "${ODOO_DATA_DIR}" ]; then
  echo Odoo data directory doesnt exist
  mkdir -p ${ODOO_DATA_DIR}
fi

if [ -z "$(ls -A "${ODOO_DATA_DIR}")" ]; then
  if [[ "$ODOO_SKIP_BOOTSTRAP" == "no" ]]; then
    echo Initializing Odoo.
    ODOO_BOOTSTRAP_MODULES=$(echo $ODOO_BOOTSTRAP_MODULES | tr -d '[:space:]')
    "$@" -i "$ODOO_BOOTSTRAP_MODULES" --stop-after-init
    echo Finished Bootstrapping Odoo
  fi
else
  echo Resuming Odoo from existing data directory
  if [[ "$ODOO_SKIP_MODULES_UPDATE" == "no" ]]; then
    echo Upgrading Odoo modules
    ODOO_UPDATE_MODULES=$(echo $ODOO_UPDATE_MODULES | tr -d '[:space:]')
    "$@" -u "$ODOO_UPDATE_MODULES" --stop-after-init
    echo Finished Upgrading Odoo
  fi
fi
