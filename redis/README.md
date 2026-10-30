# Redis

Runs a Redis server from the official `redis:<version>` image, for caches, queues, rate limits and
sessions. Docker only. Redis 8 includes the JSON, Search, TimeSeries and Bloom modules.

## Data

Redis keeps the data in memory and saves it to `data/` in the server folder: an append-only file
(`appendonlydir/`, written every second) and snapshots (`dump.rdb`). The data is loaded again on
every start, so it survives restarts and reinstalls.

## Connecting

| Setting | Value |
|---------|-------|
| Host | the address of the node |
| Port | `port` (6379) |
| Password | **Password** (no user name, or `default`) |

For example `redis://:<password>@<node-address>:6379`.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (6379) | TCP | Redis protocol |

## Caveats

- **Password** is required and is applied on every start, so changing it in the panel takes effect
  on the next restart.
- Redis may use at most 80% of the server memory (`maxmemory`). When it is full, writes fail with an
  error instead of the server being killed. For a pure cache add `--maxmemory-policy allkeys-lru` to
  **Extra Server Arguments** so old keys are evicted instead.
- Stopping sends SIGTERM; Redis saves a snapshot before it exits.
