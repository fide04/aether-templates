# Hytale

Downloads the Hytale server with Hypixel's official **Hytale Downloader** and runs
`Server/HytaleServer.jar` with Java 25 from the server root.

## Two one-time Hytale logins

Hytale has no anonymous download and the server has to be signed in to a Hytale account that
owns the game. Both logins use a link and a code, so nothing has to be typed in the panel for
the first one, and each is needed only once:

1. **Downloader (during the install).** The install console shows a login link and code. Open the
   link, sign in and approve within 15 minutes; the install then carries on by itself. The login
   is saved in `.hytale-downloader-credentials.json`, so reinstalls do not ask again. If it
   expires, delete that file and reinstall.
2. **Server (first start).** When the server has booted, type `/auth login device` in the
   console, open the link it prints (`accounts.hytale.com/device`) and enter the code within
   15 minutes. The `config.json` written by the panel stores this login encrypted
   (`AuthCredentialStore: Encrypted`), so it survives restarts; check with `/auth status`.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (5520) | UDP | Game (QUIC), the one players connect to. No TCP port is needed |

## Settings

- **Server Name, Server Password and Max Players** are written into `config.json`
  (`ServerName`, `Password`, `MaxPlayers`) before every start. The file is created the first
  time and every other setting in it is kept. Stop the server before editing it: the server
  writes it back while running.
- `MaxViewRadius` starts at 12 chunks, Hypixel's recommended maximum; view distance is what
  uses most of the memory.
- **Patchline** picks the release or pre-release build. Players must be on the same one.
- **Use AOT Cache** starts Java with `Server/HytaleServer.aot`, which shortens boot time.
- Worlds and player data are in `universe/`, plugins in `mods/`, logs in `logs/`.

## Updating

Client and server must run the exact same version. After a Hytale update, reinstall the
server: it downloads the current build (the saved downloader login is reused) and keeps
`config.json`, `universe/`, `mods/` and the other data, which live outside `Server/`.

## Requirements and caveats

- Linux, x86-64 only: the server itself runs on arm64 too, but the official downloader has no
  Linux arm64 build.
- Java 25: the host environment downloads it with the panel; the docker environment uses
  `eclipse-temurin:25-jre`.
- At least 4 GB of memory.
- Values must not contain double quotes (`"`) or backslashes, which would break the JSON.
- Hytale is in early access: file names and options may change between updates.
- Stopping sends `stop` to the console.

Sources: LinuxGSM's [`hytserver` config](https://github.com/GameServerManagers/LinuxGSM/blob/master/lgsm/config-default/config-lgsm/hytserver/_default.cfg),
[`update_hyt.sh`](https://github.com/GameServerManagers/LinuxGSM/blob/master/lgsm/modules/update_hyt.sh)
(downloader URL, flags and credentials file, `stop` command) and
[config.json template](https://github.com/GameServerManagers/Game-Server-Configs/blob/main/hyt/config.json),
and [GameServerKings' Hytale guide](https://www.gameserverkings.com/knowledge-base/hytale/hytale-dedicated-server/),
which quotes Hypixel's server manual (Java 25, UDP 5520, `/auth login device`, persistence).
