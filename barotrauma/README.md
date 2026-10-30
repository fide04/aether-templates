# Barotrauma

Installs the Barotrauma dedicated server (Steam app 1026340) and runs `DedicatedServer`.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (27015) | UDP | Game, the one players connect to |
| `queryport` (27016) | UDP | Steam query, used by the server browser |

## Settings

- **Server Name, Server Password, Max Players, Public Server and both ports** are written into
  `serversettings.xml` (attributes `name`, `password`, `maxplayers`, `public`, `port`,
  `queryport`) before every start, so changes apply on the next restart.
- The file is created with sensible defaults the first time, and every other setting in it
  (game mode, respawns, traitors, karma...) is kept. Stop the server before editing it, because
  the game saves its settings back to the file.
- Admins: give yourself a rank from the server console, for example `giverank <name> admin`.

## Requirements and caveats

- Linux, x86-64 only.
- The server runs with `DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1`, so it does not need the ICU
  library (the Steam docker image has none). On the host environment you can also install
  `libicu` instead.
- The install creates `~/.local/share/Daedalic Entertainment GmbH/Barotrauma` inside the server
  folder (the game fails to start without it, see LinuxGSM's `fix_bt.sh`).
- Values must not contain double quotes (`"`), which would break the XML attribute.
- Stopping sends `exit` to the console.

Defaults (app id, ports, settings file and its contents, stop command) follow LinuxGSM's
[`btserver` config](https://github.com/GameServerManagers/LinuxGSM/blob/master/lgsm/config-default/config-lgsm/btserver/_default.cfg),
[`fix_bt.sh`](https://github.com/GameServerManagers/LinuxGSM/blob/master/lgsm/modules/fix_bt.sh)
and its [serversettings.xml template](https://github.com/GameServerManagers/Game-Server-Configs/blob/main/bt/serversettings.xml);
the binary name `DedicatedServer` follows the
[Pelican egg](https://github.com/pelican-eggs/games-steamcmd/tree/main/barotrauma).
