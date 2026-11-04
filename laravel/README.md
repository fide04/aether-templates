# Laravel

Runs a Laravel application with PHP's built-in web server. It runs in
`ghcr.io/aether-panel/php:<version>` (Docker): the official `php:<version>-cli` image plus Composer,
git, unzip and the extensions Laravel and its database drivers need (bcmath, gd, intl, mysqli,
pdo_mysql, pdo_pgsql, redis, zip...).

## Getting your app onto the server

- **Create a Laravel Project** (on by default): with no repository and no Laravel app in the server
  folder, the install runs `composer create-project laravel/laravel`, which gives a new app with an
  SQLite database, its migrations already run, and an application key. Composer picks the newest
  Laravel the chosen PHP version supports.
- **Git Repository**: the install downloads the repository into the server folder (latest commit of
  **Git Branch**, or of the default branch when it is empty). **Reinstall** pulls the latest commit
  again. Files tracked by the repository are replaced by the repository version; untracked files
  (`.env`, `storage/`, `vendor/`, the SQLite database) are kept. For a private repository put a
  personal access token in **Git Access Token** (GitHub or GitLab, read access is enough).
- Or **upload it** with the file manager.

## Every start

1. `composer install` (with **Install Composer Packages on Start**, on by default; also on install).
   **Skip Dev Packages** adds `--no-dev`.
2. When there is no `.env`, it is copied from `.env.example`; an empty `APP_KEY` gets one
   (`php artisan key:generate`). When `.env` uses SQLite without a `DB_DATABASE`, an empty
   `database/database.sqlite` is created, as `create-project` does.
3. `public/storage` is linked to `storage/app/public` once (what `php artisan storage:link` does; the
   link is relative, so it keeps working in the file manager and in backups).
4. `php artisan migrate --force` with **Run Migrations on Start** (off by default).
5. `php artisan optimize` (config, events, routes and views caches) with **Cache Config and Routes on
   Start** (off by default). When it is off, caches left from earlier starts are cleared, so `.env`
   changes apply on the next start.
6. The app is served from `public/`:
   `php -d memory_limit=<memory>M <Extra PHP Settings> -S 0.0.0.0:<port> -t public .aether/router.php`

### Why the built-in server and not `php artisan serve`

`artisan serve` starts that same built-in server as a child process. Run directly, the server is the
only process: the stop signal reaches it, the PHP settings above apply to it (`artisan serve` does not
pass `-d` settings on), it never moves to another port when its own is busy, and it does not restart
itself when `.env` changes. The router (`.aether/router.php`, written before every start) does what
Laravel's `server.php` does (existing files are served, everything else goes to `public/index.php`)
and never serves hidden files such as `.htaccess`. **Workers** sets `PHP_CLI_SERVER_WORKERS` (4), the
requests answered at the same time.

## Database

New projects use SQLite (`database/database.sqlite` in the server folder), which needs nothing else.
For MySQL/MariaDB or PostgreSQL, create a server from the MariaDB or PostgreSQL template and set
`DB_CONNECTION`, `DB_HOST` (the node's address), `DB_PORT`, `DB_DATABASE`, `DB_USERNAME` and
`DB_PASSWORD` in `.env`. Laravel 11 and later keep sessions, cache and queued jobs in the database by
default: an app downloaded from git needs its migrations run once (turn on **Run Migrations on
Start**) before its pages work.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (8000) | TCP | HTTP |

## Caveats

- `.env.example` sets `APP_ENV=local` and `APP_DEBUG=true`, which shows error details to visitors.
  For a public site set `APP_ENV=production`, `APP_DEBUG=false` and `APP_URL` to its address in
  `.env`.
- Queue workers (`php artisan queue:work`) and the scheduler (`php artisan schedule:run`) are not
  started. With the default `QUEUE_CONNECTION=database`, queued jobs wait until a worker runs: use
  `QUEUE_CONNECTION=sync`, or run the worker in a second server.
- Logs go to `storage/logs/laravel.log`; set `LOG_CHANNEL=stderr` in `.env` to see them in the
  console.
- Frontend assets (Vite) are not built: the image has no Node.js. Run `npm run build` before
  uploading, or commit `public/build`. The default welcome page works without it.
- The built-in server speaks plain HTTP; put a reverse proxy in front for HTTPS and a domain.
- Stopping sends SIGTERM; the container runs with an init process, so the workers stop at once.
- Docker only.
