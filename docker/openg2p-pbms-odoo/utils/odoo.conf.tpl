[options]
http_port = ${ODOO_PORT_NUMBER}
; longpolling_port = ${ODOO_LONGPOLLING_PORT_NUMBER}
gevent_port = ${ODOO_LONGPOLLING_PORT_NUMBER}
proxy_mode = ${ODOO_PROXY_MODE}

admin_passwd = ${ODOO_PASSWORD}
email_from = ${ODOO_EMAIL}

addons_path = ${ODOO_ADDONS_DIR}
data_dir = ${ODOO_DATA_DIR}

; csv_internal_sep = ,

db_host = ${ODOO_DATABASE_HOST}
db_port = ${ODOO_DATABASE_PORT_NUMBER}
db_name = ${ODOO_DATABASE_NAME}
db_user = ${ODOO_DATABASE_USER}
db_password = ${ODOO_DATABASE_PASSWORD}
db_maxconn = ${ODOO_DATABASE_MAXCONN}
db_sslmode = ${ODOO_DATABASE_SSLMODE}
db_template = ${ODOO_DATABASE_TEMPLATE}
dbfilter = ${ODOO_DATABASE_FILTER_OVERRIDE}

debug_mode = ${ODOO_DEBUG_MODE}
list_db = ${ODOO_LIST_DB}

log_db = ${ODOO_LOG_DB}
log_handler = ${ODOO_LOG_HANDLER}
; log_level = info
; logfile = None

; limit_memory_hard = 2684354560
; limit_memory_soft = 2147483648
; limit_request = 8192
limit_time_cpu = ${ODOO_LIMIT_TIME_CPU}
limit_time_real = ${ODOO_LIMIT_TIME_REAL}

max_cron_threads = ${ODOO_MAX_CRON_THREADS}
workers = ${ODOO_WORKERS}

without_demo = ${WITHOUT_DEMO}
server_wide_modules = ${ODOO_SERVER_WIDE_MODULES}

; osv_memory_age_limit = 1.0
; osv_memory_count_limit = False

; xmlrpc = True
; xmlrpc_interface =
; xmlrpc_port = 8069
; xmlrpcs = True
; xmlrpcs_interface =
; xmlrpcs_port = 8071
