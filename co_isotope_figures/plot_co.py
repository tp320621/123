"""Reproducible, descriptive C-O figures using uploaded data only.
Run: python3 plot_co.py (outputs are next to this script).
Literature values are supplied by the user and are not independently verified.
"""
import os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', '/tmp/co-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
d = pd.read_csv(ROOT / 'samples_222.csv')
e = pd.read_csv(ROOT / 'references_111.csv')
assert len(d) == 28 and len(e) == 14
assert d['sample'].is_unique
assert d[['d13C_VPDB_permil', 'd18O_VPDB_permil', 'd18O_VSMOW_permil_converted']].notna().all().all()
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.labelsize': 12,
    'axes.linewidth': .8, 'xtick.direction': 'out', 'ytick.direction': 'out',
    'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none', 'savefig.facecolor': 'white'})
O = 'd18O_VSMOW_permil_converted'
C = 'd13C_VPDB_permil'
XL = r'$\delta^{18}$O (‰ VSMOW), calcite'
YL = r'$\delta^{13}$C (‰ VPDB), calcite'
colors = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#777777', '#E69F00', '#56B4E9']
refs = [
    ('Shuikoushan limestone', 14.1, 16.8, -.5, .3, '#56B4E9'),
    ('Kangjiawan ore calcite', 12.2, 16., -3.7, -1.8, '#E69F00'),
    ('Cocos Ridge sediment', 21., 28., .6, 1.9, '#009E73'),
    ('Primary igneous carbonate', 6.5, 9.5, -8., -2., '#CC79A7')]

def base(ax, xlim=(5, 29.5), ylim=(-9, 3)):
    ax.set(xlabel=XL, ylabel=YL, xlim=xlim, ylim=ylim)
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(alpha=.13, linewidth=.5)
    ax.set_axisbelow(True)

def boxes(ax, subset=range(4)):
    handles=[]
    for i in subset:
        name, x0, x1, y0, y1, color = refs[i]
        ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,facecolor=color,alpha=.11,zorder=0))
        ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,facecolor='none',edgecolor=color,
                               linewidth=1,linestyle='--',zorder=1))
        handles.append(Patch(facecolor=color,edgecolor=color,alpha=.35,label=name))
    return handles

def save(fig, name):
    for ext in ('png','pdf','svg'):
        fig.savefig(ROOT / f'{name}.{ext}', dpi=600, bbox_inches='tight')
    plt.close(fig)

def location(x):
    if x.startswith('围岩'): return 'Host rock'
    return {'矿体':'Orebody','矿化带':'Mineralized zone','矿化带边':'Zone margin','未注明':'Unspecified'}[x]
d['location_group'] = d.location.map(location)
d['sample_series'] = d['sample'].str.extract(r'^(BF\d+)',expand=False).fillna('Other IDs')
def appearance(x):
    if x=='白色': return 'White'
    if x=='肉红色': return 'Flesh-red'
    if x in ['红褐色','黑褐色','深褐色']: return 'Brown / dark'
    return 'Mixed / yellowish'
d['appearance_group'] = d.appearance.map(appearance)

# 1: context and carbonate analogues; no water/gas/organic pseudo-points.
fig, ax = plt.subplots(figsize=(12.5,6.7))
fig.subplots_adjust(right=.70)
base(ax); rh=boxes(ax)
groups=['Host rock','Orebody','Mineralized zone','Zone margin','Unspecified']
markers=['s','o','^','D','X']
for i,g in enumerate(groups):
    z=d[d.location_group==g]
    ax.scatter(z[O],z[C],s=58,c=colors[i],marker=markers[i],edgecolors='white',linewidths=.6,label=f'{g} (n={len(z)})',zorder=3)
leg=ax.legend(loc='upper left',bbox_to_anchor=(1.02,.58),frameon=False,title='Sample occurrence',fontsize=9)
ax.add_artist(leg)
ax.legend(handles=rh,loc='upper left',bbox_to_anchor=(1.02,1),frameon=False,fontsize=8.5,title='User-supplied carbonate references')
ax.set_title('A   Calcite C–O composition by occurrence',loc='left',pad=15)
fig.text(.12,.01,'Dashed boxes: independent marginal ranges, except the supplied igneous-carbonate field.\nReference values are user supplied; box overlap does not establish provenance.',fontsize=8,color='#555555')
save(fig,'01_CO_occurrence')

