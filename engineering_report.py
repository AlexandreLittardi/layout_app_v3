"""Desktop engineering report: current inputs, explicit omissions, PDF and LaTeX.

No external services and no inferred equipment ratings. ReportLab generates the
PDF without a TeX installation; the same content is also written as LuaLaTeX.
"""
from pathlib import Path
from datetime import datetime, timezone
from html import escape
import json
import os
import re
from project_validation import audit_project
from energy_charts import comparison_figure

MISSING='Not supplied'


def scalar(value):
    if value is None or value=='':return MISSING
    if isinstance(value,float):return f'{value:,.4f}'.rstrip('0').rstrip('.')
    if isinstance(value,(dict,list,tuple)):return json.dumps(value,ensure_ascii=False)
    return str(value)


def report_content(app,assets):
    assets.mkdir(parents=True,exist_ok=True)
    data=app._project_snapshot()
    data.update(app._prepare_project_save())
    for name in ('roof_image_path','roof_polygons','measures','project_notes','cable_calc_params',
                 'panel_tilt_deg','panel_azimuth_deg','panel_temp_coeff_pct','panel_noct_c',
                 'solar_latitude','solar_longitude','solar_utc_offset','north_offset_deg',
                 'pylon_img_pos','pylon_ref_img_pos','pylon_height_mm','pylon_width_mm','pylon_opacity',
                 'shadow_result','shadow_simulation_results','diagram_electrical_specs'):
        data[name]=getattr(app,name,None)
    data['panel_orientations']={str(k):v for k,v in app.panel_orientations.items()}
    # Tuple keys in shadow result dictionaries are not JSON object keys.
    def serial(obj):
        if isinstance(obj,dict):return {str(k):serial(v) for k,v in obj.items()}
        if isinstance(obj,(list,tuple)):return [serial(v) for v in obj]
        return obj
    (assets/'project_inputs.json').write_text(json.dumps(serial(data),ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    blocks=[]
    def heading(t):blocks.append(('heading',t))
    def para(t):blocks.append(('text',t))
    def table(headers,rows):blocks.append(('table',headers,[[scalar(v) for v in r] for r in rows]))
    def figure(name,caption):blocks.append(('image',assets/name,caption))
    heading('1. Project and calculation status')
    para(f"Project: {app.project_name}. Exported {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}. Application R10. Engineering review document; no certification is asserted.")
    current=app._energy_results_current()
    table(['Item','Value'],[['Module count',len(app.panels)],['Module STC power (W)',app.panel_pmax_w],
        ['Installed DC nameplate (kWp)',len(app.panels)*app.panel_pmax_w/1000],['Image scale (px/mm)',app.px_per_mm],
        ['Energy results current',current],['Source image',getattr(app,'roof_image_path',None)]])
    issues=audit_project(data)
    para('Layout checks: '+('; '.join(app._layout_issues()) or 'No overlap or out-of-zone module detected.'))
    para('Electrical/project audit: '+(scalar(issues) if issues else 'No issue returned by the implemented checks. This is not a complete electrical design verification.'))
    missing=[f'Zone {i+1}: installation height missing' for i,z in enumerate(app.roof_zones) if z.get('installation_height_m') is None]
    missing += [f'Polygon {i+1}: installation height missing' for i,z in enumerate(app.roof_polygons) if z.get('installation_height_m') is None]
    para('Missing cable inputs: '+('; '.join(missing) if missing else 'No missing area heights.'))
    heading('2. Plan, installation areas and dimensions')
    table(['Zone','Width (mm)','Height (mm)','Rotation (deg)','Cable elevation (m)','Shadow elevation (mm)'],[
        [i+1,abs(z['x2']-z['x1'])/app.px_per_mm if app.px_per_mm else None,
         abs(z['y2']-z['y1'])/app.px_per_mm if app.px_per_mm else None,z.get('angle_deg',0),
         z.get('installation_height_m'),z.get('z_mm')] for i,z in enumerate(app.roof_zones)])
    table(['Routing polygon','Vertices (image pixels)','Cable elevation (m)'],[
        [i+1,p.get('points'),p.get('installation_height_m')] for i,p in enumerate(app.roof_polygons)])
    para('Panel grid rotates as a rigid lattice. Complete panel corners must remain inside the zone. Fire corridors, mounting gaps and maintenance access must be reserved in the installation boundaries. Dimensions in this section derive from the entered image scale.')
    from matplotlib.figure import Figure
    from matplotlib.patches import Polygon
    fig=Figure(figsize=(10,7),dpi=170);ax=fig.subplots()
    if app.roof_pil_img is not None:ax.imshow(app.roof_pil_img)
    for z in app.roof_zones:
        ax.add_patch(Polygon([(z['x1'],z['y1']),(z['x2'],z['y1']),(z['x2'],z['y2']),(z['x1'],z['y2'])],fill=False,edgecolor='black',linewidth=.8))
    for coord,num in app.panels.items():
        poly=app._panel_rect(coord)
        if poly:
            ax.add_patch(Polygon(poly,facecolor='#bac6cd',edgecolor='black',linewidth=.3))
            centre=app._get_panel_physical_center(coord);ax.text(*centre,str(num),ha='center',va='center',fontsize=3)
    for name,inv in app.inverter_positions.items():ax.plot(inv['x'],inv['y'],'ks',markersize=4);ax.annotate(name,(inv['x'],inv['y']),fontsize=7)
    ax.set_aspect('equal');ax.autoscale_view();ax.set_xlabel('Image x (pixels)');ax.set_ylabel('Image y (pixels)')
    if app.roof_pil_img is None:ax.invert_yaxis()
    fig.tight_layout();fig.savefig(assets/'installation_plan.png');figure('installation_plan.png','Installation plan from current project geometry. Panel numbers are included; the JSON snapshot retains exact coordinates.')
    if app.px_per_mm:
        rows=[]
        from math import hypot
        for m in app.measures:
            if not isinstance(m,dict):continue
            dx=m['p2'][0]-m['p1'][0];dy=m['p2'][1]-m['p1'][1];mode=m.get('axis','aligned')
            length=abs(dx) if mode=='horizontal' else abs(dy) if mode=='vertical' else hypot(dx,dy)
            rows.append([mode,m['p1'],m['p2'],length/app.px_per_mm])
        table(['Dimension','Start (px)','End (px)','Length (mm)'],rows)
    heading('3. Equipment and electrical schedule')
    for category,content in app.material_categories.items():
        para('Equipment category: '+category)
        rows=content.get('rows',[])
        if rows:
            table(['Equipment row','Parameter','Entered value'],[[i+1,key,value] for i,row in enumerate(rows) for key,value in row.items()])
        else:para(MISSING)
    table(['String','Modules in electrical order','Inverter','MPPT'],[
        [sid,', '.join(str(app.panels.get(tuple(p),'MISSING')) for p in coords),
         app.string_mppt_assignment.get(sid,{}).get('block'),app.string_mppt_assignment.get(sid,{}).get('mppt')]
        for sid,coords in app.strings.items() if coords])
    for index,(name,block) in enumerate(app.blocks.items(),1):
        assignments=[(sid,a) for sid,a in app.string_mppt_assignment.items() if a.get('block')==name]
        groups={}
        for sid,a in assignments:groups.setdefault(a.get('mppt'),[]).append(sid)
        if not groups:continue
        fig=Figure(figsize=(9,max(2,len(groups)*.55)),dpi=160);ax=fig.subplots();ax.axis('off')
        for j,(mppt,strings) in enumerate(sorted(groups.items(),key=lambda x:str(x[0]))):
            y=len(groups)-j
            ax.text(.02,y,', '.join(strings),ha='left',va='center',fontsize=8)
            ax.annotate('',(.56,y),(.35,y),arrowprops={'arrowstyle':'->','color':'black'})
            ax.text(.6,y,f'MPPT {mppt}',va='center',fontsize=9)
            ax.plot([.76,.85,.85],[y,y,(len(groups)+1)/2],color='black',linewidth=.8)
        ax.text(.88,(len(groups)+1)/2,name,va='center',fontsize=10)
        ax.set_xlim(0,1.08);ax.set_ylim(0,len(groups)+1);fig.tight_layout();filename=f'single_line_{index}.png';fig.savefig(assets/filename);figure(filename,f'Functional DC topology for {name}, derived from current assignments. Protection and AC connection design are not inferred.')
    heading('4. DC cable routes and voltage-drop method')
    para('L_pole = sum(planar segment lengths) + sum(abs(height changes)) + reserve. L_loop = L_A + L_B. A starts at the first module, B at the last. Inter-module and AC wiring are excluded. Short gaps retain the upstream elevation up to the configured bridge threshold; longer unsupported spans use ground level.')
    table(['Routing input','Value'],list(app.routing_settings.items()))
    routes=[];route_issues=[]
    for sid,coords in app.strings.items():
        if not coords:continue
        rec=app._calculate_two_pole_route(sid)
        if rec:routes.append((sid,rec))
        else:route_issues.append(sid)
    table(['String','A (m)','B (m)','Loop (m)','Section (mm2)','Drop (%)'],[
        [sid,r['terminal_A']['length_m'],r['terminal_B']['length_m'],r['loop_length_m'],r.get('working_section_mm2'),r.get('drop_at_working_section_pct')] for sid,r in routes])
    table(['String / conductor','Planar (m)','Vertical steps (m)','Reserve (m)','Method'],[[sid+' / '+key[-1],r[key].get('horizontal_m'),r[key]['vertical_drop_m'],r[key]['terminal_reserve_m'],r[key]['method']] for sid,r in routes for key in ('terminal_A','terminal_B')])
    para('Routes unavailable: '+(', '.join(route_issues) if route_issues else 'None.'))
    para('Voltage drop: dU = rho I L_loop / S; dU_percent = 100 dU / U. Cross-section addresses voltage drop only. Ampacity, fault current, cable temperature, protective devices and installation conditions require separate design checks.')
    table(['Sizing input','Value'],list(app.cable_calc_params.items()))
    if routes:
        fig=Figure(figsize=(10,7),dpi=160);ax=fig.subplots()
        if app.roof_pil_img is not None:ax.imshow(app.roof_pil_img)
        for sid,r in routes:
            for key,style in [('terminal_A','-'),('terminal_B','--')]:
                pts=r[key]['roof_points_px']
                if pts:ax.plot([p[0] for p in pts],[p[1] for p in pts],style,linewidth=.6)
        ax.set_aspect('equal');ax.set_title('DC routes: A solid, B dashed; heights included in inventory')
        if app.roof_pil_img is None:ax.invert_yaxis()
        fig.tight_layout();fig.savefig(assets/'cable_routes.png');figure('cable_routes.png','Plan projection of routed conductors. Direct fallback routes remain estimates requiring site validation.')
    heading('5. Solar, thermal and shadow assumptions')
    fields=['solar_latitude','solar_longitude','solar_utc_offset','north_offset_deg','panel_tilt_deg','panel_azimuth_deg',
            'panel_temp_coeff_pct','panel_noct_c','pylon_height_mm','pylon_width_mm','pylon_opacity']
    table(['Input','Value'],[[k,data[k]] for k in fields])
    para('P = P_STC (G_effective / 1000) max(0, 1 + mu_P (T_cell - 25)/100). T_cell = T_ambient + (NOCT - 20) G_effective / 800. Shadow length = (H_obstacle - H_roof) / tan(solar elevation), for positive height difference and solar elevation. Energy integrates power over the calculation period. Shadow is a geometric approximation, not an electrical mismatch or bypass-diode simulation. Saved shadow details are included in the input snapshot; they are not asserted current without a fresh simulation.')
    heading('6. Energy and BESS comparison')
    para('PV serves the load first, surplus charges the battery, remaining PV is exported up to the grid limit, then curtailed. BESS discharge meets remaining load. No grid charging, arbitrage or ancillary-service revenue is modelled. Two cabinets double energy capacity and retain shared power limits.')
    table(['Input','Value'],list(app.energy_input_settings.items())+list(app.grid_connection_settings.items()))
    profile=app.hourly_consumption_profile or {}
    para(f"Imported consumption: {len(profile.get('hourly_kwh',[]))} hourly values, {len(profile.get('imputed_indices',[]))} filled values. Totals cover that period, not necessarily a complete year. Weather/production method: {app.self_consumption_summary.get('method',MISSING)}.")
    para('For a one-hour step: direct = min(PV, load). Charge = min(surplus, charge limit, remaining storage / eta). Discharge = min(deficit, discharge limit, available storage * eta). eta = sqrt(round-trip efficiency). Stored energy changes by charge * eta - discharge / eta. Load = direct + discharge + grid. PV = direct + charge + export + curtailment.')
    summaries=[app.self_consumption_summary,app.bess_summary,app.two_bess_summary]
    if current and all(s.get('annual') for s in summaries):
        keys=sorted(set().union(*(s['annual'] for s in summaries)))
        table(['Metric','PV only','1 BESS','2 BESS'],[[k.replace('_',' '),*[s['annual'].get(k) for s in summaries]] for k in keys])
        fig=comparison_figure(summaries);fig.savefig(assets/'energy_comparison.png',dpi=170);figure('energy_comparison.png','Current comparison: load-supply and remaining PV energy, in MWh over the imported period.')
        table(['Month','Case','PV kWh','Load kWh','Grid kWh','Export kWh'],[
            [month,label,row.get('pv_kwh'),row.get('load_kwh'),row.get('grid_kwh'),row.get('export_kwh')]
            for label,summary in zip(['PV only','1 BESS','2 BESS'],summaries) for month,row in sorted(summary.get('monthly',{}).items())])
        from energy_economics import evaluate_options
        economics=evaluate_options([s['annual'] for s in summaries],app.economic_settings)
        from energy_economics import covers_full_year
        annual_period=covers_full_year(profile)
        table(['BESS count','Export price (EUR/kWh)','Benefit over period (EUR)','Investment (EUR)','Payback (years)'],[
            [r.get('bess_count'),r.get('export_eur_kwh'),r['total_benefit_eur'],r['capex_eur'],
             r['simple_payback_years'] if annual_period else 'Not calculated: partial year'] for r in economics])
        if not annual_period:para('Payback is withheld because consumption does not cover a complete year. Monetary benefits shown cover only the imported period.')
    else:para('Energy results are missing or stale. Recalculate Energy / BESS before issuing a numerical comparison. Stored historical results remain in the JSON snapshot for traceability only.')
    heading('7. Economic inputs and interpretation')
    table(['Input','Value'],list(app.economic_settings.items()))
    para('Avoided purchases = useful PV energy supplied to load x import price. Export revenue = exported energy x export price. Compare incremental battery value against PV-only. Simple payback excludes financing, tax, discounting, degradation, maintenance and replacement unless explicitly provided in another calculation. Do not annualise partial-period values without justification.')
    heading('8. Notes and review items')
    para(getattr(app,'project_notes','') or 'No project notes supplied.')
    para('Before construction: verify as-built dimensions, structural capacity, wind/snow loads, roof fixings, fire access, cold-weather string voltage, MPPT current, cable ampacity, protection coordination, earthing, manufacturer installation requirements and grid acceptance. The application does not supply those approvals.')
    heading('9. Calculation formulas')
    from home_reference import FORMULAS
    from matplotlib.mathtext import math_to_image
    from matplotlib.font_manager import FontProperties
    for group_index,(title,intro,formulas) in enumerate(FORMULAS):
        para(title+': '+intro)
        for formula_index,(formula,explanation) in enumerate(formulas):
            name=f'formula_{group_index}_{formula_index}.png'
            math_to_image('$'+formula+'$',str(assets/name),dpi=180,format='png',color='black',prop=FontProperties(family='STIXGeneral',math_fontfamily='stix'))
            blocks.append(('formula',assets/name,explanation,formula))
    heading('10. Complete input record')
    para('The accompanying project_inputs.json contains the full exported calculation inputs, per-panel geometry references, string order, MPPT assignments, material entries, stored simulation state and source profiles. Figure files and this report share the same export folder. Missing fields are explicitly marked; no manufacturer data are supplied by the report generator.')
    data['report_calculated_cable_routes']=dict(routes)
    (assets/'project_inputs.json').write_text(json.dumps(serial(data),ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    return blocks


def export_report(app,path):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    path=Path(path);assets=path.with_name(path.stem+'_assets');blocks=report_content(app,assets)
    font='Times-Roman';bold='Times-Bold'
    fontdir=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'
    normal=fontdir/'times.ttf';heavy=fontdir/'timesbd.ttf'
    if normal.exists() and heavy.exists():
        pdfmetrics.registerFont(TTFont('TimesNewRoman',str(normal)));pdfmetrics.registerFont(TTFont('TimesNewRomanBold',str(heavy)))
        font='TimesNewRoman';bold='TimesNewRomanBold'
    if font=='Times-Roman':
        # Embed the available Times-compatible Type1 fonts on Linux to avoid
        # viewer-dependent substitutions. Windows normally uses times.ttf above.
        afmdir=Path('/usr/share/fonts/type1/urw-base35')
        pfbdir=Path('/usr/share/fonts/X11/Type1')
        if all((afmdir/(name+'.afm')).exists() and (pfbdir/(name+'.pfb')).exists() for name in ('NimbusRoman-Regular','NimbusRoman-Bold')):
            for name in ('NimbusRoman-Regular','NimbusRoman-Bold'):
                face=pdfmetrics.EmbeddedType1Face(str(afmdir/(name+'.afm')),str(pfbdir/(name+'.pfb')))
                pdfmetrics.registerTypeFace(face)
                pdfmetrics.registerFont(pdfmetrics.Font(name,face.name,'WinAnsiEncoding'))
            font='NimbusRoman-Regular';bold='NimbusRoman-Bold'
    body=ParagraphStyle('body',fontName=font,fontSize=10,leading=13,spaceAfter=7)
    title=ParagraphStyle('title',parent=body,fontName=bold,fontSize=17,leading=21,spaceAfter=14)
    heading=ParagraphStyle('heading',parent=body,fontName=bold,fontSize=12,leading=15,spaceBefore=14,spaceAfter=8,keepWithNext=True)
    cell=ParagraphStyle('cell',parent=body,fontSize=8,leading=10,wordWrap='CJK')
    story=[Paragraph('Photovoltaic installation and storage study',title),Paragraph(escape(str(app.project_name)),heading)]
    if font!='TimesNewRoman':story.append(Paragraph('Typography: '+font+' (Times-compatible fallback). Times New Roman is embedded when available in Windows Fonts.',body))
    def par(text,style=body):return Paragraph(escape(str(text)).replace('\n','<br/>'),style)
    for block in blocks:
        kind=block[0]
        if kind=='heading':story.append(par(block[1],heading))
        elif kind=='text':story.append(par(block[1]))
        elif kind in ('image','formula'):
            from PIL import Image as PILImage
            with PILImage.open(block[1]) as im:w,h=im.size
            factor=min(475/w,570/h,72/180 if block[1].name.startswith("formula_") else 10)
            story.append(KeepTogether([Image(str(block[1]),width=w*factor,height=h*factor),par(block[2])]))
        elif kind=='table':
            headers,rows=block[1:]
            if not rows:story.append(par('No entries.'));continue
            data=[[par(h,cell) for h in headers]]+[[par(v,cell) for v in row] for row in rows]
            tab=Table(data,colWidths=[475/len(headers)]*len(headers),repeatRows=1,hAlign='LEFT')
            tab.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.6,colors.black),('LINEBELOW',(0,-1),(-1,-1),.4,colors.black),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
            story.extend([tab,Spacer(1,8)])
    def footer(c,doc):
        c.setFont(font,8);c.drawString(60,32,'Engineering study - '+str(app.project_name)[:70]);c.drawRightString(A4[0]-60,32,str(doc.page))
    doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=60,leftMargin=60,topMargin=48,bottomMargin=52,title=str(app.project_name),author='')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    write_latex(path.with_suffix('.tex'),blocks,app.project_name)


def write_latex(path,blocks,project):
    def tex(value):
        chars={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
        return ''.join(chars.get(c,c) for c in str(value))
    lines=[r'\documentclass[11pt,a4paper]{article}',r'\usepackage[margin=22mm]{geometry}',r'\usepackage{fontspec,longtable,graphicx,array,amsmath}',r'\IfFontExistsTF{Times New Roman}{\setmainfont{Times New Roman}}{\setmainfont{TeX Gyre Termes}}',r'\setlength{\parindent}{0pt}',r'\setlength{\parskip}{6pt}',r'\begin{document}',r'\begin{center}\Large Photovoltaic installation and storage study\end{center}',tex(project)]
    for b in blocks:
        if b[0]=='heading':lines.append(r'\section*{'+tex(b[1])+'}')
        elif b[0]=='text':lines.append(tex(b[1])+'\n')
        elif b[0]=='formula':
            lines += [r'\['+b[3]+r'\]',tex(b[2])]
        elif b[0]=='image':
            relative=b[1].relative_to(path.parent).as_posix()
            lines += [r'\begin{center}\includegraphics[width=\linewidth,height=.72\textheight,keepaspectratio]{\detokenize{'+relative+r'}}\end{center}',tex(b[2])]
        elif b[0]=='table' and b[2]:
            n=len(b[1]);spec=''.join('p{'+f'{.94/n:.3f}'+r'\linewidth}' for _ in b[1])
            lines += [r'\begin{longtable}{'+spec+'}', ' & '.join(tex(v) for v in b[1])+r'\\\hline\endhead']
            lines += [' & '.join(tex(v) for v in row)+r'\\' for row in b[2]]
            lines += [r'\end{longtable}']
    lines.append(r'\end{document}');path.write_text('\n'.join(lines),encoding='utf-8')
