# MongoDB

Runs a MongoDB server from the official `mongo:<version>` image. Docker only.

## First start

The first start creates the database files in `data/` in the server folder and the **Root User** with
**Root Password** in the `admin` database. Authentication is always on. Later starts reuse `data/`, so
the data survives restarts, reinstalls and image updates.

## Connecting

| Setting | Value |
|---------|-------|
| Host | the address of the node |
| Port | `port` (27017) |
| User / password | **Root User** (`admin`) and **Root Password** |
| Auth database | `admin` |

For example `mongodb://admin:<password>@<node-address>:27017/?authSource=admin`. Creating a separate
user per app (`db.createUser`) is a good idea.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (27017) | TCP | MongoDB protocol |

## Caveats

- The root user and password are only applied when `data/` is created. To change the password later
  use `db.changeUserPassword()` in `mongosh` and update the panel value.
- MongoDB 8 does not start on Linux kernel 6.19 and newer (MongoDB issue
  [SERVER-121912](https://jira.mongodb.org/browse/SERVER-121912)): 8.0 refuses to start and 8.2
  crashes on the first connection. MongoDB 7 is the default until MongoDB fixes it; check the
  kernel with `uname -r` before choosing 8.
- Upgrade one major version at a time (7 to 8) and do not go back to an older version with
  existing data.
- MongoDB needs a CPU with AVX on x86-64, or ARMv8.2-A on ARM (Raspberry Pi 4 and older are not
  supported).
- Do not edit or delete files in `data/` while the server runs. A file backup of a running database
  can be inconsistent; stop the server first or keep `mongodump` exports.
- Stopping sends SIGTERM, which shuts MongoDB down cleanly.