# 2: sample-number series, not inferred stages or temporal trends.
fig,ax=plt.subplots(figsize=(10.5,6.7))
base(ax,xlim=(10,22.5),ylim=(-8.3,2.1)); rh=boxes(ax,[0,1])
series=['BF5','BF8','BF9','BF10','BF11','Other IDs']
for i,g in enumerate(series):
    z=d[d.sample_series==g]
    ax.scatter(z[O],z[C],s=62,c=colors[i],marker=['o','s','^','D','P','X'][i],edgecolors='white',linewidths=.6,label=f'{g} (n={len(z)})',zorder=3)
for sid,offset in [('BF9-8-1',(9,-2)),('BF9-8-2',(-80,-7)),('BF9-2-2',(9,-2)),('BF5-2-1',(8,12)),('BF11-3-1',(-77,12))]:
    z=d[d['sample']==sid].iloc[0]
    ax.annotate(sid,(z[O],z[C]),xytext=offset,textcoords='offset points',fontsize=8,
                arrowprops={'arrowstyle':'-','color':'#777777','lw':.6})
leg=ax.legend(loc='lower left',frameon=False,ncol=2,title='Sample ID series',fontsize=9)
ax.add_artist(leg)
ax.legend(handles=rh,loc='upper left',frameon=False,fontsize=8.5)
ax.set_title('B   Sample series and carbonate reference ranges',loc='left',pad=15)
fig.text(.12,.01,'Series are derived only from sample IDs; they are not assigned mineralization stages.\nTwo reference boxes show independent C and O marginal ranges, not paired measurements.',fontsize=8,color='#555555')
save(fig,'02_CO_sample_series')

# 3: marginal distributions retain all observed points; no synthetic confidence region.
fig=plt.figure(figsize=(10.5,7.4))
gs=fig.add_gridspec(2,2,width_ratios=[5,1.2],height_ratios=[1.1,5],hspace=.06,wspace=.06)
ax=fig.add_subplot(gs[1,0]); top=fig.add_subplot(gs[0,0],sharex=ax); right=fig.add_subplot(gs[1,1],sharey=ax)
base(ax,xlim=(10,22.5),ylim=(-8.3,2.1)); rh=boxes(ax,[0,1])
appearance_groups=['White','Flesh-red','Brown / dark','Mixed / yellowish']
for i,g in enumerate(appearance_groups):
    z=d[d.appearance_group==g]
    ax.scatter(z[O],z[C],s=54,c=colors[i],marker=['o','s','D','^'][i],edgecolors='white',linewidths=.55,label=f'{g} (n={len(z)})',zorder=3)
top.hist(d[O],bins=np.arange(10,23,1),color='#7B8794',edgecolor='white',linewidth=.5)
right.hist(d[C],bins=np.arange(-8.5,2.6,.5),orientation='horizontal',color='#7B8794',edgecolor='white',linewidth=.5)
top.set_ylabel('Count',fontsize=9); right.set_xlabel('Count',fontsize=9)
top.tick_params(axis='x',labelbottom=False); right.tick_params(axis='y',labelleft=False)
for a in [top,right]: a.spines[['top','right']].set_visible(False)
leg=ax.legend(loc='lower left',frameon=False,title='Appearance (descriptive)',fontsize=8.5)
ax.add_artist(leg); ax.legend(handles=rh,loc='upper left',frameon=False,fontsize=8)
top.set_title('C   Appearance and observed isotope distributions',loc='left',pad=15)
fig.text(.12,.01,'Histograms summarize all 28 calcites. Appearance groups do not imply different generations.\nAnalytical uncertainties were not provided; error bars are therefore omitted.',fontsize=8,color='#555555')
save(fig,'03_CO_appearance_marginals')

# Explicitly normalized references, preserving phase and scale limitations.
carbon=[('Marine DIC',[0]),('Shuikoushan limestone',[-.5,.3]),('Cocos Ridge sediment',[.6,1.9]),
 ('Primary igneous carbonate',[-8,-2]),('Mantle carbon',[-5]),('MORB glass CO2',[-7.5,-4.2]),
 ('Atmospheric CO2',[-6.5,-8]),('Ancient organic carbon',[-32,-26]),('Modern organic carbon',[-22,-18]),
 ('Microbial methane',[-110,-55]),('Kangjiawan ore calcite',[-3.7,-1.8])]
