# Java App

Runs any Java program packaged as a jar: a Discord bot (JDA, Javacord), a Spring Boot app, a tool.
In Docker it uses the Eclipse Temurin image of the chosen version (`eclipse-temurin:<version>`); on
the host environment the panel downloads that Temurin release itself.

## Getting the jar onto the server

- **Upload it** with the file manager and set **Jar File** to its name (default `app.jar`), or
- **Jar Download URL**: a direct link to a jar. The install downloads it and saves it as the jar
  file; reinstalling downloads it again (handy for updates).

## Starting

`java -Xmx<memory>M <Extra JVM Flags> -jar <Jar File>`

- The heap limit (`-Xmx`) is the server memory. The JVM needs some memory beyond the heap, so on
  small servers put a lower `-Xmx` in **Extra JVM Flags** (it overrides the first one), for example
  `-Xmx850M` for a 1024 MB server.
- The app gets the port in the `PORT` environment variable.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (8080) | TCP | Only for apps that serve HTTP. Discord bots do not need it |

## Caveats

- Stopping sends SIGTERM, which runs the app's shutdown hooks.
- Jar file names and flags cannot contain spaces or double quotes.
- With **Jar Download URL** the file is saved under the name the server sends; if that is not the
  name at the end of the URL, the rename to **Jar File** fails and the install says so.
