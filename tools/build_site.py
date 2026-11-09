#!/usr/bin/env python3
"""Builds the catalogue page served at the root of templates.aetherpanel.es.

Reads templates.json and every template, keeps what a visitor needs to choose one (name, logo,
kind, default resources, the settings a server owner can change, where it runs) and writes
public/index.html from site/index.html with that data inlined, plus the logos it uses.
Run by tools/build.sh after public/ has the templates.
"""
import html
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
REPO = "https://github.com/fide04/aether-templates"

# The same logo files and keys as the panel (client/frontend/src/lib/template-logos.ts).
# plate: a dark mark on a transparent background that needs a light tile behind it.
LOGOS = {
    "nodejs": ("nodejs.svg", True), "python": ("python.svg", True), "java": ("java.svg", True),
    "bun": ("bun.svg", True), "go": ("go.svg", True), "php": ("php.svg", True),
    "laravel": ("laravel.svg", True), "dotnet": ("dotnet.svg", False),
    "mariadb": ("mariadb.svg", True), "mongodb": ("mongodb.svg", True),
    "postgresql": ("postgresql.svg", True), "redis": ("redis.svg", True),
    "lavalink": ("lavalink.svg", False), "n8n": ("n8n.svg", False),
    "teamspeak3": ("teamspeak3.svg", True), "discord": ("discord.svg", True),
    "cstrike": ("cstrike.svg", True), "fivem": ("fivem.svg", True),
}
ALIASES = {
    "minecraft": "minecraft-java", "pocketmine": "minecraft-bedrock", "vintage-story": "vintagestory",
    "eco9": "eco", "teamspeak": "teamspeak3", "ts3": "teamspeak3", "node": "nodejs",
    "projectzomboid": "zomboid", "garrysmod": "gmod",
}

KINDS = {
    "language": {"nodejs", "python", "java", "bun", "go", "php", "laravel", "dotnet"},
    "database": {"mariadb", "mongodb", "postgresql", "redis"},
    "bot": {"discord"},
    "service": {"lavalink", "n8n", "teamspeak3"},
}

SECRET = re.compile(r"pass|secret|token|key", re.I)
TAG = re.compile(r"<[^>]+>")


def text(value):
    """A description as plain text: some templates write links as HTML for the panel."""
    return " ".join(html.unescape(TAG.sub("", str(value or ""))).split())


def internal(key, field):
    """Fields the template fills by itself (resolved versions), not something to set by hand."""
    return key.lower().startswith("resolved") or text(field.get("desc")).lower().startswith("internal")


def logo_files():
    files = {k: v for k, v in LOGOS.items()}
    for name in os.listdir(os.path.join(SITE, "icons")):
        key, ext = os.path.splitext(name)
        if ext == ".png" and key not in files:
            files[key] = (name, False)
    return files


def logo_key(files, raw):
    name = (raw or "").strip().lower()
    if not name:
        return None
    if name in files:
        return name
    if name in ALIASES:
        return ALIASES[name]
    if name.startswith("minecraft-bedrock"):
        return "minecraft-bedrock"
    if name.startswith("minecraft-"):
        return "minecraft-java"
    for key in files:
        if name.startswith(key + "-"):
            return key
    for alias, key in ALIASES.items():
        if name.startswith(alias + "-"):
            return key
    return None


def number(data, key):
    value = (data.get(key) or {}).get("value")
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def setting(key, field):
    value = field.get("value")
    if SECRET.search(key) or field.get("type") == "password" or isinstance(value, (dict, list)):
        value = None
    elif isinstance(value, str) and len(value) > 80:
        value = value[:77] + "…"
    return {
        "name": text(field.get("display")) or key,
        "desc": text(field.get("desc")),
        "value": value,
        "options": [o.get("display") or o.get("value") for o in field.get("options") or [] if isinstance(o, dict)][:12],
    }


def entry(files, name, template):
    data = template.get("data") or {}
    key = logo_key(files, template.get("icon")) or logo_key(files, name)
    kind = "game"
    for k, keys in KINDS.items():
        if key in keys:
            kind = k
    envs = [e.get("type") for e in template.get("supportedEnvironments") or [] if e.get("type")]
    if not envs:
        envs = [(template.get("environment") or {}).get("type") or "host"]
    req = template.get("requirements") or {}
    return {
        "id": name,
        "name": template.get("display") or name,
        "kind": kind,
        "logo": files[key][0] if key else None,
        "plate": bool(key and files[key][1]),
        "memory": number(data, "memory"),
        "disk": number(data, "disk"),
        "cpu": number(data, "cpu"),
        "port": number(data, "port"),
        "envs": envs,
        "os": req.get("os"),
        "arch": req.get("arch"),
        "settings": [setting(k, f) for k, f in data.items()
                     if isinstance(f, dict) and f.get("userEdit") and k not in ("memory", "disk", "cpu")
                     and not internal(k, f)],
        "readme": os.path.isfile(os.path.join(ROOT, name, "README.md")),
        "json": f"{name}/{name}.json",
        "source": f"{REPO}/tree/main/{name}",
    }


def main(out):
    files = logo_files()
    index = json.load(open(os.path.join(ROOT, "templates.json"), encoding="utf-8"))
    catalog = []
    for name in sorted(index):
        with open(os.path.join(ROOT, name, f"{name}.json"), encoding="utf-8") as f:
            catalog.append(entry(files, name, json.load(f)))
    catalog.sort(key=lambda t: t["name"].lower())

    payload = json.dumps({"repo": REPO, "templates": catalog}, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/")
    with open(os.path.join(SITE, "index.html"), encoding="utf-8") as f:
        page = f.read()
    if "/*CATALOG*/null" not in page:
        sys.exit("site/index.html has no /*CATALOG*/null placeholder")
    page = page.replace("/*CATALOG*/null", payload)

    os.makedirs(os.path.join(out, "icons"), exist_ok=True)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    shutil.copy(os.path.join(SITE, "emblem.svg"), out)
    used = {t["logo"] for t in catalog if t["logo"]}
    for logo in used:
        shutil.copy(os.path.join(SITE, "icons", logo), os.path.join(out, "icons", logo))
    missing = [t["id"] for t in catalog if not t["logo"]]
    print(f"catalogue: {len(catalog)} templates, {len(used)} logos" + (f", no logo: {', '.join(missing)}" if missing else ""))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "public"))
