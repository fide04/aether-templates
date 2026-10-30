# Killing Floor 2

Installs the Killing Floor 2 dedicated server (Steam app 232130) and runs
`Binaries/Win64/KFGameSteamServer.bin.x86_64` (the Linux binary really lives in that folder).

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (7777) | UDP | Game, the one players connect to |
| `queryport` (27015) | UDP | Steam query, used by the server browser |
| `webadminport` (8080) | TCP | WebAdmin web panel, only when **WebAdmin** is on |

## Settings

- **Map, Game Mode, Difficulty, Max Players and the ports** go on the command line, so they
  apply on every start.
- **Server Name, Server Password and Admin Password** are written into
  `KFGame/Config/LinuxServer-KFGame.ini` before every start (`ServerName`, `GamePassword`,
  `AdminPassword`). **WebAdmin** and its port are written into `KFGame/Config/KFWeb.ini`
  (`bEnabled`, `ListenPort`). Log in to WebAdmin as `admin` with the admin password.
- KF2 only creates those ini files the first time it runs, so the install starts the server
  once for up to 90 seconds to generate them (as LinuxGSM does after installing).
- **Max Players**: Survival, Weekly and Endless allow up to 6, Versus up to 12.
- Every other setting (game length, map cycle, workshop maps...) is edited in those ini files
  and is kept.

## Requirements and caveats

- Linux, x86-64 only.
- Values must not contain line breaks. The password must not contain `?`.
- Stopping sends SIGINT, which shuts the server down cleanly.

Defaults (app id, executable path, query port, map) follow LinuxGSM's
[`kf2server` config](https://github.com/GameServerManagers/LinuxGSM/blob/master/lgsm/config-default/config-lgsm/kf2server/_default.cfg),
[`fix_kf2.sh`](https://github.com/GameServerManagers/LinuxGSM/blob/master/lgsm/modules/fix_kf2.sh)
and its [ini templates](https://github.com/GameServerManagers/Game-Server-Configs/tree/main/kf2);
the URL options (`?Port=`, `?Difficulty=`) follow the
[Pelican egg](https://github.com/pelican-eggs/games-steamcmd/tree/main/killing_floor_2).
