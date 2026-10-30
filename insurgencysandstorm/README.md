# Insurgency: Sandstorm

Installs the Insurgency: Sandstorm dedicated server (Steam app 581330) and runs
`Insurgency/Binaries/Linux/InsurgencyServer-Linux-Shipping`.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (27102) | UDP | Game, the one players connect to |
| `queryport` (27131) | UDP | Steam query, used by the server browser |
| `rconport` (27015) | TCP | RCON, only when an RCON password is set |

## Settings

All settings go on the command line, so changes apply on the next start:

- **Map** and **Scenario** form the start URL (`Oilfield?Scenario=Scenario_Refinery_Push_Security`).
  The scenario has to belong to the map.
- **Max Players** and **Server Password** are URL options (`?MaxPlayers=`, `?Password=`).
- **Server Name** is `-hostname`.
- **RCON Password** turns RCON on (`-Rcon -RconPassword -RconListenPort`). Empty leaves it off.
- **GSLT Token** is passed as `-GSLTToken`. Create one at
  <https://steamcommunity.com/dev/managegameservers> for app 581320 (the game). Without it the
  server runs but is not listed in the server browser.

Map cycle, admins and game rules live in `Insurgency/Config/Server/` (`MapCycle.txt`,
`Admins.txt`) and `Insurgency/Saved/Config/LinuxServer/Game.ini`; the panel never touches them.

## Requirements and caveats

- Linux, x86-64 only.
- The server password must not contain spaces or `?`, which would break the start URL.
- Stopping sends SIGINT, which shuts the server down cleanly.

Defaults (app id, executable, ports, map, scenario, flags) follow LinuxGSM's
[`inssserver` config](https://github.com/GameServerManagers/LinuxGSM/blob/master/lgsm/config-default/config-lgsm/inssserver/_default.cfg);
`?Password=` follows hosting guides such as
[Nodecraft's](https://nodecraft.com/support/games/insurgency-sandstorm/configuring-your-sandstorm-insurgency-server).
