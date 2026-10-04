import pandas as pd, numpy as np
d=pd.read_pickle('d.pkl')
def cl(s,valid=None):
    s=s.astype(float).copy(); s[s<0]=np.nan
    if valid is not None: s[~s.isin(valid)]=np.nan
    return s
d['kor']=(d.country!='Morocco').astype(int)
d['year']=d.a14y
d['TA']=-cl(d.r6,range(1,7))
d['TT']=cl(d.r7,range(1,5))
d['TH']=cl(d.r5,range(1,4))
d['bonus']=cl(d.r8,[1,2]).map({1:1,2:0})
d['perfeval']=cl(d.r10,[1,2,3,4]).map(lambda x: np.nan if pd.isna(x) else float(x==1))
d['r9c']=cl(d.r9,[1,2,3,4])
d['own_team']=d.r9c.map(lambda x: np.nan if pd.isna(x) else float(x in (1,2)))
d['needhelp_low']=d.own_team
emp=cl(d.l1); d['ln_size']=np.log(emp.where(emp>0))
b5=cl(d.b5); age=(d.year-b5.where(b5>=1900)); d['ln_age']=np.log(age.where(age>0))
d['mgr_exp']=cl(d.b7)
d['public']=(cl(d.b1,range(1,6))==1).astype(float).where(cl(d.b1).notna())
d['foreign']=(cl(d.b2b)>=10).astype(float).where(cl(d.b2b).notna())
d['state']=(cl(d.b2c)>0).astype(float).where(cl(d.b2c).notna())
d['group']=cl(d.a7,[1,2]).map({1:1,2:0})
d['loan']=cl(d.k82,[1,2,3,4]).map(lambda x: np.nan if pd.isna(x) else float(x in (1,2,3)))
d['quality']=cl(d.b8,[1,2]).map({1:1,2:0})
d['informal']=cl(d.e11,[1,2]).map({1:1,2:0})
d['outage']=cl(d.c6,[1,2]).map({1:1,2:0})
d['elec_obs']=cl(d.c30a,range(0,5)).map(lambda x: np.nan if pd.isna(x) else float(x>=3))
sales=cl(d.d2); d['ln_prod']=np.log((sales/emp).where(sales>0))
# productivity standardized within country (currencies differ)
d['z_prod']=d.groupby('country').ln_prod.transform(lambda s:(s-s.mean())/s.std())
d['export']=((cl(d.d3b).fillna(0)+cl(d.d3c).fillna(0))>0).astype(float).where(cl(d.d3b).notna()|cl(d.d3c).notna())
d['cap']=cl(d.f1); d['highcap']=(d.cap>=80).astype(float).where(d.cap.notna())
for k,c in [('prod_inn','h1'),('proc_inn','h5'),('rd','h8')]:
    d[k]=cl(d[c],[1,2]).map({1:1,2:0})
d['inn_any']=d[['prod_inn','proc_inn']].max(axis=1,skipna=False)
d['sector']=d.country.str[:3]+'_'+d.a4a.astype(str)
d['has_target']=cl(d.r4,[1,2]).map({1:1,2:0})
d['manuf_mod']=d.r4.notna()&(d.r4>0)
d.to_pickle('p.pkl')
print(d.groupby('country')[['TA','TT','TH','bonus','perfeval','ln_size','ln_age','z_prod','prod_inn','proc_inn','rd','highcap']].agg(['count','mean']).T.to_string())
