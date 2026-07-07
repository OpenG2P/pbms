if [[ $WAIT_FOR_POSTGRES -ge 0 ]]; then
  wait-for-psql.py --db_host $ODOO_DATABASE_HOST --db_port ${ODOO_DATABASE_PORT_NUMBER} --db_user ${ODOO_DATABASE_USER} --db_password ${ODOO_DATABASE_PASSWORD} --timeout $WAIT_FOR_POSTGRES
fi
