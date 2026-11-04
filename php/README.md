# PHP App

Runs a PHP web application with PHP's built-in web server: plain PHP, Symfony, CodeIgniter 4, Slim
or WordPress. It runs in `ghcr.io/aether-panel/php:<version>` (Docker): the official `php:<version>-cli`
image plus Composer, git, unzip and the extensions apps usually need (bcmath, exif, gd, intl, mysqli,
opcache, pcntl, pdo_mysql, pdo_pgsql, pgsql, redis, sockets, zip). For Laravel use the Laravel
template.

## Getting your code onto the server

- **Upload it** with the file manager, or
- **Git Repository**: the install downloads the repository into the server folder (latest commit of
  **Git Branch**, or of the default branch when it is empty). **Reinstall** pulls the latest commit
  again. Files tracked by the repository are replaced by the repository version; untracked files
  (`.env`, uploads, `vendor/`) are kept. For a private repository put a personal access token in
  **Git Access Token** (GitHub or GitLab, read access is enough).
- **WordPress**: with **Framework** set to WordPress and no repository, the install downloads the
  latest WordPress when the server folder has none (files already there, such as `wp-config.php`,
  are kept).
- With no code and no repository, the install writes a placeholder `index.php` (in `public/` for a
  framework) that says what to do next.

## Composer

When there is a `composer.json`, `composer install` runs on install and, with **Install Composer
Packages on Start** (on by default), before every start too. **Skip Dev Packages** adds `--no-dev`;
only turn it on when the app runs in production mode (Symfony: `APP_ENV=prod` in `.env`), as dev
bundles are left out. Composer's cache stays in `.aether/composer` in the server folder.

## Serving

`php -d memory_limit=<memory>M <Extra PHP Settings> -S 0.0.0.0:<port> -t <document root> .aether/router.php`

- **Document Root**: the folder served on the web. Empty picks it from **Framework**: Plain PHP serves
  `public/` when it exists, otherwise the server folder; Symfony, CodeIgniter 4 and Slim serve
  `public/`; WordPress serves the server folder.
- With a framework (and WordPress) every request that is not a file goes to the front controller
  `index.php`, so routes and pretty permalinks work. Plain PHP serves files as they are (a folder
  shows its `index.php`).
- The router (`.aether/router.php`, written before every start) never serves hidden files and folders
  (`.env`, `.git`, `.htaccess`), nor `vendor/` and the Composer files when the document root is the
  project folder.
- **Workers** (`PHP_CLI_SERVER_WORKERS`, 4) is how many requests are answered at the same time.
- `memory_limit` is the server memory; each worker can use up to that, the server as a whole can
  not. **Extra PHP Settings** takes more `-d` settings, for example
  `-d upload_max_filesize=64M -d post_max_size=64M` (the defaults are 2 MB and 8 MB).
- The app gets the port in the `PORT` environment variable.

## WordPress

WordPress needs a MySQL or MariaDB database, which you provide: for example a server made from the
MariaDB template. Start the server, open its address and enter the database name, user, password and
host (the node's address and the MariaDB port, for example `203.0.113.10:3306`). The setup writes
`wp-config.php` into the server folder. Set the site address to the address people use, as WordPress
redirects to it.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (8000) | TCP | HTTP |

## Caveats

- The built-in server speaks plain HTTP. For HTTPS and a domain, put a reverse proxy in front (the
  panel's subdomains, Cloudflare, nginx).
- PHP's built-in server is meant for small and medium sites; it has no static file cache, gzip or
  rewrite rules (`.htaccess` is ignored).
- Stopping sends SIGTERM; the container runs with an init process, so the workers stop at once.
- Frontend assets (npm, Vite, Webpack Encore) are not built: the image has no Node.js. Build them
  before uploading or commit the built files.
- Docker only.
