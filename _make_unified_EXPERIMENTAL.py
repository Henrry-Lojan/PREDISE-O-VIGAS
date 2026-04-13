import re

viga_path = 'Predimensionamiento_vigas.html'
with open(viga_path, 'r', encoding='utf-8') as f:
    viga_content = f.read()

# Parse Viga parts
head_match = re.search(r'(<!DOCTYPE html>.*?<title>).*?(</title>.*?</style>)', viga_content, re.DOTALL)
if head_match:
    head_html = head_match.group(1) + "Dashboard Unificado - Ingeniería" + head_match.group(2)
else:
    head_html = ""

def build_module(name, content, active=False):
    # Buscar el inicio del layout
    start_tag = '<div class="layout">'
    start_index = content.find(start_tag)
    if start_index == -1: return ""
    
    # Buscar el final: ya sea el tooltip interactivo o el cierre del body
    end_markers = ['<!-- Interactive Equation Tooltip -->', '</body>', '</html>']
    end_index = len(content)
    for marker in end_markers:
        pos = content.find(marker)
        if pos != -1 and pos < end_index:
            end_index = pos
            
    # Extraer el bloque completo
    inner_html = content[start_index + len(start_tag) : end_index].strip()
    
    # Quitar el último </div> que pertenece al layout original
    if inner_html.endswith('</div>'):
        inner_html = inner_html[:-6].strip()

    active_class = "active" if active else ""
    return f'<div id="tab-{name}" class="module-container layout {active_class}">{inner_html}</div>'

def build_arch_block(prefix=''):
    return f"""        <!-- ARQUITECTÓNICOS -->
        <div class="input-group arch-group">
          <div class="input-group-title"><span style="color:var(--accent)">◈</span> { 'Datos Coordinados (Globales)' if prefix != '' else 'Datos Coordinados (Globales)'}</div>
          <div class="input-row"><label>Longitud en eje x (L1)</label><div class="input-wrap"><input type="number" id="{prefix}L1" class="sync-L1" value="5.50" step="0.01" min="0.1"><span class="input-unit">m</span></div></div>
          <div class="input-row"><label>Longitud en eje x (L2)</label><div class="input-wrap"><input type="number" id="{prefix}L2" class="sync-L2" value="4.50" step="0.01" min="0.1"><span class="input-unit">m</span></div></div>
          <div class="input-row"><label>Longitud en eje y (L3)</label><div class="input-wrap"><input type="number" id="{prefix}L3" class="sync-L3" value="4.80" step="0.01" min="0.1"><span class="input-unit">m</span></div></div>
          <div class="input-row"><label>Longitud en eje y (L4)</label><div class="input-wrap"><input type="number" id="{prefix}L4" class="sync-L4" value="4.20" step="0.01" min="0.1"><span class="input-unit">m</span></div></div>
          <div class="input-row"><label>Número de pisos (N°)</label><div class="input-wrap"><input type="number" id="{prefix}pisos" class="sync-pisos" value="2" step="1" min="1"><span class="input-unit">u</span></div></div>
          <div class="input-row"><label>Altura entrepiso</label><div class="input-wrap"><input type="number" id="{prefix}He" class="sync-He" value="2.60" step="0.05" min="1"><span class="input-unit">m</span></div></div>
          <div class="input-row"><label>Uso</label><div class="input-wrap" style="width:150px;">
            <select id="{prefix}uso" class="sync-uso" style="font-size:11px;">
              <option value="0.200">Vivienda / Departamentos</option>
              <option value="0.240">Oficinas</option>
              <option value="0.480">Gimnasios / Áreas de baile</option>
              <option value="0.480">Áreas de reunión / Teatros</option>
              <option value="0.480">Comercial (Primer piso)</option>
              <option value="0.360">Comercial (Pisos sup.)</option>
              <option value="0.300">Escuelas (Aulas)</option>
              <option value="0.480">Escuelas (Corredores p. sup)</option>
              <option value="0.300">Garajes (Livianos < 4t)</option>
              <option value="0.180">Cubierta accesible (Terrazas)</option>
              <option value="0.070">Cubierta no accesible</option>
              <option value="0.480">Balcones</option>
            </select>
          </div></div>
          <div style="font-size:10px; color:var(--muted); text-align:right; margin-top:5px; opacity:0.8;">(Catálogo unificado NEC-SE-CG)</div>
        </div>"""

import re
vig_arch_regex = r'<!-- ARQUITECTÓNICOS -->.*?<!-- CARGAS -->'
# Extraer el layout de Vigas de forma robusta
start_tag = '<div class="layout">'
v_start = viga_content.find(start_tag)
v_end = viga_content.find('<!-- Interactive Equation Tooltip -->')
if v_end == -1: v_end = viga_content.find('</body>')
viga_layout = viga_content[v_start + len(start_tag) : v_end].strip()
if viga_layout.endswith('</div>'):
    viga_layout = viga_layout[:-6].strip()

vig_arch_regex = r'<!-- ARQUITECTÓNICOS -->.*?<!-- CARGAS -->'
viga_layout = re.sub(vig_arch_regex, build_arch_block('') + "\n        <!-- CARGAS -->", viga_layout, flags=re.DOTALL)


script_match = re.search(r'<script>(.*?)</script>', viga_content, re.DOTALL)
viga_script = script_match.group(1) if script_match else ""

# Modify Viga Script to trigger Columna update when Cu changes
viga_script = viga_script.replace(
    "const cuEl = document.getElementById('cu_display'); if (cuEl) cuEl.textContent = Cu.toFixed(2);",
    """const cuEl = document.getElementById('cu_display'); if (cuEl) cuEl.textContent = Cu.toFixed(2);
      // MACRO: Push Cu to Columnas
      const colCuInput = document.getElementById('col_cu');
      if (colCuInput && Math.abs((parseFloat(colCuInput.value)||0) - Cu) > 0.01) {
          colCuInput.value = Cu.toFixed(2);
          colCuInput.style.backgroundColor = "rgba(127,255,107,0.3)";
          setTimeout(() => { colCuInput.style.backgroundColor = ""; }, 1000);
          if (typeof recalcCol === 'function') recalcCol();
      }
      
      // MACRO: Push b to Columnas bvig
      const colBvigInput = document.getElementById('col_bvig');
      if (colBvigInput && colBvigInput.value != b) {
          colBvigInput.value = b;
      }
    """
)

# LOSAS UI
losa_inputs = build_arch_block('losa_') + """
        <div class="input-group">
          <div class="input-group-title"><span style="color:var(--accent2)">◈</span> Sección Losa / Nervios</div>
          <div class="input-row"><label>Vigas Intermedias</label><div class="input-wrap"><input type="number" id="losa_vint" value="0"><span class="input-unit">u</span></div></div>
          <div class="input-row"><label>Altura de losa alivianada (Hl)</label><div class="input-wrap"><input type="number" id="losa_hl" value="25"><span class="input-unit">cm</span></div></div>
          <div class="input-row"><label>Ancho del nervio (bn)</label><div class="input-wrap"><input type="number" id="losa_bn" value="10"><span class="input-unit">cm</span></div></div>
          <div class="input-row"><label>Ancho del bloque alivianado (bb)</label><div class="input-wrap"><input type="number" id="losa_bb" value="40"><span class="input-unit">cm</span></div></div>
          <div class="input-row"><label>Tabla de compresion (tc)</label><div class="input-wrap"><input type="number" id="losa_tc" value="5"><span class="input-unit">cm</span></div></div>
        </div>
        <div class="input-group">
          <div class="input-group-title"><span style="color:var(--warn)">◈</span> Cargas Muertas Adicionales (CM)</div>
          <div class="input-row"><label>Paredes / Tabiques</label><div class="input-wrap">
            <select id="losa_paredes" style="width:150px; text-overflow:ellipsis;">
              <option value="0.18">Ladrillo macizo</option>
              <option value="0.12">Bloque pomez 10 cm</option>
              <option value="0.05">Steel Framing</option>
            </select>
          </div></div>
          <div class="input-row"><label>Alivianador en losa</label><div class="input-wrap">
            <select id="losa_alivian" style="width:150px; text-overflow:ellipsis;">
              <option value="0.10">Bloque de pomez</option>
              <option value="0.15">Ladrillo o bloque pesado</option>
              <option value="0.005">Caseton</option>
              <option value="0.000">Sin alivianador</option>
            </select>
          </div></div>
          <div class="input-row"><label>Masillado</label><div class="input-wrap"><input type="number" id="losa_masillado" value="0.08" step="0.01"><span class="input-unit">t/m2</span></div></div>
          <div class="input-row"><label>Acabados</label><div class="input-wrap"><input type="number" id="losa_acabados" value="0.02" step="0.01"><span class="input-unit">t/m2</span></div></div>
          <div class="input-row"><label>Instalaciones</label><div class="input-wrap"><input type="number" id="losa_instalaciones" value="0.02" step="0.01"><span class="input-unit">t/m2</span></div></div>
        </div>
"""

