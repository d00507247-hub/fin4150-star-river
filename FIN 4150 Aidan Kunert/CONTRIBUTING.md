# Contributing — team setup

The assignment requires commits from every member. Each person commits their own
work from their own machine, under their own name. Do not commit on someone else's
behalf: the point of the requirement is that the history shows who did what.

## One-time setup

Clone the repo, then **set your identity inside it** before committing anything:

```bash
git clone <repo-url>
cd fin4150-star-river
git config user.name "Your Name"
git config user.email "your.email@utahtech.edu"
```

Check it took before your first commit — this is the step people forget, and a commit
authored as `unknown` does not count toward the requirement:

```bash
git config user.name && git config user.email
```

Use the same email as your GitHub account so the commits link to your profile.

## Before you commit a change to the model

Install the tooling once:

```bash
pip install openpyxl formulas
```

Then run the verifier. It evaluates the workbook and asserts the eight headline
outputs, the five check cells and horizon independence:

```bash
python3 verify.py
```

**Exit 0 means every assertion passed.** If you changed an input on purpose, the
expected values in `verify.py` need updating in the same commit — and say in the
commit message why the number moved.

Excel writes formulas without computing them, so a workbook can look finished and be
wrong. Do not push a model change you have not run the verifier against.

## Commit conventions

One logical change per commit. Write a subject line that says what changed, then a
body explaining *why* — the reasoning is what gets graded, and it is invisible from a
diff of a binary `.xlsx`.

```
Update WACC to derived figure from Exhibit 5

Replaces the given 11% with 10.4% derived from the comparables. Advantage of
waiting falls to SGD 1xx,xxx; the recommendation is unchanged because the
break-even discount rate is 6.6%.
```

Binary `.xlsx` files do not diff, so the message is the only record of your reasoning.

## Never commit

- `.env` or any file with credentials. It is in `.gitignore`; leave it there.
- API keys in scripts. Read them from `os.environ` inside the script instead.
- Excel lock files (`~$*.xlsx`) — already ignored.

If a secret ever does get committed, say so immediately rather than quietly deleting
it. Removing the file in a later commit does **not** remove it from history.

## Splitting the work

Coordinate so two people are not editing the same `.xlsx` at once — Excel files cannot
be merged, and git will make you pick one version and discard the other. Suggested
split, each area a separate commit from a different member:

| Area | Files |
|---|---|
| Machine model and verification | `model/`, `verify.py` |
| Financial health (case question 1) | new sheet or a separate workbook |
| Risk assessment (case question 4) | write-up |
| WACC derivation from Exhibit 5 | `Inputs` sheet |

Question 1 (financial health) and question 4 (risk) are not yet in the repository —
see the known limits in `README.md`.
