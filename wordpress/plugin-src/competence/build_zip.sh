#!/bin/bash

set -e

PLUGIN_NAME="competence-wp"
DIST_DIR="dist/$PLUGIN_NAME"

echo "🧹 Cleaning previous dist and build..."
rm -rf dist
mkdir -p "$DIST_DIR"

#echo "🔧 Building the plugin..."
#npm run build

echo "📁 Copying plugin files..."
cp competence-wp.php "$DIST_DIR"
cp -r build "$DIST_DIR/build"

echo "🗜️ Creating ZIP archive..."
cd dist
zip -r "$PLUGIN_NAME.zip" "$PLUGIN_NAME"
cd ..

echo "✅ Plugin packaged at: dist/$PLUGIN_NAME.zip"