losa_results = """
        <div class="mini-card diagram-mini">
          <div class="mini-header"><span style="color:var(--accent)">&#9658;</span> Predimensionamiento de Losa</div>
          <div class="mini-body" style="padding:15px;">
             <div style="display:flex;gap:10px;">
                <div id="dcIndicator_losa" style="flex:1;background:rgba(0,229,255,0.1);border:1px solid rgba(0,229,255,0.3);border-radius:8px;padding:10px;text-align:center;margin-bottom:15px;">
                  <div style="font-size:24px;font-weight:700;font-family:var(--sans);" id="r_losa_hmin">—</div>
                  <div style="font-size:10px;color:var(--muted);margin-top:4px;letter-spacing:0.1em">ESPESOR MINIMO CALC. (cm)</div>
                </div>
                <div id="status_losa_check" style="flex:1;background:rgba(255,184,48,0.1);border:1px solid rgba(255,184,48,0.3);border-radius:8px;padding:10px;text-align:center;margin-bottom:15px;">
                  <div style="font-size:14px;font-weight:700;font-family:var(--sans);margin-top:5px" id="r_losa_ok">—</div>
                  <div style="font-size:10px;color:var(--muted);margin-top:4px;letter-spacing:0.1em">CHEQUEO ESPESOR</div>
                </div>
             </div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_lmax" data-eq-title="Luz M\u00e1xima" data-eq-body="\\text{M\u00e1xima luz entre L1, L2, L3 y L4}">Luz M\u00e1xima Arquitect\u00f3nica (Lm\u00e1x)</span><span class="rv" id="r_losa_lmax">—</span><span class="ru">m</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_lreal" data-eq-title="Luz C\u00e1lculo" data-eq-body="L_{real} = \\frac{L_{m\\acute{a}x}}{V_{int} + 1}">Luz Efectiva de C\u00e1lculo (Lreal)</span><span class="rv accent-v" id="r_losa_lreal">—</span><span class="ru">m</span></div>
            <div class="mini-sep"></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_imin" data-eq-title="Inercia M\u00ednima Requerida" data-eq-body="I_{min} = \\frac{100 \\cdot h_{min}^3}{12}">Inercia m\u00ednima requerida de losa maciza (1m)</span><span class="rv" id="r_losa_imin">—</span><span class="ru">cm4</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_isteiner" data-eq-title="Inercia Alivianada (Steiner)" data-eq-body="I_{total} = \\sum I_{individuales}">Inercia de la losa alivianada de espesor — cm</span><span class="rv accent-v" id="r_losa_isteiner">—</span><span class="ru">cm4</span></div>
          </div>
        </div>
        <div class="mini-card diagram-mini">
          <div class="mini-header"><span style="color:var(--accent)">&#9658;</span> <span id="lbl_losa_graf_title">LOSA ALIVIANADA DE — CM</span></div>
          <div class="mini-body" style="padding:15px; text-align:center;">
             <div style="background:rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.08); border-radius:6px; padding:25px 15px 15px 15px; margin-bottom:15px; position:relative;">
                <div style="display:flex; align-items:center;">
                   <div style="display:flex; flex-direction:column; justify-content:center; align-items:center; border-left:1px solid rgba(255,255,255,0.3); padding-left:5px; margin-right:15px; position:relative;" id="dib_h_cota">
                      <div style="border-top:1px solid rgba(255,255,255,0.3); width:5px; position:absolute; top:0; left:0;"></div>
                      <div style="font-size:10px; color:var(--muted); font-weight:bold; writing-mode:vertical-rl; transform:rotate(180deg); letter-spacing:0.05em; white-space:nowrap;" id="dib_h_val">Hl = 25 cm</div>
                      <div style="border-bottom:1px solid rgba(255,255,255,0.3); width:5px; position:absolute; bottom:0; left:0;"></div>
                   </div>
                   <div style="flex:1;">
                      <div style="display:flex; width:100%; border-bottom:1px solid rgba(255,255,255,0.3); margin-bottom:2px; position:relative;">
                         <div style="position:absolute; top:-16px; width:100%; text-align:center; font-size:10px; color:var(--muted); font-weight:bold; letter-spacing:0.05em;">ANCHO DE AN\u00c1LISIS = 1.00 m</div>
                         <div style="border-left:1px solid rgba(255,255,255,0.3); height:5px; position:absolute; left:0; bottom:0;"></div>
                         <div style="border-right:1px solid rgba(255,255,255,0.3); height:5px; position:absolute; right:0; bottom:0;"></div>
                      </div>
                      <div id="dib_tabla" style="background:var(--accent); width:100%; height:15px; border-radius:2px 2px 0 0; display:flex; align-items:center; justify-content:center; color:rgba(0,0,0,0.7); font-size:11px; font-weight:800; letter-spacing:0.05em;">
                         Tabla de compresi\u00f3n
                      </div>
                      <div id="dib_nervios_container" style="display:flex; width:100%; justify-content:flex-start;">
                         <!-- JS injected webs -->
                      </div>
                   </div>
                </div>
                <div id="dib_labels" style="margin-top:15px; font-size:12px; color:var(--text); font-family:var(--sans); background:rgba(0,229,255,0.05); padding:8px; border-radius:4px; border:1px solid rgba(0,229,255,0.2);"></div>
             </div>
             <div class="mini-row" style="text-align:left;"><span class="rl clickable-label" id="lbl_losa_heq" data-eq-title="Altura Equivalente Losa Maciza" data-eq-body="H_{eq} = \\left( \\frac{12 \\cdot I_t}{100} \\right)^{1/3}">Altura losa maciza equiv. (Heq)</span><span class="rv accent-v" id="r_losa_heq">—</span><span class="ru">cm</span></div>
             <div class="mini-row" style="text-align:left;"><span class="rl clickable-label" id="lbl_losa_lmaxperm" data-eq-title="Longitud M\u00e1x Permitida" data-eq-body="L_{m\\acute{a}x\\,perm} = \\frac{H_{eq}}{0.03 \\cdot 100}">Longitud m\u00e1xima para una losa de — cm</span><span class="rv accent-v" id="r_losa_lmaxperm">—</span><span class="ru">m</span></div>
          </div>
        </div>
        <div class="mini-card">
          <div class="mini-header"><span style="color:var(--accent2)">&#9658;</span> Peso del hormig\u00f3n</div>
          <div class="mini-body">
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_vtot" data-eq-title="Vol. Total" data-eq-body="V_{tot} = \\frac{100 \\times 100}{10000} \\times \\frac{Hl}{100}">Volumen total en funci\u00f3n de geometr\u00eda</span><span class="rv" id="r_losa_vtot">—</span><span class="ru">m\u00b3</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_vbloq" data-eq-title="Vol. Bloques" data-eq-body="V_{bloq} = \\frac{bb^2 \\times (Hl-tc) \\times 4}{10^6}">Volumen del bloque en funci\u00f3n de geometr\u00eda</span><span class="rv" id="r_losa_vbloq">—</span><span class="ru">m\u00b3</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_vhorm" data-eq-title="Vol. Hormig\u00f3n" data-eq-body="V_{horm} = V_{tot} - V_{bloq}">Volumen del hormig\u00f3n</span><span class="rv" id="r_losa_vhorm">—</span><span class="ru">m\u00b3</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_peso" data-eq-title="Peso Hormig\u00f3n" data-eq-body="P_{h} = V_{horm} \\times 2.4">Peso hormig\u00f3n (\u03b3 = 2.4 t/m\u00b3)</span><span class="rv" id="r_losa_peso">—</span><span class="ru">t</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_area" data-eq-title="\u00c1rea" data-eq-body="A = \\frac{100 \\times 100}{10000}">\u00c1rea unitaria</span><span class="rv" id="r_losa_area">—</span><span class="ru">m\u00b2</span></div>
            <div class="mini-sep"></div>
            <div class="mini-row"><span class="rl" style="color:var(--accent3);font-weight:700">CARGA MUERTA DE LA LOSA</span><span class="rv accent-v" id="r_losa_phorm_final">—</span><span class="ru">t/m\u00b2</span></div>
          </div>
        </div>
        <div class="mini-card diagram-mini">
          <div class="mini-header"><span style="color:var(--warn)">&#9658;</span> Cargas Muertas Adicionales y Totales</div>
          <div class="mini-body" style="padding:15px;">
            <div class="mini-row"><span class="rl" id="lbl_losa_cpared">Paredes / Tabiquer\u00eda equivalentes</span><span class="rv" id="r_losa_cpared">—</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl" id="lbl_losa_caliv">Alivianador de losa</span><span class="rv" id="r_losa_caliv">—</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl">Masillado</span><span class="rv" id="r_losa_cmasillado">—</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl">Acabados</span><span class="rv" id="r_losa_cacabados">—</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl">Instalaciones</span><span class="rv" id="r_losa_cinstal">—</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-sep"></div>
            <div class="mini-row"><span class="rl" style="color:var(--accent2);font-weight:700">CARGAS MUERTAS INSTALACIONES</span><span class="rv" id="r_losa_csuper">—</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl" style="color:var(--accent2);font-weight:700">CARGA MUERTA LOSA</span><span class="rv" id="r_losa_cmlosa">—</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-sep"></div>
            <div class="mini-row"><span class="rl" style="color:var(--warn);font-weight:800;font-size:13px">CARGA MUERTA TOTAL</span><span class="rv" style="color:var(--warn);font-size:15px" id="r_losa_cm_total">—</span><span class="ru">t/m\u00b2</span></div>
            <div style="font-size:10px; color:var(--muted); text-align:right; margin-top:4px;">* Suma transferida din\u00e1micamente al m\u00f3dulo Vigas</div>
          </div>
        </div>
        <div class="mini-card">
          <div class="mini-header"><span style="color:var(--accent2)">&#9658;</span> Cargas Vivas (NEC-SE-CG 2015)</div>
          <div class="mini-body">
            <div class="mini-row"><span class="rl">Uso seleccionado</span><span class="rv" id="r_losa_uso_txt" style="font-size:11px;text-align:right;">—</span><span class="ru"></span></div>
            <div class="mini-row"><span class="rl">Carga viva (CV)</span><span class="rv accent-v" id="r_losa_cv">—</span><span class="ru">t/m²</span></div>
            <div class="mini-sep"></div>
            <div class="mini-row"><span class="rl" style="color:var(--accent2);font-weight:700">CARGA VIVA TOTAL</span><span class="rv" id="r_losa_cv_total" style="color:var(--accent2);font-size:15px;font-weight:700">—</span><span class="ru">t/m²</span></div>
          </div>
        </div>
        <div class="mini-card diagram-mini">
          <div class="mini-header"><span style="color:var(--accent)">&#9658;</span> Inercia Teorema Steiner (1m)</div>
          <div class="mini-body" style="padding:10px;">
             <table style="width:100%; text-align:right; font-size:11px; border-collapse:collapse; margin-top:5px;">
               <thead>
                 <tr style="border-bottom:1px solid rgba(255,255,255,0.1); color:var(--muted);">
                   <th style="padding-bottom:5px;text-align:center">Pieza</th>
                   <th style="padding-bottom:5px">A</th>
                   <th style="padding-bottom:5px">y</th>
                   <th style="padding-bottom:5px">Ay</th>
                   <th style="padding-bottom:5px">Io</th>
                   <th style="padding-bottom:5px">d\u00b2</th>
                   <th style="padding-bottom:5px; color:var(--accent)">It</th>
                 </tr>
               </thead>
               <tbody id="tb_steiner" style="color:var(--text);">
                 <!-- JS -->
               </tbody>
               <tfoot>
                 <tr style="border-top:1px solid rgba(255,255,255,0.1); font-weight:700;">
                   <td style="padding-top:5px;text-align:center;color:var(--accent2)">\u2211</td>
                   <td id="st_A_tot" style="padding-top:5px"></td>
                   <td style="padding-top:5px"></td>
                   <td id="st_Ay_tot" style="padding-top:5px"></td>
                   <td style="padding-top:5px"></td>
                   <td style="padding-top:5px"></td>
                   <td id="st_It_tot" style="padding-top:5px; color:var(--accent)"></td>
                 </tr>
               </tfoot>
             </table>
             <div style="font-size:11px; color:var(--muted); text-align:right; margin-top:15px; border-top:1px dashed rgba(255,255,255,0.1); padding-top:8px;">
               Centroide Real (Yc) = <span id="st_Yc" style="color:var(--text);font-weight:700;font-size:13px"></span> cm
             </div>
          </div>
        </div>
"""

