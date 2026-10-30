# Lavalink

Installs the latest [Lavalink](https://github.com/lavalink-devs/Lavalink) release (`Lavalink.jar`
from GitHub) and runs it with Java. Lavalink is the audio node that music bots (discord.js with
Shoukaku/Riffy/lavalink-client, Wavelink, Lavalink.py, JDA with Lavalink-Client...) send their audio
work to.

## Settings

- **Port** and **Password** are passed to Lavalink on every start (`SERVER_PORT` and
  `LAVALINK_SERVER_PASSWORD`), so changing them in the panel takes effect on the next restart.
- Everything else is in `application.yml`, which the install writes with sensible defaults only when
  the file does not exist yet. Your edits are kept.

## Connecting your bot

| Setting | Value |
|---------|-------|
| Host | the address of the node |
| Port | `port` (2333) |
| Password | **Password** |
| Secure (SSL) | no |

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (2333) | TCP | REST API and WebSocket the bot connects to |

## YouTube

The built-in YouTube source is deprecated and off. To play YouTube, uncomment the `plugins` block in
`application.yml` and put the latest version of
[youtube-source](https://github.com/lavalink-devs/youtube-source); Lavalink downloads the plugin into
`plugins/` on the next start. The SoundCloud, Bandcamp, Twitch, Vimeo and HTTP sources are built in;
sites change often, so keep Lavalink and its plugins up to date.

## Caveats

- Updating Lavalink: reinstall the server, it downloads the latest release and keeps
  `application.yml` and `plugins/`.
- Needs Java 17 or newer (Java 21 by default). The heap limit is the server memory.
- Stopping sends SIGTERM, Lavalink closes the players and exits.
