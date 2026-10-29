"""Single-deposit delta65Cu: stage bands with mineral-based colors and legend.
Run python3 plot_minerals.py. Mineral assignments are user-confirmed in data_minerals.csv.
"""
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/cu-stages-mpl')
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
d=pd.read_csv(ROOT/'data_minerals.csv')
raw=pd.read_csv(ROOT/'data_transcribed.csv')
assert len(d)==40 and d.row.is_unique and set(d.row)==set(raw.row)
for col in ['delta65Cu_permil','two_SD_permil','stage']:
    assert d[col].equals(raw[col]), f'Original {col} values must remain unchanged'
assert d.groupby('stage').size().to_dict()=={'early':2,'late':8,'main':30}
assert d.mineral.value_counts().to_dict()=={'Cc':32,'Bn':5,'Cv':3}
assert d.two_SD_permil.gt(0).all()
STYLES={
    'Cc':('#069ED0','Cc  辉铜矿','Cc  Chalcocite'),
    'Bn':('#F18719','Bn  斑铜矿','Bn  Bornite'),
    'Cv':('#60A579','Cv  铜蓝','Cv  Covellite'),
}
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':11,
    'mathtext.fontset':'dejavuserif','pdf.fonttype':42,'svg.fonttype':'none',
    'xtick.direction':'out','axes.unicode_minus':True,'savefig.facecolor':'white'})
fdir=Path('/usr/share/fonts/opentype/noto')
cjk=font_manager.FontProperties(fname=str(fdir/'NotoSerifCJK-Regular.ttc'))
cjkbold=font_manager.FontProperties(fname=str(fdir/'NotoSerifCJK-Bold.ttc'))
stages=[('early',2.5,'早期','Early'),('main',1.5,'主成矿期','Main ore stage'),('late',.5,'晚期','Late')]

def pack_stage(z,center):
    """Non-overlapping intervals share display rows; no depth or time encoded."""
    lanes=[]; entries=[]
    for _,r in z.sort_values(['delta65Cu_permil','row']).iterrows():
        left=r.delta65Cu_permil-r.two_SD_permil
        right=r.delta65Cu_permil+r.two_SD_permil
        lane=next((i for i,ends in enumerate(lanes)
                   if all(right+.065<a or left-.065>b for a,b in ends)),None)
        if lane is None: lane=len(lanes);lanes.append([])
        lanes[lane].append((left,right));entries.append((r,int(lane)))
    n=len(lanes); span=min(.79,max(0.,(n-1)*.085))
    ys=np.linspace(center+span/2,center-span/2,n)
    return [(r,float(ys[lane])) for r,lane in entries]

mapping=[]
def render(lang):
    cn=lang=='CN'
    fig,ax=plt.subplots(figsize=(8.6,5.7))
    fig.subplots_adjust(left=.07,right=.98,bottom=.25,top=.98)
    ax.set(xlim=(-2.1,2.3),ylim=(0,3),yticks=[])
    ax.spines[['top','left','right']].set_visible(False)
    ax.spines['bottom'].set_linewidth(2)
    ax.set_xticks(np.arange(-1.5,2.01,.5))
    ax.tick_params(axis='x',length=4,width=1,pad=7,labelsize=11)
    ax.set_xlabel(r'$\delta^{65}\mathrm{Cu}$ (‰)',fontsize=15,labelpad=10)
    ax.axvline(0,color='#B7B7B7',ls=(0,(3,4)),lw=.65,zorder=0)
    for y in [1,2]:ax.axhline(y,color='#424242',ls=(0,(1,3)),lw=1,zorder=0)
    for stage,center,label_cn,label_en in stages:
        z=d[d.stage==stage]
        for r,y in pack_stage(z,center):
            color=STYLES[r.mineral][0]
            ax.errorbar(r.delta65Cu_permil,y,xerr=r.two_SD_permil,fmt='none',
                ecolor=color,elinewidth=1.8,capsize=3,capthick=1.8,zorder=3)
            if cn:mapping.append({'row':int(r.row),'stage':stage,'mineral':r.mineral,'y_layout_only':y})
        ax.text(-1.98,center+.06,label_cn if cn else label_en,
            fontproperties=cjkbold if cn else None,fontweight='normal' if cn else 'bold',
            fontsize=13 if cn else 11,va='center',ha='left')
        ax.text(-1.98,center-.13,f'n = {len(z)}',color='#666666',fontsize=9,va='center')
    # Legend colors indicate mineral identity, not stages.
    handles=[]; labels=[]
    for mineral,(color,label_cn,label_en) in STYLES.items():
        if mineral not in set(d.mineral):continue
        h=ax.errorbar([],[],xerr=[],fmt='none',ecolor=color,elinewidth=1.8,capsize=3,capthick=1.8)
        handles.append(h);labels.append(label_cn if cn else label_en)
    ax.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,-.23),
        ncol=2,frameon=False,handlelength=1.6,columnspacing=2.5,
        prop=cjk if cn else {'size':10},borderaxespad=0)
    for ext in ['png','pdf','svg']:
        fig.savefig(ROOT/f'Cu_minerals_{lang}.{ext}',dpi=600,bbox_inches='tight',pad_inches=.13)
    fig.savefig(ROOT/f'Cu_minerals_{lang}_preview.png',dpi=160,bbox_inches='tight',pad_inches=.13)
    plt.close(fig)

render('CN');render('EN')
assert len(mapping)==40 and len({r['row'] for r in mapping})==40
pd.DataFrame(mapping).to_csv(ROOT/'point_row_mapping.csv',index=False)
d.groupby(['stage','mineral']).agg(n=('row','size'),min_delta65Cu=('delta65Cu_permil','min'),
    max_delta65Cu=('delta65Cu_permil','max')).to_csv(ROOT/'stage_summary.csv')
(ROOT/'validation.json').write_text(json.dumps({'analysis_rows':40,
    'counts':{'early':2,'main':30,'late':8},'mineral_counts':d.mineral.value_counts().to_dict(),
    'legend_encodes':'mineral; stage is encoded by vertical section only',
    'source':'user screenshot and subsequent user confirmation',
    'mineral_assignment_complete':True,
    'BF5_5_2':'rows 2 and 3 confirmed as Bn by user',
    'within_stage_y_positions':'interval packing for display only',
    'uncertainty':'mean +/- supplied 2SD','original_measurements_preserved':True,
    'CC_band':'not copied; numeric range not provided'},ensure_ascii=False,indent=2),encoding='utf-8')
print('Rendered all 40 analyses with mineral legend:',d.mineral.value_counts().to_dict())
