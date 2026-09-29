"""Verify the delivered R09 toolbar and English BESS chart using a Tk display."""
import os, sys, tempfile, time
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
os.environ['PV_APP_RECENTS_FILE']=str(Path(tempfile.gettempdir())/'pv_r09_recents.json')
from app import PVLayoutRibbonApp
from battery_dispatch import BatterySettings,simulate_three_options
r=tk.Tk();errors=[]
r.report_callback_exception=lambda *args:errors.append(args)
a=PVLayoutRibbonApp(r)
def pump():
 for _ in range(6):r.update();time.sleep(.08)
pump()
assert 'R09' in r.title()
assert a.ribbon_frame.winfo_children()==[a.ribbon_notebook],a.ribbon_frame.winfo_children()
for width in (480,640,1024,1440):
 r.geometry(f'{width}x850');pump()
 visible=set()
 for x in range(a.ribbon_notebook.winfo_width()):
  try:visible.add(a.ribbon_notebook.index(f'@{x},10'))
  except tk.TclError:pass
 assert visible==set(range(10)),(width,visible)
 print('Visible tabs:',width,sorted(visible),flush=True)
r.geometry('1440x900');pump()
from PIL import ImageGrab
folder=Path(os.environ.get('PV_SCREENSHOTS',tempfile.gettempdir()));folder.mkdir(parents=True,exist_ok=True)
ImageGrab.grab(xdisplay=os.environ['DISPLAY']).crop((0,0,1440,200)).save(folder/'r09_toolbar.png')
p={'start_date':'2026-01-01','end_date':'2026-01-01','hourly_kwh':[100]*24,'imputed_indices':[]}
pv=[0]*6+[200]*12+[0]*6
cfg=BatterySettings()
result=simulate_three_options(p,pv,cfg,300)
a.hourly_consumption_profile=p;a.hourly_pv_kwh=pv
a.self_consumption_summary=result['without_bess']
a.bess_summary={**result['one_bess'],'battery_settings':result['one_bess']['settings']}
a.two_bess_summary={**result['two_bess'],'battery_settings':result['two_bess']['settings']}
a.energy_source_signature=a._energy_signature()
a._open_hourly_chart();pump()
win=next(w for w in r.winfo_children() if isinstance(w,tk.Toplevel) and 'hourly PV' in w.title())
canvas=next(w for w in win.winfo_children() if isinstance(w,tk.Canvas))
texts=[canvas.itemcget(item,'text') for item in canvas.find_all() if canvas.type(item)=='text']
assert 'PV production and load (kWh/h)' in texts
assert 'Sources supplying the load (kWh/h)' in texts
canvas.event_generate('<Button-1>',x=50,y=100);pump()
labels=[w.cget('text') for w in win.winfo_children() if isinstance(w,ttk.Label)]
assert any('Grid import' in text and 'Grid export' in text for text in labels),labels
ImageGrab.grab(xdisplay=os.environ['DISPLAY']).save(folder/'r09_hourly_chart.png')
assert not errors,errors
print('Delivered R09 navigation and English chart verified',flush=True)
r.destroy()
