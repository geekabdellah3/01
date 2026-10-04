import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, statsmodels.formula.api as smf
from statsmodels.miscmodels.ordinal_model import OrderedModel
d=pd.read_pickle('p.pkl').copy()
# winsorize continuous at 1/99 within country
for c in ['ln_size','ln_age','mgr_exp','z_prod']:
    d[c]=d.groupby('country')[c].transform(lambda s:s.clip(s.quantile(.01),s.quantile(.99)))
CTRL=['ln_size','ln_age','mgr_exp','public','foreign','group','loan','quality','informal','outage','z_prod','export']
d['TTk']=d.TT*d.kor; d['THk']=d.TH*d.kor
S=d[d.manuf_mod].copy()
print('manuf module N',len(S),S.country.value_counts().to_dict())
def fit(y,x,data,fe='C(sector)',ctrl=CTRL,extra=''):
    f=f'{y} ~ {" + ".join(x)} + {" + ".join(ctrl)} + {fe}{extra}'
    dd=data.dropna(subset=[y]+x+ctrl)
    return smf.ols(f,dd).fit(cov_type='HC3'),dd
def row(m,vs):
    return {v:f"{m.params[v]:.3f} ({m.bse[v]:.3f}) p={m.pvalues[v]:.3f}" for v in vs if v in m.params}
res={}
for name,x in [('Eq1',['TT']),('Eq2',['TH']),('Both',['TT','TH'])]:
    for cn,data in [('Pooled',S),('Morocco',S[S.kor==0]),('Korea',S[S.kor==1])]:
        m,dd=fit('TA',x,data); print(name,cn,len(dd),row(m,x),'R2=%.3f'%m.rsquared)
        res[(name,cn)]=(m,dd)
# interaction
m,dd=fit('TA',['TT','TH','TTk','THk'],S); print('INTER',len(dd),row(m,['TT','TH','TTk','THk']))
# no controls
for x in (['TT'],['TH']):
    m=smf.ols(f'TA ~ {x[0]} + C(sector)',S.dropna(subset=['TA']+x)).fit(cov_type='HC3'); print('nocontrols',x,row(m,x))
# subsamples
subs={'PerfEval=1':('perfeval',1),'PerfEval=0':('perfeval',0),'HighCap=1':('highcap',1),'HighCap=0':('highcap',0),
 'OwnTeamBonus':('own_team',1),'FirmBonus':('own_team',0),'ElecObs=1':('elec_obs',1),'ElecObs=0':('elec_obs',0)}
for k,(v,val) in subs.items():
    sd=S[S[v]==val]
    for x in (['TT'],['TH']):
        try:
            m,dd=fit('TA',x,sd,ctrl=CTRL); print('SUB',k,x,len(dd),row(m,x))
        except Exception as e: print('SUB',k,x,'err',e)
# ordered logit
for x in (['TT'],['TH'],['TT','TH']):
    dd=S.dropna(subset=['TA']+x+CTRL)
    X=dd[x+CTRL+['kor']].astype(float)
    om=OrderedModel(dd.TA.astype(int),X,distr='logit').fit(method='bfgs',disp=0,maxiter=500)
    print('OLOGIT',x,len(dd),{v:f"{om.params[v]:.3f} p={om.pvalues[v]:.3f}" for v in x})