losa_js = """
    function recalcLosa() {
      const lmax = Math.max(getVal('losa_L1'), getVal('losa_L2'), getVal('losa_L3'), getVal('losa_L4'));
      const vint = getVal('losa_vint');
      const lreal = lmax / (vint + 1);
      const hl = getVal('losa_hl'), bn = getVal('losa_bn'), bb = getVal('losa_bb'), tc = getVal('losa_tc');
      
      const hmin = lreal * 100 * 0.03; 
      
      const wr = 1.16 * 0.5; 
      const mu = wr * lreal * lreal / 12; 
      const As = 30 * mu / (hl - 3) * 0.75; 
      
      const b_tot = bn + bb;
      const hw = hl - tc;
      
      const num_bloques_1m2 = 10000 / ((b_tot) * (b_tot));
      const vtot_1m2 = 1.0 * (hl/100);
      const vbloq_1m2 = (bb/100) * (bb/100) * (hw/100) * num_bloques_1m2;
      const vhorm_1m2 = vtot_1m2 - vbloq_1m2;
      const Peso_horm = vhorm_1m2 * 2.4; 
      const Area_1m2 = 1.0;
      const Phorm_final = Peso_horm / Area_1m2;
      
      const paredSel = document.getElementById('losa_paredes');
      const paredText = paredSel ? paredSel.options[paredSel.selectedIndex].text : '';
      const c_pared = parseFloat(paredSel.value) || 0;
      
      const alivSel = document.getElementById('losa_alivian');
      const alivText = alivSel ? alivSel.options[alivSel.selectedIndex].text : '';
      const c_aliv = parseFloat(alivSel.value) || 0;
      
      const c_mas = parseFloat(document.getElementById('losa_masillado').value) || 0;
      const c_aca = parseFloat(document.getElementById('losa_acabados').value) || 0;
      const c_inst = parseFloat(document.getElementById('losa_instalaciones').value) || 0;
      
      const C_superimpuesta = c_pared + c_aliv + c_mas + c_aca + c_inst;
      const P_eq = Phorm_final + C_superimpuesta;
      
      const width_m = 100;
      const I_min = (width_m*Math.pow(hmin, 3))/12;
      
      // Steiner: Sección T per 1m
      const numNervios = width_m / b_tot; 
      
      let rowsData = [];
      for(let i=0; i<Math.floor(numNervios); i++) {
          rowsData.push({ name: String(i+1), A: bn * hw, y: hw/2, Io: bn * Math.pow(hw, 3)/12 });
      }
      const partial = numNervios - Math.floor(numNervios);
      if (partial > 0.001) {
          const w = bn * partial;
          rowsData.push({ name: String(Math.floor(numNervios)+1), A: w * hw, y: hw/2, Io: w * Math.pow(hw, 3)/12 });
      }
      rowsData.push({ name: String(Math.ceil(numNervios)+1), A: width_m * tc, y: hw + tc/2, Io: width_m * Math.pow(tc, 3)/12 });
      
      let sumA = 0, sumAy = 0;
      rowsData.forEach(r => {
          sumA += r.A;
          sumAy += r.A * r.y;
      });
      const Yc = sumA > 0 ? sumAy / sumA : 0;
      
      let sumIt = 0;
      let htmlRows = '';
      let itVals = [];
      rowsData.forEach(r => {
          const d = Math.abs(r.y - Yc);
          const d2 = d*d;
          const It = r.Io + r.A * d2;
          sumIt += It;
          itVals.push(It.toFixed(0));
          htmlRows += `<tr>
            <td style="padding:4px 0; text-align:center; color:var(--muted)">${r.name}</td>
            <td style="padding:4px 0">${r.A.toFixed(0)}</td>
            <td style="padding:4px 0">${r.y.toFixed(2)}</td>
            <td style="padding:4px 0">${(r.A * r.y).toFixed(0)}</td>
            <td style="padding:4px 0">${r.Io.toFixed(0)}</td>
            <td style="padding:4px 0">${d2.toFixed(2)}</td>
            <td style="padding:4px 0; color:var(--accent)">${It.toFixed(0)}</td>
          </tr>`;
      });
      
      const tb = document.getElementById('tb_steiner');
      if (tb) tb.innerHTML = htmlRows;
      setResult('st_A_tot', sumA, 0);
      setResult('st_Ay_tot', sumAy, 0);
      setResult('st_It_tot', sumIt, 0);
      setResult('st_Yc', Yc, 2);

      const I_steiner = sumIt;
      
      setResult('r_losa_lmax', lmax, 2);
      setResult('r_losa_lreal', lreal, 2);
      setResult('r_losa_hmin', hmin, 1);
      
      // Chequeo espesor min e inercia
      const stateBox = document.getElementById('status_losa_check');
      const txtBox = document.getElementById('r_losa_ok');
      if (hmin > hl || I_min > I_steiner) {
         stateBox.style.background = 'rgba(255,113,113,0.1)';
         stateBox.style.borderColor = 'rgba(255,71,87,0.4)';
         txtBox.style.color = 'var(--bad)';
         txtBox.textContent = 'Suba h o añada vigas interm.';
         txtBox.style.fontSize = '12px';
      } else {
         stateBox.style.background = 'rgba(127,255,107,0.1)';
         stateBox.style.borderColor = 'rgba(127,255,107,0.4)';
         txtBox.style.color = 'var(--accent3)';
         txtBox.textContent = 'OK';
         txtBox.style.fontSize = '18px';
      }
      
      setResult('r_losa_imin', I_min, 0);
      setResult('r_losa_isteiner', I_steiner, 0);
      
      const heq = Math.pow((12 * I_steiner) / 100, 1/3);
      setResult('r_losa_heq', heq, 2);
      
      const lmaxperm = heq / (0.03 * 100);
      setResult('r_losa_lmaxperm', lmaxperm, 2);
      
      setResult('r_losa_vtot', vtot_1m2, 2);
      setResult('r_losa_vbloq', vbloq_1m2, 2);
      setResult('r_losa_vhorm', vhorm_1m2, 2);
      setResult('r_losa_peso', Peso_horm, 2);
      setResult('r_losa_area', Area_1m2, 2);
      setResult('r_losa_phorm_final', Phorm_final, 2);
      
      setResult('r_losa_cpared', c_pared, 2);
      setResult('r_losa_caliv', c_aliv, 2);
      setResult('r_losa_cmasillado', c_mas, 2);
      setResult('r_losa_cacabados', c_aca, 2);
      setResult('r_losa_cinstal', c_inst, 2);
      
      setResult('r_losa_csuper', C_superimpuesta, 2);
      setResult('r_losa_cmlosa', Phorm_final, 2);
      setResult('r_losa_cm_total', P_eq, 2);
      
      const L1 = getVal('losa_L1'), L2 = getVal('losa_L2'), L3 = getVal('losa_L3'), L4 = getVal('losa_L4');
      document.getElementById('lbl_losa_lmax')?.setAttribute('data-eq-calc', `\\\\max(${L1}, ${L2}, ${L3}, ${L4}) = ${lmax.toFixed(2)} \\\\text{ m}`);
      document.getElementById('lbl_losa_lreal')?.setAttribute('data-eq-calc', `\\\\frac{${lmax.toFixed(2)}}{${vint} + 1} = ${lreal.toFixed(2)} \\\\text{ m}`);
      document.getElementById('lbl_losa_imin')?.setAttribute('data-eq-calc', `\\\\frac{100 \\\\cdot ${hmin.toFixed(1)}^3}{12} = ${I_min.toFixed(0)} \\\\text{ cm}^4/m`);
      document.getElementById('lbl_losa_isteiner')?.setAttribute('data-eq-calc', `${itVals.join(' + ')} = ${I_steiner.toFixed(0)} \\\\text{ cm}^4/m`);
      document.getElementById('lbl_losa_heq')?.setAttribute('data-eq-calc', `\\\\left( \\\\frac{12 \\\\cdot ${I_steiner.toFixed(0)}}{100} \\\\right)^{1/3} = ${heq.toFixed(2)} \\\\text{ cm}`);
      document.getElementById('lbl_losa_lmaxperm')?.setAttribute('data-eq-calc', `\\\\frac{${heq.toFixed(2)}}{0.03 \\\\cdot 100} = ${lmaxperm.toFixed(2)} \\\\text{ m}`);
      
      document.getElementById('lbl_losa_vtot')?.setAttribute('data-eq-calc', `1.0 \\\\times \\\\frac{${hl}}{100} = ${vtot_1m2.toFixed(4)} \\\\text{ m}^3`);
      document.getElementById('lbl_losa_vbloq')?.setAttribute('data-eq-calc', `(${bb}/100)^2 \\\\times \\\\frac{${hw}}{100} \\\\times ${num_bloques_1m2.toFixed(1)} = ${vbloq_1m2.toFixed(4)} \\\\text{ m}^3`);
      document.getElementById('lbl_losa_vhorm')?.setAttribute('data-eq-calc', `${vtot_1m2.toFixed(4)} - ${vbloq_1m2.toFixed(4)} = ${vhorm_1m2.toFixed(4)} \\\\text{ m}^3`);
      document.getElementById('lbl_losa_peso')?.setAttribute('data-eq-calc', `${vhorm_1m2.toFixed(4)} \\\\times 2.4 = ${Peso_horm.toFixed(4)} \\\\text{ t}`);
      document.getElementById('lbl_losa_area')?.setAttribute('data-eq-calc', `1.00 \\\\text{ m}^2`);
      
      const txtSteiner = document.getElementById('lbl_losa_isteiner');
      if(txtSteiner) txtSteiner.innerText = `Inercia de la losa alivianada de espesor ${hl} cm`;
      
      const txtLmaxPerm = document.getElementById('lbl_losa_lmaxperm');
      if(txtLmaxPerm) txtLmaxPerm.innerText = `Longitud máxima para una losa de ${hl} cm`;
      
      const lblCpared = document.getElementById('lbl_losa_cpared');
      if(lblCpared) lblCpared.innerText = `Paredes (${paredText})`;
      
      const lblCaliv = document.getElementById('lbl_losa_caliv');
      if(lblCaliv) lblCaliv.innerText = `Alivianador (${alivText})`;
      
      const lblGra = document.getElementById('lbl_losa_graf_title');
      if(lblGra) lblGra.innerText = `LOSA ALIVIANADA DE ${hl} CM`;
      
      const cont = document.getElementById('dib_nervios_container');
      const dib_tabla = document.getElementById('dib_tabla');
      const vlbl = document.getElementById('dib_labels');
      const dib_h_cota = document.getElementById('dib_h_cota');
      const dib_h_val = document.getElementById('dib_h_val');
      
      if(cont && dib_tabla && vlbl) {
         const h_tc = Math.max(tc * 2, 16);
         const h_hw = Math.max(hw * 2, 30);
         dib_tabla.innerText = `Tabla de compresión (${tc} cm)`;
         dib_tabla.style.height = h_tc + 'px';
         
         if(dib_h_cota && dib_h_val) {
             dib_h_cota.style.height = (h_tc + h_hw) + 'px';
             dib_h_val.innerText = `Hl = ${hl} cm`;
         }
         
         let nerviosHtml = '';
         let currentWidth = 0;
         let isBlock = true;
         // Interleave blocks and ribs up to 100cm width (1m profile)
         while (currentWidth < 100) {
             const pieceW = isBlock ? bb : bn;
             let wToDraw = pieceW;
             if (currentWidth + pieceW > 100) wToDraw = 100 - currentWidth;
             
             if (isBlock) {
                 nerviosHtml += `<div style="width:${wToDraw}%; background:rgba(255,200,50,0.15); border:1px dashed rgba(255,200,50,0.4); border-top:none; box-sizing:border-box; border-radius:0 0 3px 3px; color:rgba(255,200,50,0.8); font-size:10px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; height:${h_hw}px;">${wToDraw >= 15 ? 'Bloque<br>(' + bb + 'x' + hw + 'cm)' : ''}</div>`;
             } else {
                 nerviosHtml += `<div style="background:var(--accent); width:${wToDraw}%; height:${h_hw}px; border-radius:0 0 3px 3px; box-shadow:inset 0px 4px 0px rgba(0,0,0,0.15); display:flex; justify-content:center; align-items:center; color:rgba(0,0,0,0.7); font-size:10px; font-weight:800;"><span style="writing-mode:vertical-rl; transform:rotate(180deg); white-space:nowrap;">${wToDraw >= 5 ? 'nervio' : ''}</span></div>`;
             }
             currentWidth += wToDraw;
             isBlock = !isBlock;
         }
         
         cont.innerHTML = nerviosHtml;
         vlbl.innerHTML = `<span style="color:var(--accent);font-weight:bold;font-size:13px">Losa alivianada de ${hl} cm</span> <br> <span style="display:inline-block;margin-top:4px;font-size:11px">Nervio: <span style="color:var(--white);font-weight:700">${bn}</span> x <span style="color:var(--white);font-weight:700">${hw}</span> cm &nbsp;|&nbsp; Bloque: <span style="color:var(--white);font-weight:700">${bb}</span> x <span style="color:var(--white);font-weight:700">${hw}</span> cm</span>`;
      }
      
      // MACRO LINK: Transferir a Vigas
      const vigaCm = document.getElementById('Cm');
      if (vigaCm && Math.abs((parseFloat(vigaCm.value)||0) - P_eq) > 0.01) {
          vigaCm.value = P_eq.toFixed(3);
          vigaCm.style.backgroundColor = "rgba(127,255,107,0.3)";
          setTimeout(() => { vigaCm.style.backgroundColor = ""; }, 1000);
          if (typeof recalc === 'function') recalc(); // Actualiza viga
      }

      // === CARGA VIVA NEC-SE-CG 2015 ===
      const cvSel = document.getElementById('losa_uso');
      if (cvSel) {
        const cv_val = parseFloat(cvSel.value);
        const cv_uso = cvSel.options[cvSel.selectedIndex].text;
        const elCv = document.getElementById('r_losa_cv');
        const elCvTot = document.getElementById('r_losa_cv_total');
        const elUso = document.getElementById('r_losa_uso_txt');
        if (elCv) elCv.textContent = cv_val.toFixed(2);
        if (elCvTot) elCvTot.textContent = cv_val.toFixed(2);
        if (elUso) elUso.textContent = cv_uso;
      }
    }
    document.querySelectorAll('[id^=losa_]').forEach(el => el.addEventListener('input', recalcLosa));
     document.querySelectorAll('[id^=losa_]').forEach(el => el.addEventListener('change', recalcLosa));
"""

