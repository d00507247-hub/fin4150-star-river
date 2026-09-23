# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

s = doc.sections[0]
s.page_width = Inches(8.5)
s.page_height = Inches(11)
for m in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
    setattr(s, m, Inches(1))

st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(10.5)
st.paragraph_format.space_after = Pt(8)
st.paragraph_format.line_spacing = 1.12
rpr = st.element.get_or_add_rPr()
rf = rpr.get_or_add_rFonts()
for a in ("w:ascii", "w:hAnsi", "w:cs"):
    rf.set(qn(a), "Calibri")

ACCENT = RGBColor(0x1F, 0x3B, 0x57)
LQ = "“"
RQ = "”"
DASH = "—"
EN = "–"


def rule(p, size=6, color="1F3B57"):
    pPr = p._p.get_or_add_pPr()
    b = OxmlElement("w:pBdr")
    bot = OxmlElement("w:bottom")
    bot.set(qn("w:val"), "single")
    bot.set(qn("w:sz"), str(size))
    bot.set(qn("w:space"), "4")
    bot.set(qn("w:color"), color)
    b.append(bot)
    pPr.append(b)


def shade(cell, hexfill):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hexfill)
    tcPr.append(sh)


def h(text, size=12.5, space_before=14, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = ACCENT
    return p


def para(text="", bold_lead=None, size=None, after=8, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    if bold_lead:
        r = p.add_run(bold_lead)
        r.bold = True
        if size:
            r.font.size = Pt(size)
    if text:
        r = p.add_run(text)
        r.italic = italic
        if size:
            r.font.size = Pt(size)
    return p


def bullet(text, bold_lead=None, size=10.5):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.left_indent = Inches(0.3)
    if bold_lead:
        r = p.add_run(bold_lead)
        r.bold = True
        r.font.size = Pt(size)
    r = p.add_run(text)
    r.font.size = Pt(size)
    return p


def table(headers, rows, widths, size=9.5, right_from=1, bold_rows=()):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    hdr = t.rows[0].cells
    for i, txt in enumerate(headers):
        hdr[i].width = Inches(widths[i])
        shade(hdr[i], "1F3B57")
        p = hdr[i].paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        if i >= right_from:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = p.add_run(txt)
        r.bold = True
        r.font.size = Pt(size)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, txt in enumerate(row):
            cells[i].width = Inches(widths[i])
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            if i >= right_from:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run(txt)
            r.font.size = Pt(size)
            if ri in bold_rows:
                r.bold = True
                shade(cells[i], "EAEFF5")
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


# ------------------------- letterhead -------------------------
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(2)
r = p.add_run("MEMORANDUM")
r.bold = True
r.font.size = Pt(18)
r.font.color.rgb = ACCENT
rule(p, size=12)

meta = [
    ("TO:", "Adeline Koh, Chief Executive Officer, Star River Electronics Ltd."),
    ("FROM:", "[Team members] " + DASH + " Financial Analysis"),
    ("DATE:", "July 6, 2001"),
    ("SUBJECT:", "Financial condition and the packaging-machine decision"),
]
mt = doc.add_table(rows=len(meta), cols=2)
mt.autofit = False
for i, (k, v) in enumerate(meta):
    c0, c1 = mt.rows[i].cells
    c0.width = Inches(0.85)
    c1.width = Inches(5.65)
    for c in (c0, c1):
        c.paragraphs[0].paragraph_format.space_after = Pt(1)
    r = c0.paragraphs[0].add_run(k)
    r.bold = True
    r.font.size = Pt(10)
    r = c1.paragraphs[0].add_run(v)
    r.font.size = Pt(10)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(10)
rule(p, size=6, color="AFBCCB")

# ------------------------- recommendation -------------------------
h("RECOMMENDATION", space_before=2)
p = para(
    "Do not buy the packaging machine now. Wait and replace the current equipment in 2004, when growth "
    "forces the purchase anyway. At an 11% cost of capital, waiting costs "
)
r = p.add_run("SGD173,265 less in present value")
r.bold = True
p.add_run(" " + DASH + " ")
r = p.add_run("SGD25,669 per year")
r.bold = True
p.add_run(
    " on an equivalent annual basis. Esmond Lim's recommendation to buy now is not supported by the numbers "
    "in his own memo: the savings he quantifies are real, but they are small and they run out after three "
    "years, while the cost of buying three years early is the time value of SGD1.82 million."
)
para(
    "We would add one thing you did not ask for. The packaging machine is the smallest financial problem in "
    "front of you. Star River's operations consumed cash in each of the last two years, and the entire gap "
    "was filled with short-term bank borrowing. That is what Mr. Tan means by " + LQ + "growing beyond its "
    "financial capabilities," + RQ + " and it should shape how you open tomorrow's conversation with him."
)

# ------------------------- 1. financial condition -------------------------
h("1.  Financial condition: growing, profitable on paper, and out of cash")

para(after=4, bold_lead="Strengths to put in front of the bank.")
bullet(
    "Sales have compounded at roughly 14% a year, from SGD71.9 million in 1998 to SGD106.0 million in 2001. "
    "Star River survived a shakeout that killed less efficient producers, and did it on reputation."
)
bullet(
    "The company is profitable at every line. Operating margin was 16.1% in 2001 and net earnings of "
    "SGD7.1 million were up 46% on 2000. Reported return on equity recovered from 11.7% to 15.2%."
)
bullet(
    "Interest has been covered in every year, and the 2001 recovery in margin shows the 2000 deterioration "
    "was not a permanent loss of pricing power."
)

para(after=4, bold_lead="Weaknesses, in the order we would fix them.")
bullet(
    "Net earnings plus depreciation came to SGD18.5 million in 2001, but working "
    "capital absorbed SGD19.6 million, leaving operating cash flow of negative SGD1.1 million " + DASH +
    " after negative SGD15.8 million in 2000. After capital spending, free cash flow was negative SGD18.4 "
    "million in 2001 and negative SGD33.5 million in 2000.",
    bold_lead="Cash, not profit, is the problem. ",
)
bullet(
    "Inventories grew from SGD23.3 million to SGD63.8 million " + DASH + " 2.7 times " + DASH + " while "
    "sales grew 1.5 times. Days of inventory went from 252 to 436, and the cash conversion cycle from 231 "
    "days to 466. Returning inventory to its 1998 turns would release roughly SGD27 million: fifteen times "
    "the cost of the packaging machine. Receivables slipped too, from 112 days to 122.",
    bold_lead="Inventory is the cause. ",
)
bullet(
    "Short-term borrowings went from SGD29.0 million to SGD85.0 million, 2.9 "
    "times, in three years. Debt to equity rose from 1.13 to 2.20, debt to EBITDA from 1.8 to 3.6, and "
    "interest coverage slipped from 2.45 to 2.18. The quick ratio is 0.34 " + DASH + " SGD41.3 million of "
    "cash and receivables against SGD119.7 million of current liabilities.",
    bold_lead="The gap was financed by the bank. ",
)
bullet(
    "Decomposed, 1998 return on equity was a 7.96% margin on 0.65 "
    "asset turns at 3.21 times leverage. In 2001 it was a 6.74% margin on 0.57 turns at 3.93 times leverage. "
    "Both operating terms deteriorated; only leverage rose. The recovery was borrowed, not earned.",
    bold_lead="The improvement in ROE is leverage, not performance. ",
)
bullet(
    "SGD2 million has gone out in dividends in each of the last four "
    "years while free cash flow was negative and debt rose SGD20 million. Star River is borrowing to pay its "
    "owners. We would suspend the dividend before asking New Era and Starlight for fresh equity.",
    bold_lead="Dividends are being funded with debt. ",
)

para(
    "All of this sits in front of SGD54.6 million of DVD manufacturing capital expenditure still to be "
    "funded. The balance sheet has no room in it, and that is the lens through which we assessed the "
    "packaging machine."
)

doc.add_page_break()

# ------------------------- 2. cost of capital -------------------------
h("2.  Cost of capital", space_before=2)
para(
    "We have used an 11% weighted-average cost of capital throughout, as directed. It is a defensible figure "
    "for Star River: well above the 6.70% pre-tax rate on the company's bank line (prime of 5.2% plus 1.5%), "
    "and consistent with the equity betas of the Exhibit 5 comparables against a 3.6% risk-free rate and a 6% "
    "market risk premium. The recommendation below is not sensitive to this assumption within any plausible "
    "range " + DASH + " it holds for any discount rate above 6.61%."
)

# ------------------------- 3. the project -------------------------
h("3.  The packaging machine: free cash flows and the decision")

p = para(bold_lead="How we framed it. ", after=6)
p.add_run(
    "This is not an " + LQ + "is the NPV positive" + RQ + " question. Both paths end with the same machine "
    "running indefinitely " + DASH + " Exhibit 4 states it is " + LQ + "the last packaging equipment we will "
    "ever have to purchase" + RQ + " " + DASH + " and the current equipment cannot serve past 2004 either "
    "way. Output, revenue and capacity are identical under both alternatives, so there is no revenue line in "
    "the analysis. What differs is only the cost of two purchase dates. We built both alternatives on one "
    "13-year timeline, 2001 to 2014. From 2015 onward the two cash-flow streams are identical to the cent, so "
    "the answer does not depend on where the model stops."
)

para(bold_lead="What is in the cash flows.", after=6)
table(
    ["Cash-flow item", "Buy now (2001)", "Wait " + DASH + " buy in 2004"],
    [
        ["Purchase price, escalating 5% p.a.", "(1,820,000) in 2001", "(2,106,878) in 2004"],
        ["", "", "SGD286,878 more, as Exhibit 4 states"],
        ["Write-off of old machine", "+53,508 tax shield, 2001", "none " + DASH + " depreciated 2002" + EN + "04"],
        ["   book value SGD218,400, no salvage", "", "at SGD72,800 per year"],
        ["Depreciation, straight line", "182,000 p.a., 2002" + EN + "2011", "210,688 p.a., 2005" + EN + "2014"],
        ["Maintenance contract", "3,640 in 2002, +5% p.a.", "15,470 in 2002, +1.5% p.a. to 2004,"],
        ["", "", "then new contract at +5% p.a."],
        ["Operator, regular time", "63,700, +1.5% p.a.", "63,700, +1.5% p.a. (no saving)"],
        ["Overtime premium", "eliminated", "18,200 in 2002, +1.5% p.a. to 2004"],
        ["Terminal / salvage value", "none", "none"],
    ],
    widths=[2.55, 1.9, 2.05],
    right_from=1,
    size=9,
)
para(
    "Every operating item is taxed at 24.5%. Depreciation is not a cash flow; it enters only through its tax "
    "shield. Year-by-year free cash flows are in Exhibit A.",
    size=9.5,
    italic=True,
    after=12,
)

para(bold_lead="Result.", after=6)
table(
    ["At an 11% cost of capital", "Buy now", "Wait to 2004", "Advantage of waiting"],
    [
        ["Present value of costs", "(1,875,495)", "(1,702,230)", "173,265"],
        ["Equivalent annual cost", "(277,856)", "(252,187)", "25,669"],
    ],
    widths=[2.15, 1.3, 1.35, 1.7],
    right_from=1,
    size=9.5,
    bold_rows={0, 1},
)
para(
    "Both alternatives are annualised over the same 13 years. Annualising " + LQ + "buy now" + RQ + " over "
    "the machine's 10-year depreciable life and " + LQ + "wait" + RQ + " over 13 would show an advantage of "
    "SGD66,275 a year, 2.6 times the true figure, because it divides the two present values by different "
    "numbers of years. We report the common-basis figure.",
    size=9.5,
    italic=True,
    after=12,
)

p = para(bold_lead="Why buying now loses. ", after=8)
p.add_run(
    "The savings Mr. Lim identifies are genuine but modest and short-lived. Eliminating overtime (SGD18,200) "
    "and the old maintenance bill (SGD15,470 against SGD3,640) saves about SGD30,000 a year before tax, and "
    "only for the three years until the old machine must go " + DASH + " roughly SGD22,700 a year after tax, "
    "about SGD55,000 in present value. Buying now also pulls forward the SGD53,508 tax shield on writing off "
    "the old machine. Set against that, buying now spends SGD1.82 million three years early. Deferring to "
    "SGD2,106,878 in 2004 costs only about SGD1.54 million in today's money. The SGD286,878 the manufacturer "
    "will add to the price does not come close to offsetting three years of the time value of SGD1.82 million."
)

para(
    "Andy Chin's instinct was right: the decision does hinge on the discount rate. The two alternatives break "
    "even at 6.61%. Below that, buy now; above it, wait. At 11% the margin is not close."
)

doc.add_page_break()

# ------------------------- 4. risks -------------------------
h("4.  Risks: what would have to be true for this recommendation to be wrong", space_before=2)

para("The recommendation survives most of what could reasonably be doubted. We tested it; see Exhibit B.")
bullet(
    "Even if growth forces replacement in 2003, or "
    "even 2002, waiting still wins, by SGD117,100 and SGD58,455 respectively. The case for waiting does not "
    "rest on the old machine holding out.",
    bold_lead="The old machine failing early does not change it. ",
)
bullet(
    "At 5% rather than 1.5%, the answer "
    "is essentially unchanged at SGD171,199, because higher inflation raises the old machine's costs and the "
    "new machine's labour bill almost equally.",
    bold_lead="Higher labour and maintenance inflation does not change it. ",
)
bullet(
    "Waiting still wins for equipment price escalation up to "
    "9.4% a year, against the 5% the manufacturer has charged historically.",
    bold_lead="Faster equipment inflation has room to run. ",
)

para(bold_lead="Three things would overturn it.", after=6)
bullet(
    "If Star River financed this at the bank's "
    "rate " + DASH + " 6.70% pre-tax, 5.06% after tax " + DASH + " buying now would win by SGD64,777. Anyone "
    "who argues that 11% is too high for an in-place, cost-saving asset with near-certain cash flows has a "
    "real argument. We disagree: 11% is the firm's cost of capital, and Star River's marginal funding is a "
    "short-term line the bank is already trying to shrink, not fresh borrowing at prime.",
    bold_lead="1.  A cost of capital below 6.61%. ",
)
bullet(
    "This is the real gap in the plant manager's memo. He describes constant monitoring, frequent shutdowns, "
    + LQ + "several two-shift days catching up with production," + RQ + " and greater packaging flexibility "
    + DASH + " and quantifies none of it. If reliability and flexibility are worth SGD34,000 a year, a little "
    "over 0.03% of sales, buying now is correct. Before you turn this request down, ask Mr. Lim to put a "
    "number on downtime and on what flexible packaging would do for the DVD line.",
    bold_lead="2.  Unquantified benefits worth more than about SGD34,000 a year, pre-tax, in perpetuity. ",
)
bullet(
    "Eliminating overtime saves SGD18,200 a year. To "
    "justify buying now on labour alone you would need SGD110,811 a year " + DASH + " more than the "
    "operator's entire SGD81,900 compensation. Labour savings cannot carry this decision even if the machine "
    "ran unattended.",
    bold_lead="3.  Labour savings far larger than claimed. ",
)

p = para(bold_lead="One further consideration, beyond the arithmetic. ", after=8)
p.add_run(
    "Even if the two alternatives were a coin flip, the balance sheet is not. You will ask City Bank for an "
    "extension tomorrow with SGD85 million of short-term borrowings outstanding, a quick ratio of 0.34, and "
    "SGD54.6 million of DVD equipment still to fund. Spending SGD1.82 million of cash in 2001 to save "
    "SGD22,700 a year through 2004 is the wrong use of the scarcest resource the company has. The same "
    "SGD1.82 million is a rounding error next to the roughly SGD27 million sitting in excess inventory, which "
    "is where we would point the plant's attention instead."
)

doc.add_page_break()

# ------------------------- exhibits -------------------------
h("Exhibit A  " + DASH + "  Incremental free cash flows (SGD)", size=12, space_before=2)
para(
    "Costs shown as negative. " + LQ + "Advantage of waiting" + RQ + " is the wait cash flow less the "
    "buy-now cash flow; positive means waiting is better in that year.",
    size=9.5,
    italic=True,
    after=6,
)
fcf = [
    (2001, 0, "(1,766,492)", "0", "1,766,492"),
    (2002, 1, "(6,252)", "(55,678)", "(49,427)"),
    (2003, 2, "(7,111)", "(56,781)", "(49,671)"),
    (2004, 3, "(7,987)", "(2,164,778)", "(2,156,791)"),
    (2005, 4, "(8,882)", "(1,853)", "7,028"),
    (2006, 5, "(9,795)", "(2,767)", "7,028"),
    (2007, 6, "(10,728)", "(3,699)", "7,028"),
    (2008, 7, "(11,680)", "(4,652)", "7,028"),
    (2009, 8, "(12,653)", "(5,625)", "7,028"),
    (2010, 9, "(13,647)", "(6,619)", "7,028"),
    (2011, 10, "(14,663)", "(7,634)", "7,028"),
    (2012, 11, "(60,291)", "(8,672)", "51,618"),
    (2013, 12, "(61,352)", "(9,734)", "51,618"),
    (2014, 13, "(62,437)", "(10,818)", "51,618"),
]
rows = [[str(y), str(t), a, b, d] for (y, t, a, b, d) in fcf]
rows.append(["PV at 11%", "", "(1,875,495)", "(1,702,230)", "173,265"])
table(
    ["Year", "t", "Buy now", "Wait to 2004", "Advantage of waiting"],
    rows,
    widths=[0.75, 0.4, 1.4, 1.45, 1.6],
    right_from=1,
    size=9,
    bold_rows={len(rows) - 1},
)
para(
    "From 2015 onward both alternatives carry identical maintenance, identical labour and zero depreciation, "
    "so every later year's difference is exactly zero and the horizon cannot affect the answer. Stopping at "
    "2011, the new machine's depreciable life, would look natural and would understate the advantage of "
    "waiting by SGD44,425.",
    size=9,
    italic=True,
    after=14,
)

h("Exhibit B  " + DASH + "  Sensitivity of the advantage of waiting (SGD, present value)", size=12)
table(
    ["Assumption changed", "Advantage of waiting", "Decision"],
    [
        ["Base case: 11% WACC, 5% equipment escalation, 1.5% inflation", "173,265", "Wait"],
        ["WACC 14%", "281,813", "Wait"],
        ["WACC 8%", "56,677", "Wait"],
        ["WACC 6.61% " + DASH + " break-even", "0", "Indifferent"],
        ["WACC 6%", "(25,238)", "Buy now"],
        ["WACC 5.06%, the after-tax cost of bank debt", "(64,777)", "Buy now"],
        ["Equipment escalation 8%, against 5%", "57,208", "Wait"],
        ["Equipment escalation 9.42% " + DASH + " break-even", "0", "Indifferent"],
        ["Equipment escalation 12%", "(107,892)", "Buy now"],
        ["Labour and maintenance inflation 5%, against 1.5%", "171,199", "Wait"],
        ["Old machine must be replaced in 2003, not 2004", "117,100", "Wait"],
        ["Old machine must be replaced in 2002, not 2004", "58,455", "Wait"],
        ["Unquantified benefits of SGD34,000 p.a. pre-tax " + DASH + " break-even", "0", "Indifferent"],
        ["Annual labour saving of SGD110,811, against SGD18,200 " + DASH + " break-even", "0", "Indifferent"],
    ],
    widths=[3.75, 1.55, 1.2],
    right_from=1,
    size=9,
    bold_rows={0},
)
para(
    "Prepared from Exhibits 1 to 4. Model assumptions: 24.5% marginal tax rate; straight-line depreciation "
    "for tax and reporting; no salvage on the old equipment; no terminal value on the new equipment, which "
    "Exhibit 4 states will operate indefinitely; no change in net working capital, since packaging throughput "
    "is unchanged between the alternatives.",
    size=9,
    italic=True,
)

doc.save("FIN 4150 Project - Memo.docx")
print("written")
