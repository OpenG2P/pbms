#!/usr/bin/env bash

set -e
set -o pipefail

export_from_packages(){
  if [ -f $1 ]; then
    IFS=$'\n' packages_file_content=($(envsubst < $1))
    prefix="$2"
    for package in ${packages_file_content[@]}; do
      package=${package//[[:space:]]/}
      if [ -n "$package" ]; then
        if [[ "$package" != "#"* ]]; then
          IFS="=" read -r package_var package_value <<< "$package"
          combo="${prefix}${package_var}"
          if [ -z "${!combo}" ];then
            export $combo=$package_value
          fi
        fi
      fi
    done
  fi
}

export_from_env(){
  set -a
  source "$1"
  set +a
}

get_final_env_prefix(){
  PREFIX=$1
  PACKAGE_FILE_NAME=$(basename $2 ".txt")
  PACKAGE_FILE_NAME=${PACKAGE_FILE_NAME//\./_}
  PACKAGE_FILE_NAME=${PACKAGE_FILE_NAME//\-/_}
  PACKAGE_FILE_NAME=${PACKAGE_FILE_NAME//[[:space:]]/}
  echo "${PREFIX}${PACKAGE_FILE_NAME}_"
}

get_vars_from_prefix(){
  PACKAGES_VARS=()
  PACKAGES_VALUES=()
  prefix=$1
  IFS=$'\n' packages_list=($(awk 'BEGIN{for(v in ENVIRON) print v}' | grep "^$prefix"))
  for package in ${packages_list[@]}; do
    if [[ "${!package}" != "#"* ]]; then
      PACKAGES_VALUES+=("${!package}")
      var=${package#"$prefix"}
      PACKAGES_VARS+=(${var//_/-})
    fi
  done
  export PACKAGES_VALUES
  export PACKAGES_VARS
}

download_packages(){
  PACKAGE_TXT_PATH="$1"
  PREFIX="$2"
  PACKAGES_TMPDIR="$3"

  PREFIX=$(get_final_env_prefix $PREFIX $PACKAGE_TXT_PATH)

  export_from_packages $PACKAGE_TXT_PATH $PREFIX
  if [ -f .env ]; then
    export_from_env .env
  fi

  get_vars_from_prefix $PREFIX

  rm -rf $PACKAGES_TMPDIR
  mkdir $PACKAGES_TMPDIR

  GIT_PREFIX=${GIT_PREFIX:-"git://"}
  FILE_PREFIX=${FILE_PREFIX:-"file://"}

  for i in ${!PACKAGES_VARS[@]}; do
    package_value=${PACKAGES_VALUES[i]}
    if [[ ${PACKAGES_VALUES[i]} == "$GIT_PREFIX"* ]]; then
      package_value=${package_value#"$GIT_PREFIX"}
      branch_name=${package_value%%"//"*}
      git_address=${package_value#*"//"}
      git clone --depth 1 -b ${branch_name} ${git_address} $PACKAGES_TMPDIR/${PACKAGES_VARS[i]}
    elif [[ ${PACKAGES_VALUES[i]} == "$FILE_PREFIX"* ]]; then
      package_value=${package_value#"$FILE_PREFIX"}
      cp -r $package_value $PACKAGES_TMPDIR/${PACKAGES_VARS[i]}
    fi
  done
}

if [[ "$0" == "$BASH_SOURCE" ]]; then
  if [ $# -lt 1 ] ; then
    echo "Package txt path argument missing" 1>&2
    exit 1
  fi
  ENV_PREFIX=${ENV_PREFIX:-"G2P_PACKAGE_"}
  PACKAGES_TMPDIR=${PACKAGES_TMPDIR:-"tmpdir"}
  download_packages $1 $ENV_PREFIX $PACKAGES_TMPDIR
fi
