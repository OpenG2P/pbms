export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y --no-install-recommends \
  build-essential \
  autoconf \
  libtool \
  gettext \
  libjpeg-dev \
  git \
  zlib1g-dev
for dir in $EXTRA_ADDONS_DIR/*/; do
  if [[ -f ${dir}requirements.txt ]]; then
    pip install -r ${dir}requirements.txt
  fi
done
apt-get purge -y build-essential autoconf libtool
apt-get autoremove -y
apt-get clean
rm -rf /var/lib/apt/lists /var/cache/apt/archives
