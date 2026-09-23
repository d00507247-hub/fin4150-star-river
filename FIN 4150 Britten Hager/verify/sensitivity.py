import importlib.util, sys
spec=importlib.util.spec_from_file_location("m","verify/model.py")
# re-implement compactly instead of importing (model.py prints on import)
TAX=0.245
def run(wacc=0.11, infl=0.015, esc=0.05, wait_yrs=3, ot=18200.0,
        maint_old=15470.0, p_now=1_820_000.0, extra_benefit=0.0, H=13, life=10):
    old_bv=218_400.0; dep_old=old_bv/min(3,wait_yrs) if wait_yrs>0 else 0
    maint_new=3640.0; wage=63700.0
    p_w=p_now*(1+esc)**wait_yrs
    dep_now=p_now/life; dep_w=p_w/life
    def esc_(b,r,t): return b*(1+r)**(t-1)
    def npv(scn,r):
        tot=0.0
        for t in range(0,H+1):
            if scn=="now":
                if t==0:
                    f=-p_now+old_bv*TAX
                else:
                    c=esc_(maint_new,esc,t)+esc_(wage,infl,t)
                    d=dep_now if t<=life else 0.0
                    f=-(c)*(1-TAX)+d*TAX+extra_benefit*(1-TAX)
            else:
                if t==0: f=0.0
                else:
                    if t<=wait_yrs:
                        c=esc_(maint_old,infl,t)+esc_(wage,infl,t)+esc_(ot,infl,t)
                        d=old_bv/wait_yrs
                    else:
                        c=esc_(maint_new,esc,t)+esc_(wage,infl,t)
                        d=dep_w if t<=wait_yrs+life else 0.0
                    f=-(c)*(1-TAX)+d*TAX+(-p_w if t==wait_yrs else 0.0)
            tot+=f/(1+r)**t
        return tot
    return npv("wait",wacc)-npv("now",wacc)

base=run()
print(f"BASE advantage of waiting @11%: {base:,.0f}\n")
print("Sensitivities (advantage of waiting; negative = BUY NOW wins)")
rows=[
 ("Equipment escalation 5% -> 8%",      dict(esc=0.08)),
 ("Equipment escalation 5% -> 12%",     dict(esc=0.12)),
 ("Equipment escalation 5% -> 3%",      dict(esc=0.03)),
 ("Labor/maint inflation 1.5% -> 5%",   dict(infl=0.05)),
 ("Overtime saving 18,200 -> 40,000",   dict(ot=40000.0)),
 ("Overtime saving 18,200 -> 91,000",   dict(ot=91000.0)),
 ("Old machine forces replacement in 2 yrs", dict(wait_yrs=2)),
 ("Old machine forces replacement in 1 yr",  dict(wait_yrs=1)),
 ("WACC 11% -> 8%",                     dict(wacc=0.08)),
 ("WACC 11% -> 6%",                     dict(wacc=0.06)),
 ("WACC 11% -> 5.06% (after-tax cost of bank debt)", dict(wacc=0.0506)),
 ("WACC 11% -> 14%",                    dict(wacc=0.14)),
]
for lab,kw in rows:
    v=run(**kw)
    print(f"  {lab:<50} {v:>12,.0f}  -> {'WAIT' if v>0 else 'BUY NOW'}")

# breakeven: extra un-modelled annual pre-tax benefit of the new machine, yrs 1-3 only?
# (modelled as a permanent extra benefit while the new machine runs -- conservative: yrs 1-3)
def breakeven_extra():
    lo,hi=0.0,500000.0
    for _ in range(200):
        mid=(lo+hi)/2
        if run(extra_benefit=mid)>0: lo=mid
        else: hi=mid
    return (lo+hi)/2
print(f"\nBreakeven: extra pre-tax annual benefit the new machine must deliver,")
print(f"  every year from 2002 on, to make BUYING NOW the better choice: SGD{breakeven_extra():,.0f}")

# breakeven escalation rate
def breakeven_esc():
    lo,hi=0.05,1.0
    for _ in range(200):
        mid=(lo+hi)/2
        if run(esc=mid)>0: hi=mid
        else: lo=mid
    return (lo+hi)/2
print(f"Breakeven: equipment price escalation that flips it to BUY NOW: {breakeven_esc():.2%} per year")
