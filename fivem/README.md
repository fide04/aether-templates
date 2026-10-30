# FiveM (GTA V)

Installs the **recommended** FXServer build for Linux, as published by Cfx.re at
<https://changelogs-live.fivem.net/api/changelog/versions/linux/server>, and runs it.

## License key (required)

FXServer will not start without a license key. Create one at <https://portal.cfx.re> →
*Server Registration Keys* and paste it into **License Key**.

## Two ways to run it

### With txAdmin (default)

`txadmin` on. FXServer starts txAdmin, the official web control panel, on **txAdmin Port** (40120).
The first time, open `http://<server-address>:40120`, enter the PIN printed in the console, and
txAdmin walks through creating the server from a recipe (vanilla, ESX, QBCore...). txAdmin then
owns `server.cfg`, the resources and restarts.

### Plain FXServer

`txadmin` off. The install also downloads the default resources
([cfx-server-data](https://github.com/citizenfx/cfx-server-data)) and writes a minimal `server.cfg`
with the name, slots and license key from the panel. Edit `server.cfg` to add resources.
The file is only written when it does not exist, so later edits are kept.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (30120) | TCP and UDP | Game |
| `txadminport` (40120) | TCP | txAdmin web panel (txAdmin mode only) |

## Requirements and caveats

- Linux, x86-64 only. The Linux build runs inside `proot`, so the host must allow `ptrace`.
- More than 48 players needs OneSync and a Cfx.re subscription tier that allows it.
- Updating FXServer: reinstall the server; it fetches the build that is recommended at that moment
  and keeps `server.cfg`, `resources` and the txAdmin data.
