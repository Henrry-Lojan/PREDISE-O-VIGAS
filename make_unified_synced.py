import re

def build_arch_block(prefix=''):
    return f"""        <!-- ARQUITECTÓNICOS -->
        <div class="input-group arch-group">
          <div class="input-group-title"><span style="color:var(--accent)">◈</span> {'Datos Coordinados (Globales)'}</div>
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

viga_path = 'Predimensionamiento_vigas.html'
with open(viga_path, 'r', encoding='utf-8') as f:
    viga_content = f.read()

# Extraer el layout de Vigas de forma robusta
start_tag = '<div class="layout">'
v_start = viga_content.find(start_tag)
v_end = viga_content.find('<!-- Interactive Equation Tooltip -->')
if v_end == -1: v_end = viga_content.find('</body>')
viga_layout = viga_content[v_start + len(start_tag) : v_end].strip()
if viga_layout.endswith('</div>'):
    viga_layout = viga_layout[:-6].strip()

# Replace architectural block in viga_layout
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
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_lmax" data-eq-title="Luz Máxima" data-eq-body="\\\\text{Máxima luz entre L1, L2, L3 y L4}">Luz Máxima Arquitectónica (Lmáx)</span><span class="rv" id="r_losa_lmax">—</span><span class="ru">m</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_lreal" data-eq-title="Luz Cálculo" data-eq-body="L_{real} = \\\\frac{L_{m\\\\acute{a}x}}{V_{int} + 1}">Luz Efectiva de Cálculo (Lreal)</span><span class="rv accent-v" id="r_losa_lreal">—</span><span class="ru">m</span></div>
            <div class="mini-sep"></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_imin" data-eq-title="Inercia Mínima Requerida" data-eq-body="I_{min} = \\\\frac{100 \\\\cdot h_{min}^3}{12}">Inercia mínima requerida de losa maciza (1m)</span><span class="rv" id="r_losa_imin">—</span><span class="ru">cm4</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_isteiner" data-eq-title="Inercia Alivianada (Steiner)" data-eq-body="I_{total} = \\\\sum I_{individuales}">Inercia de la losa alivianada de espesor — cm</span><span class="rv accent-v" id="r_losa_isteiner">—</span><span class="ru">cm4</span></div>
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
                         <div style="position:absolute; top:-16px; width:100%; text-align:center; font-size:10px; color:var(--muted); font-weight:bold; letter-spacing:0.05em;">ANCHO DE ANÁLISIS = 1.00 m</div>
                         <div style="border-left:1px solid rgba(255,255,255,0.3); height:5px; position:absolute; left:0; bottom:0;"></div>
                         <div style="border-right:1px solid rgba(255,255,255,0.3); height:5px; position:absolute; right:0; bottom:0;"></div>
                      </div>
                      <div id="dib_tabla" style="background:var(--accent); width:100%; height:15px; border-radius:2px 2px 0 0; display:flex; align-items:center; justify-content:center; color:rgba(0,0,0,0.7); font-size:11px; font-weight:800; letter-spacing:0.05em;">
                         Tabla de compresión
                      </div>
                      <div id="dib_nervios_container" style="display:flex; width:100%; justify-content:flex-start;">
                         <!-- JS injected webs -->
                      </div>
                   </div>
                </div>
                <div id="dib_labels" style="margin-top:15px; font-size:12px; color:var(--text); font-family:var(--sans); background:rgba(0,229,255,0.05); padding:8px; border-radius:4px; border:1px solid rgba(0,229,255,0.2);"></div>
             </div>
             <div class="mini-row" style="text-align:left;"><span class="rl clickable-label" id="lbl_losa_heq" data-eq-title="Altura Equivalente Losa Maciza" data-eq-body="H_{eq} = \\\\left( \\\\frac{12 \\\\cdot I_t}{100} \\\\right)^{1/3}">Altura losa maciza equiv. (Heq)</span><span class="rv accent-v" id="r_losa_heq">—</span><span class="ru">cm</span></div>
             <div class="mini-row" style="text-align:left;"><span class="rl clickable-label" id="lbl_losa_lmaxperm" data-eq-title="Longitud Máx Permitida" data-eq-body="L_{m\\\\acute{a}x\\\\,perm} = \\\\frac{H_{eq}}{0.03 \\\\cdot 100}">Longitud máxima para una losa de — cm</span><span class="rv accent-v" id="r_losa_lmaxperm">—</span><span class="ru">m</span></div>
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
      
      const b_tot = bn + bb;
      const hw = hl - tc;
      
      const num_bloques_1m2 = 10000 / ((b_tot) * (b_tot));
      const vtot_1m2 = 1.0 * (hl/100);
      const vbloq_1m2 = (bb/100) * (bb/100) * (hw/100) * num_bloques_1m2;
      const vhorm_1m2 = vtot_1m2 - vbloq_1m2;
      const Peso_horm = vhorm_1m2 * 2.4; 
      const Phorm_final = Peso_horm;
      
      const paredSel = document.getElementById('losa_paredes');
      const c_pared = parseFloat(paredSel.value) || 0;
      const alivSel = document.getElementById('losa_alivian');
      const c_aliv = parseFloat(alivSel.value) || 0;
      
      const c_mas = parseFloat(document.getElementById('losa_masillado').value) || 0;
      const c_aca = parseFloat(document.getElementById('losa_acabados').value) || 0;
      const c_inst = parseFloat(document.getElementById('losa_instalaciones').value) || 0;
      
      const C_superimpuesta = c_pared + c_aliv + c_mas + c_aca + c_inst;
      const P_eq = Phorm_final + C_superimpuesta;
      
      const width_m = 100;
      const I_min = (width_m*Math.pow(hmin, 3))/12;
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
      rowsData.forEach(r => { sumA += r.A; sumAy += r.A * r.y; });
      const Yc = sumA > 0 ? sumAy / sumA : 0;
      
      let sumIt = 0;
      rowsData.forEach(r => {
          const d = Math.abs(r.y - Yc);
          sumIt += r.Io + r.A * d*d;
      });
      const I_steiner = sumIt;
      
      setResult('r_losa_lmax', lmax, 2);
      setResult('r_losa_lreal', lreal, 2);
      setResult('r_losa_hmin', hmin, 1);
      setResult('r_losa_imin', I_min, 0);
      setResult('r_losa_isteiner', I_steiner, 0);
      
      const heq = Math.pow((12 * I_steiner) / 100, 1/3);
      setResult('r_losa_heq', heq, 2);
      setResult('r_losa_lmaxperm', heq / (0.03 * 100), 2);
      setResult('r_losa_phorm_final', Phorm_final, 2);
      setResult('r_losa_cm_total', P_eq, 2);

      // Link to Vigas
      const vigaCm = document.getElementById('Cm');
      if (vigaCm) { vigaCm.value = P_eq.toFixed(3); if(typeof recalc === 'function') recalc(); }
    }
    document.querySelectorAll('[id^=losa_]').forEach(el => el.addEventListener('input', recalcLosa));
"""

