import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, statsmodels.formula.api as smf, json
from statsmodels.miscmodels.ordinal_model import OrderedModel
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
exec(open('models.py').read().split("def fit")[0].replace("print('manuf","#"))
S=d[d.manuf_mod].copy(); S['stretch']=-S.TA
def fit(y,x,data,ctrl=CTRL,fe='C(sector)'):
    dd=data.dropna(subset=[y]+x+ctrl)
    return smf.ols(f'{y} ~ {" + ".join(x)} + {" + ".join(ctrl)} + {fe}',dd).fit(cov_type='HC3'),dd
def star(p): return '***' if p<.01 else '**' if p<.05 else '*' if p<.1 else ''
def cell(m,v): return f"{m.params[v]:.3f}{star(m.pvalues[v])}\n({m.bse[v]:.3f})" if v in m.params else ''
out={}
# Table 2
cols=[('(1)\nPooled',['TT'],S),('(2)\nPooled',['TH'],S),('(3)\nPooled',['TT','TH'],S),('(4)\nMorocco',['TT','TH'],S[S.kor==0]),('(5)\nKorea',['TT','TH'],S[S.kor==1])]
ms=[]
for n,x,dat in cols:
    m,dd=fit('TA',x,dat); ms.append((n,m,len(dd)))
rows=[]
labels={'TT':'Target transparency','TH':'Target horizon','ln_size':'Size (ln employees)','ln_age':'Age (ln years)','mgr_exp':'Manager experience','public':'Publicly listed','foreign':'Foreign-owned (≥10%)','group':'Part of larger firm','loan':'Has loan/credit line','quality':'Quality certification','informal':'Faces informal competitors','outage':'Power outages','z_prod':'Productivity (z, within country)','export':'Exporter'}
for v,l in labels.items():
    rows.append([l]+[cell(m,v) for _,m,_ in ms])
rows.append(['Country × sector FE']+['Yes']*5)
rows.append(['Observations']+[str(n) for _,_,n in ms])
rows.append(['R²']+[f"{m.rsquared:.3f}" for _,m,_ in ms])
out['t2']={'head':['']+[n for n,_,_ in ms],'rows':rows}
# coefficient plot data
cp={}
for nm,dat in [('Pooled',S),('Morocco',S[S.kor==0]),('Korea',S[S.kor==1])]:
    m,dd=fit('TA',['TT','TH'],dat); cp[nm]={v:(m.params[v],*m.conf_int().loc[v]) for v in ['TT','TH']}
fig,ax=plt.subplots(figsize=(6.5,3.4))
cols_={'Pooled':'#1f3a5f','Morocco':'#c4622d','Korea':'#2a8c82'}
for i,v in enumerate(['TT','TH']):
    for j,nm in enumerate(['Pooled','Morocco','Korea']):
        b,lo,hi=cp[nm][v]; y=i*4+j
        ax.errorbar(b,y,xerr=[[b-lo],[hi-b]],fmt='o',color=cols_[nm],capsize=3,label=nm if i==0 else None)
ax.axvline(0,color='grey',lw=.8,ls='--')
ax.set_yticks([1,5]); ax.set_yticklabels(['Target transparency','Target horizon']); ax.invert_yaxis()
ax.set_xlabel('Coefficient on Target_Achievement (95% CI, HC3)\n← targets harder to achieve'); ax.legend(frameon=False,loc='lower right')
for s in ['top','right']: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig('fig1.png',dpi=220)
# Table 3 contingencies with difference tests
subs=[('Performance evaluation','perfeval','Yes (promotion on performance only)','No'),('Planning (capacity utilisation ≥ 80%)','highcap','High','Low'),('Need for help (bonus on own/team performance)','own_team','Own/team bonus','Firm bonus'),('Environmental uncertainty (electricity obstacle)','elec_obs','High','Low')]
t3=[]
for lab,v,a,b in subs:
    r=[lab]
    for x in ('TT','TH'):
        res=[]
        for val in (1,0):
            m,dd=fit('TA',[x],S[S[v]==val]); res.append((m.params[x],m.bse[x],m.pvalues[x],len(dd)))
        dd=S.dropna(subset=['TA',x,v]+CTRL).copy(); dd['xs']=dd[x]*dd[v]
        mi=smf.ols(f'TA ~ {x} + xs + {v} + '+'+'.join(CTRL)+' + C(sector)',dd).fit(cov_type='HC3')
        r+= [f"{res[0][0]:.3f}{star(res[0][2])}\n({res[0][1]:.3f}) N={res[0][3]}", f"{res[1][0]:.3f}{star(res[1][2])}\n({res[1][1]:.3f}) N={res[1][3]}", f"{mi.params['xs']:.3f}\n(p={mi.pvalues['xs']:.2f})"]
    t3.append(r)
out['t3']=t3
# Table 4 robustness
rob=[]
def ol(x,dat=S):
    dd=dat.dropna(subset=['TA']+x+CTRL)
    X=dd[x+CTRL+(['kor'] if dat is S else [])].astype(float)
    return OrderedModel(dd.TA.astype(int),X,distr='logit').fit(method='bfgs',disp=0,maxiter=500),len(dd)
