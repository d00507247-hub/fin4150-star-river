yrs=[1998,1999,2000,2001]
sales=[71924,80115,92613,106042]
prod=[33703,38393,46492,53445]
sga=[16733,17787,21301,24177]
dep=[8076,9028,10392,11360]
op=[13412,14908,14429,17059]
int_=[5464,6010,7938,7818]
ni=[5728,6576,4889,7148]
div=[2000]*4
cash=[4816,5670,6090,5795]
ar=[22148,25364,28078,35486]
inv=[23301,27662,53828,63778]
ap=[12315,12806,11890,13370]
accr=[24608,26330,25081,21318]
std=[29002,37160,73089,84981]
ltd=[10000,10000,10000,18200]
eq=[34391,38967,41856,47004]
ta=[110317,125262,161916,184873]
gppe=[64611,80153,97899,115153]

def pct(x): return f"{x*100:5.1f}%"
print(f"{'':28}"+"".join(f"{y:>10}" for y in yrs))
def row(lab,vals,f=lambda v:f"{v:10,.1f}"):
    print(f"{lab:28}"+"".join(f(v) for v in vals))
row("Sales growth",[None]+[sales[i]/sales[i-1]-1 for i in range(1,4)],
    lambda v:"        na" if v is None else f"{v*100:9.1f}%")
row("Operating margin",[op[i]/sales[i] for i in range(4)],lambda v:f"{v*100:9.1f}%")
row("Net margin",[ni[i]/sales[i] for i in range(4)],lambda v:f"{v*100:9.1f}%")
row("Interest cover (EBIT/int)",[op[i]/int_[i] for i in range(4)])
row("Total debt",[std[i]+ltd[i] for i in range(4)])
row("Debt/equity",[(std[i]+ltd[i])/eq[i] for i in range(4)])
row("Debt/EBITDA",[(std[i]+ltd[i])/(op[i]+dep[i]) for i in range(4)])
row("Current ratio",[(cash[i]+ar[i]+inv[i])/(std[i]+ap[i]+accr[i]) for i in range(4)])
row("Quick ratio",[(cash[i]+ar[i])/(std[i]+ap[i]+accr[i]) for i in range(4)])
row("Days receivable",[ar[i]/sales[i]*365 for i in range(4)])
row("Days inventory (on COGS)",[inv[i]/prod[i]*365 for i in range(4)])
row("Days payable (on COGS)",[ap[i]/prod[i]*365 for i in range(4)])
ccc=[ar[i]/sales[i]*365+inv[i]/prod[i]*365-ap[i]/prod[i]*365 for i in range(4)]
row("Cash conversion cycle",ccc)
row("ROE",[ni[i]/eq[i] for i in range(4)],lambda v:f"{v*100:9.1f}%")
row("ROA (NI/assets)",[ni[i]/ta[i] for i in range(4)],lambda v:f"{v*100:9.1f}%")
print()
print("DuPont: ROE = margin x asset turns x leverage")
for i in range(4):
    m=ni[i]/sales[i]; t=sales[i]/ta[i]; l=ta[i]/eq[i]
    print(f"  {yrs[i]}  margin {m*100:5.2f}%  turns {t:4.2f}  leverage {l:4.2f}  = ROE {m*t*l*100:5.2f}%")
print()
print("Cash flow (approx, SGD000):")
print(f"{'':28}"+"".join(f"{y:>10}" for y in yrs[1:]))
ocf=[];fcf=[]
for i in range(1,4):
    dwc=(ar[i]-ar[i-1])+(inv[i]-inv[i-1])-(ap[i]-ap[i-1])-(accr[i]-accr[i-1])
    o=ni[i]+dep[i]-dwc
    capex=gppe[i]-gppe[i-1]
    ocf.append(o); fcf.append(o-capex)
row("  NI + depreciation",[ni[i]+dep[i] for i in range(1,4)])
row("  less increase in WC",[-((ar[i]-ar[i-1])+(inv[i]-inv[i-1])-(ap[i]-ap[i-1])-(accr[i]-accr[i-1])) for i in range(1,4)])
row("  = operating cash flow",ocf)
row("  less capex",[-(gppe[i]-gppe[i-1]) for i in range(1,4)])
row("  = free cash flow",fcf)
row("  dividends paid",[-2000]*3)
row("  increase in debt",[(std[i]+ltd[i])-(std[i-1]+ltd[i-1]) for i in range(1,4)])
print()
print(f"Short-term bank debt 1998 -> 2001: {std[0]:,} -> {std[3]:,}  ({std[3]/std[0]:.2f}x)")
print(f"Inventory 1998 -> 2001:            {inv[0]:,} -> {inv[3]:,}  ({inv[3]/inv[0]:.2f}x)  vs sales {sales[3]/sales[0]:.2f}x")
print(f"Cost of bank debt: prime 5.2% + 1.5% = 6.70% pre-tax; {6.70*(1-0.245):.2f}% after tax")
