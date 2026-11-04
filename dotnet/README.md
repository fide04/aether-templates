# .NET App

Builds and runs a .NET application: an ASP.NET Core site or API, a Discord bot (Discord.Net,
DSharpPlus) or any other .NET program. It runs in Microsoft's .NET SDK image
(`mcr.microsoft.com/dotnet/sdk:<version>`, Docker), which builds the project and runs it.

## Getting your code onto the server

- **Upload it** with the file manager: the project (`.csproj`) or solution (`.sln`, `.slnx`) with its
  sources, or an app you published yourself (set **Start DLL**), or
- **Git Repository**: the install downloads the repository into the server folder (latest commit of
  **Git Branch**, or of the default branch when it is empty). **Reinstall** pulls the latest commit
  again. Files tracked by the repository are replaced by the repository version; untracked files
  (databases, logs, `appsettings.Production.json` you added) are kept. For a private repository put
  a personal access token in **Git Access Token** (GitHub or GitLab, read access is enough).
- With no code and no repository, the install writes a placeholder web app
  (`AetherPlaceholder.csproj` and `Program.cs`) that answers on the server port and says what to do
  next. It is removed on the next start once the folder has a project of its own (or **Project** is
  set).

## Building and starting

`dotnet publish <Project> -c Release -o .aether/publish`, then `dotnet .aether/publish/<App>.dll`

- **Project**: the `.csproj` (or its folder) to publish, for example `src/MyApp/MyApp.csproj`. Empty
  publishes the project or solution in the server folder.
- **Build on Start** (on by default) publishes before every start; the install publishes once, so
  build errors show up there. Off, the last build is run (built again only when there is none).
- The `.dll` that is started is the only one in `.aether/publish` with a `.runtimeconfig.json` that
  is not a test project, otherwise the one named after the project's `AssemblyName`. A solution with
  two or more apps needs **Project** set to the one to run.
- **Start DLL** runs a `.dll` you published and uploaded (for example `publish/MyApp.dll`) and builds
  nothing.
- ASP.NET Core listens on the server port (`ASPNETCORE_URLS=http://0.0.0.0:<port>`); the app also
  gets it in `PORT`.
- **Environment** sets `DOTNET_ENVIRONMENT` and `ASPNETCORE_ENVIRONMENT` (`Production`), which
  picks `appsettings.<Environment>.json`.

NuGet packages and the SDK's own files stay in `.aether/` in the server folder (`NUGET_PACKAGES`,
`DOTNET_CLI_HOME`), so rebuilds are fast and the space counts against the server's disk. Telemetry is
off.

## .NET versions

**.NET Version** picks the SDK image: 8.0 (LTS), 9.0 or 10.0 (LTS). The project's
`TargetFramework` must not be newer than it (`net10.0` needs 10.0). An SDK also builds and runs
older target frameworks only when that runtime is in the image, so pick the version the project
targets.

## Ports

| Port | Protocol | Use |
|------|----------|-----|
| `port` (5000) | TCP | Only for apps that serve HTTP. Discord bots do not need it |

## Caveats

- Stopping sends SIGTERM, which .NET's host turns into a graceful shutdown.
- HTTPS is not set up (no development certificate); put a reverse proxy in front for HTTPS. Remove
  `app.UseHttpsRedirection()` if it sends visitors to an HTTPS port that does not exist.
- Building needs memory: give small servers at least 1 GB.
- The SDK images are about 300 MB compressed (900 MB on disk); the first install downloads it.
- Docker only.
