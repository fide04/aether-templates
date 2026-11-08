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

templates.aetherpanel.es is served by Cloudflare Pages (project `aether-templates`), published by
`.github/workflows/check-and-publish.yml`:

- **Every pull request** runs the format check (`tools/validate.py`), the tests of the security
  check, and the **security check** (`tools/security_check.py`) on the templates it changes. The
  security report is left as a comment on the pull request.
- **Every push to `main`** runs the same checks on what it changed and, only if they pass, builds
  `public/` (`tools/build.sh`) and publishes it with Wrangler. A failed check publishes nothing; the
  site keeps the previous version.

## Security check

Everything a template runs or downloads (install, uninstall, pre and post steps, start and stop
commands, files it writes, environment variables, Docker settings) is checked by rules, only for
what is new or changed:

- **Block** (the check fails): reverse shells, a download piped into a shell, hidden code
  (base64 and the like), crypto miners, wiping the disk, touching the host (users, cron, firewall,
  Docker socket), a privileged container, `LD_PRELOAD`.
- **Review**: a download from a host outside the trusted list or from a GitHub project outside
  the trusted projects (`TRUSTED_GITHUB`: the vendors' own, such as `lavalink-devs/*`), `sudo`, background processes,
  `eval`, encoded text, a download from a raw IP, unusual Docker settings, environment variables
  that change how programs run, paths with `..`. These go to an AI on Cloudflare Workers AI
  (`@cf/meta/llama-3.3-70b-instruct-fp8-fast`, free up to 10,000 neurons a day; a review costs a
  few hundred), which answers safe, unsafe or unsure. Only "safe" passes. Without its
  credentials, or when the AI cannot answer, they fail and need a person.

A review finding a person has checked and accepts goes in `tools/security-allow.txt` (the report
prints the exact line). Blocks cannot be accepted: change the template.

Run it locally with `pip install -r tools/requirements.txt` and
`python3 tools/security_check.py --base origin/main` (or `--all`); tests with
`python3 -m unittest discover -s tools -p "test_*.py"`.

## Repository secrets

| Secret | Used for |
|---|---|
| `CLOUDFLARE_API_TOKEN` | Publishing (**Account → Cloudflare Pages → Edit**) and the AI review (**Workers AI → Read** and **Edit**) |
| `CLOUDFLARE_ACCOUNT_ID` | The Cloudflare account that has the project and Workers AI |
| `CLOUDFLARE_AI_TOKEN` | Optional: a separate token for the AI review, used instead of `CLOUDFLARE_API_TOKEN` |
