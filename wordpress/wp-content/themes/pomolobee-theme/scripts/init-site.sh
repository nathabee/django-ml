#!/usr/bin/env bash
set -euo pipefail
cd /var/www/html

# ensure uploads dir is writable before importing media
 

# ensure WP is installed (you must finish the browser installer first)
if ! wp core is-installed > /dev/null 2>&1; then
  echo "❌ WordPress not installed yet. Finish installer at http://localhost:8082 first."
  exit 1
fi

# activate your theme
wp theme activate pomolobee-theme || true

# site basics
wp option update blogname 'PomoloBee'
wp option update blogdescription 'Smart orchard & field management'

# permalinks
wp option update permalink_structure '/%postname%/'

# import & set logo from theme assets (if present)
LOGO="/var/www/html/wp-content/themes/pomolobee-theme/assets/images/logo.png"
if [ -f "$LOGO" ]; then
  ID="$(wp media import "$LOGO" --porcelain)"
  echo "Imported logo attachment ID: $ID"
  wp theme mod set custom_logo "$ID" || true
  wp option add site_logo "$ID" || wp option update site_logo "$ID" || true
fi

wp cache flush || true
echo "✅ init-site done."
