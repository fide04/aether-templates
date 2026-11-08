# n8n

Runs [n8n](https://n8n.io), the workflow automation tool, from the official `n8nio/n8n:<version>`
image. Docker only.

## First start

Open `http://<node-address>:<port>/` (5678) and create the owner account. Everything n8n keeps
(the SQLite database, the encryption key in `config`, community nodes, binary data) is in `.n8n/`
in the server folder, so it survives restarts, reinstalls and image updates. Reinstalling only creates `.n8n/` if it is missing and downloads the image again.

## Settings

| Variable | Use |
|----------|-----|
| **n8n Version** | Image tag: `stable` (newest release), `beta`, or an exact version such as `2.46.6`. Reinstalling downloads the newest image of the tag again (a restart keeps the one already downloaded). n8n migrates the database forward on start; going back to an older version is not supported, so back up `.n8n/` (or the PostgreSQL database) first |
| **Public URL** | The address people and webhooks use, for example `https://n8n.example.com/`. It is the base of the webhook URLs n8n shows (`WEBHOOK_URL`) and of the links in its emails (`N8N_EDITOR_BASE_URL`). Empty shows `http://localhost:5678/`, which only works on the node itself |
| **Behind an HTTPS Reverse Proxy** | On: the login cookie is sent over HTTPS only (`N8N_SECURE_COOKIE=true`) and n8n trusts one proxy's `X-Forwarded-For` (`N8N_PROXY_HOPS=1`). Off (default): you can log in over plain `http://<node-address>:5678/`. Turn it on together with an `https://` **Public URL** |
| **Timezone** | `GENERIC_TIMEZONE` and `TZ`: when Schedule Trigger nodes fire and how date nodes read times |
| **Encryption Key** | `N8N_ENCRYPTION_KEY`, which encrypts the saved credentials. Empty: n8n creates one on first start in `.n8n/config`. Set it only when moving an existing n8n here, with the key it used there |
| **Database** | `sqlite` (a file in `.n8n/`) or `postgresdb`. For PostgreSQL fill in host, port, database, user and password; the database must exist. A PostgreSQL server made with the PostgreSQL template works: use the node address and its port |

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (5678) | TCP | Editor, REST API and webhooks (HTTP) |

## Caveats

- **Keep the encryption key.** Without `.n8n/config` (or the same **Encryption Key**) the saved
  credentials cannot be decrypted. Back up `.n8n/` with the server's backups.
- **Moving from SQLite to PostgreSQL** does not move the data. Export the workflows and
  credentials first (`n8n export:workflow --all` and `n8n export:credentials --all --decrypted`
  in an n8n of the same version) and import them into the new one.
- **HTTPS** needs a reverse proxy (Nginx, Caddy, Cloudflare Tunnel) in front of the port; n8n here
  serves plain HTTP. Webhooks from services such as Telegram or Stripe need the HTTPS **Public URL**.
- **Code node**: JavaScript runs in n8n's internal task runner. Python in the Code node needs n8n's
  external runner image (`n8nio/runners`), which this template does not start.
- Stopping sends SIGTERM: n8n stops taking new executions and waits for the running ones (up to
  30 seconds) before it exits.
- Old executions are pruned by n8n itself (default: older than 14 days).