col_inputs = build_arch_block('col_') + """
        <div class="input-group">
          <div class="input-group-title"><span style="color:var(--accent)">◈</span> Geometría y Cargas (Vienen de Vigas)</div>
          <div class="input-row"><label>Área Tributaria (At)</label><div class="input-wrap"><input type="number" id="col_at" value="23.45"><span class="input-unit">m2</span></div></div>
          <div class="input-row"><label>Carga Mayorada (Cu)</label><div class="input-wrap"><input type="number" id="col_cu" value="1.16" style="color:var(--accent3)"><span class="input-unit">t/m2</span></div></div>
          <div class="input-row"><label>Viga ancho conectada</label><div class="input-wrap"><input type="number" id="col_bvig" value="30" readonly style="color:#717b91"><span class="input-unit">cm</span></div></div>
        </div>
        <div class="input-group">
          <div class="input-group-title"><span style="color:var(--warn)">◈</span> Sección Columna</div>
          <div class="input-row"><label>Perfil Ancho (b)</label><div class="input-wrap"><input type="number" id="col_bc" value="30"><span class="input-unit">cm</span></div></div>
          <div class="input-row"><label>Perfil Prof. (h)</label><div class="input-wrap"><input type="number" id="col_hc" value="30"><span class="input-unit">cm</span></div></div>
          <div class="input-row"><label>f'c</label><div class="input-wrap"><input type="number" id="col_fc" value="210"><span class="input-unit">kg/cm2</span></div></div>
        </div>
        <div class="input-group">
          <div class="input-group-title"><span style="color:var(--accent3)">◈</span> Acero</div>
          <div class="input-row"><label>Diám. long. (Øl)</label><div class="input-wrap"><input type="number" id="col_fil" value="16"><span class="input-unit">mm</span></div></div>
          <div class="input-row"><label>Varillas Ancho (x)</label><div class="input-wrap"><input type="number" id="col_nx" value="3"><span class="input-unit">u</span></div></div>
          <div class="input-row"><label>Varillas Prof. (y)</label><div class="input-wrap"><input type="number" id="col_ny" value="3"><span class="input-unit">u</span></div></div>
          <div class="input-row"><label>Ramas int. (vinchas)</label><div class="input-wrap"><input type="number" id="col_vinc" value="1"><span class="input-unit">u</span></div></div>
        </div>
"""

