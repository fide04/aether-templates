# PostgreSQL

Runs a PostgreSQL server from the official `postgres:<version>` image. Docker only.

## First start

The first start creates the cluster in `data/` in the server folder (`PGDATA=/SkyPanel/data`), the
**Superuser** with **Password**, and **Database**. Later starts reuse `data/`, so the data survives
restarts, reinstalls and image updates.

## Connecting

| Setting | Value |
|---------|-------|
| Host | the address of the node |
| Port | `port` (5432) |
| User / password | **Superuser** (`postgres`) and **Password** |
| Database | **Database** (`app`) |

For example `postgresql://postgres:<password>@<node-address>:5432/app`. Remote connections use
scram-sha-256 password authentication.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (5432) | TCP | PostgreSQL protocol |

## Caveats

- The superuser, password and database are only applied when `data/` is created. To change the
  password later run `ALTER USER postgres PASSWORD '...'` and update the panel value.
- `data/` only starts with the major version that created it. To move to a newer major version, dump
  the data (`pg_dumpall`), create a new server with the new version and restore it there.
- Do not edit or delete files in `data/` while the server runs. A file backup of a running database
  can be inconsistent; stop the server first or keep `pg_dump` exports.
- Settings go in **Extra Server Arguments** as `-c name=value`, for example
  `-c max_connections=200 -c shared_buffers=256MB`, or in `data/postgresql.conf`.
- Stopping sends SIGINT (fast shutdown): open connections are closed and the data is flushed.
