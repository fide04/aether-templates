# Bun App

Runs a JavaScript or TypeScript application with [Bun](https://bun.sh): a Discord bot, an API, any
program that runs on Bun. In Docker it uses the official `oven/bun:<version>` image.

## Getting your code onto the server

- **Upload it** with the file manager, or
- **Git Repository**: the install downloads the repository into the server folder (latest commit of
  **Git Branch**, or of the default branch when it is empty). **Reinstall** pulls the latest commit
  again. Files tracked by the repository are replaced by the repository version; untracked files
  (`.env`, databases, logs) are kept. For a private repository put a personal access token in
  **Git Access Token** (GitHub or GitLab, read access is enough).
- With no code and no repository, the install writes a small placeholder `index.ts` that prints a
  message, so a fresh server starts and shows what to do next.

## Starting

- **Start File** (`index.ts`) is run with `bun run`. Bun loads `.env` files by itself.
- **Use bun run start** runs the `start` script of `package.json` instead.
- **Install Dependencies on Start** runs `bun install` before every start (on by default). The install
  step does the same once.
- **Bun Version** is the image tag: `1` follows the newest 1.x, `latest`, `canary`, or an exact
  version such as `1.3.0`.
- The app gets the port in the `PORT` environment variable.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (3000) | TCP | Only for apps that serve HTTP. Discord bots do not need it |

## Caveats

- Stopping sends SIGTERM. The container runs with an init process, so the app exits even without a
  signal handler.
- The Bun image has no git, so when a repository is set the install step adds git to its own
  temporary container with `apt-get` (a few seconds). This needs the containers to run as root, which
  is how the panel runs them when it is deployed with Docker.
- Bun blocks dependency postinstall scripts unless the package is in `trustedDependencies` of
  `package.json`.
- Host environment: uses the `bun` installed on the machine (the version setting is ignored) and needs
  `bash`, and `git` when a repository is set.