col_results = """
        <div class="mini-card diagram-mini">
          <div class="mini-header"><span style="color:var(--accent)">▸</span> Predimensionamiento de Columnas</div>
          <div class="mini-body" style="padding:15px;">
             <div style="display:flex;gap:10px;">
                <div id="status_col_cuant" style="flex:1;background:rgba(0,229,255,0.1);border:1px solid rgba(0,229,255,0.3);border-radius:8px;padding:10px;text-align:center;margin-bottom:15px;">
                  <div style="font-size:20px;font-weight:700;font-family:var(--sans);" id="r_col_cuant">—</div>
                  <div style="font-size:10px;color:var(--muted);margin-top:4px;letter-spacing:0.1em">CUANTIA (%)</div>
                </div>
                <div id="status_col_ag" style="flex:1;background:rgba(255,184,48,0.1);border:1px solid rgba(255,184,48,0.3);border-radius:8px;padding:10px;text-align:center;margin-bottom:15px;">
                  <div style="font-size:20px;font-weight:700;font-family:var(--sans);" id="r_col_agnec">—</div>
                  <div style="font-size:10px;color:var(--muted);margin-top:4px;letter-spacing:0.1em">Ag NEC (req) cm2</div>
                </div>
             </div>
            <div class="mini-row"><span class="rl">Área Bruta Actual (Ac)</span><span class="rv accent-v" id="r_col_ac">—</span><span class="ru">cm2</span></div>
            <div class="mini-row"><span class="rl">Carga Última Axial (Pult)</span><span class="rv" id="r_col_pult">—</span><span class="ru">t</span></div>
            <div class="mini-sep"></div>
            <div class="mini-row"><span class="rl">Acero Total Long. (As)</span><span class="rv accent-v" id="r_col_as">—</span><span class="ru">cm2</span></div>
            <div class="mini-sep"></div>
            <div class="mini-header" style="color:#ff6b35;padding:0;margin-top:10px;"><span style="color:#ff6b35;">▸</span> Nudo Fuerte - Viga Débil</div>
            <div class="mini-row"><span class="rl">Cortante Resistido Nudo (Vj)</span><span class="rv accent2-v" id="r_col_vj">—</span><span class="ru">t</span></div>
            <div class="mini-row"><span class="rl">Cortante de diseño Nudo</span><span class="rv" id="r_col_vhz">—</span><span class="ru">t</span></div>
            <div class="mini-row"><span class="rl">Chequeo ∑Mcol >= 1.2 ∑Mvig</span><span class="rv" id="r_col_nudo"></span></div>
          </div>
        </div>
"""

