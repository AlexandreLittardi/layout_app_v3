# CODEMAP (généré par tools/gen_codemap.py, ne pas éditer à la main)
Utilisation : lis cette carte AVANT d'explorer. Lis ensuite uniquement la plage de lignes utile.

### app.py (305 lignes)
Classe principale de l'application : assemble tous les mixins et contient
Imports internes : constants, mixins.cable_network, mixins.canvas_grid, mixins.detailed_electrical_ui, mixins.diagram_tools, mixins.editor_interactions, mixins.equipment_tools, mixins.hourly_chart_ui, mixins.installation_geometry, mixins.inverter_tools, mixins.material_tools, mixins.notes_tools, mixins.paths_tools, mixins.project_integrity, mixins.project_io, mixins.project_workspace, mixins.responsive_ui, mixins.self_consumption_ui, mixins.shadow_tools, mixins.spreadsheet_interactions, mixins.spreadsheet_tools, mixins.stringing_tools, mixins.two_pole_cables, mixins.ui_builders, mixins.workspace_improvements, mixins.zone_tools
- **class PVLayoutRibbonApp** L42-301
  - `__init__(root)` L69-301

### battery_dispatch.py (147 lignes)
Dispatch orario AC del BESS: solo surplus FV, senza ricarica da rete.
Imports internes : self_consumption
- **class BatterySettings** L12-34
  - `validate()` L22-34
- `simulate_bess(profile, pv_kwh, settings, export_limit_kw)` L37-94 — Restituisce i due scenari con bilanci energetici coerenti.
- `simulate_three_options(profile, pv_kwh, one_cabinet, export_limit_kw)` L97-117 — Un solo FV e carico per le tre configurazioni simultanee.
- `write_comparison_csv(path, comparison, imputed_indices)` L120-147 — Confronto a 3 opzioni sullo stesso timestamp (una riga per ora).

### constants.py (14 lignes)
Couleurs utilisees pour les strings et les blocs.
Constantes : STRING_COLORS, BLOCK_COLORS

### detailed_electrical.py (322 lignes)
Rebuildable site wiring schedule and editable, documented single-line SVG.
Imports internes : project_validation, single_line_516
Constantes : HYBRID_MODEL, BESS_MODEL
- `source_fingerprint(project)` L20-27 — Engineering design must be checked again after connections or geometry change.
- `default_design()` L30-42
- `normalise_design(saved)` L45-59
- `_rating(value, label, issues, required)` L62-70
- `build_detailed_model(project, saved_design)` L73-211
- `write_detailed_svg(model, path)` L214-322 — Produce a readable vector drawing and wiring schedule with per-field open items.

### energy_charts.py (24 lignes)
Comparable AC energy charts. Never mix battery charging with useful load supply.
- `comparison_figure(summaries)` L5-24

### energy_economics.py (76 lignes)
Value useful PV and grid exports without double-counting battery charging.
Constantes : DEFAULTS
- `validate_settings(settings)` L13-23
- `evaluate_options(annuals, settings)` L25-51
- `write_economic_csv(path, rows)` L53-57
- `storage_margin_per_charge_kwh(settings, round_trip_efficiency)` L59-65 — Gross incremental value per kWh charged and later used by the load.
- `covers_full_year(profile)` L68-76 — A complete anniversary-to-anniversary load period, including leap years.

### energy_reference.py (47 lignes)
Engineering documentation of the Energy / BESS implementation, in English.
Constantes : ENERGY_FORMULAS

### engineering_report.py (265 lignes)
Desktop engineering report: current inputs, explicit omissions, PDF and LaTeX.
Imports internes : energy_charts, energy_economics, home_reference, project_validation
Constantes : MISSING
- `scalar(value)` L18-22
- `report_content(app, assets)` L25-189
- `export_report(app, path)` L192-244
- `write_latex(path, blocks, project)` L247-265

### geometry_layout.py (96 lignes)
Shared, unit-neutral rigid layout geometry and installation cable elevations.
- `rotate(point, centre, degrees)` L5-9
- `inside(point, polygon)` L12-22
- `grid_spec(zone, width, height, scale)` L25-35
- `route_elevation(points, surfaces, scale, inverter_height, reserve, bridge_gap)` L38-86 — Split each planar segment at surface edges. Orthogonal height steps.
- `polygons_overlap(a, b)` L89-96 — Strict overlap of convex panels; shared edges are allowed.

### home_reference.py (54 lignes)
User-facing, code-audited guide. Equations are Matplotlib mathtext strings.
Imports internes : energy_reference, user_guide
Constantes : FORMULAS

### main.py (16 lignes)
Point d'entree de l'application Aide au Layout et Stringing PV.
Imports internes : app, platform_setup

### mixins/__init__.py (0 lignes)

