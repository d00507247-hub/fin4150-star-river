# CLAUDE.md — FIN 4150 Star River Electronics

Working conventions for this repository. These are the rules the work was actually
built under, not aspirations.

## What this project is

A capital-budgeting model for the Star River Electronics case (Bruner Case 24).
The decision: buy the new packaging machine now, or wait three years.

Deliverable is an Excel model (`.xlsx`) built on the course-provided template
`source/Star River Project Analysis_Template.xls`.

## Non-negotiable rules for the model

**Every input traces to a case exhibit.** The `Inputs` sheet carries one row per
input with a `Source` column quoting the exhibit text. The calculation sheet
contains no typed numbers — every cell is a formula pointing at `Inputs`.

**Derived figures stay visibly derived.** Overtime is `=C26-C25` (81,900 − 63,700),
not a typed 18,200. Old depreciation is `=C19/C20`. The deferred purchase price is
`=C11*(1+C8)^C23`. If a grader clicks a number they land on a sourced input.

**Inputs that are not from an exhibit say so.** The 11% WACC is labelled
`GIVEN in assignment prompt (not an exhibit figure)`. Do not invent a citation.

**Self-checks are live formulas.** The `Inputs` sheet ends with checks comparing
model-derived values against figures the case states independently (SGD 182,000
depreciation, SGD 286,878 purchase-price saving, replacement year 2004). They
re-verify when an input changes.

## Verification discipline

**Never report a number from a formula you have not evaluated.** `openpyxl` writes
formulas but does not compute them. Run `verify.py`, which evaluates the workbook
with the `formulas` package and asserts the headline outputs and every check cell.

**Never ship a formula the evaluator cannot confirm.** `OFFSET` was used first for
the horizon table and returned `#NAME?` under evaluation. It was replaced with
`SUMPRODUCT` tested against the model's own year row. If it cannot be verified, it
does not go in.

**Prefer two independent routes to the same number.** The advantage of waiting is
computed both as the difference of the two scenario NPVs (`D50`) and as the NPV of
the year-by-year difference row (`D53`). Cell `D61` asserts they agree.

## Model-specific facts worth not re-deriving

- Year 0 is 2001; the horizon runs to 2014 (year 13).
- Year 13 is not arbitrary: from year 14 both scenarios carry identical maintenance,
  identical labour and zero depreciation, so their difference is exactly zero. The
  answer is therefore horizon-independent. `Unequal Lives` proves this.
- Depreciation is **straight-line**, per Exhibit 4 — not MACRS, despite the generic
  course replacement template using MACRS.
- There is no net working capital and no terminal value in this case.
- The old machine is scrapped with zero proceeds, so the whole SGD 218,400 book value
  becomes a loss and the tax benefit lands in year 0.
- EAA here **restates** the NPV decision on a common annual basis. It is not the
  replication-based EAC correction — the machine is never repeated. See the METHOD
  block on the `Unequal Lives` sheet.

## Google Drive

Reading from Drive works. **Writing binary files to Drive does not.** The connector's
only upload path takes base64 that must be reproduced character-for-character, and at
~14k characters it corrupts. Two uploads were produced and verified broken before this
was established. Build and verify `.xlsx` locally; move it to Drive by hand.

## Environment

- `.env` is the priority source for environment variables; load with override so it
  beats shell exports. **Never commit it** — see `.gitignore`.
- Never print API keys, write them to files, or pass them on a command line. Read them
  via `os.environ` inside a script.
- `xlrd` reads legacy `.xls`. `openpyxl` reads/writes `.xlsx`. `formulas` evaluates a
  workbook. There is no LibreOffice on this machine, so `.xls` formatting cannot be
  carried across to `.xlsx`.

## Style

Report outcomes faithfully. If a check fails, say so with the output. If something was
not verified, say that rather than implying it was.