col_js = """
    function recalcCol() {
      const at = getVal('col_at'), pisos = getVal('pisos')||2, cu = getVal('col_cu');
      const b = getVal('col_bc'), h = getVal('col_hc'), fc = getVal('col_fc');
      const fy = 4200;
      const fil = getVal('col_fil'), nx = getVal('col_nx'), ny = getVal('col_ny');
      const rec = 2.5;
      
      const pult = at * pisos * cu * 1.3 / 0.85; 
      const ag_nec = (pult * 1000) / (0.85 * fc + 0.012 * fy);
      const ac = b * h;
      
      const num_var = nx * 2 + (ny - 2) * 2;
      const As = num_var * Math.PI * (fil/20)**2;
      const cuant = (As / ac) * 100;
      
      setResult('r_col_ac', ac, 0);
      setResult('r_col_agnec', ag_nec, 0);
      setResult('r_col_pult', pult, 1);
      setResult('r_col_as', As, 2);
      setResult('r_col_cuant', cuant, 2);
      
      const ind_c = document.getElementById('status_col_cuant');
      if (ind_c) {
          if(cuant >= 1.0 && cuant <= 12.0) { ind_c.style.background='rgba(127,255,107,0.1)'; ind_c.style.borderColor='rgba(127,255,107,0.4)'; }
          else { ind_c.style.background='rgba(255,71,87,0.1)'; ind_c.style.borderColor='rgba(255,71,87,0.4)'; }
      }
      const ind_ag = document.getElementById('status_col_ag');
      if (ind_ag) {
          if(ac >= ag_nec) { ind_ag.style.background='rgba(127,255,107,0.1)'; ind_ag.style.borderColor='rgba(127,255,107,0.4)'; }
          else { ind_ag.style.background='rgba(255,71,87,0.1)'; ind_ag.style.borderColor='rgba(255,71,87,0.4)'; }
      }
      
      const d = h - rec - 1 - fil/20;
      const vcol = (1.25*As*fy*(h-d)/100000)*2 / 3.4; 
      const vhz = (1.25 * As * fy / 1000) - vcol; 
      const vj = 3.3 * Math.sqrt(fc) * b * h / 1000; 
      
      setResult('r_col_vj', vj, 2);
      setResult('r_col_vhz', vhz, 2);
      setStatus('r_col_nudo', vj >= vhz, vj >= vhz ? 'CUMPLE V j > V hz' : 'AUMENTAR SECCIÓN');
    }
    document.querySelectorAll('[id^=col_]').forEach(el => el.addEventListener('input', recalcCol));
"""

sismo_inputs = """
        <div class="input-group">
          <div class="input-group-title"><span style="color:var(--accent)">◈</span> Parámetros Terreno y Zona</div>
          <div class="input-row"><label>Factor Zona (Z)</label><div class="input-wrap"><input type="number" id="sis_Z" value="0.4"><span class="input-unit"></span></div></div>
          <div class="input-row"><label>Tipo de Suelo</label><div class="input-wrap">
            <select id="sis_suelo"><option value="C">C</option><option value="D">D</option><option value="E">E</option></select>
          </div></div>
          <div class="input-row"><label>Importancia (I)</label><div class="input-wrap"><input type="number" id="sis_I" value="1.0" step="0.1"><span class="input-unit"></span></div></div>
          <div class="input-row"><label>Reducción R</label><div class="input-wrap"><input type="number" id="sis_R" value="6" step="1"><span class="input-unit"></span></div></div>
        </div>
        <div class="input-group">
          <div class="input-group-title"><span style="color:var(--warn)">◈</span> Irregularidades</div>
          <div class="input-row"><label>Planta (Øp)</label><div class="input-wrap"><input type="number" id="sis_fip" value="0.9" step="0.05"><span class="input-unit"></span></div></div>
          <div class="input-row"><label>Elevación (Øe)</label><div class="input-wrap"><input type="number" id="sis_fie" value="1.0" step="0.05"><span class="input-unit"></span></div></div>
          <div class="input-row"><label>Factor n</label><div class="input-wrap"><input type="number" id="sis_n" value="2.48" step="0.01"><span class="input-unit"></span></div></div>
        </div>
        <div class="input-group">
            <div class="input-group-title"><span style="color:var(--accent2)">◈</span> Validación de Derivas</div>
            <div class="input-row"><label>Deriva ETABS X</label><div class="input-wrap"><input type="number" id="sis_derx" value="0.0026" step="0.0001"></div></div>
            <div class="input-row"><label>Deriva ETABS Y</label><div class="input-wrap"><input type="number" id="sis_dery" value="0.0022" step="0.0001"></div></div>
        </div>
"""

