---
name: never-expose-api-keys
description: "Never print, write to a file, or pass API keys on a command line; read them with os.environ inside a script."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4e7b9f46-15ec-47da-b752-3869ac97c906
  modified: 2026-09-09T19:02:43.626Z
---

The user's FRED API key lives in the environment variable `FRED_API_KEY`.
Instruction given 2026-09-09: never print it, never write it into a file, never
paste it into a command line. Read it with `os.environ` inside a script.

**Why:** A value on a command line lands in the process argv (readable by any
local user via `ps`), in shell history, and in any tool output that echoes the
command. Printing it puts it in the conversation transcript. Writing it into a
file risks it being committed or synced. Reading via `os.environ` at runtime
keeps the value in-process only.

**How to apply:**
- In Python: `key = os.environ["FRED_API_KEY"]`, then pass it via the request
  library's params dict (e.g. `requests.get(url, params={...})`) — never
  f-string it into a URL that gets logged or printed.
- Never `echo`, `curl ...api_key=$KEY`, or interpolate the key into a Bash call.
- For verification, report only length / format match, never a prefix or the value.
- On error paths, scrub the key from any URL before printing the exception.
- Applies to all provider keys in this project, not just FRED. See
  [[env-file-is-priority-source]] for where keys are stored and loaded from.
