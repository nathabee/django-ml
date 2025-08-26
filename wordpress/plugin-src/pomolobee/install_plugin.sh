#!/bin/bash

set -e

PLUGIN_NAME="pomolobee-wp"
BUILD_PLUGIN="dist/$PLUGIN_NAME"
WORDPRESS_PLUGIN_DIR="../../wp-content/plugins/"

echo "Moving plugin to Wordpress"
 

cp -rp $BUILD_PLUGIN  $WORDPRESS_PLUGIN_DIR
echo "✅ Plugin installed : $WORDPRESS_PLUGIN_DIR/$PLUGIN_NAME"
