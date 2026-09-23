#!/usr/bin/env python3
"""Evaluate the Star River workbook and assert its headline outputs.

openpyxl writes formulas but does not compute them, so a model can look finished and
be wrong. This script evaluates the workbook with the `formulas` package and checks
the results against the values the analysis claims.

    pip install openpyxl formulas
    python3 verify.py [path-to-xlsx]

Exit code 0 = every assertion passed.
"""
import sys
from pathlib import Path

DEFAULT = Path(__file__).parent / "model" / "TEST 2 - Star River Project Analysis.xlsx"

# (sheet, cell, label, expected) — expected values are the analysis's stated results
EXPECTED = [
    ("PROJECT ANALYSIS", "D29", "NPV (wait three years)",   -1_702_230.14),
    ("PROJECT ANALYSIS", "D47", "NPV (buy now)",            -1_875_494.72),
    ("PROJECT ANALYSIS", "D50", "Advantage of waiting (PV)",    173_264.58),
    ("PROJECT ANALYSIS", "D53", "PV gain from waiting",         173_264.58),
    ("PROJECT ANALYSIS", "D55", "Equivalent annual annuity",     25_669.32),
    ("PROJECT ANALYSIS", "D58", "Equiv. annual cost — wait",  -252_187.08),
    ("PROJECT ANALYSIS", "D59", "Equiv. annual cost — now",   -277_856.40),
    ("PROJECT ANALYSIS", "D60", "Advantage of waiting /yr",      25_669.32),
]

# Cells that must contain a passing verdict string
VERDICTS = [
    ("INPUTS", "E33", "OK"),   # depreciation vs Exhibit 4
    ("INPUTS", "E34", "OK"),   # purchase-price saving vs Exhibit 4
    ("INPUTS", "E35", "OK"),   # replacement year vs Exhibit 4
    ("PROJECT ANALYSIS", "D61", "OK"),      # two EAA routes agree
    ("UNEQUAL LIVES", "E28", "ZERO"),       # cash-flow streams converge
]

# Horizon-independence: the advantage must stop moving once year 13 is included
HORIZONS = [("C11", 128_839.72), ("C12", 145_217.41),
            ("C13", 159_972.08), ("C14", 173_264.58)]

TOL = 0.02


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not path.exists():
        print(f"FAIL  workbook not found: {path}")
        return 1

    import formulas
    sol = formulas.ExcelModel().loads(str(path)).finish().calculate()
    tag = f"[{path.name.upper()}]"

    def get(sheet, cell):
        for key, val in sol.items():
            if key.upper() == f"'{tag}{sheet}'!{cell}":
                try:
                    return val.value[0, 0]
                except Exception:
                    return val.value
        return None

    failures = []
    print(f"Verifying {path.name}\n")

    print("Headline outputs")
    for sheet, cell, label, want in EXPECTED:
        got = get(sheet, cell)
        ok = isinstance(got, (int, float)) and abs(float(got) - want) < TOL
        failures.append(label) if not ok else None
        shown = f"{float(got):,.2f}" if isinstance(got, (int, float)) else repr(got)
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:<28} {cell}  {shown:>16}")

    print("\nCheck cells")
    for sheet, cell, needle in VERDICTS:
        got = get(sheet, cell)
        ok = isinstance(got, str) and needle in got
        failures.append(f"{sheet}!{cell}") if not ok else None
        print(f"  [{'PASS' if ok else 'FAIL'}] {sheet}!{cell:<5} {str(got)[:62]}")

    print("\nHorizon independence (advantage must settle at year 13)")
    for cell, want in HORIZONS:
        got = get("UNEQUAL LIVES", cell)
        ok = isinstance(got, (int, float)) and abs(float(got) - want) < TOL
        failures.append(f"horizon {cell}") if not ok else None
        shown = f"{float(got):,.2f}" if isinstance(got, (int, float)) else repr(got)
        print(f"  [{'PASS' if ok else 'FAIL'}] {cell}  {shown:>14}")

    print()
    if failures:
        print(f"FAILED: {len(failures)} assertion(s) — {', '.join(failures)}")
        return 1
    print("All assertions passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
