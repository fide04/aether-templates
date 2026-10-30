# Palworld Dedicated Server

Installs the Palworld dedicated server (Steam app 2394010) and runs `PalServer.sh`.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (8211) | UDP | Game, the one players connect to |
| `queryport` (27015) | UDP | Steam query, only needed for the community server list |

## Settings

- **Server Name, Server Password, Admin Password, Max Players and the game port** are written into
  `Pal/Saved/Config/LinuxServer/PalWorldSettings.ini` before every start, so changing them in the
  panel takes effect on the next restart.
- **Every other world setting** (EXP rate, day length, death penalty...) is edited directly in that
  file and is never overwritten. Copy the lines you want from `DefaultPalWorldSettings.ini` in the
  server root into the `OptionSettings=(...)` line.
- **Community Server** adds `-publiclobby`, which lists the server in the in-game community browser.

## Requirements and caveats

- Linux, x86-64 only (there is no ARM build of the server).
- Palworld is memory hungry: 8 GB is the bare minimum, 16 GB is recommended for a handful of
  players, more for full servers or long-running worlds.
- Values must not contain double quotes (`"`), which would break the ini line.
- Stopping sends SIGINT, which makes the server save before it exits.
