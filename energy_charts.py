"""Comparable AC energy charts. Never mix battery charging with useful load supply."""
from matplotlib.figure import Figure


def comparison_figure(summaries):
    fig=Figure(figsize=(10,6),dpi=100,constrained_layout=True)
    supply,output=fig.subplots(1,2)
    names=['PV only','1 BESS','2 BESS'];rows=[s['annual'] for s in summaries]
    direct=[r.get('direct_kwh',r.get('self_kwh',0))/1000 for r in rows]
    discharge=[r.get('discharge_ac_kwh',0)/1000 for r in rows]
    grid=[r['grid_kwh']/1000 for r in rows]
    supply.bar(names,direct,label='Direct PV',color='#697e60')
    supply.bar(names,discharge,bottom=direct,label='BESS to load',color='#708ca6')
    supply.bar(names,grid,bottom=[a+b for a,b in zip(direct,discharge)],label='Grid to load',color='#b5b5b5')
    supply.set(title='How the load is supplied',ylabel='AC energy (MWh over imported period)')
    supply.legend(loc='upper center',bbox_to_anchor=(.5,-.12),ncol=1,frameon=False)
    export=[r['export_kwh']/1000 for r in rows];cut=[r.get('curtailed_kwh',0)/1000 for r in rows]
    output.bar(names,export,label='Grid export',color='#92927d')
    output.bar(names,cut,bottom=export,label='Curtailed PV',color='#d2c6b7')
    output.set(title='PV remaining after site use',ylabel='AC energy (MWh over imported period)')
    output.legend(loc='upper center',bbox_to_anchor=(.5,-.12),frameon=False)
    for ax in (supply,output):
        ax.set_ylim(bottom=0);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    return fig
