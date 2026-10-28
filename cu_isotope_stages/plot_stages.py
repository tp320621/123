"""A single-deposit, three-stage delta65Cu figure from a screenshot transcription.

Run from any directory: python3 /path/to/plot_stages.py
The x error supplied is interpreted as a HALF-WIDTH, i.e. mean +/- reported 2SD.
No measurements, stages, uncertainty values or mineral identities are inferred.
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

ROOT = Path(__file__).resolve().parent
data = pd.read_csv(ROOT / 'data_transcribed.csv')
assert len(data) == 40 and data.row.is_unique
assert data.groupby('stage').size().to_dict() == {'early': 2, 'late': 8, 'main': 30}
assert np.isfinite(data[['delta65Cu_permil', 'two_SD_permil']]).all().all()
assert data.two_SD_permil.gt(0).all()

plt.rcParams.update({
    'font.family': 'DejaVu Serif', 'font.size': 12,
    'mathtext.fontset': 'dejavuserif',
    'pdf.fonttype': 42, 'svg.fonttype': 'none',
    'axes.unicode_minus': True,
    'xtick.direction': 'out', 'savefig.facecolor': 'white',
})
cjk_path = Path('/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc')
cjk_bold_path = Path('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc')
cjk = font_manager.FontProperties(fname=str(cjk_path)) if cjk_path.exists() else None
cjk_bold = font_manager.FontProperties(fname=str(cjk_bold_path)) if cjk_bold_path.exists() else cjk
stages = [
    ('early', 2.5, '#60A579', '早期', 'Early stage'),
    ('main', 1.5, '#049CD1', '主成矿期', 'Main ore stage'),
    ('late', 0.5, '#E57724', '晚期', 'Late stage'),
]
positions=[]

def render(language):
    fig, ax = plt.subplots(figsize=(10.2, 8.1))
    fig.subplots_adjust(left=.065, right=.985, bottom=.15, top=.96)
    ax.set(xlim=(-2.10,2.30), ylim=(-.015,3.015), yticks=[])
    ax.spines[['top','left','right']].set_visible(False)
    ax.spines['bottom'].set_linewidth(2.3)
    ax.tick_params(axis='x', width=1.2, length=5, pad=7, labelsize=12)
    ax.set_xticks(np.arange(-1.5,2.01,.5))
    ax.axvline(0,color='#AAAAAA',ls=(0,(3,4)),lw=.8,zorder=0)
    for boundary in (1,2):
        ax.axhline(boundary,color='#444444',ls=(0,(1,3)),lw=1.1,zorder=0)
    ax.set_xlabel(r'$\delta^{65}\mathrm{Cu}$ (‰)',fontsize=17,labelpad=12)
    for stage,center,color,label_cn,label_en in stages:
        z=data[data.stage==stage].copy()
        span=.28 if len(z)==2 else .80
        ys=np.linspace(center+span/2,center-span/2,len(z))
        ax.errorbar(z.delta65Cu_permil,ys,xerr=z.two_SD_permil,
                    fmt='none',ecolor=color,elinewidth=1.7,capsize=2.25,
                    capthick=1.7,zorder=3)
        ax.text(-1.96,center+.055,label_cn if language=='cn' else label_en,
                fontproperties=cjk_bold if language=='cn' else None,
                fontweight='normal' if language=='cn' else 'bold',
                fontsize=15 if language=='cn' else 12.5,ha='left',va='center',color='#222222')
        ax.text(-1.96,center-.12,f'n = {len(z)}',ha='left',va='center',fontsize=10.5,color='#666666')
        if language=='cn':
            for row,y in zip(z.row,ys): positions.append({'row':int(row),'stage':stage,'y_layout_only':float(y)})
    # Legend represents an individual analysis; bars are not stage-wide ranges.
    # Use axes coordinates so this key has no isotope-value interpretation.
    tx=.34; ty=-.145
    ax.plot([tx,tx+.065],[ty,ty],transform=ax.transAxes,lw=1.5,color='#444444',clip_on=False)
    ax.plot([tx,tx],[ty-.012,ty+.012],transform=ax.transAxes,lw=1.5,color='#444444',clip_on=False)
    ax.plot([tx+.065,tx+.065],[ty-.012,ty+.012],transform=ax.transAxes,lw=1.5,color='#444444',clip_on=False)
    ax.text(tx+.08,ty,('单条分析：均值 ± 2SD' if language=='cn' else 'Individual analysis: mean ± 2SD'),
            transform=ax.transAxes,va='center',fontsize=10,
            fontproperties=cjk if language=='cn' else None,color='#555555')
    suffix='CN' if language=='cn' else 'EN'
    for ext in ('png','pdf','svg'):
        fig.savefig(ROOT/f'Cu_stages_{suffix}.{ext}',dpi=600,bbox_inches='tight',pad_inches=.14)
    fig.savefig(ROOT/f'Cu_stages_{suffix}_preview.png',dpi=150,bbox_inches='tight',pad_inches=.14)
    plt.close(fig)

render('cn')
render('en')
pd.DataFrame(positions).to_csv(ROOT/'point_row_mapping.csv',index=False)
summary=data.groupby('stage').agg(n=('row','size'),min_delta65Cu=('delta65Cu_permil','min'),
    max_delta65Cu=('delta65Cu_permil','max'))
summary.to_csv(ROOT/'stage_summary.csv')
(ROOT/'validation.json').write_text(json.dumps({
    'analysis_rows':40,'counts':{'early':2,'main':30,'late':8},
    'source':'Manual transcription of user-provided screenshot; not an original spreadsheet',
    'screenshot_order_within_stages_preserved':True,
    'same_visible_prefix_rows_not_merged':True,
    'uncertainty_assumption':'reported 2SD is plotted as +/-2SD (half-width)',
    'within_stage_y_positions':'layout only; not depth or time',
    'reference_standard':'not specified; no standard assigned',
    'CC_reference_band':'not copied because no numeric definition was provided',
    'missing_depth_rows':[39],
    'data_status':'screenshot transcription; check against original spreadsheet before publication',
},ensure_ascii=False,indent=2),encoding='utf-8')
print(summary.to_string())
print('Saved Chinese and English figures (PNG 600 dpi, PDF and editable SVG).')
