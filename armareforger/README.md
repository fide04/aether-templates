# Arma Reforger

Installs the Arma Reforger dedicated server (Steam app 1874900) and runs `ArmaReforgerServer`
with `config.json` and a `profile` folder in the server root.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (2001) | UDP | Game, the one players connect to |
| `queryport` (17777) | UDP | Steam query (A2S) |
| `rconport` (19999) | UDP | RCON (BattlEye RCon protocol) |

## Settings

- `config.json` is written the first time with the panel values and the defaults from
  LinuxGSM. Later edits are kept: before every start the panel only rewrites these values in
  place:
  - **Server Name, Server Password, Admin Password** (`game.name`, `game.password`,
    `game.passwordAdmin`), **Max Players**, **Scenario ID**, **Visible**;
  - **RCON port and password** (`rcon.port`, `rcon.password`);
  - **Public IP** (`publicAddress`) and the ports (`bindPort`, `publicPort`, `a2s.port`). The
    game and query ports are also passed as `-bindPort` and `-a2sPort`.
- Keep the key order the file was written with for `game` (`name`, `password`,
  `passwordAdmin`), `rcon` (`port`, `password`) and `a2s` (`port`): the panel finds those values
  by their position, and if you reorder them the panel stops updating them (the server still
  starts).
- Mods, admins, `gameProperties` and anything else are edited directly in `config.json`.
- **Scenario ID**: the server prints every available scenario to the log at startup
  (`-listScenarios`). The default is Conflict on Everon.
- **Max FPS** caps the server frame rate. Bohemia strongly recommends 60 to 120.
- **RCON permission** is `monitor` (read-only commands). Change it to `admin` in `config.json` if
  you want RCON to be able to kick, ban and so on.

## Requirements and caveats

- Linux, x86-64 only. The server needs `libcurl4` (the docker environment uses
  `ghcr.io/aether-panel/steamcmd`, which has it).
- **Docker or NAT**: Bohemia's wiki warns that by default the server registers the container's
  IP, so players fail to connect. Put the machine's public IP in **Public IP** in that case.
- The RCON password needs at least 3 characters and no spaces, or the server refuses to start.
- Values must not contain double quotes (`"`) or backslashes, which would break the JSON.
- Stopping sends SIGINT, which shuts the server down cleanly.

Defaults (app id, ports, start parameters, config contents) follow LinuxGSM's
[`armarserver` config](https://github.com/GameServerManagers/LinuxGSM/blob/master/lgsm/config-default/config-lgsm/armarserver/_default.cfg)
and [server.json template](https://github.com/GameServerManagers/Game-Server-Configs/blob/main/armar/server.json),
and Bohemia's [Server Hosting](https://community.bistudio.com/wiki/Arma_Reforger:Server_Hosting)
and [Startup Parameters](https://community.bistudio.com/wiki/Arma_Reforger:Startup_Parameters) pages.
