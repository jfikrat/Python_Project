# Bun Runner (bun x) Cheat Sheet

This project uses Bun 1.3+ as the package runner for this Next.js application.

## Why `bun x` (aka bunx)?

- Fast package execution (similar to `npx`, but faster and cache‑friendly).
- Works well with Next.js and typical web tooling.
- You can alias `bunx` → `bun x` in your shell:

```bash
alias bunx='bun x'
```

## Common commands

```bash
# Install deps
bun install

# Dev server (uses bun x next dev)
bun run dev

# Build (uses bun x next build)
bun run build

# Start prod (uses bun x next start)
bun run start

# Lint (uses bun x eslint)
bun run lint
```

## Postinstall prompts

If Bun blocks some postinstall hooks:

```bash
bun pm untrusted
```

## Cross‑platform watcher (optional)

Use any dev command; default here is `bun run dev`.

macOS/Linux (bash):

```bash
session="dev"
log="./logs/watchers/$session.log"
pid="./logs/watchers/$session.pid"
mkdir -p ./logs/watchers
DEV_CMD=${DEV_CMD:-"bun run dev"}
nohup bash -lc "$DEV_CMD" > "$log" 2>&1 & echo $! > "$pid"
# Stop
pid_val="$(cat "$pid")" || true
kill -15 "$pid_val" 2>/dev/null || true
sleep 2
kill -9 "$pid_val" 2>/dev/null || true
```

Windows (PowerShell 7):

```powershell
$session = "dev"
$log = "./logs/watchers/$session.log"
$pidFile = "./logs/watchers/$session.pid"
New-Item -ItemType Directory -Force -Path ./logs/watchers | Out-Null
$cmd = $env:DEV_CMD; if (-not $cmd) { $cmd = "bun run dev" }
$proc = Start-Process pwsh -ArgumentList "-NoLogo","-NoProfile","-Command","$cmd *> $log" -PassThru
$proc.Id | Out-File -Encoding ascii $pidFile -Force

# Stop
$pid = Get-Content $pidFile
if (Get-Process -Id $pid -ErrorAction SilentlyContinue) { Stop-Process -Id $pid -Force }
```

## Environment files

Copy the example and fill required keys:

```bash
cp .env.example .env.local
```

Set:

- `OPENAI_API_KEY`

See also: `docs/ENVIRONMENT.md`.