# --- CARGAR COLUMNAS ---
col_path = 'Predimensionamiento_columnas.html'
with open(col_path, 'r', encoding='utf-8') as f:
    col_content = f.read()
c_start = col_content.find('<div class="layout">')
c_end = col_content.find('<!-- Interactive Equation Tooltip -->')
if c_end == -1: c_end = col_content.find('</body>')
col_layout = col_content[c_start + 20 : c_end].strip() # 20 is len of <div class="layout">
if col_layout.endswith('</div>'): col_layout = col_layout[:-6].strip()
col_js_match = re.search(r'<script>(.*?)</script>', col_content, re.DOTALL)
col_js = col_js_match.group(1) if col_js_match else ""

# --- CARGAR SISMO ---
sismo_path = 'Analisis_sismico.html'
with open(sismo_path, 'r', encoding='utf-8') as f:
    sismo_content = f.read()
s_start = sismo_content.find('<div class="layout">')
s_end = sismo_content.find('<!-- Interactive Equation Tooltip -->')
if s_end == -1: s_end = sismo_content.find('</body>')
sismo_layout = sismo_content[s_start + 20 : s_end].strip()
if sismo_layout.endswith('</div>'): sismo_layout = sismo_layout[:-6].strip()
sismo_js_match = re.search(r'<script>(.*?)</script>', sismo_content, re.DOTALL)
sismo_js = sismo_js_match.group(1) if sismo_js_match else ""

# --- TABS UI ---
tabs_html = """
    <div class="tabs-nav" style="display:flex; gap:10px; padding:10px 24px; background:var(--panel); border-bottom:1px solid var(--border);">
      <button class="tab-btn active" onclick="openTab('tab-losas', this)">🟦 LOSAS</button>
      <button class="tab-btn" onclick="openTab('tab-vigas', this)">🏗️ VIGAS</button>
      <button class="tab-btn" onclick="openTab('tab-columnas', this)">🗼 COLUMNAS</button>
      <button class="tab-btn" onclick="openTab('tab-sismo', this)">📈 SISMO</button>
    </div>
    <style>
      .tab-btn { background:transparent; border:1px solid transparent; color:var(--muted); font-family:var(--display); font-size:13px; font-weight:700; padding:8px 16px; cursor:pointer; border-radius:6px; transition:all 0.2s; }
      .tab-btn.active { background:rgba(0, 229, 255, 0.1); border-color:rgba(0, 229, 255, 0.3); color:var(--accent); }
      .module-container { display: none; }
      .module-container.active { display: grid; }
    </style>
    <script>
      function openTab(id, btn) {
        document.querySelectorAll('.module-container').forEach(e => e.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(e => e.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        btn.classList.add('active');
      }
    </script>
"""

modules_html = f"""
    <div id="tab-losas" class="module-container layout active">
      <div class="inputs-panel"><div class="inputs-body">{losa_inputs}</div></div>
      <div class="results-panel">{losa_results}</div>
    </div>
    <div id="tab-vigas" class="module-container layout">
      {viga_layout}
    </div>
    <div id="tab-columnas" class="module-container layout">
      {col_layout}
    </div>
    <div id="tab-sismo" class="module-container layout">
      {sismo_layout}
    </div>
"""

# Re-construir el head con los estilos originales de Vigas
head_match = re.search(r'<head>(.*?)</head>', viga_content, re.DOTALL)
head_html = "<!DOCTYPE html><html lang='es'><head>" + head_match.group(1) + "</head>"

header_match = re.search(r'<header>(.*?)</header>', viga_content, re.DOTALL)
header_html = "<header style='margin-bottom:0;border-bottom:none'>" + header_match.group(1) + "</header>" if header_match else ""

full_html = head_html + "<body>" + header_html + tabs_html + "<div>" + modules_html + "</div><script>" + viga_script + losa_js + col_js + sismo_js + "</script></body></html>"

with open('Suite_Estructural_Unificada.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Unified Suite synchronization complete")
