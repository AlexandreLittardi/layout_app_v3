"""Desktop integration smoke test; requires a real Tk display (e.g. Windows)."""
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
import tkinter as tk
from tkinter import messagebox
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import PVLayoutRibbonApp
from PIL import Image

with tempfile.TemporaryDirectory() as tmp:
    root=tk.Tk();errors=[]
    root.report_callback_exception=lambda *args:errors.append(args)
    app=PVLayoutRibbonApp(root);root.update()
    assert 'R10' in root.title()
    app.roof_pil_img=Image.new('RGB',(900,700),'white')
    app.roof_image_path=None;app.px_per_mm=.1
    app.roof_zones=[{'id':1,'x1':30,'y1':30,'x2':700,'y2':650,'angle_deg':30,'installation_height_m':8,'z_mm':11000}]
    app.roof_polygons=[{'id':1,'points':[(0,0),(850,0),(850,680),(0,680)],'installation_height_m':8}]
    app.generate_panels_from_zones();assert app.panels and not app._layout_issues()
    for i in range(10):
        app.ribbon_notebook.select(i);root.update();app.draw_grid();root.update()
    app.ribbon_notebook.select(7);root.update()
    app.diagram_nodes={'custom::1':{'x':150,'y':150,'label':'Test A','type':'custom'},'custom::2':{'x':500,'y':150,'label':'Test B','type':'custom'}}
    app.diagram_links=[];app.diagram_selected_nodes=set(app.diagram_nodes);app.diagram_selected_node='custom::1'
    app._diagram_group_start=(0,0);app._diagram_group_original={k:(v['x'],v['y']) for k,v in app.diagram_nodes.items()}
    app.on_left_drag(SimpleNamespace(x=25,y=30,state=0));app.on_left_release(SimpleNamespace(x=25,y=30,state=0))
    assert app.diagram_nodes['custom::2']['x']-app.diagram_nodes['custom::1']['x']==350
    app.measures=[{'p1':(0,0),'p2':(100,200),'label':(50,-20),'axis':'horizontal'}]
    app.current_project_filepath=str(Path(tmp)/'fixture.json');app.project_name='GUI smoke fixture'
    app.bess_entries['discharge_kw'].delete(0,'end');app.bess_entries['discharge_kw'].insert(0,'200')
    with patch.object(messagebox,'showinfo'),patch.object(messagebox,'showerror') as err:
        app.save_project()
        app._load_project_file(app.current_project_filepath)
        assert not err.called,err.call_args
    assert app.roof_polygons[0]['installation_height_m']==8
    assert app.roof_zones[0]['z_mm']==11000
    assert app.measures[0]['axis']=='horizontal'
    assert float(app.bess_entries['discharge_kw'].get())==200
    app._open_equipment_configuration();root.update()
    assert app._equipment_window.winfo_viewable()
    assert app.material_notebook.master==app._equipment_window
    assert not errors,errors
    root.destroy()
print('R10 desktop integration passed')