oxygen=[('Ocean water',[0]),('Shuikoushan limestone',[14.1,16.8]),('Cocos Ridge sediment',[21,28]),
 ('Primary igneous carbonate',[6.5,9.5]),('Upper-mantle rock',[5.4,6]),('Granite whole rock',[7,10]),
 ('Kangjiawan ore calcite',[12.2,16])]
carbonate_names={r[0] for r in refs}
fig,axs=plt.subplots(1,3,figsize=(16,7.3),gridspec_kw={'width_ratios':[1.35,1.35,1.15]})
for ax,items,col,xlim,title,xlabel in [(axs[0],carbon,C,(-115,4),'D1   Carbon: full reference extent',r'$\delta^{13}$C (‰ VPDB)'),
 (axs[1],carbon,C,(-35,4),'D2   Carbon: expanded view',r'$\delta^{13}$C (‰ VPDB)'),
 (axs[2],oxygen,O,(-2,30),'D3   Oxygen: separate references',r'$\delta^{18}$O (‰ VSMOW)')]:
    n=len(items); ax.axvspan(d[col].min(),d[col].max(),color='#0072B2',alpha=.08,zorder=0)
    ax.scatter(d[col],np.full(len(d),n+.35),s=24,color='#0072B2',alpha=.8,zorder=4)
    for j,(name,vals) in enumerate(items):
        y=n-1-j; color='#009E73' if name in carbonate_names else '#777777'
        if name=='Atmospheric CO2':
            ax.scatter(vals,[y,y],color=color,s=30,marker='D',zorder=3)
        elif len(vals)==1:
            ax.scatter(vals,[y],color=color,s=40,marker='D',zorder=3)
        else:
            lo,hi=min(vals),max(vals)
            ax.plot([lo,hi],[y,y],color=color,lw=2.5,solid_capstyle='butt')
            ax.plot([lo,hi],[y,y],color=color,ls='none',marker='|',markersize=10)
        if ax==axs[1] and name=='Microbial methane':
            ax.annotate('off scale: −110 to −55',(-34,y),fontsize=8,color='#666666',va='center')
    ax.set(yticks=list(range(n))+[n+.35],yticklabels=[t[0] for t in items][::-1]+['This study: 28 calcites'],
           xlim=xlim,ylim=(-.8,n+1.1),xlabel=xlabel)
    ax.set_title(title,fontsize=11,loc='left',pad=15)
    ax.tick_params(axis='y',length=0,labelsize=8.5,pad=7)
    ax.spines[['top','right','left']].set_visible(False)
    ax.grid(axis='x',alpha=.15,linewidth=.5)
fig.subplots_adjust(left=.13,right=.99,top=.88,bottom=.15,wspace=.8)
fig.text(.13,.045,'Blue dots: measured calcites; blue shading: their observed range. Green: carbonate references; gray: other materials.\nC and O rows are independent comparisons, not paired C–O endmember points. Atmospheric values are two time-specific points.\nWater, gas, organic matter and whole-rock references require phase/fractionation constraints before source interpretation.',fontsize=9,color='#555555')
save(fig,'04_CO_endmember_comparison')

# Audit products.
d['conversion_1_03092_30_92'] = 1.03092*d['d18O_VPDB_permil']+30.92
d['conversion_residual_permil'] = d[O]-d['conversion_1_03092_30_92']
d.to_csv(ROOT/'samples_audited.csv',index=False)
rows=[]
for isotope,items in [('C',carbon),('O',oxygen)]:
    for name,vals in items:
        rows.append({'isotope':isotope,'label':name,'low':min(vals),'high':max(vals),
            'reference_scale':'VPDB' if isotope=='C' else 'VSMOW',
            'display_type':'two_time_points' if name=='Atmospheric CO2' else ('point' if len(vals)==1 else 'interval'),
            'independently_verified':False})
pd.DataFrame(rows).to_csv(ROOT/'references_plot_values.csv',index=False)
print('Generated 4 figures in PNG (600 dpi), PDF and editable SVG; 28 samples retained.')
