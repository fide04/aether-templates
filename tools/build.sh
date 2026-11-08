#!/bin/sh
# Cloudflare Pages runs this on every push: it checks the templates and copies what the panels
# download (templates.json and each template's folder) to public/. A template that fails the
# check stops the publish, and the site keeps the previous version.
set -eu
cd "$(dirname "$0")/.."
python3 -m pip install --quiet jsonschema==4.23.0
python3 tools/validate.py
rm -rf public
mkdir public
cp templates.json public/
for dir in */; do
  name=${dir%/}
  if [ -f "$name/$name.json" ]; then
    cp -R "$name" public/
  fi
done
echo "public/: $(ls public | wc -l | tr -d ' ') entries"
