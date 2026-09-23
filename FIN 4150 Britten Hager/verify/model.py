# Independent recomputation of the Star River packaging-machine decision.
# Built from Exhibit 4 text only -- NOT from the team's workbook.
TAX   = 0.245
WACC  = 0.11
INFL  = 0.015     # labor & maintenance inflation (Ex.4)
ESC   = 0.05      # equipment price + service-contract escalation (Ex.4)

P_NOW   = 1_820_000.0
LIFE    = 10
DEP_NOW = P_NOW / LIFE            # 182,000  (Ex.4 states this)
WAIT    = 3
P_W     = P_NOW * (1+ESC)**WAIT   # deferred price
DEP_W   = P_W / LIFE

OLD_BV  = 218_400.0
OLD_LIFE= 3
DEP_OLD = OLD_BV / OLD_LIFE       # 72,800
SALV    = 0.0

MAINT_OLD = 15_470.0              # year 1 = FY2002
MAINT_NEW = 3_640.0               # first year of contract, today's price
WAGE_REG  = 63_700.0
WAGE_ACT  = 81_900.0
OT        = WAGE_ACT - WAGE_REG   # 18,200

H = 13                            # horizon, years 0..13

def esc(base, rate, t):           # cost in year t (t>=1), year 1 = base
    return base * (1+rate)**(t-1)

def flows(scenario):
    """returns list of (t, maint, labor, ot, dep, capex, writeoff_shield, fcf)"""
    rows=[]
    for t in range(0, H+1):
        capex=0.0; wo=0.0
        if scenario=="now":
            if t==0:
                capex   = -P_NOW
                wo      = (OLD_BV - SALV)*TAX        # writeoff of old machine
                rows.append((t,0,0,0,0,capex,wo,capex+wo)); continue
            maint = esc(MAINT_NEW, ESC, t)
            labor = esc(WAGE_REG, INFL, t)
            ot    = 0.0
            dep   = DEP_NOW if t<=LIFE else 0.0
        else:  # wait
            if t==0:
                rows.append((t,0,0,0,0,0,0,0.0)); continue
            if t<=WAIT:
                maint = esc(MAINT_OLD, INFL, t)
                ot    = esc(OT, INFL, t)
                dep   = DEP_OLD
            else:
                maint = esc(MAINT_NEW, ESC, t)
                ot    = 0.0
                dep   = DEP_W if t<=WAIT+LIFE else 0.0
            labor = esc(WAGE_REG, INFL, t)
            capex = -P_W if t==WAIT else 0.0
        cash_cost = maint+labor+ot
        fcf = -(cash_cost)*(1-TAX) + dep*TAX + capex
        rows.append((t,maint,labor,ot,dep,capex,0.0,fcf))
    return rows

def npv(rows, r):
    return sum(f[-1]/(1+r)**f[0] for f in rows)

now  = flows("now")
wait = flows("wait")

print(f"Deferred price         {P_W:>14,.0f}   (saving by buying now {P_W-P_NOW:,.0f})")
print(f"Dep, new machine now   {DEP_NOW:>14,.0f}")
print(f"Dep, new machine later {DEP_W:>14,.0f}")
print(f"Dep, old machine       {DEP_OLD:>14,.0f}   writeoff shield {OLD_BV*TAX:,.0f}")
print()
hdr=f"{'t':>3} {'FCF now':>13} {'FCF wait':>13} {'wait-now':>13}"
print(hdr); print("-"*len(hdr))
for a,b in zip(now,wait):
    print(f"{a[0]:>3} {a[-1]:>13,.0f} {b[-1]:>13,.0f} {b[-1]-a[-1]:>13,.0f}")
print("-"*len(hdr))
pv_now, pv_wait = npv(now,WACC), npv(wait,WACC)
print(f"PV of costs, BUY NOW  @11%: {pv_now:>15,.0f}")
print(f"PV of costs, WAIT 3Y  @11%: {pv_wait:>15,.0f}")
print(f"Advantage of WAITING (NPV wait - NPV now): {pv_wait-pv_now:>12,.0f}")
print()
# equivalent annual, common 13-year basis
def pmt(r,n,pv): return pv*r/(1-(1+r)**-n)
eac_now  = pmt(WACC,H,-pv_now)
eac_wait = pmt(WACC,H,-pv_wait)
print(f"Equivalent annual cost, BUY NOW : {eac_now:>12,.0f}")
print(f"Equivalent annual cost, WAIT    : {eac_wait:>12,.0f}")
print(f"Advantage of waiting, per year  : {eac_now-eac_wait:>12,.0f}")
print()
# crossover discount rate
lo,hi=0.0001,0.60
for _ in range(200):
    mid=(lo+hi)/2
    d=npv(wait,mid)-npv(now,mid)
    if d>0: hi=mid
    else: lo=mid
print(f"Crossover discount rate (wait = buy now): {(lo+hi)/2:.4%}")
for r in (0.05,0.07,0.08,0.09,0.10,0.11,0.12,0.15,0.20):
    d=npv(wait,r)-npv(now,r)
    print(f"  r={r:>5.1%}  advantage of waiting = {d:>12,.0f}   -> {'WAIT' if d>0 else 'BUY NOW'}")