### mixins/cable_network.py (595 lignes) ⚠ GROS FICHIER : ne pas lire en entier, utiliser les plages de lignes
Réseau de chemins de câbles (self.cable_paths, tracé dans l'onglet "Chemins")
Constantes : _NET_ROUTE_COLORS, _GRID_NEIGHBORS, _MAX_GRID_DIM
- **class CableNetworkMixin** L59-595
  - `_build_cable_network_graph()` L64-109 — Construit un graphe {noeud: [(voisin, poids_px), ...]} à partir de
  - `_segment_intersection(seg1, seg2)` L112-127 — Retourne le point d'intersection de deux segments, ou None s'ils ne
  - `_snap_point_to_network(graph, pt)` L129-165 — Projette pt sur le segment le plus proche du réseau de chemins de
  - `_dijkstra(graph, start, end)` L168-202 — Plus court chemin entre deux nœuds du graphe de chemins tracés.
  - `_build_walkable_grid()` L208-229 — Rasterise la zone de passage (polygones de l'onglet Chemins moins
  - `_nearest_walkable_cell(grid, gw, gh, gx, gy)` L232-253 — Cellule de passage la plus proche de (gx, gy) (recherche en anneaux).
  - `_grid_dijkstra(grid, gw, gh, src)` L256-280
  - `_grid_smooth_path(cells)` L283-299 — Simplifie le chemin en grille en ne gardant que les points de
  - `_route_via_walkable_area(point_a, point_b)` L301-340 — Route point_a -> point_b en évitant les obstacles, via la zone de
  - `_orthogonal_points(p1, p2)` L343-357 — Chemin à un coude (deux segments perpendiculaires) entre p1 et
  - `compute_cable_route(string_id, terminal)` L363-431 — Retourne (longueur_totale_mm, route_kind, points) pour la string
  - `compute_cable_length_mm(string_id)` L433-439 — Compatibilité : retourne (longueur_mm, via_reseau_ou_zone) — utilisé
  - `compute_all_cable_routes()` L441-467
  - `_draw_cable_network_routes(zoom)` L469-499 — Dessine les câbles calculés par compute_all_cable_routes().
  - `_dist_point_to_zone_rect(px, py, z)` L506-511
  - `_get_panel_zone_idx(coord)` L513-523 — Retourne l'index (dans self.roof_zones) de la zone contenant ce
  - `_get_zone_gather_point(zone_idx, inverter_point)` L525-552 — Point où les câbles d'une même zone se rassemblent avant le tronc
  - `_place_gather_point_at(img_x, img_y)` L554-574 — Place/déplace manuellement le point de rassemblement de la zone la
  - `_activate_gather_point_mode()` L576-581
  - `_reset_gather_points()` L583-595 — Repasse toutes les zones en calcul automatique du point de

### mixins/canvas_grid.py (1356 lignes) ⚠ GROS FICHIER : ne pas lire en entier, utiliser les plages de lignes
Interactions souris sur le canvas et dessin de la grille de panneaux.
Imports internes : constants
- **class CanvasGridMixin** L22-1352
  - `on_left_press(event)` L23-249
  - `on_left_drag(event)` L251-358
  - `on_left_release(event)` L360-482
  - `on_right_press(event)` L484-519
  - `on_right_drag(event)` L521-526
  - `_handle_ctrl_click_add(cell)` L532-553
  - `_handle_ctrl_click_remove(cell)` L555-570
  - `_zoom_at_pointer(event, delta)` L576-599
  - `create_new_block()` L605-619
  - `delete_active_block()` L621-629
  - `_update_combo_blocks()` L631-641
  - `_on_block_selected(event)` L643-647
  - `_get_grid_bounds()` L653-660
  - `_get_string_display_color(string_id, color)` L662-706 — Retourne la couleur d'affichage d'une string selon le toggle de focus (Onglet St…
  - `_is_inactive_string_dimmed(string_id)` L708-714 — Indique si une string doit être visuellement grisée.
  - `draw_grid()` L716-1256
  - `_set_layout_orientation_entries(tilt, azimuth)` L1258-1261
  - `apply_panel_orientation()` L1263-1281
  - `_update_stats_display()` L1283-1302
  - `center_view_on_origin()` L1304-1310
  - `_get_cell_coords(event)` L1312-1349
  - `_get_active_tab_index()` L1351-1352

### mixins/detailed_electrical_ui.py (287 lignes)
Editable engineering schedule for the active PV project; compact toolbar entry.
Imports internes : detailed_electrical, project_validation
- **class DetailedElectricalUIMixin** L15-287
  - `_detailed_project_snapshot()` L16-23
  - `_export_detailed_electrical_svg()` L25-35
  - `_show_detailed_electrical_editor()` L37-287

### mixins/diagram_tools.py (549 lignes) ⚠ GROS FICHIER : ne pas lire en entier, utiliser les plages de lignes
Onglet Schéma Unifilaire : génère automatiquement un schéma
Imports internes : single_line_516
Constantes : NODE_COLORS, NODE_W, NODE_H, LINK_STYLES
- **class DiagramToolsMixin** L28-549
  - `_build_tab_diagram_tools()` L33-71
  - `_build_side_panel_diagram()` L77-99
  - `_export_site_single_line(batteries, language)` L105-139 — Rebuild the site topology from the CURRENT project, not a saved image.
  - `generate_diagram_auto()` L141-228
  - `_add_custom_diagram_node()` L234-262
  - `_toggle_diagram_link_mode(style)` L264-273
  - `_cancel_diagram_link_mode()` L275-278
  - `_edit_diagram_electrical_specs()` L280-363 — Record STC module ratings and an optional nominal inverter AC rating.
  - `_toggle_diagram_electrical()` L365-371
  - `_diagram_node_metric_lines(node_id)` L373-405 — Calculate STC DC ratings using each string's actual number of modules.
  - `_delete_selected_diagram_node()` L407-418
  - `_hit_test_diagram_node(cx, cy)` L420-428
  - `_diagram_node_size(node_id)` L430-432
  - `_on_diagram_list_select(event)` L434-440
  - `_refresh_diagram_list()` L442-449
  - `_get_string_length_m(sid)` L451-462 — Longueur cumulée (en m) du câblage d'une string, panneau à panneau.
  - `_draw_diagram()` L468-549

### mixins/editor_interactions.py (88 lignes)
Explicit desktop editor gestures, without left-button canvas panning conflicts.
Imports internes : mixins.canvas_grid
- **class EditorInteractionsMixin** L4-88
  - `on_left_press(event)` L5-36
  - `on_left_drag(event)` L38-55
  - `on_left_release(event)` L57-66
  - `_on_diagram_list_select(event)` L68-70
  - `_delete_selected_diagram_node()` L72-76
  - `draw_grid()` L78-84
  - `_on_zone_combo_selected(event)` L86-88

### mixins/equipment_tools.py (457 lignes)
Gestion des equipements et repartition des strings dans les MPPT.
Imports internes : project_validation
- `natural_sort_key(s)` L21-23 — Clé de tri naturel pour ordonner correctement 'INV2' avant 'INV10' et 'String 2'…
- **class EquipmentToolsMixin** L26-453
  - `_on_block_selected_equip(event)` L27-31
  - `_update_equipment_panel_from_active()` L33-45
  - `_refresh_block_capacity_label()` L47-61
  - `_set_mppt_capacity_label(label, color)` L63-67
  - `_apply_block_equipment()` L69-86
  - `_on_mppt_current_string_changed(event)` L88-98
  - `export_mppt_csv()` L100-130 — Export every nonempty string, including unassigned strings, in a readable CSV.
  - `_get_block_string_count(block_name)` L132-142 — Nombre de strings connectées (au moins un panneau) à ce bloc/onduleur.
  - `_get_string_block(string_id)` L148-155 — Retourne le nom du bloc (onduleur) auquel appartient la string, ou None.
  - `_prune_mppt_assignments()` L157-172 — Nettoie les affectations MPPT devenues invalides (string supprimée, bloc supprim…
  - `_assign_string_to_mppt(string_id, block_name, mppt_idx, show_errors)` L174-213 — Tente d'affecter une string à un MPPT donné, en respectant la capacité et
  - `_unassign_string_from_mppt(string_id)` L215-216
  - `_clear_mppt_assignments()` L218-223
  - `_auto_distribute_strings_to_mppt()` L225-326 — Distribue les strings dans l'ordre naturel (String 1, 2, 3...) :
  - `_refresh_equipment_tree()` L328-411
  - `_format_cable_length_label(string_id)` L413-423 — Formate la longueur de câble string -> onduleur pour l'arbre équipement,
  - `_on_equip_tree_press(event)` L425-427
  - `_on_equip_tree_release(event)` L429-453

### mixins/hourly_chart_ui.py (172 lignes)
Interactive 24-hour PV, demand, load supply and battery SOC chart.
Imports internes : battery_dispatch, self_consumption
- **class HourlyChartMixin** L10-172
  - `_open_annual_chart()` L11-44
  - `_open_hourly_chart()` L46-172

### mixins/installation_geometry.py (118 lignes)
Installation transforms, common panel geometry, dimensions and elevations.
Imports internes : geometry_layout
- **class InstallationGeometryMixin** L7-118
  - `_recalculate_zone_grids()` L8-14
  - `_zone_rotate_rect(zone, x1, y1, x2, y2)` L16-20
  - `_valid_zone_cell(zone, r, c)` L22-28
  - `_get_panel_physical_center(coord)` L30-33
  - `_get_cell_coords(event)` L35-44
  - `generate_panels_from_zones()` L46-62
  - `_show_installation_heights()` L64-91
  - `_activate_dimension(mode)` L93-94
  - `_draw_dimension(measure, zoom)` L96-107
  - `_layout_issues()` L109-118

### mixins/inverter_tools.py (245 lignes)
Placement physique des onduleurs sur le plan (Onglet Layout & Blocs).
Imports internes : mixins.material_tools
- `natural_sort_key(s)` L18-20 — Clé de tri naturel pour ordonner correctement 'INV2' avant 'INV10' et 'String 2'…
- **class InverterToolsMixin** L23-245
  - `open_inverter_selection_dialog()` L28-104
  - `_start_inverter_placement(material_row)` L110-120
  - `_place_pending_inverter_at(img_x, img_y)` L122-138 — Appelé depuis on_left_press (canvas_grid.py) lorsque layout_mode == 'place_inver…
  - `remove_inverter_placement()` L140-153
  - `assign_strings_to_inverters()` L159-219 — Affecte séquentiellement les strings aux MPPT des onduleurs.
  - `_draw_inverters(zoom)` L225-245 — Dessine un marqueur pour chaque onduleur placé. Appelé depuis draw_grid()

### mixins/material_tools.py (694 lignes) ⚠ GROS FICHIER : ne pas lire en entier, utiliser les plages de lignes
Fiche matériel du projet : modules PV, onduleurs, câbles/protections et
Constantes : MATERIAL_CATEGORY_DEFS, MATERIAL_TITLES_EN, MATERIAL_COLUMNS_EN, SHEET_ALIASES, _CELL_REF_RE, _TOKEN_SPEC, _TOKEN_RE
- `default_material_categories()` L53-56 — Structure par défaut (utilisée à l'init de l'app et au chargement d'un
- `_resolve_sheet(name, default_key)` L71-77
- `_col_index_to_letters(idx)` L80-86
- `_col_letters_to_index(letters)` L89-93
- `_parse_cell_ref(token_str, sheet)` L99-105
- `_sanitize_ident(name)` L108-117 — Transforme un nom de champ personnalisé ('Marge %') en identifiant
- `_to_number(raw)` L120-131 — Convertit une valeur brute de cellule en float pour usage dans une
- `_tokenize(s)` L155-167
- **class _FormulaParser** L170-262 — Grammaire : expr := terme (('+'|'-') terme)* ; terme := unaire
  - `__init__(tokens)` L177-179
  - `_peek()` L181-182
  - `_advance()` L184-187
  - `_expect(kind)` L189-193
  - `parse()` L195-198
  - `_parse_expr()` L200-206
  - `_parse_term()` L208-214
  - `_parse_unary()` L216-221
  - `_parse_primary()` L223-235
  - `_parse_ident_expr()` L237-262
- **class MaterialToolsMixin** L265-694
  - `_build_side_panel_material()` L270-333
  - `_make_scrollable_grid(parent)` L335-376 — Zone avec ascenseurs vertical + horizontal contenant une grille de widgets.
  - `_build_material_grid_header(inner, columns)` L378-390
  - `_rebuild_material_grid_rows(key)` L396-424
  - `_rebuild_all_material_grids()` L426-429
  - `_select_material_row(key, row_idx)` L431-437
  - `_add_material_row(key)` L439-443
  - `_delete_material_row(key)` L445-454
  - `_on_material_cell_focus_in(key, row_idx, col_idx)` L460-468 — Au clic sur une cellule : affiche la formule brute (pas le résultat) pour éditio…
  - `_on_material_cell_commit(key, row_idx, col_idx)` L470-479
  - `_on_material_cell_return(key, row_idx, col_idx)` L481-489 — Entrée : valide la cellule et passe à la ligne suivante (comme un tableur).
  - `_get_material_global_vars()` L495-524 — Variables globales du projet utilisables dans une formule
  - `_compute_material_formulas()` L530-647 — Calcule toutes les cellules-formules de la fiche matériel.
  - `_format_computed_value(value)` L650-655
  - `_refresh_material_trees()` L657-694 — Point d'entrée public (nom conservé : appelé par project_io.py après

### mixins/notes_tools.py (351 lignes)
Cabling workspace: route inventory, DC voltage-drop estimate and project notes.
Imports internes : project_validation
Constantes : STANDARD_DC_SECTIONS
- `calculate_dc_cable_size(current_a, voltage_v, length_m, resistivity, target_drop_pct)` L13-29 — Estimate a two-conductor DC circuit from one-way cable length.
- **class NotesToolsMixin** L32-351
  - `_init_notes_state()` L33-42
  - `_build_tab_notes_tools()` L44-84
  - `_build_side_panel_notes()` L86-176
  - `_capture_cable_inputs()` L178-187 — Store valid edits so tab switches and project saves keep the current input.
  - `_compute_cable_size()` L189-202
  - `_on_notes_changed(event)` L204-208
  - `_refresh_notes()` L210-219
  - `_refresh_cabling_paths()` L221-234
  - `_invalidate_cable_routes()` L236-241
  - `_on_cable_path_tree_selected(event)` L243-252
  - `_refresh_cable_route_table(summary)` L254-285
  - `_on_cable_route_selected(event)` L287-290
  - `_calculate_and_show_cable_routes()` L292-299
  - `_hide_cable_routes()` L301-303
  - `_on_click_trace_cables()` L305-310 — Retained for old callbacks; the new toolbar uses the route inventory.
  - `_use_longest_cable_route()` L312-322
  - `_export_cable_routes_csv()` L324-351

### mixins/paths_tools.py (387 lignes)
Outils de tracage des chemins/polygones de cablage et mesures de distance.
- **class PathsToolsMixin** L20-387
  - `_activate_polygon_select_mode()` L21-24
  - `_activate_polygon_draw_mode()` L26-36
  - `_cancel_polygon_draw()` L38-41
  - `_finish_polygon_draw()` L43-59
  - `_update_polygon_combo()` L61-67
  - `_on_polygon_combo_selected(event)` L69-74
  - `_activate_cable_path_draw_mode()` L80-89
  - `_cancel_cable_path_draw()` L91-94
  - `_finish_cable_path_draw()` L96-114
  - `_update_cable_path_combo()` L116-126
  - `_on_cable_path_combo_selected(event)` L128-133
  - `delete_active_cable_path()` L135-147
  - `delete_active_polygon()` L149-158
  - `_point_in_polygon(px, py, points)` L161-171 — Test point-dans-polygone (ray casting).
  - `_hit_test_polygon(img_x, img_y)` L173-178 — img_x, img_y en coordonnées image d'origine. Retourne l'index du polygone conten…
  - `_toggle_distance_mode()` L184-195
  - `clear_distance_markers()` L197-199
  - `_get_all_borders()` L201-220 — Renvoie la liste de tous les bords : contour(s) du/des polygone(s) et contour de…
  - `_nearest_point_on_segment(px, py, x1, y1, x2, y2)` L223-230
  - `_nearest_point_on_borders(px, py, borders, exclude_source)` L232-243 — Retourne (x, y, distance, border) du point le plus proche de (px, py) parmi tous…
  - `_add_distance_marker_at(img_x, img_y)` L245-268 — Trouve le bord le plus proche du clic, puis le bord OPPOSÉ le plus proche de ce …
  - `_hit_test_distance_marker(cx, cy, threshold)` L270-283 — cx, cy en coordonnées canvas (déjà zoomées). Retourne l'index de la mesure la pl…
  - `_draw_text_with_bg(x, y, text, fill, font, anchor)` L285-296 — Dessine un texte sur le canvas avec un fond blanc opaque derrière, pour la lisib…
  - `_compute_polygon_overlay(zoom)` L302-325
  - `_on_canvas_motion(event)` L327-378
  - `_on_escape_key(event)` L380-387

### mixins/project_integrity.py (166 lignes)
Keep equipment, diagrams and saved simulation provenance consistent.
Imports internes : detailed_electrical, energy_economics, project_validation
Constantes : EXTRA_FIELDS
- **class ProjectIntegrityMixin** L15-166
  - `_init_energy_state()` L16-27
  - `_project_snapshot()` L29-38
  - `_sync_module_power()` L40-56
  - `_read_shadow_params_from_entries(show_errors)` L58-61
  - `_prepare_project_save()` L63-70
  - `_load_energy_state(data)` L72-99
  - `_energy_signature()` L101-114
  - `_require_current_energy()` L116-120
  - `draw_grid()` L122-132
  - `_show_electrical_audit()` L134-166

### mixins/project_io.py (516 lignes) ⚠ GROS FICHIER : ne pas lire en entier, utiliser les plages de lignes
Sauvegarde/chargement du projet JSON et exports (CSV, JPG).
Imports internes : mixins.material_tools, mixins.spreadsheet_tools, project_validation
- **class ProjectIOMixin** L24-516
  - `save_project(silent)` L25-142
  - `_on_ctrl_s(event)` L144-146
  - `_auto_save()` L148-154
  - `_flash_autosave_notice()` L156-160 — Affiche brièvement une confirmation discrète de sauvegarde automatique.
  - `import_project()` L162-169
  - `_load_project_file(filepath)` L171-434
  - `export_csv()` L436-477
  - `export_jpg_final(scale)` L480-516 — Capture le Canvas Tkinter et l'exporte directement en image JPG Ultra HD.

### mixins/project_workspace.py (96 lignes)
Project setup, embedded BESS comparison and report entry point.
Imports internes : energy_charts, engineering_report
- **class ProjectWorkspaceMixin** L7-96
  - `_build_tab_file_tools()` L8-11
  - `_show_project_configuration()` L13-28
  - `_open_equipment_configuration()` L30-31
  - `_show_grid_configuration()` L33-44
  - `_install_energy_workspace()` L46-60
  - `_refresh_energy_workspace()` L62-80
  - `_export_engineering_report()` L82-89
  - `_calculate_self_consumption()` L91-96

### mixins/responsive_ui.py (211 lignes)
Single-row ribbon with accessible overflow, no whole-window scrollbars.
- **class ResponsiveUIMixin** L5-211
  - `_on_ribbon_tab_changed(event)` L6-9
  - `_build_root_scroller()` L11-14
  - `_install_responsive_ui()` L16-36
  - `_paginate_shadow_panel()` L38-39
  - `_install_compact_zoom()` L41-56
  - `_responsive_tab_changed(event)` L58-59
  - `_fit_tab_labels()` L61-74
  - `_schedule_responsive(event)` L76-79
  - `_layout_responsive()` L81-127
  - `_fit_roof_to_window()` L129-131
  - `_apply_roof_fit()` L133-140
  - `_zoom_button_change(factor)` L142-144
  - `_zoom_at_pointer(event, delta)` L146-148
  - `_add_overflow_item(menu, w)` L150-158
  - `_show_toolbar_fields(tab)` L160-200
  - `_fit_dialog(window, width, height)` L202-206
  - `_cap_mapped_dialog(event)` L208-211

### mixins/self_consumption_ui.py (350 lignes)
Onglet Volfrigo: bilancio orario produzione FV / consumo frigorifero.
Imports internes : battery_dispatch, energy_economics, self_consumption
- **class SelfConsumptionMixin** L15-350
  - `_build_self_consumption_tab()` L16-42
  - `_show_energy_settings()` L44-45
  - `_load_consumption_excel()` L47-62
  - `_show_energy_economics()` L64-152
  - `_import_historical_weather()` L154-163
  - `_download_historical_weather()` L165-199
  - `_calculate_self_consumption()` L201-250
  - `_show_self_consumption_result()` L252-336
  - `_export_self_consumption()` L338-350

### mixins/shadow_energy.py (231 lignes)
Position solaire, irradiance ciel clair, puissance/energie des panneaux, agregation par string.
- **class ShadowEnergyMixin** L21-231
  - `_get_clear_sky_irradiance(elevation_deg)` L22-40 — Estime le DNI (irradiance normale directe) en W/m².
  - `_get_clear_sky_poa_irradiance(elevation_deg, solar_azimuth_deg, panel_coord)` L42-77 — Convertit le DNI simplifié en irradiance approximative sur le plan du module.
  - `_estimate_cell_temperature(poa_irradiance)` L79-81 — Température cellule estimée par NOCT, sans données météo réelles.
  - `_estimate_panel_power_w(poa_irradiance, shaded_fraction)` L83-104 — Puissance électrique estimée du panneau à partir de Pmax STC.
  - `_panel_energy_step(poa_irradiance, shaded_fraction, dt_hours)` L106-112 — Retourne (énergie idéale Wh, énergie ombrée Wh, perte Wh).
  - `_summarize_string_group(string_id, members)` L114-140 — Agrège les résultats panneau (dict issus de `results`) d'une string.
  - `_aggregate_shadow_results_by_string(results)` L142-171 — Regroupe les résultats de simulation par string électrique.
  - `_compute_solar_position(lat_deg, lon_deg, day, month, hour_decimal, utc_offset, year)` L173-231 — Calcule l'élévation et l'azimut solaire avec haute précision (Spencer/NOAA).

### mixins/shadow_geometry.py (246 lignes)
Geometrie de l'ombre : polygones, enveloppe convexe, projection, pourcentages d'ombrage.
- **class ShadowGeometryMixin** L21-246
  - `_polygon_area(points)` L23-30
  - `_clip_polygon_against_edge(subject, edge_start, edge_end)` L33-62 — Clippe un polygone convexe par une arête orientée (Sutherland-Hodgman).
  - `_polygon_clip(subject, clip)` L65-75
  - `_panel_rect(coord)` L77-99 — Retourne le rectangle physique du panneau en coordonnées image.
  - `_convex_hull(points)` L102-124 — Retourne l'enveloppe convexe d'un nuage de points 2D.
  - `_compute_shadow_geometry(elevation, azimuth)` L126-178 — Calcule les polygones d'ombre projetés par le pylône, par hauteur de zone.
  - `_calculate_shadow_percentages(elevation, azimuth)` L180-235 — Calcule le % d'ombre panneau par panneau, avec la hauteur de sa zone.
  - `_point_near_segment(px, py, x1, y1, x2, y2, max_dist)` L237-246

### mixins/shadow_simulation.py (1271 lignes) ⚠ GROS FICHIER : ne pas lire en entier, utiliser les plages de lignes
Fenetre de simulation temporelle d'ombrage (multi-jours, heatmap, export).
Constantes : _HEAT_STOPS, _MONTH_ABBR, _STEP_UNITS, _UNIT_SECONDS, _CHART_MAX_PERIODS, _CHART_METRICS, _CHART_PALETTES
- `_heat_rgb(t)` L26-32 — Couleur (r, g, b) du dégradé pour t dans [0, 1].
- `_rgb_hex(rgb)` L35-36
- `_text_on(rgb)` L39-42 — Texte sombre ou blanc selon la luminance du fond.
- `_nice_ticks(vmax, n)` L45-57 — Graduations « rondes » (1, 2, 2.5, 5 × 10^k) couvrant [0, vmax].
- **class ShadowSimulationMixin** L86-1271
  - `_open_shadow_simulation()` L87-788 — Ouvre la simulation temporelle d'ombrage avec intégration par intervalles.
  - `_aggregate_shadow_series(results, unit, count)` L794-886 — Agrège l'énergie simulée par période.
  - `_chart_label(unit, start, prev_start, multi_year)` L889-903 — Étiquette de l'axe X : « jan. », « 15 jan. », « 14:05\n15 jan. »…
  - `_chart_range_text(unit, start, end)` L906-927 — Description complète d'une période (info-bulle).
  - `_show_simulation_chart()` L932-1271

### mixins/shadow_tools.py (518 lignes) ⚠ GROS FICHIER : ne pas lire en entier, utiliser les plages de lignes
Onglet/panneau lateral ombre du pylone et callbacks UI.
Imports internes : .shadow_energy, .shadow_geometry, .shadow_simulation
- **class ShadowToolsMixin** L25-515
  - `_build_tab_shadow_tools()` L26-60
  - `_build_side_panel_shadow()` L62-237 — Construit le panneau latéral de paramétrage de l'ombre du pylône.
  - `_toggle_shadow_params_panel()` L239-244
  - `_activate_place_pylon_mode()` L246-251
  - `_activate_place_ref_mode()` L253-258
  - `_clear_pylon()` L260-269
  - `_update_shadow_delta_entries()` L271-280
  - `_apply_pylon_delta_position()` L282-298
  - `_refresh_shadow_zone_list()` L300-306
  - `_on_shadow_zone_selected(event)` L308-317
  - `_apply_shadow_zone_height()` L319-332
  - `_decimal_hour_to_hhmm(hour)` L335-338
  - `_hhmm_to_decimal_hour(value)` L341-348
  - `_on_shadow_hour_slider(value)` L350-365 — Synchronise le curseur avec l'heure solaire locale et recalcule immédiatement.
  - `_schedule_shadow_recompute(event)` L367-373
  - `_auto_recompute_shadow()` L375-381
  - `_read_shadow_params_from_entries(show_errors)` L383-429 — Lit les entrées du panneau latéral et met à jour les paramètres. Renvoie True si…
  - `_update_shadow_status_label()` L431-465
  - `_recompute_shadow()` L471-515 — Recalcule la position solaire et le % d'ombre de chaque panneau.

### mixins/spreadsheet_interactions.py (183 lignes)
Cell-range selection, fill handle, formula references and clipboard actions.
Imports internes : mixins.spreadsheet_tools
Constantes : _REFERENCE
- `shift_formula(formula, dr, dc)` L9-16 — Shift relative references when a formula is dragged to another cell.
- **class SpreadsheetInteractionsMixin** L19-183
  - `_rebuild_spreadsheet_grid()` L20-25
  - `_init_spreadsheet_state()` L27-32
  - `_build_material_spreadsheet_area()` L34-40
  - `_spreadsheet_rect_coords(first, last)` L42-47
  - `_draw_spreadsheet_selection()` L49-62
  - `_insert_clicked_cell_reference(cell)` L64-72
  - `_on_spreadsheet_cell_click(event)` L74-98
  - `_spreadsheet_cell_drag(event)` L100-113
  - `_spreadsheet_cell_release(event)` L115-122
  - `_spreadsheet_fill_to(target)` L124-157
  - `_spreadsheet_copy(event)` L159-167
  - `_spreadsheet_paste(event)` L169-183

### mixins/spreadsheet_tools.py (1276 lignes) ⚠ GROS FICHIER : ne pas lire en entier, utiliser les plages de lignes
Feuille de calcul type tableur (façon Google Sheets simplifié) affichée
Imports internes : project_validation
Constantes : DEFAULT_ROWS, DEFAULT_COLS, MAX_ROWS, MAX_COLS, _CELL_REF_RE, _COLON_RANGE_RE, _RANGE_TOKEN_RE, _BINOPS, _UNARY
- `col_letter(index)` L71-78 — 0 -> 'A', 25 -> 'Z', 26 -> 'AA' ...
- `col_index(letters)` L81-86 — 'A' -> 0, 'Z' -> 25, 'AA' -> 26 ...
- `cell_id(row, col)` L89-91 — (0, 0) -> 'A1' (row/col 0-indexés).
- `parse_cell_id(ref)` L94-100 — 'C3' -> (2, 2) (row, col 0-indexés), ou None si ce n'est pas une
- `_to_number(raw)` L103-114 — Convertit une valeur brute de cellule en float si possible, sinon la
- `default_spreadsheet_state()` L117-121 — Structure par défaut (utilisée à l'init de l'app et au chargement
- **class _FormulaError** L128-129
- `_eval_formula_ast(expr, cell_lookup, variables)` L132-196 — Évalue en toute sécurité une formule : + - * / % ** parenthèses,
- **class SpreadsheetToolsMixin** L199-1276
  - `_init_spreadsheet_state()` L204-225
  - `_get_spreadsheet_variables()` L231-305 — Variables numériques disponibles dans les formules, en plus des
  - `_refresh_variable_explorer()` L307-338
  - `_insert_selected_variable()` L340-343
  - `_compute_spreadsheet_values()` L349-386 — Calcule toutes les cellules de la feuille de calcul. Retourne
  - `_format_spreadsheet_value(value)` L389-396
  - `_build_material_spreadsheet_area()` L402-497 — Construit la grille de calcul dessinée nativement sur un Canvas
  - `_on_spreadsheet_data_yscroll(first, last)` L499-501
  - `_on_spreadsheet_data_xscroll(first, last)` L503-505
  - `_on_spreadsheet_mousewheel(event)` L507-509
  - `_on_spreadsheet_mousewheel_shift(event)` L511-513
  - `_spreadsheet_col_w(c)` L523-527
  - `_spreadsheet_row_h(r)` L529-533
  - `_spreadsheet_col_x(c)` L535-536
  - `_spreadsheet_row_y(r)` L538-539
  - `_spreadsheet_set_col_w(c, width)` L541-546
  - `_spreadsheet_set_row_h(r, height)` L548-553
  - `_zoom_spreadsheet(factor)` L555-558
  - `_reset_spreadsheet_zoom()` L560-563
  - `_spreadsheet_col_border_at(cx)` L565-573 — Index de la colonne dont la bordure droite passe près de cx, ou None.
  - `_spreadsheet_row_border_at(cy)` L575-582
  - `_on_spreadsheet_colheader_motion(event)` L586-591
  - `_on_spreadsheet_colheader_press(event)` L593-600
  - `_on_spreadsheet_colheader_drag(event)` L602-608
  - `_on_spreadsheet_colheader_release(event)` L610-613
  - `_on_spreadsheet_rowheader_motion(event)` L617-622
  - `_on_spreadsheet_rowheader_press(event)` L624-631
  - `_on_spreadsheet_rowheader_drag(event)` L633-639
  - `_on_spreadsheet_rowheader_release(event)` L641-644
  - `_rebuild_spreadsheet_grid()` L649-717 — (Re)dessine entièrement la grille (après ajout/suppression de
  - `_refresh_spreadsheet()` L719-739 — Recalcule toutes les formules et met à jour l'affichage de
  - `_draw_spreadsheet_selection()` L745-768
  - `_spreadsheet_ensure_visible(row, col)` L770-796
  - `_spreadsheet_cell_at_event(event)` L798-822
  - `_on_spreadsheet_cell_click(event)` L824-832
  - `_on_spreadsheet_cell_double_click(event)` L834-840
  - `_spreadsheet_move_selection(dr, dc)` L842-857
  - `_spreadsheet_start_edit(initial_text)` L863-892
  - `_spreadsheet_finish_edit(move_down, move_right)` L894-914
  - `_spreadsheet_commit_edit()` L916-919 — Valide la cellule en cours d'édition sans déplacer la sélection
  - `_spreadsheet_cancel_edit()` L921-922
  - `_spreadsheet_destroy_edit_widget()` L924-937
  - `_on_spreadsheet_key_return(event)` L943-948
  - `_on_spreadsheet_key_delete(event)` L950-957
  - `_on_spreadsheet_key_type(event)` L959-970 — Taper directement un caractère sur une cellule sélectionnée
  - `_add_spreadsheet_row()` L976-981
  - `_add_spreadsheet_col()` L983-988
  - `_remove_spreadsheet_row()` L990-1012
  - `_remove_spreadsheet_col()` L1014-1036
  - `_clear_spreadsheet()` L1038-1044
  - `_get_zone_string_insert_vars()` L1046-1067 — Variables numériques (catégorie A) générées dynamiquement à partir
  - `_insert_text_into_active_cell(text)` L1070-1088 — Insère `text` dans la cellule active, à la position du curseur si
  - `_insert_spreadsheet_variable(name)` L1090-1120
  - `_apply_spreadsheet_formula_bar(event)` L1122-1135
  - `_export_spreadsheet_csv()` L1137-1153
  - `_import_spreadsheet_csv()` L1155-1187
  - `_show_spreadsheet_chart()` L1189-1276

### mixins/stringing_tools.py (444 lignes)
Gestion des strings (creation, edition, generation automatique).
Imports internes : project_validation
- `natural_sort_key(s)` L21-23 — Clé de tri naturel pour ordonner correctement 'INV2' avant 'INV10' et 'String 2'…
- **class StringingToolsMixin** L26-444
  - `add_panel_to_string(cell)` L27-43
  - `remove_panel_from_strings(cell)` L45-55
  - `_clean_deleted_panels_from_strings()` L57-59
  - `_update_string_listbox(selected_panel_index)` L61-88
  - `_on_string_tree_selected(event)` L90-101
  - `_selected_string_panel_index()` L103-110
  - `_move_panel_in_string(direction)` L112-123
  - `_add_panel_manual_dialog()` L125-138
  - `_remove_panel_from_string_list()` L140-149
  - `add_new_string()` L151-166
  - `delete_active_string()` L168-183
  - `clear_all_strings()` L185-192
  - `_get_sorted_string_keys()` L194-195
  - `_update_combo_strings()` L197-206
  - `_on_active_string_changed(event)` L208-213
  - `_get_panel_physical_center(coord)` L219-238
  - `generate_auto_strings()` L240-387
  - `_split_balanced(items, min_per_string, max_per_string)` L389-408
  - `_get_next_available_panel_number()` L414-419
  - `update_dimensions()` L421-431
  - `_find_zone_for_panel(coord)` L433-444

### mixins/two_pole_cables.py (119 lignes)
Both string terminals, using the supplied router and verified saved routes.
Imports internes : geometry_layout, mixins.notes_tools, project_validation, single_line_516
- **class TwoPoleCablesMixin** L8-119
  - `_route_signature()` L9-17
  - `get_two_pole_route(sid)` L19-26
  - `_calculate_two_pole_route(sid)` L28-67
  - `compute_cable_length_mm(sid)` L69-71
  - `compute_all_cable_routes()` L73-92
  - `_draw_cable_network_routes(zoom)` L94-119

### mixins/ui_builders.py (703 lignes) ⚠ GROS FICHIER : ne pas lire en entier, utiliser les plages de lignes
Construction de l'interface ruban (onglets, panneaux lateraux).
Constantes : QUICK_START_GUIDE, FORMULA_GUIDE, TECHNICAL_GUIDE
- **class UIBuildersMixin** L93-698
  - `_load_ui_preferences()` L94-111
  - `_show_ui_preferences()` L113-154
  - `_build_root_scroller()` L156-176 — One outer scrollbar pair for the complete toolbar and work area.
  - `_update_root_scrollregion(event)` L178-179
  - `_resize_root_scroll_content(event)` L181-189
  - `_show_help(page)` L191-218 — Affiche une aide intégrée sans dépendre d'un fichier externe.
  - `_center_window(window, width, height)` L220-226
  - `_fix_combobox_popdown_position(combo)` L228-242
  - `_zoom_button_change(factor)` L244-250
  - `_reset_zoom()` L252-255
  - `_get_image_resample_filter()` L258-263 — Retourne un filtre de redimensionnement compatible avec Pillow.
  - `_build_ribbon_ui()` L269-307
  - `_build_tab_file_tools()` L313-348
  - `_build_tab_roof_tools()` L354-426
  - `_build_tab_layout_tools()` L432-518
  - `_build_tab_stringing_tools()` L524-563
  - `_show_string_settings()` L565-582
  - `_build_tab_equipment_tools()` L588-634
  - `_show_mppt_settings()` L636-658
  - `_build_tab_material_tools()` L664-698

### mixins/workspace_improvements.py (408 lignes)
Home, recent projects, compact layout controls and universal CSV preview.
Imports internes : home_reference
- **class WorkspaceImprovementsMixin** L17-408
  - `_build_tab_file_tools()` L18-30
  - `_build_tab_layout_tools()` L32-79
  - `_show_panel_configuration()` L81-107
  - `_install_home()` L109-187
  - `_install_energy_workspace()` L189-212
  - `_refresh_energy_workspace()` L214-231
  - `_energy_results_current()` L233-235
  - `_calculate_self_consumption()` L237-240
  - `_on_ribbon_tab_changed(event)` L242-252
  - `_show_home()` L254-257
  - `_show_help(page)` L259-262
  - `_recent_path()` L264-265
  - `_read_recent_projects()` L267-272
  - `_remember_recent_project(path)` L274-288
  - `_refresh_recent_projects()` L290-298
  - `_open_recent_selection()` L300-307
  - `on_left_press(event)` L309-323
  - `on_left_drag(event)` L325-333
  - `on_left_release(event)` L335-346
  - `_export_with_csv_preview(callback, initialfile)` L348-362 — Run the existing CSV writer against a private temporary path, then preview and s…
  - `_preview_csv_file(staged, initialfile)` L364-402
  - `export_csv()` L404-404
  - `export_mppt_csv()` L405-405
  - `_export_cable_routes_csv()` L406-406
  - `_export_spreadsheet_csv()` L407-407
  - `_export_self_consumption()` L408-408

### mixins/zone_tools.py (675 lignes) ⚠ GROS FICHIER : ne pas lire en entier, utiliser les plages de lignes
Gestion des zones de toiture, de l'echelle et de la zone principale.
- **class ZoneToolsMixin** L20-671
  - `_build_main_area()` L21-239
  - `_toggle_zone_params_panel()` L243-249
  - `_on_string_tree_start_drag(event)` L255-256
  - `_on_string_tree_drop(event)` L258-276
  - `_on_ribbon_tab_changed(event)` L282-355
  - `load_roof_image()` L361-401
  - `_activate_scale_mode()` L403-409
  - `_activate_measure_mode()` L411-420
  - `clear_measures()` L422-426
  - `_activate_zone_mode()` L428-437
  - `_activate_zone_select_mode()` L439-442
  - `_update_zone_combo()` L444-450
  - `_on_zone_combo_selected(event)` L452-458
  - `delete_active_zone()` L460-479
  - `_update_zone_entries_from_active()` L481-509
  - `update_active_zone_params()` L511-546
  - `_recalculate_zone_grids()` L548-604 — Calcule le nombre de lignes/colonnes et l'offset exact au mm près pour chaque zo…
  - `_zone_panel_center(x1, y1, x2, y2)` L614-615
  - `_zone_rotate_point(zone, cx, cy, x, y)` L617-628 — Tourne un point (x, y) autour du centre donné (cx, cy), selon
  - `_zone_rotate_rect(zone, x1, y1, x2, y2)` L630-635 — 4 coins tournés (TL, TR, BR, BL) d'un panneau autour de SON PROPRE
  - `_update_zones_from_scale()` L637-641 — Recalcule les grilles de zones et rafraîchit l'affichage suite au calibrage.
  - `generate_panels_from_zones()` L643-671

### platform_setup.py (16 lignes)
Reglages specifiques a la plateforme (DPI Windows).
- `configure_windows_dpi()` L5-16 — A appeler une seule fois au demarrage sur Windows pour un rendu net.

### project_validation.py (185 lignes)
Project migrations and electrical checks; never invent missing ratings.
Constantes : INVERTER_MODEL, FORMULA_ALIASES
- `string_label(identifier)` L10-13 — Compact visible label without changing saved string identifiers.
- `english_formula(value)` L23-34
- `normalize_formula_storage(data)` L36-43 — Migrate formula identifiers in both saved sheets, preserving nonformula text.
- `number(value)` L45-50
- `natural(value)` L52-53
- `sync_diagram(data)` L55-96 — Assignments own generated wiring. Preserve custom devices and positions.
- `resolve_image(filepath, stored)` L98-109
- `normalize_project(original)` L111-145
- `audit_project(data)` L147-185 — Return explicit failures and missing engineering inputs, without approval.

### self_consumption.py (253 lignes)
Profili orari e bilancio FV/utenza. Nessuna batteria nel calcolo.
- `read_open_meteo_json(path, profile)` L12-57 — Allinea meteo storico Open-Meteo alle 24 colonne locali per giorno.
- `read_daily_excel(path)` L60-102 — Legge il formato Volfrigo: data, giorno, colonne 0..23 in kWh.
- `timestamps(profile)` L105-112
- `production_from_program(app, profile, ac_factor, progress, weather)` L115-216 — Usa gli stessi metodi di energia, sole e ombra del programma.
- `balance(profile, pv_kwh, export_limit_kw)` L219-245
- `write_hourly_csv(path, result)` L248-253

### single_line_516.py (262 lignes)
Preliminary AC/DC single-line drawing derived from the active PV project.
Imports internes : project_validation
Constantes : INVERTER, BATTERY
- `route_is_current(data, sid)` L18-51
- `build_model(data, batteries)` L54-105
- `write_svg(model, path, language)` L108-262 — One drawing with site one-line and exact string-to-MPPT schedule.

### tests/test_detailed_electrical.py (63 lignes)
Ensure the exported physical connections follow the active project.
Imports internes : detailed_electrical
Constantes : PROJECT
- **class DetailedElectricalTests** L14-60
  - `setUp()` L15-16
  - `test_project_mppt_two_poles_and_dc_battery_ports()` L18-31
  - `test_two_cabinets_do_not_invent_parallel_connection()` L33-40
  - `test_stale_design_ratings_and_valid_vector_export()` L42-60

### tests/test_installation.py (77 lignes)
Imports internes : energy_economics, geometry_layout, mixins.cable_network, mixins.installation_geometry, mixins.paths_tools, mixins.shadow_geometry, single_line_516
- **class Geometry** L8-9
- `surface(x1, x2, h)` L11-12
- **class InstallationTests** L14-59
  - `test_bridge_keeps_upstream_height_and_counts_single_step()` L15-22
  - `test_bridge_across_several_polyline_segments()` L24-27
  - `test_missing_and_conflicting_height_rejected()` L29-31
  - `test_no_shadow_height_fallback()` L33-35
  - `test_rotated_grid_containment_adjacency_and_area()` L37-50
  - `test_panel_centre_matches_rotated_corners()` L52-56
  - `test_legacy_cable_plan_is_not_current()` L58-59
- **class PeriodTests** L61-66
  - `test_payback_requires_complete_anniversary_period()` L62-66
- **class TrayProjectionTests** L68-77
  - `test_two_projections_on_same_tray_use_direct_interval()` L69-77

### tests/test_regressions.py (121 lignes)
Imports internes : battery_dispatch, energy_economics, mixins.spreadsheet_interactions, project_validation, self_consumption, single_line_516
Constantes : ROOT
- **class Regressions** L16-119
  - `test_all_supplied_projects()` L17-32
  - `test_generated_links_ignore_stale_manual_wiring()` L34-41
  - `test_orphans_numbering_and_coordinates()` L43-49
  - `test_portable_image_alias()` L51-54
  - `test_storage_before_export_curtailment_and_shared_power()` L56-68
  - `test_export_zero_and_invalid()` L70-75
  - `test_economics_net_cost_and_foregone_exports()` L77-85
  - `test_all_site_diagram_exports()` L87-97
  - `test_missing_specs_are_not_validated()` L99-103
  - `test_saved_french_formulas_migrate_without_touching_plain_text()` L105-115
  - `test_dragged_formula_moves_cell_references_only()` L117-119

### tests/test_technical_reference.py (26 lignes)
Protect the revised solar-year and displayed technical formulas.
Imports internes : home_reference, mixins.shadow_energy
- **class TechnicalReferenceTests** L9-23
  - `test_dated_solar_position_uses_leap_year_when_requested()` L10-14
  - `test_all_home_equations_render()` L16-23

### user_guide.py (125 lignes)
Expanded desktop workflow adapted from the supplied earlier tutorial.
Constantes : WORKFLOWS
