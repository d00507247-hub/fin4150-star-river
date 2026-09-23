# FIN 4150 — Star River Electronics Ltd. (Bruner Case 24)

Capital-budgeting analysis of the packaging-machine investment. The question put to
Adeline Koh: buy the new machine now, or wait three years.

## Recommendation

**Wait.** At the given 11% WACC, deferring to 2004 is worth **SGD 173,265** in present
value, or **SGD 25,669 per year** on an equivalent annual basis.

| | |
|---|---|
| NPV of costs — wait three years | −SGD 1,702,230 |
| NPV of costs — buy now | −SGD 1,875,495 |
| **Advantage of waiting** | **SGD 173,265** |
| Equivalent annual cost — wait | −SGD 252,187 /yr |
| Equivalent annual cost — buy now | −SGD 277,856 /yr |
| **Advantage of waiting, per year** | **SGD 25,669 /yr** |

This runs against the plant manager's recommendation in Exhibit 4. His operational
complaints are real, but the only quantified benefit is SGD 18,200/yr of avoided
overtime — roughly 1% of the SGD 1.82m purchase price. It would need to be about six
times larger to justify buying now. The break-even discount rate is 6.6%; above that,
waiting wins, and the margin widens as the rate rises.

The figure is also conservative: it prices pure timing of known cash flows. Star River
faced real uncertainty (CD-ROM drives were forecast to fall from 93% of optical-drive
shipments in 1999 to 41% by 2005), and genuine uncertainty makes an option to defer
more valuable, not less.

## Layout

```
model/   TEST  — first build on the provided template
         TEST 2 — final: EAA foregrounded, unequal-lives proofs, methodology note
source/  course-provided templates the model is built on
verify.py         evaluates the workbook and asserts every headline output
CLAUDE.md         working conventions the model was built under
agent-instructions/   configuration the AI assistant ran with
```

`model/TEST 2` is the deliverable. `model/TEST` is kept so the change is visible.

## Verifying

```
pip install openpyxl formulas
python3 verify.py
```

Evaluates the workbook and asserts the eight headline outputs, all five check cells,
and horizon independence. Exit 0 means everything passed.

## How the model is built

Two sheets carry the analysis and one carries the proofs.

**Project Analysis** reproduces the provided template cell-for-cell — same blocks
(Initial Investment / Incremental Operating Cash Flow / Terminal Cashflow / Free Cash
Flow / NPV), same row order, years 0–13 across columns D–Q. It contains no typed
numbers; every cell is a formula.

**Inputs** holds every assumption with the exhibit text it came from, and ends with
three live checks against figures the case states independently:

| Check | Model | Case states |
|---|---|---|
| Annual depreciation, new machine | 182,000 | 182,000 |
| Saving in purchase price by buying now | 286,878 | 286,878 |
| Replacement year | 2004 | 2004 |

**Unequal Lives** proves the horizon is legitimate rather than asserting it:

- *Test 1* — the advantage at each cut-off: 128,840 / 145,217 / 159,972 / **173,265**.
  Stopping early understates it; from year 13 the number stops moving.
- *Test 2* — years 14 and 15 rebuilt independently from Inputs, showing both scenarios
  produce identical cash flows. Difference: exactly 0.00. The streams converge, so no
  longer horizon can change the answer.
- *Test 3* — the discarded approach. Annualising each alternative over its own asset
  life gives 66,275/yr against the correct 25,669/yr, a 2.58× overstatement. Rejected
  because both alternatives' service lives are indefinite, so there are no unequal
  lives to correct for.
- *METHOD* — why the per-year figure is legitimate: NPV decides, the annual figure
  restates. This is not replication-based EAC; the machine is never repeated.

## Case facts driving the model

Straight-line depreciation (Exhibit 4 states it explicitly — not MACRS). No net
working capital. No terminal value: the new packager "will operate indefinitely" and
the old one has "no salvage value at all". The old machine is scrapped with zero
proceeds, so its full SGD 218,400 book value becomes a loss and the SGD 53,508 tax
benefit falls in year 0. Labour and maintenance inflate at 1.5%; the equipment price
and its maintenance contract escalate at 5%.

## Known limits

- Formatting is rebuilt rather than inherited from the `.xls` template — no LibreOffice
  on the build machine to carry it across.
- The financial-health analysis (case question 1) is not in the workbook; the template
  covers the machine decision only.
- WACC is taken as given at 11% rather than derived from Exhibit 5.
