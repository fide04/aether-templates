# Core Keeper

Installs the Core Keeper dedicated server (Steam app 1963720) and runs `CoreKeeperServer`
inside a virtual X display (Xvfb), which the Linux server needs even in batch mode.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (27015) | UDP | Game, only with **Direct Connect** on |

## Two ways to join

- **Direct Connect** on (default): the server listens on `port` and players join with
  IP, port and password. This is also what crossplay with Epic, GOG and the Microsoft Store
  needs. The address and password are written to `GameInfo.txt` in the server root.
- **Direct Connect** off: the server uses Steam's relay. No port is opened and only Steam
  players can join, by entering the Game ID from `GameID.txt` (or the console log).

## Settings

All settings are passed on the command line before every start: **Server Name** (world name),
**Server Password** (Direct Connect only, up to 28 characters; if empty, the game makes up a
random one and writes it to `GameInfo.txt`), **Max Players**, **World Slot** (0 to 29),
**World Seed** and **World Mode** (both only used when the world is created) and **Game ID**.

Worlds and `ServerConfig.json` are stored in `gamedata/`; the log is `logs/CoreKeeperServer.log`
and is shown in the console.

## How it starts

Before every start the panel writes `aether-corekeeper.sh` (edits to it are overwritten). It
starts Xvfb on a display derived from the port, starts the server with the panel settings
(passed as `CK_*` environment variables, never through a shell), streams the log to the
console and, when the server stops, stops Xvfb too.

## Requirements and caveats

- Linux, x86-64 only.
- On the host environment the machine needs `xvfb` and `libxi6` (Debian/Ubuntu:
  `apt install xvfb libxi6`).
- The docker environment uses the panel's own `ghcr.io/aether-panel/steamcmd` image, which ships
  SteamCMD, its 32-bit libraries, Xvfb and `libxi6` (the plain `steamcmd/steamcmd` image has no
  Xvfb). It needs the image built from Aether Panel 2.0 or later.
- Stopping sends SIGINT; the launcher passes it to the server as SIGTERM, which saves the world
  and exits.

Defaults (app id, `-batchmode`, the need for Xvfb and `libxi6`, `-datapath`) follow LinuxGSM's
[`ckserver` config](https://github.com/GameServerManagers/LinuxGSM/blob/master/lgsm/config-default/config-lgsm/ckserver/_default.cfg)
and [dependency list](https://github.com/GameServerManagers/LinuxGSM/blob/master/lgsm/data/ubuntu-24.04.csv);
the launch options, the Xvfb flags and the stop handling follow the
[Pelican egg](https://github.com/pelican-eggs/games-steamcmd/tree/main/core_keeper) and
[escapingnetwork/core-keeper-dedicated](https://github.com/escapingnetwork/core-keeper-dedicated).