for lab,fn in [('OLS, baseline (Table 2, col. 3)',lambda: fit('TA',['TT','TH'],S)),
  ('OLS, no firm controls',lambda: (smf.ols('TA ~ TT + TH + C(sector)',S.dropna(subset=['TA','TT','TH'])).fit(cov_type='HC3'),len(S.dropna(subset=['TA','TT','TH'])))),
  ('OLS, Country FE only',lambda: fit('TA',['TT','TH'],S,fe='C(country)')),
  ('OLS, WLS with WBES strict weights',None),
  ('Ordered logit (country dummy)',None)]:
    if lab.startswith('Ordered'):
        om,n=ol(['TT','TH']); rob.append([lab,f"{om.params['TT']:.3f}{star(om.pvalues['TT'])}\n({om.bse['TT']:.3f})",f"{om.params['TH']:.3f}{star(om.pvalues['TH'])}\n({om.bse['TH']:.3f})",str(n)])
    elif lab.startswith('OLS, WLS'):
        dd=S.dropna(subset=['TA','TT','TH']+CTRL)
        m=smf.wls('TA ~ TT + TH + '+'+'.join(CTRL)+' + C(sector)',dd,weights=dd.wstrict).fit(cov_type='HC3'); rob.append([lab,cell(m,'TT'),cell(m,'TH'),str(len(dd))])
    else:
        r=fn(); m=r[0]; n=r[1] if isinstance(r[1],int) else len(r[1]); rob.append([lab,cell(m,'TT'),cell(m,'TH'),str(n)])
# country interaction
S['TTk']=S.TT*S.kor; S['THk']=S.TH*S.kor
m,dd=fit('TA',['TT','TH','TTk','THk'],S)
rob.append(['Interaction with Korea: TT / TH main effect (Morocco)',cell(m,'TT'),cell(m,'TH'),str(len(dd))])
rob.append(['Interaction with Korea: TT×Korea / TH×Korea',cell(m,'TTk'),cell(m,'THk'),str(len(dd))])
out['t4']=rob
# Table 5 innovation (AMEs)
base=CTRL
t5=[]
for y,lab in [('prod_inn','Product innovation'),('proc_inn','Process innovation'),('rd','R&D spending'),('inn_any','Product or process innovation')]:
    dd=S.dropna(subset=[y,'stretch','TT','TH']+base)
    m=smf.logit(f'{y} ~ stretch + TT + TH + '+'+'.join(base)+' + C(sector)',dd).fit(disp=0,cov_type='HC1',maxiter=200)
    ame=m.get_margeff().summary_frame()
    t5.append([lab]+[f"{ame.loc[v,'dy/dx']:.3f}{star(ame.loc[v,'Pr(>|z|)'])}\n({ame.loc[v,'Std. Err.']:.3f})" for v in ['stretch','TT','TH']]+[str(len(dd)),f"{dd[y].mean():.3f}"])
out['t5']=t5
# has_target
ht=[]
for y,lab in [('prod_inn','Product'),('proc_inn','Process'),('rd','R&D')]:
    dd=S.dropna(subset=[y,'has_target']+base)
    m=smf.logit(f'{y} ~ has_target + '+'+'.join(base)+' + C(sector)',dd).fit(disp=0,cov_type='HC1',maxiter=200)
    ame=m.get_margeff().summary_frame(); ht.append([lab,f"{ame.loc['has_target','dy/dx']:.3f}{star(ame.loc['has_target','Pr(>|z|)'])}",f"{ame.loc['has_target','Pr(>|z|)']:.4f}",len(dd)])
out['ht']=ht
# Table 1 descriptives
vs=[('TA','Target achievement (−1×difficulty, 1–6)'),('TT','Target transparency (1–4)'),('TH','Target horizon (1–3)'),('perfeval','Promotion on performance only'),('highcap','Capacity utilisation ≥ 80%'),('elec_obs','Electricity major/very severe obstacle'),('ln_size','Size (ln)'),('ln_age','Age (ln)'),('mgr_exp','Manager experience (yrs)'),('public','Publicly listed'),('foreign','Foreign-owned'),('loan','Loan/credit line'),('quality','Quality certification'),('informal','Informal competitors'),('export','Exporter'),('prod_inn','Product innovation'),('proc_inn','Process innovation'),('rd','R&D spending')]
t1=[]
for v,l in vs:
    r=[l]
    for k in (0,1):
        s=S[S.kor==k][v]; r+=[str(s.count()),f"{s.mean():.2f}"]
    # test diff
    from scipy import stats
    a=S[S.kor==0][v].dropna(); b=S[S.kor==1][v].dropna()
    p=stats.ttest_ind(a,b,equal_var=False).pvalue; r.append('<0.001' if p<.001 else f"{p:.3f}")
    t1.append(r)
out['t1']=t1
# TA distribution
dist=S.groupby('country').TA.value_counts(normalize=True).unstack().round(3)
print(dist)
sd=S.groupby('country').TA.agg(['mean','std','count']); print(sd)
json.dump(out,open('tables.json','w'),ensure_ascii=False,indent=1)
for k,v in out.items(): print(k); [print(r) for r in (v['rows'] if k=='t2' else v)]