sismo_results = """
        <div class="mini-card diagram-mini">
          <div class="mini-header"><span style="color:var(--accent)">▸</span> Espectro Sísmico (NEC-15)</div>
          <div class="mini-body" style="padding:15px;">
             <div style="display:flex;gap:10px;">
                <div style="flex:1;background:rgba(0,229,255,0.06);border-radius:8px;padding:10px;text-align:center;margin-bottom:15px;">
                  <div style="font-size:20px;font-weight:700;font-family:var(--sans);color:var(--accent)" id="r_sis_fa">—</div>
                  <div style="font-size:10px;color:var(--muted);margin-top:4px;letter-spacing:0.1em">Fa</div>
                </div>
                <div style="flex:1;background:rgba(0,229,255,0.06);border-radius:8px;padding:10px;text-align:center;margin-bottom:15px;">
                  <div style="font-size:20px;font-weight:700;font-family:var(--sans);color:var(--accent)" id="r_sis_fd">—</div>
                  <div style="font-size:10px;color:var(--muted);margin-top:4px;letter-spacing:0.1em">Fd</div>
                </div>
                <div style="flex:1;background:rgba(0,229,255,0.06);border-radius:8px;padding:10px;text-align:center;margin-bottom:15px;">
                  <div style="font-size:20px;font-weight:700;font-family:var(--sans);color:var(--accent)" id="r_sis_fs">—</div>
                  <div style="font-size:10px;color:var(--muted);margin-top:4px;letter-spacing:0.1em">Fs</div>
                </div>
             </div>
            <div class="mini-row"><span class="rl">Periodo crítico Tc (s)</span><span class="rv accent-v" id="r_sis_tc">—</span></div>
            <div class="mini-row"><span class="rl">Espectro Elástico Máximo (Sa max)</span><span class="rv" id="r_sis_sael">—</span><span class="ru">g</span></div>
            <div class="mini-row"><span class="rl" style="font-weight:700;color:var(--warn)">Espectro Inelástico (Sa de diseño)</span><span class="rv accent2-v" id="r_sis_saine">—</span><span class="ru">g</span></div>
            <div class="mini-sep"></div>
            <div class="mini-header" style="color:#ff6b35;padding:0;margin-top:10px;"><span style="color:#ff6b35;">▸</span> Verificación Derivas Inelásticas</div>
            <div class="mini-row"><span class="rl">Deriva Inelástica Calculada X</span><span class="rv accent-v" id="r_sis_inex">—</span> <span id="r_sis_okx"></span></div>
            <div class="mini-row"><span class="rl">Deriva Inelástica Calculada Y</span><span class="rv accent-v" id="r_sis_iney">—</span> <span id="r_sis_oky"></span></div>
          </div>
        </div>
"""

sismo_js = """
    function recalcSis() {
      const Z = getVal('sis_Z'), suelo = document.getElementById('sis_suelo').value;
      const I = getVal('sis_I'), R = getVal('sis_R');
      const fip = getVal('sis_fip'), fie = getVal('sis_fie'), n = getVal('sis_n');
      
      let fa = 1.0, fd = 1.0, fs = 1.0;
      if (Z == 0.4) {
          if (suelo === 'C') { fa=1.2; fd=1.19; fs=1.28; }
          else if (suelo === 'D') { fa=1.12; fd=1.11; fs=1.20; }
          else if (suelo === 'E') { fa=0.9; fd=0.9; fs=1.0; }
      }
      const tc = 0.55 * fs * fd / fa;
      const sa_max = Z * fa * n;
      const sa_ine_max = sa_max * I / (R * fip * fie);
      
      setResult('r_sis_fa', fa, 2); setResult('r_sis_fd', fd, 2); setResult('r_sis_fs', fs, 2);
      setResult('r_sis_tc', tc, 3);
      setResult('r_sis_sael', sa_max, 3);
      setResult('r_sis_saine', sa_ine_max, 4);
      
      const dx = getVal('sis_derx'), dy = getVal('sis_dery');
      const dx_ine = dx * 0.75 * R, dy_ine = dy * 0.75 * R;
      
      setResult('r_sis_inex', dx_ine, 4);
      setResult('r_sis_iney', dy_ine, 4);
      setStatus('r_sis_okx', dx_ine <= 0.02, dx_ine <= 0.02 ? 'OK (< 2%)' : 'RECHAZA');
      setStatus('r_sis_oky', dy_ine <= 0.02, dy_ine <= 0.02 ? 'OK (< 2%)' : 'RECHAZA');
    }
    document.querySelectorAll('[id^=sis_]').forEach(el => el.addEventListener('input', recalcSis));
"""

# Tabs wrapper HTML
tabs_html = """
    <div style="display:flex; gap:10px; background:var(--panel); padding:10px 24px; border-bottom:1px solid var(--border);">
      <button class="tab-btn active" onclick="openTab('tab-losas', this)">🟦 Losas</button>
      <button class="tab-btn" onclick="openTab('tab-vigas', this)">🏗️ Vigas</button>
      <button class="tab-btn" onclick="openTab('tab-columnas', this)">🗼 Columnas</button>
      <button class="tab-btn" onclick="openTab('tab-sismo', this)">📈 Sismo</button>
    </div>
    
    <style>
      .tab-btn { background:transparent; border:1px solid transparent; color:var(--muted); font-family:var(--display); font-size:14px; padding:8px 16px; cursor:pointer; border-radius:6px; transition:all 0.2s;}
      .tab-btn.active { background:rgba(0, 229, 255, 0.1); border:1px solid rgba(0, 229, 255, 0.3); color:var(--accent);}
      .tab-btn:hover:not(.active) { color:var(--text); background:rgba(255, 255, 255, 0.05); }
      .module-container { display: none; }
      .module-container.active { display: grid; }
    </style>
    
    <script>
      
      // --- PERSISTENCIA DE DATOS (LocalStorage) ---
      function saveAllData() {
        const data = {};
        document.querySelectorAll('input, select').forEach(el => {
          if (el.id) data[el.id] = el.value;
        });
        localStorage.setItem('structural_suite_data', JSON.stringify(data));
      }

      
      // --- SYNCHRONIZE INPUTS ACROSS TABS ---
      
      // --- EVENT DELEGATION GLOBAL SYNC ---
      document.addEventListener('input', function(e) {
          const t = e.target;
          if (!t.classList) return;
          const cls = Array.from(t.classList).find(c => c.startsWith('sync-'));
          if (cls) {
              document.querySelectorAll('.' + cls).forEach(s => {
                  if (s !== t && s.value !== t.value) {
                      s.value = t.value;
                      s.style.backgroundColor = "rgba(0,229,255,0.2)";
                      setTimeout(() => s.style.backgroundColor = "", 500);
                      
                      const id = s.id;
                      if (id.startsWith('losa_')) { if(typeof recalcLosa === 'function') recalcLosa(); }
                      else if (id.startsWith('col_')) { if(typeof recalcCol === 'function') recalcCol(); }
                      else { if(typeof recalc === 'function') recalc(); }
                  }
              });
              if (cls === 'sync-uso') {
                  const cv_viga = document.getElementById('Cv');
                  if (cv_viga) {
                      cv_viga.value = t.value;
                      cv_viga.style.backgroundColor = "rgba(0,229,255,0.2)";
                      setTimeout(() => cv_viga.style.backgroundColor = "", 500);
                      if(typeof recalc === 'function') recalc();
                  }
                  
                  // Also manually sync it for CV in Losas
                  const elCv = document.getElementById('r_losa_cv');
                  const elCvTot = document.getElementById('r_losa_cv_total');
                  const elUso = document.getElementById('r_losa_uso_txt');
                  if (elCv) elCv.textContent = parseFloat(t.value).toFixed(2);
                  if (elCvTot) elCvTot.textContent = parseFloat(t.value).toFixed(2);
                  if (elUso && t.options) elUso.textContent = t.options[t.selectedIndex].text;
              }
          }
      });
      document.addEventListener('change', function(e) {
          // just trigger an input event to catch select changes
          if (e.target.tagName === 'SELECT' && Array.from(e.target.classList).find(c => c.startsWith('sync-'))) {
              e.target.dispatchEvent(new Event('input', {bubbles: true}));
          }
      });


\n      function loadAllData() {
        const saved = localStorage.getItem('structural_suite_data');
        if (!saved) return;
        const data = JSON.parse(saved);
        Object.keys(data).forEach(id => {
          const el = document.getElementById(id);
          if (el) {
            el.value = data[id];
            // Trigger UI styling for specialized elements if they were active
            if (el.tagName === 'INPUT' && el.style.backgroundColor) {
               // optional: handle highlighting here if needed
            }
          }
        });
      }

      // Add persistence triggers
      document.addEventListener('input', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {
          saveAllData();
        }
      });
      document.addEventListener('change', (e) => {
        if (e.target.tagName === 'SELECT') {
          saveAllData();
        }
      });
\n      function openTab(tabId, btn) {
        document.querySelectorAll('.module-container').forEach(e => e.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(e => e.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        btn.classList.add('active');
      }
      
      // Init all engines on load
      const originalOnload = window.onload;
      window.onload = function() {
          if (originalOnload) originalOnload();
          try { loadAllData(); } catch(e) { console.error('Error loading data', e); } \n          // delegated sync catch(e) { console.error('Error initSync', e); }
          // trigger initial sync for CV
          const glUso = document.getElementById('uso'); if(glUso){ const cv_viga = document.getElementById('Cv'); if(cv_viga&&glUso.value!=='') cv_viga.value = glUso.value; }
          recalcLosa();
          if (typeof recalc === 'function') recalc(); // Vigas
          recalcCol();
          recalcSis();
      };
    </script>
"""

