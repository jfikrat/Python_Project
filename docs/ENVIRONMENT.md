# Environment Setup (Bun + Next.js)

This project uses Next.js with OpenAI Agents SDK and Bun 1.3+ for package management and scripts.

## Prerequisites

- Bun 1.3.0+ (`bun -v`)
- An OpenAI API key for using the Agents SDK

## Create your environment file

```bash
cp .env.example .env.local
```

Set the following variables in `.env.local`:

- `OPENAI_API_KEY` — Your OpenAI API key for Agents SDK

> Important: Keep `.env.local` out of version control. The repo’s `.gitignore` allows committing `.env.example` only.

## Install and run

```bash
bun install
bun run dev
```

- App runs at `http://localhost:3000`
- Next.js loads environment from `.env.local`

## Build & start (production)

```bash
bun run build
bun run start
```

## Bun runner notes

- `bun run dev` executes scripts that use Bun’s runner: `bun x next dev`
- Prefer `bun x` over `npx`; you may alias it as `bunx`:
  ```bash
  alias bunx='bun x'
  ```

## Troubleshooting

- Postinstall hooks blocked:
  ```bash
  bun pm untrusted
  ```
- Missing API key → the app will error; confirm `OPENAI_API_KEY` exists in `.env.local`.
- Domain allowlist: before deploying, add your domain to OpenAI's allowlist in the dashboard.
