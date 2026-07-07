remove_matching_addons() {
  local pattern="${1?missng pattern}"
  shift
  for dir in "$@"; do
    find "$dir" -maxdepth 1 -type d -print0 | sort -z | while read -r -d '' sub_dir; do
      if [[ "$sub_dir" != "$dir" ]] && basename "$sub_dir" | grep -qP "$pattern"; then
        echo "Removing addon: $sub_dir"
        rm -rf "$sub_dir"
      fi
    done
  done
}

MODULES_TO_REMOVE=$(echo $MODULES_TO_REMOVE | tr -d '[:space:]')
if [ -n "$MODULES_TO_REMOVE" ]; then
  IFS=',' read -r -a addon_dirs <<< "$MODULES_TO_REMOVE_PATHS"
  remove_matching_addons $MODULES_TO_REMOVE ${addon_dirs[@]}
fi
