# Left 4 Dead 2

Installs the Left 4 Dead 2 dedicated server (Steam app 222860) and runs it with `srcds_run`.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (27015) | UDP | Game and Steam query, the one players connect to |
| `port` (27015) | TCP | RCON (only when an RCON password is set) |

`clientport` (27005) is the port srcds uses for its own outgoing connections. It does not need
to be opened, it only has to be different on each server of the same machine.

## Settings

- **Server Name, Server Password and RCON Password** are written to `left4dead2/cfg/aether.cfg`
  before every start, so changes in the panel apply on the next restart. The server runs with
  `+servercfgfile aether.cfg`, and that file first runs `exec server.cfg` and then sets the
  panel values, so the panel always wins for those three.
- **Everything else** goes in `left4dead2/cfg/server.cfg`. The install writes a starter file
  (lobby-free connections, logging, voice) only when it does not exist, and your edits are kept.
- **Map** is the map loaded at startup, for example `c1m1_hotel` or `c5m1_waterfront`.
- **Max Players**: the unmodded game supports 4 players in campaign and 8 in versus. More
  slots need a plugin such as L4DToolZ.

## Requirements and caveats

- Linux, x86-64 only. srcds for this game is a 32-bit program: on the host environment the
  machine needs the 32-bit runtime (`lib32gcc-s1`, `lib32stdc++6` on Debian/Ubuntu). The docker
  environment uses `ghcr.io/aether-panel/steamcmd`, which already has it.
- `sv_allow_lobby_connect_only 0` in the starter `server.cfg` lets players join with
  `connect ip:port` from the console; remove it if you only want lobby joins.
- Values must not contain double quotes (`"`), which would break the cfg line.
- Stopping sends `quit` to the console.

Defaults (app id, `srcds_run -game left4dead2`, ports, map) follow LinuxGSM's
[`l4d2server` config](https://github.com/GameServerManagers/LinuxGSM/blob/master/lgsm/config-default/config-lgsm/l4d2server/_default.cfg)
and its [server.cfg template](https://github.com/GameServerManagers/Game-Server-Configs/blob/main/l4d2/server.cfg).
