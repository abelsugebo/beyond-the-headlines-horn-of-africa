#!/usr/bin/env python3
"""Visualize coded sample counts, with explicit labels for synthetic demos."""
import argparse,json
from pathlib import Path
import matplotlib.pyplot as plt

def plot(input_file,outdir):
    s=json.loads(input_file.read_text(encoding='utf-8'))
    chart=s['by_primary_theme']
    names=list(chart);values=[chart[x] for x in names]
    fig,ax=plt.subplots(figsize=(9,5.3))
    ax.barh(names[::-1],values[::-1])
    ax.set_xlabel('Records in coded sample (not impressions or audience reach)')
    ax.set_title('Primary frames in monitored sample',loc='left')
    ax.text(0.02,-0.18,f"n={s['total_coded_records']} | {s['status']}",
            transform=ax.transAxes,fontsize=9,alpha=0.85)
    if 'SYNTHETIC' in s['status']:
        fig.text(.5,.52,'SYNTHETIC DEMO - NOT FINDINGS',ha='center',va='center',rotation=18,alpha=.17,fontsize=21,weight='bold')
    fig.tight_layout()
    outdir.mkdir(parents=True,exist_ok=True)
    target=outdir/'frame_counts.png';fig.savefig(target,dpi=170,bbox_inches='tight');plt.close(fig)
    print('Saved',target)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--summary',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();plot(a.summary,a.output)
