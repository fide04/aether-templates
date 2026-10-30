# Necesse

Installs the Necesse dedicated server (Steam app 1169370) and runs `Server.jar` with the Java
runtime the server ships in `jre/`, without the GUI (`-nogui`).

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (14159) | UDP | Game, the one players connect to |

## Settings

- The server runs with `-localdir`, so its settings (`cfg/server.cfg`), saves (`saves/`) and
  logs (`logs/`) stay in the server folder.
- **Port, Max Players, Server Password and Message of the Day** are written into
  `cfg/server.cfg` before every start (`port`, `slots`, `password`, `MOTD`). The file is
  created the first time and every other setting in it is kept.
- **World Name** is passed with `-world`. If no world with that name exists, a new one is
  created.
- Owner and admin permissions are given with the `permissions` command in the server console
  (`help` lists the commands).

## Requirements and caveats

- Linux, x86-64 only.
- The password must not contain commas and the message of the day must not contain double
  quotes, which would break the line in `server.cfg`.
- Stopping sends `stop` to the console, which saves the world and exits.

Defaults (app id, port, `-localdir -world`, `server.cfg` contents) follow LinuxGSM's
[`necserver` config](https://github.com/GameServerManagers/LinuxGSM/blob/master/lgsm/config-default/config-lgsm/necserver/_default.cfg)
and [server.cfg template](https://github.com/GameServerManagers/Game-Server-Configs/blob/main/nec/server.cfg),
the [Necesse wiki](https://necessewiki.com/Multiplayer) (UDP 14159, launch options) and the
[Pelican egg](https://github.com/pelican-eggs/games-steamcmd/tree/main/necesse) (bundled
`jre/bin/java`, `stop` command).
