#!/usr/bin/env bash
set -euo pipefail

# Fix the bind-mounted wp-content on the HOST so both you and www-data can write
WP_CONTENT="./wordpress/wp-content"
mkdir -p "$WP_CONTENT"

# Optional: add your user to www-data group (re-login to take effect)
if ! id -nG "$USER" | grep -qw "www-data"; then
  echo "👉 Adding $USER to www-data group (re-login required) ..."
  sudo usermod -aG www-data "$USER" || true
fi

echo "👉 Fixing ownership/permissions on $WP_CONTENT ..."
sudo chgrp -R www-data "$WP_CONTENT"
sudo chmod -R g+rwX "$WP_CONTENT"
sudo find "$WP_CONTENT" -type d -exec chmod g+s {} \;

# If available, make new files inherit group perms
if command -v setfacl >/dev/null 2>&1; then
  sudo setfacl -R -m g:www-data:rwx "$WP_CONTENT"
  sudo setfacl -R -d -m g:www-data:rwx "$WP_CONTENT"
fi

echo "✅ wp-content is writable by www-data + your group."
