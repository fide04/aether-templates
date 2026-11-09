#!/bin/sh
# Cloudflare Pages runs this on every push: it checks the templates and copies what the panels
# download (templates.json and each template's folder) and the catalogue page to public/. A template that fails the
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
# the catalogue page at the root of the site (site/index.html with the templates inlined)
python3 tools/build_site.py public
echo "public/: $(ls public | wc -l | tr -d ' ') entries"
