if [ -f "${ODOO_RC}.tpl" ]; then
  envsubst < ${ODOO_RC}.tpl > ${ODOO_RC}
fi
