# Node.js App

Runs a Node.js application: a Discord bot (discord.js, Eris...), an API, a dashboard or any other
Node.js program. In Docker it uses the official `node:<version>` image; on the host environment the
panel downloads that Node.js release itself.

## Getting your code onto the server

- **Upload it** with the file manager, or
- **Git Repository**: the install downloads the repository into the server folder (latest commit of
  **Git Branch**, or of the default branch when it is empty). **Reinstall** pulls the latest commit
  again. Files tracked by the repository are replaced by the repository version; untracked files
  (`.env`, databases, logs) are kept. For a private repository put a personal access token in
  **Git Access Token** (GitHub or GitLab, read access is enough).
- With no code and no repository, the install writes a small placeholder start file that prints a
  message, so a fresh server starts and shows what to do next.

## Starting

- **Start File** (`index.js`) is run with `node`. A `.env` file in the server folder is loaded
  automatically.
- **Use npm start** runs the `start` script of `package.json` instead.
- **Install Dependencies on Start** runs `npm install` before every start (on by default), so packages
  added to `package.json` are picked up. When a `pnpm-lock.yaml` or `yarn.lock` is present, pnpm or
  yarn is used instead. The install step does the same once.
- **NODE_ENV** `production` skips `devDependencies`. Projects that compile TypeScript at start need
  `development`, or commit the built files.
- The app gets the port in the `PORT` environment variable.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (3000) | TCP | Only for apps that serve HTTP (web dashboards, APIs). Discord bots do not need it |

## Caveats

- Stopping sends SIGTERM. The container runs with an init process, so Node.js exits even when the
  app has no signal handler.
- Node.js 26 no longer ships corepack; pnpm and yarn are then run through `npx`.
- Host environment: needs `bash`, and `git` when a repository is set.
- The `node` images are about 1 GB, the first install takes a while to download it.
