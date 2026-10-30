"""Checks every template before it is published to templates.aetherpanel.es.

Errors (the check fails):
  - templates.json and the template folders do not match
  - a template is not valid JSON, misses a required field or breaks spec.json
  - a Docker image is not ours (ghcr.io/aether-panel/*), an official Docker Hub image or a
    vendor's own image
  - a default port is one the panel uses itself (the server could not be created)

Problems already known and waiting for a fix are listed in tools/pending.txt as
"<template> <check>" (check: image, port, environments): they are reported as warnings, and an
entry that is no longer needed is reported too, so the list only shrinks.

usage: python3 tools/validate.py [repository folder]
"""
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")

# ports of a standard install: panel, Adminer, SFTP, MariaDB
PANEL_PORTS = {8080: "the panel", 8081: "Adminer", 5657: "SFTP", 3307: "the panel's MariaDB"}

# images published by the vendor of the software itself
VENDOR_IMAGES = ("mcr.microsoft.com/dotnet/", "oven/bun")

errors, warnings = [], []
PENDING, USED = set(), set()


def error(template, msg, check=""):
    if (template, check) in PENDING:
        USED.add((template, check))
        warnings.append(f"{template}: {msg} (pending)")
    else:
        errors.append(f"{template}: {msg}")


def load_pending():
    path = os.path.join(ROOT, "tools", "pending.txt")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                parts = line.split("#")[0].split()
                if len(parts) == 2:
                    PENDING.add((parts[0], parts[1]))


def image_allowed(image):
    image = re.sub(r"\$\{[^}]*\}", "x", image)  # ${version} tags
    if image.startswith("ghcr.io/aether-panel/") or image.startswith(VENDOR_IMAGES):
        return True
    repo = image.split(":")[0]
    return "/" not in repo or repo.startswith("library/")  # official Docker Hub images


def check_template(name, schema):
    path = os.path.join(ROOT, name, f"{name}.json")
    try:
        with open(path, encoding="utf-8") as f:
            t = json.load(f)
    except (OSError, ValueError) as e:
        error(name, f"cannot read {name}.json: {e}")
        return

    for field in ("type", "display", "run", "environment"):
        if field not in t:
            error(name, f"missing \"{field}\"")
    if not t.get("supportedEnvironments"):
        error(name, "no supportedEnvironments: the panel cannot offer it", "environments")
    if "run" in t and not t["run"].get("command"):
        error(name, "run.command is empty")
    if t.get("type") and t["type"] != t["type"].lower():
        error(name, "type must be lowercase")

    if schema is not None:
        import jsonschema  # installed by the workflow
        for e in sorted(jsonschema.Draft202012Validator(schema).iter_errors(t), key=str)[:5]:
            error(name, f"spec.json: {'/'.join(map(str, e.path)) or '(root)'}: {e.message[:200]}")

    envs = list(t.get("supportedEnvironments") or []) + [t.get("environment") or {}]
    for env in envs:
        image = env.get("image") if isinstance(env, dict) else None
        if env.get("type") == "docker" and image and not image_allowed(image):
            error(name, f"third-party image {image}: use ghcr.io/aether-panel/* or the official image", "image")

    for var, spec in (t.get("data") or {}).items():
        if "port" not in var.lower() or not isinstance(spec, dict):
            continue
        try:
            port = int(spec.get("value"))
        except (TypeError, ValueError):
            continue
        if port in PANEL_PORTS:
            error(name, f"default {var} {port} is used by {PANEL_PORTS[port]}", "port")


def main():
    with open(os.path.join(ROOT, "templates.json"), encoding="utf-8") as f:
        index = json.load(f)
    folders = sorted(d for d in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT, d, f"{d}.json")))
    for name in sorted(set(index) - set(folders)):
        error(name, "listed in templates.json without a folder")
    for name in sorted(set(folders) - set(index)):
        error(name, "folder not listed in templates.json")
    for name, entry in index.items():
        if entry.get("url") != f"{name}/{name}.json":
            error(name, f"templates.json url should be {name}/{name}.json")

    schema = None
    try:
        import jsonschema  # noqa: F401
        with open(os.path.join(ROOT, "spec.json"), encoding="utf-8") as f:
            schema = json.load(f)
    except ImportError:
        warnings.append("jsonschema is not installed: spec.json not checked (pip install jsonschema)")

    load_pending()
    for name in folders:
        check_template(name, schema)
    for name, check in sorted(PENDING - USED):
        warnings.append(f"{name} {check}: fixed, remove it from tools/pending.txt")

    for w in warnings:
        print("warning: " + w)
    for e in errors:
        print("ERROR: " + e)
    print(f"{len(folders)} templates, {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


main()
