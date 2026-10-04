import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, statsmodels.formula.api as smf
exec(open('models.py').read().split("def fit")[0].replace("print('manuf","#"))
d['stretch']=-d.TA  # difficulty 1..6
d['stretch_z']=(d.stretch-d.stretch.mean())/d.stretch.std()
S=d[d.manuf_mod].copy()
print(S[['prod_inn','proc_inn','rd','inn_any']].groupby(S.country).mean())
S['stretch']=-S.TA
S['prod_proc']=S[['prod_inn','proc_inn']].min(axis=1,skipna=False)
base=['ln_size','ln_age','mgr_exp','public','foreign','group','loan','quality','informal','outage','z_prod','export']
for fe in ['C(country)','C(sector)']:
  print('FE',fe)
  for y in ['prod_inn','proc_inn','rd','inn_any']:
    for x in (['stretch'],['stretch','TT','TH']):
        dd=S.dropna(subset=[y]+x+base)
        try:
            m=smf.logit(f'{y} ~ {" + ".join(x)} + {" + ".join(base)} + {fe}',dd).fit(disp=0,maxiter=200,cov_type='HC1')
            ame=m.get_margeff(at='overall').summary_frame()
            print(y,x,len(dd),{v:f"b={m.params[v]:.3f} p={m.pvalues[v]:.3f} AME={ame.loc[v,'dy/dx']:.3f}" for v in x})
        except Exception as e: print(y,x,'err',str(e)[:80])
# Descriptive: innovation rate by TT, TH levels, and by stretch
S['hard']=(S.stretch>=4).astype(float).where(S.stretch.notna())
for c in ['TT','TH','hard']:
    print(S.groupby([c])[['prod_inn','proc_inn','rd']].agg(['mean','count']).round(3))
# Country x stretch interaction for innovation
S['strk']=S.stretch*S.kor
dd=S.dropna(subset=['inn_any','stretch']+base)
m=smf.logit('inn_any ~ stretch + strk + kor + '+'+'.join(base),dd).fit(disp=0,cov_type='HC1');print(m.params[['stretch','strk','kor']],m.pvalues[['stretch','strk','kor']])
# per country
for k in (0,1):
    dd=S[S.kor==k].dropna(subset=['inn_any','stretch']+base)
    m=smf.logit('inn_any ~ stretch + '+'+'.join(base),dd).fit(disp=0,cov_type='HC1');print('country',k,len(dd),m.params['stretch'],m.pvalues['stretch'])
# bonus & targets
for y in ['prod_inn','proc_inn','rd']:
    dd=S.dropna(subset=[y,'has_target']+base)
    m=smf.logit(f'{y} ~ has_target + '+'+'.join(base)+' + C(country)',dd).fit(disp=0,cov_type='HC1');print('has_target',y,len(dd),round(m.params['has_target'],3),round(m.pvalues['has_target'],3))
# descriptives table
T=S[['TA','TT','TH','bonus','perfeval','ln_size','ln_age','mgr_exp','public','foreign','group','loan','quality','informal','outage','export','prod_inn','proc_inn','rd']]
print(T.groupby(S.country).agg(['count','mean','std']).T.round(3).to_string())
print(S[['TA','TT','TH']].corr().round(3))
