# MariaDB

Runs a MariaDB server from the official `mariadb:<version>` image, for bots and apps that need a
MySQL-compatible database. Docker only.

## First start

The first start creates the database files in `data/` in the server folder, sets the root password,
and creates **Database** and **User** (with **User Password** and full access to that database) when
they are set. Later starts reuse `data/`, so the data survives restarts, reinstalls and image
updates.

## Connecting

| Setting | Value |
|---------|-------|
| Host | the address of the node |
| Port | `port` (3306) |
| User / password | **User** and **User Password**, or `root` and **Root Password** |
| Database | **Database** (`app`) |

For example `mysql://app:<password>@<node-address>:3306/app`.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (3306) | TCP | MySQL protocol |

## Caveats

- The passwords, database and user are only applied when `data/` is created. To change them later,
  use SQL (`ALTER USER ...`) and then update the panel values so they match.
- Upgrading **MariaDB Version** is fine, the upgrade runs automatically on start. Going back to an
  older version with existing data is not supported.
- Do not edit or delete files in `data/` while the server runs. A file backup of a running database
  can be inconsistent; stop the server first or keep `mariadb-dump` exports.
- Tuning options go in **Extra Server Arguments**, for example
  `--innodb-buffer-pool-size=512M --max-connections=200`.
- Stopping sends SIGTERM, which shuts MariaDB down cleanly.