modules_html = f"""
    <div id="tab-losas" class="module-container layout active">
      <div class="inputs-panel"><div class="inputs-body">
         <div class="section-header"><div class="section-dot"></div><h2>Losas (Datos van a Vigas)</h2></div>
         {losa_inputs}
      </div></div>
      <div class="results-panel"><div class="results-row-wrap">
         {losa_results}
      </div></div>
    </div>
    
    <div id="tab-vigas" class="module-container layout">
      {viga_layout}
    </div>
    
    <div id="tab-columnas" class="module-container layout">
      <div class="inputs-panel"><div class="inputs-body">
         <div class="section-header"><div class="section-dot"></div><h2>Columnas (Datos vienen de Vigas)</h2></div>
         {col_inputs}
      </div></div>
      <div class="results-panel"><div class="results-row-wrap">
         {col_results}
      </div></div>
    </div>
    
    <div id="tab-sismo" class="module-container layout">
      <div class="inputs-panel"><div class="inputs-body">
         <div class="section-header"><div class="section-dot"></div><h2>Análisis Sísmico</h2></div>
         {sismo_inputs}
      </div></div>
      <div class="results-panel"><div class="results-row-wrap">
         {sismo_results}
      </div></div>
    </div>
"""

tooltip_html = """
<div id="eqTooltip" class="eq-tooltip">
  <div class="eq-tooltip-title">Ecuación</div>
  <div class="eq-tooltip-formula"></div>
  <div class="eq-tooltip-calc"></div>
  <div class="eq-tooltip-status"></div>
</div>
"""

full_html = head_html + "<body><header style='margin-bottom:0;border-bottom:none'>" + head_match.string[head_match.string.find('<div class="logo-badge">'):head_match.string.find('</header>')] + "</header>" + tabs_html + "<div>" + modules_html + "</div>" + tooltip_html + "<script>" + viga_script + losa_js + col_js + sismo_js + "</script></body></html>"
with open('Suite_Estructural_Unificada.html', 'w', encoding='utf-8') as f:
    # Inyectar catálogos NEC-15 y Modales antes de cerrar el body
    catalogs_html = """
    <!-- CATALOG MODALS -->
    <div id="modal-container" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:10000; align-items:center; justify-content:center; backdrop-filter:blur(5px);">
        <div style="background:var(--panel); border:1px solid var(--accent); border-radius:12px; width:90%; max-width:700px; max-height:85vh; overflow:hidden; display:flex; flex-direction:column; box-shadow:0 0 50px rgba(0,229,255,0.2);">
            <div style="padding:15px; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
                <h3 id="modal-title" style="color:var(--accent); font-family:var(--display); font-size:16px;">CATÁLOGO NEC-15</h3>
                <button onclick="closeSismoModal()" style="background:transparent; border:none; color:var(--muted); font-size:24px; cursor:pointer;">&times;</button>
            </div>
            <div id="modal-body" style="padding:15px; overflow-y:auto; font-size:13px; color:var(--text);">
                <!-- Table injected via JS -->
            </div>
        </div>
    </div>
    
    <script>
    const CATALOGS = {
        importance: [
            { category: "EDIFICACIONES ESENCIALES", desc: "Hospitales, centros de salud, estaciones de bomberos, policía, centrales eléctricas, etc.", factor: 1.5 },
            { category: "ESTRUCTURAS ESPECIALES", desc: "Museos, iglesias, escuelas, centros comerciales, o lugares con alta concentración de personas.", factor: 1.3 },
            { category: "OTRAS ESTRUCTURAS", desc: "Viviendas, oficinas, hoteles, o cualquier otra estructura no incluida arriba.", factor: 1.0 }
        ],
        soil: [
            { type: "A", desc: "Perfil de roca competente.", s: 1.0 },
            { type: "B", desc: "Roca de rigidez media.", s: 1.0 },
            { type: "C", desc: "Perfiles de suelos muy densos.", s: 1.2 },
            { type: "D", desc: "Perfiles de suelos rígidos.", s: 1.4 },
            { type: "E", desc: "Perfiles de suelos blandos.", s: 1.5 }
        ]
    };

    function openSismoModal(type) {
        const modal = document.getElementById('modal-container');
        const title = document.getElementById('modal-title');
        const body = document.getElementById('modal-body');
        modal.style.display = 'flex';
        
        let html = '<table style="width:100%; border-collapse:collapse; margin-top:10px;">';
        if(type === 'I') {
            title.innerText = 'FACTOR DE IMPORTANCIA (I) - NEC-15';
            html += '<tr style="border-bottom:2px solid var(--border); color:var(--muted); text-align:left;"><th style="padding:10px;">Categoría</th><th style="padding:10px;">Descripción</th><th style="padding:10px;">Factor</th><th style="padding:10px;">Acción</th></tr>';
            CATALOGS.importance.forEach(item => {
                html += `<tr style="border-bottom:1px solid var(--border);">
                    <td style="padding:12px; font-weight:700; color:var(--accent);">${item.category}</td>
                    <td style="padding:12px;">${item.desc}</td>
                    <td style="padding:12px; font-family:var(--mono); text-align:center;">${item.factor}</td>
                    <td style="padding:12px;"><button onclick="selectSismoValue('sis_i', ${item.factor})" style="background:var(--accent); color:#000; border:none; padding:5px 10px; border-radius:4px; font-weight:700; cursor:pointer;">Elegir</button></td>
                </tr>`;
            });
        }
        html += '</table>';
        body.innerHTML = html;
    }

    function closeSismoModal() { document.getElementById('modal-container').style.display = 'none'; }
    function selectSismoValue(id, val) {
        const input = document.getElementById(id);
        if(input) {
            input.value = val;
            input.dispatchEvent(new Event('input'));
        }
        closeSismoModal();
    }
    </script>
    """
    f.write(full_html.replace('</body>', catalogs_html + '</body>'))

print("Unified SPA created")
