# Mordhau

Installs the Mordhau dedicated server (Steam app 629800) and runs
`Mordhau/Binaries/Linux/MordhauServer-Linux-Shipping`.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (7777) | UDP | Game, the one players connect to |
| `beaconport` (15000) | UDP | Beacon |
| `queryport` (27015) | UDP | Steam query, used by the server browser |

## Settings

- **Map** and the ports go on the command line.
- **Server Name, Server Password, Admin Password and Max Players** are written into
  `Mordhau/Saved/Config/LinuxServer/Game.ini` (`ServerName`, `ServerPassword`, `AdminPassword`,
  `MaxSlots`) before every start, so changes apply on the next restart.
- `Game.ini` is created the first time with LinuxGSM's defaults, including the full map
  rotation. Every other setting in it (map rotation, damage, respawn times, RCON...) is kept.
- Log in as admin from the in-game console with `adminlogin <password>`.

## Requirements and caveats

- Linux, x86-64 only.
- RCON is off (`RconPort=0`). To use it, set `RconPort` and `RconPassword` in `Game.ini` and
  open that port (TCP).
- Values must not contain line breaks.
- Stopping sends SIGINT, which shuts the server down cleanly.

Defaults (app id, executable, ports, start parameters, map, `Game.ini` contents) follow
LinuxGSM's [`mhserver` config](https://github.com/GameServerManagers/LinuxGSM/blob/master/lgsm/config-default/config-lgsm/mhserver/_default.cfg)
and [Game.ini template](https://github.com/GameServerManagers/Game-Server-Configs/blob/main/mh/Game.ini).
