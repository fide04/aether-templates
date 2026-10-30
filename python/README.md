# Python App

Runs a Python application: a Discord bot (discord.py, nextcord, py-cord...), a Flask/FastAPI app or
any other Python program. In Docker it uses the official `python:<version>-slim` image.

## Getting your code onto the server

- **Upload it** with the file manager, or
- **Git Repository**: the install downloads the repository into the server folder (latest commit of
  **Git Branch**, or of the default branch when it is empty). **Reinstall** pulls the latest commit
  again. Files tracked by the repository are replaced by the repository version; untracked files
  (`.env`, databases, logs) are kept. For a private repository put a personal access token in
  **Git Access Token** (GitHub or GitLab, read access is enough).
- With no code and no repository, the install writes a small placeholder `main.py` that prints a
  message, so a fresh server starts and shows what to do next.

## Dependencies

Packages go into a virtual environment, `.venv` in the server folder, so they survive restarts and
reinstalls. When `requirements.txt` exists it is installed on install and, with **Install Requirements
on Start** (on by default), before every start too. Changing **Python Version** recreates `.venv`
on the next start.

## Starting

**Start File** (`main.py`) is run with `.venv/bin/python -u`. The app gets the port in the `PORT`
environment variable.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (8000) | TCP | Only for apps that serve HTTP (web dashboards, APIs). Discord bots do not need it |

## Caveats

- Stopping sends SIGINT (like Ctrl+C), which raises `KeyboardInterrupt`; discord.py and asyncio apps
  close cleanly on it.
- The slim image has no git, so when a repository is set the install step adds git to its own
  temporary container with `apt-get` (a few seconds). This needs the containers to run as root, which
  is how the panel runs them when it is deployed with Docker.
- Packages without wheels for the platform need a compiler, which the slim image does not have.
- Host environment: uses `python<version>` when the machine has it, otherwise `python3`. Needs `bash`,
  the `venv` module (`python3-venv` on Debian/Ubuntu), and `git` when a repository is set.
