import re
with open(r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Modify how viga_layout handles its ARQUITECTÓNICOS section
# We inject a replacment right after getting viga_layout
old_viga_layout = 'viga_layout = layout_match.group(1) if layout_match else ""'
new_viga_layout = '''viga_layout = layout_match.group(1) if layout_match else ""

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
viga_layout = re.sub(vig_arch_regex, build_arch_block('') + "\\n        <!-- CARGAS -->", viga_layout, flags=re.DOTALL)
'''
code = code.replace(old_viga_layout, new_viga_layout, 1)

# 2. Replace losa_inputs entirely
old_losa_inputs_start = 'losa_inputs = """'
# we find the end of losa_inputs
idx_start = code.find(old_losa_inputs_start)
idx_end = code.find('"""', idx_start + len(old_losa_inputs_start))
old_losa_inputs_full = code[idx_start:idx_end+3]

new_losa_inputs_full = '''losa_inputs = build_arch_block('losa_') + """
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
"""'''
code = code.replace(old_losa_inputs_full, new_losa_inputs_full, 1)

# 3. Modify col_inputs to also have the arch block at the beginning
old_col_inputs_start = 'col_inputs = """'
idx_start2 = code.find(old_col_inputs_start)
idx_end2 = code.find('"""', idx_start2 + len(old_col_inputs_start))
old_col_inputs_full = code[idx_start2:idx_end2+3]

new_col_inputs_full = '''col_inputs = build_arch_block('col_') + """
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
"""'''
code = code.replace(old_col_inputs_full, new_col_inputs_full, 1)

# 4. Update JS logic. Losa needs `losa_uso` instead of `losa_cv`.
# And columns need to read `col_pisos` instead of `getVal('pisos')||2` (or keep reading 'pisos', wait! the JS syncing will keep them identical anyway!)
code = code.replace("const cvSel = document.getElementById('losa_cv');", "const cvSel = document.getElementById('losa_uso');")

# 5. Add Sync logic!
sync_js = """
      // --- SYNCHRONIZE INPUTS ACROSS TABS ---
      const syncClasses = ['sync-L1', 'sync-L2', 'sync-L3', 'sync-L4', 'sync-pisos', 'sync-He', 'sync-uso'];
      syncClasses.forEach(cls => {
          document.querySelectorAll('.' + cls).forEach(el => {
              const handleSync = (e) => {
                  const val = e.target.value;
                  document.querySelectorAll('.' + cls).forEach(sibling => {
                      if (sibling !== e.target && sibling.value !== val) {
                          sibling.value = val;
                          sibling.style.backgroundColor = "rgba(0,229,255,0.2)";
                          setTimeout(() => { sibling.style.backgroundColor = ""; }, 500);
                          // We don't dispatch direct input to avoid infinite loops,
                          // but since they all recalculate on tab switch or periodically, it's fine.
                          // Actually, we SHOULD manually trigger recalculation for their respective modules:
                          if (sibling.id.startsWith('losa_')) { if(typeof recalcLosa === 'function') recalcLosa(); }
                          else if (sibling.id.startsWith('col_')) { if(typeof recalcCol === 'function') recalcCol(); }
                          else { if(typeof recalc === 'function') recalc(); }
                      }
                  });
                  // EXCEPTION: 'Uso' also affects Vigas' 'Cv' input
                  if (cls === 'sync-uso') {
                      const cv_viga = document.getElementById('Cv');
                      if (cv_viga) {
                          cv_viga.value = val;
                          cv_viga.style.backgroundColor = "rgba(0,229,255,0.2)";
                          setTimeout(() => { cv_viga.style.backgroundColor = ""; }, 500);
                          if(typeof recalc === 'function') recalc();
                      }
                  }
              };
              el.addEventListener('input', handleSync);
              el.addEventListener('change', handleSync);
          });
      });
"""

# Insert `sync_js` right after `loadAllData()` definition in the persistent block
code = code.replace("function loadAllData() {", sync_js + "\\n      function loadAllData() {")

# 6. For vigas, we need to handle "Cv" natively when `uso` changes on load!
old_load = "try { loadAllData(); } catch(e) { console.error('Error loading data', e); }"
new_load = "try { loadAllData(); } catch(e) { console.error('Error loading data', e); }\n          // trigger initial sync for CV\n          const glUso = document.getElementById('uso'); if(glUso){ const cv_viga = document.getElementById('Cv'); if(cv_viga&&glUso.value!=='') cv_viga.value = glUso.value; }"
code = code.replace(old_load, new_load)


with open(r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified_synced.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Python script generated!")
