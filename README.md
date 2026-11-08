# Templates

To add a template to this repository, please make a pull request following the existing location structure of the other templates.

Make sure to include a `README.md` file in your template's directory to document any prerequisites, workarounds, or caveats.

Please see [this documentation](https://docs.skypanel.app/en/latest/templates/templates.html) for instructions on how to create your own template.

# Formattng rules

Order of fields:
- Type (required)
- Display (required)
- Data
- Install
- Run (required)
  - Command (required)
  - Stop
  - Stop Code
  - Environment variables
  - Pre
  - Post
- Environment (required)
- Supported environments (matches environment, required)
- Requirements

Type must be lowercase
Display must include if the environment is docker via (Docker)
File is spaced using 2 spaces
Type of operations must be the first line in the object

# Checks

Every pull request runs `tools/validate.py` (see `.github/workflows/validate.yml`). It fails when
`templates.json` and the folders do not match, a template breaks `spec.json`, a template uses a
third-party Docker image (use `ghcr.io/aether-panel/*` or the official image), or a default port is
one the panel uses (8080, 8081, 5657, 3307). Known problems waiting for a fix are listed in
`tools/pending.txt`; remove the line in the change that fixes it.

Run it locally with `pip install jsonschema && python3 tools/validate.py`.

# Publishing

templates.aetherpanel.es is served by Cloudflare Pages from the `main` branch of this repository.
On every push Pages runs `sh tools/build.sh`: it runs the check above and copies `templates.json`
and each template folder to `public/`, which is what the site serves. A push that fails the check
is not published; the site keeps the previous version. A merge to `main` is live within a minute or
two, and every pull request gets its own preview address.
