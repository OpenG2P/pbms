remove_data_file_from_addon() {
  addon_path=${1?missing addon path}
  data_file_path=${2?missing file path}
  manifest_path="${addon_path}/__manifest__.py"
  grep -vF $data_file_path $manifest_path > /tmp/manifest && mv /tmp/manifest $manifest_path
  rm -f "${addon_path}/${data_file_path}"
}

remove_web_editor_iap_dep() {
  main_controller_path=/usr/lib/python3/dist-packages/odoo/addons/web_editor/controllers/main.py
  grep -vF "import iap_tools" $main_controller_path > /tmp/main && mv /tmp/main $main_controller_path
  sed -i '/iap_tools.iap_jsonrpc/i\            from odoo.addons.iap.tools import iap_tools' $main_controller_path
}

if [[ "$ODOO_REMOVE_BASE_IR_MODULE_MODULES_DATA" != "false" ]]; then
  remove_data_file_from_addon "/usr/lib/python3/dist-packages/odoo/addons/base" "data/ir_module_module.xml"
fi

if [[ "$ODOO_REMOVE_WEB_EDITOR_IAP_DEP" != "false" ]]; then
  remove_web_editor_iap_dep
fi
