# Go App

Builds and runs a Go application: a web server or API, a Discord bot (discordgo, arikawa...) or any
other Go program. It runs in the official `golang:<version>` image (Docker), which has the Go
toolchain, git and a C compiler for cgo.

## Getting your code onto the server

- **Upload it** with the file manager (the folder with your `go.mod`), or
- **Git Repository**: the install downloads the repository into the server folder (latest commit of
  **Git Branch**, or of the default branch when it is empty). **Reinstall** pulls the latest commit
  again. Files tracked by the repository are replaced by the repository version; untracked files
  (`.env`, databases, logs) are kept. For a private repository put a personal access token in
  **Git Access Token** (GitHub or GitLab, read access is enough).
- With no code and no repository, the install writes a placeholder `main.go` and `go.mod`: a small
  web server on the server port that says what to do next. When you upload your own `go.mod`, a
  placeholder `main.go` left next to it is removed on the next start; a git repository removes both.

`go.mod` has to be at the top of the server folder, or in the **Build Target** folder: a module of
its own (like `helloserver` in `golang/example`), which is then built and run from that folder.

## Building and starting

On every start the app is built and then run:

`go build -o .aether/bin/app <Build Target>`, then `.aether/bin/app <Start Arguments>`

- **Build Target** (`.`) is the package with `func main`, for example `./cmd/server`.
- **Start Arguments** are passed to the app, for example `-addr :8000`.
- The install downloads the modules and builds once, so mistakes show up there and the first start
  is quick. Later builds only compile what changed.
- **Run with go run** starts the app with `go run` instead (off by default). `go run` does not pass
  the stop signal on to the app, so the app is killed without a graceful shutdown.
- The app gets the port in the `PORT` environment variable. A web server has to listen on all
  addresses (`:8000` or `0.0.0.0:8000`), not on `localhost`.

Modules, the build cache and the binary stay in `.aether/` in the server folder (`GOPATH`,
`GOCACHE`), so rebuilds are fast and the space counts against the server's disk. Delete `.aether/`
to free it; the next start downloads and compiles everything again.

## Go versions

**Go Version** picks the image (`golang:1.26` or `golang:1.27`). When `go.mod` asks for a newer Go
(its `go` or `toolchain` line), that toolchain is downloaded into the server folder
(`GOTOOLCHAIN=auto`), so a project still builds when the image is a patch release behind.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (8000) | TCP | Only for apps that serve HTTP (web servers, APIs). Discord bots do not need it |

## Caveats

- Stopping sends SIGTERM. A Go program without a signal handler exits at once; handle
  `syscall.SIGTERM` (`signal.NotifyContext`) to shut down cleanly. The container runs with an init
  process, so the signal reaches the app.
- Private modules need `GOPRIVATE` and credentials, which the template does not set up; vendor them
  (`go mod vendor`) instead.
- The `golang` images are about 300 MB compressed (900 MB on disk); the first install downloads it.
- Host environment: needs `bash` and `go` on the node (the panel cannot download Go), and `git` when
  a repository is set. **Go Version** does not apply there.
