# Agent instructions

Everything the AI assistant (Claude Code, model Claude Opus 5) ran with on this
project. Included for the submission requirement to hand over "whatever prompt or
instruction files your agent uses."

## What steers the agent

**`../CLAUDE.md`** — the main one. Project conventions, loaded automatically at the
start of every session in this directory. It carries the rules the model was built
under: every input traces to an exhibit, never report a number from an unevaluated
formula, never ship a formula the evaluator cannot confirm.

**`../.claude/settings.local.json`** — local permissions. One allowed Bash command.
No secrets.

**`../.claude/skills/`** — two skills available in this project. Each is a `SKILL.md`
(a description telling the agent when to invoke it) plus a script it runs:

| Skill | Purpose |
|---|---|
| `fred-data` | Look up economic statistics by calling the FRED API, never from memory |
| `time-value` | Solve time-value-of-money problems by running a script, never by hand |

Both encode the same rule: compute it, don't recall it. Neither was triggered during
the Star River work — the case supplies its own figures and the arithmetic lives in
the workbook — but they were available.

**`memory/`** — persistent facts carried across sessions. `MEMORY.md` is the index
loaded into context each time; each entry is a separate file.

| Memory | What it enforces |
|---|---|
| `env-file-is-priority-source.md` | `.env` wins over shell exports; load with override |
| `never-expose-api-keys.md` | No printing, no files, no command lines; read via `os.environ` |

## Not included

One memory file (`aviation-career-track.md`) is personal career information unrelated
to this coursework and is deliberately left out. Say so if the submission needs it.

`.env` is excluded by `.gitignore` and is not in this repository or any archive of it.

## Conversation transcripts

The session transcripts are not in this repo. They live under
`~/.claude/projects/<project>/` on the author's machine and can be exported if the
submission requires the full prompt history.
