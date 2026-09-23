---
name: env-file-is-priority-source
description: The analyst-desk .env file is the priority source for environment variables; prefer it over shell exports or hardcoded values.
metadata: 
  node_type: memory
  type: project
  originSessionId: 4e7b9f46-15ec-47da-b752-3869ac97c906
  modified: 2026-09-09T18:44:07.262Z
---

In the analyst-desk project, `.env` at the project root is the priority source for
environment variables and API keys. Stated by the user on 2026-09-09.

**Why:** The user wants one canonical place for credentials rather than values
scattered across shell profiles, hardcoded literals, or ad-hoc exports.

**How to apply:**
- Read keys from `.env`, never hardcode them and never read from a shell profile.
- When adding a new provider key, add it to `.env` rather than exporting it elsewhere.
- Load it so `.env` *wins* over any pre-existing environment value:
  - shell: `set -a && . ./.env && set +a` (overrides by default)
  - python: `load_dotenv(override=True)` — the default is `override=False`,
    which silently lets a stale shell export beat `.env`
- `.env` is chmod 600 and listed in `.gitignore`. Never print its contents or
  echo a key value into the transcript; report length or a prefix instead.
