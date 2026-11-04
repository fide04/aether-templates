# Java App

Runs any Java program packaged as a jar: a Discord bot (JDA, Javacord), a Spring Boot app, a tool.
It can also build the jar from source with Maven or Gradle. In Docker it uses the Eclipse Temurin
image of the chosen version (`eclipse-temurin:<version>`, a full JDK); on the host environment the
panel downloads that Temurin JDK itself.

## Getting the jar onto the server

- **Upload it** with the file manager and set **Jar File** to its name (default `app.jar`), or
- **Jar Download URL**: a direct link to a jar. The install downloads it and saves it as the jar
  file; reinstalling downloads it again (handy for updates), or
- **Git Repository** with a **Build Tool**: the install downloads the repository into the server
  folder (latest commit of **Git Branch**, or of the default branch when it is empty) and builds it.
  **Reinstall** pulls the latest commit and builds again. Files tracked by the repository are
  replaced by the repository version; untracked files (configs, databases, logs) are kept. For a
  private repository put a personal access token in **Git Access Token** (GitHub or GitLab, read
  access is enough). Uploaded sources are built the same way.

## Building

**Build Tool** (`None` by default: the jar is run as it is):

| Build Tool | Runs | Default **Build Arguments** | Jar looked for in |
|------------|------|-----------------------------|-------------------|
| Maven | `./mvnw` when the project has the wrapper, otherwise Maven 3.9 | `package -DskipTests -Dcheckstyle.skip` | `target/`, `*/target/` |
| Gradle | `./gradlew` when the project has the wrapper, otherwise Gradle 9 (Gradle 8.14 on Java 8 and 11) | `assemble` | `build/libs/`, `*/build/libs/` |

- The build runs on install; with **Build on Start** also before every start.
- Without a wrapper, the official Maven (archive.apache.org) or Gradle (services.gradle.org)
  release is downloaded into `.aether/` in the server folder once.
- Dependencies stay in `.aether/` too (the Maven repository, `GRADLE_USER_HOME`), so rebuilds are
  fast and the space counts against the server's disk. Gradle runs with `--no-daemon`, so nothing
  is left running next to the app.
- **Jar File** can be a pattern such as `target/*.jar`: the largest jar it matches is run, leaving
  out `-plain`, `-sources`, `-javadoc`, `-tests` and `original-` jars (the runnable Spring Boot or
  shaded jar is the largest). With a build tool, a **Jar File** that does not exist (the default
  `app.jar`, for example) is looked for in the build's output folders the same way.
- The caches are inside the project folder, so a build step that checks every file of the project
  would check them too. Checkstyle is skipped by default for that reason (Spring projects run the
  nohttp check with it over the whole folder); other such checks need their skip property in
  **Build Arguments**. Tests and checks belong in CI, not in the build that deploys the app.
- **Java Version** must be at least the version the project compiles for (`<java.version>` in
  `pom.xml`, the Gradle toolchain); Gradle cannot download a toolchain here.

## Starting

`java -Xmx<memory>M <Extra JVM Flags> -jar <Jar File>`

- The heap limit (`-Xmx`) is the server memory. The JVM needs some memory beyond the heap, so on
  small servers put a lower `-Xmx` in **Extra JVM Flags** (it overrides the first one), for example
  `-Xmx850M` for a 1024 MB server.
- The app gets the port in the `PORT` environment variable. Spring Boot does not read `PORT`: put
  `-Dserver.port=<port>` in **Extra JVM Flags** (or `server.port=${PORT}` in
  `application.properties`).

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (8090) | TCP | Only for apps that serve HTTP. Discord bots do not need it |

## Caveats

- Stopping sends SIGTERM, which runs the app's shutdown hooks. The container runs with an init
  process, so a stop during a build on start stops the build too.
- Jar file names and flags cannot contain spaces or double quotes.
- With **Jar Download URL** the file is saved under the name the server sends; if that is not the
  name at the end of the URL, the rename to **Jar File** fails and the install says so.
- Building needs memory: give the server at least 1.5 GB for a Spring Boot build.
- The Temurin image has no git, so when a repository is set the install step adds git to its own
  temporary container with `apt-get` (a few seconds).
- Host environment: needs `bash`, `curl` and `tar` for a build tool, and `git` when a repository is
  set.
