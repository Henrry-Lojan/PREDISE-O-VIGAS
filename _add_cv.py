path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add CV input section right before closing </div>\n"""
old_inputs_end = '          <div class="input-row"><label>Instalaciones</label><div class="input-wrap"><input type="number" id="losa_instalaciones" value="0.02" step="0.01"><span class="input-unit">t/m2</span></div></div>\n        </div>\n"""'

new_inputs_end = '''          <div class="input-row"><label>Instalaciones</label><div class="input-wrap"><input type="number" id="losa_instalaciones" value="0.02" step="0.01"><span class="input-unit">t/m2</span></div></div>
        </div>
        <div class="input-group">
          <div class="input-group-title"><span style="color:var(--bad)">&#9670;</span> Carga Viva &mdash; NEC-SE-CG 2015</div>
          <div class="input-row"><label>Uso del edificio</label><div class="input-wrap" style="width:150px;">
            <select id="losa_cv" onchange="recalcLosa()">
              <option value="0.200">Vivienda / Departamentos</option>
              <option value="0.240">Oficinas</option>
              <option value="0.300">Aulas / Escuelas</option>
              <option value="0.300">Corredores (resid.)</option>
              <option value="0.300">Escaleras</option>
              <option value="0.300">Garajes (< 4 t)</option>
              <option value="0.480">Salas de reuni\u00f3n</option>
              <option value="0.290">Biblioteca - lectura</option>
              <option value="0.720">Biblioteca - dep\u00f3sito</option>
              <option value="0.200">Hospital - salas</option>
              <option value="0.380">Hospital - corredores</option>
              <option value="0.200">Hotel - cuartos</option>
              <option value="0.380">Hotel - corredores</option>
              <option value="0.480">Comercial planta baja</option>
              <option value="0.360">Comercial plantas sup.</option>
              <option value="0.180">Cubierta accesible</option>
              <option value="0.070">Cubierta no accesible</option>
            </select>
          </div></div>
        </div>
"""'''

c = c.replace(old_inputs_end, new_inputs_end, 1)

# 2. Add CV results card after Cargas Muertas card (before Inercia Steiner)
old_steiner_card = '''        <div class="mini-card diagram-mini">
          <div class="mini-header"><span style="color:var(--accent)">&#9658;</span> Inercia Teorema Steiner'''

new_steiner_card = '''        <div class="mini-card">
          <div class="mini-header"><span style="color:var(--bad)">&#9670;</span> Carga Viva &mdash; NEC-SE-CG 2015</div>
          <div class="mini-body" style="padding:12px 15px;">
            <div style="font-size:10px;font-weight:700;letter-spacing:1px;color:var(--bad);margin-bottom:8px;padding-bottom:4px;border-bottom:1px dashed rgba(255,71,87,0.3);">CARGAS VARIABLES M\u00cdNIMAS (Tabla NEC-SE-CG)</div>
            <div class="mini-row"><span class="rl" id="lbl_losa_uso" style="white-space:nowrap">Uso seleccionado</span><span class="rv" id="r_losa_uso_txt" style="color:var(--bad);font-size:11px;text-align:right;white-space:nowrap">—</span><span class="ru"></span></div>
            <div class="mini-row"><span class="rl" style="white-space:nowrap">Carga viva (CV)</span><span class="rv" id="r_losa_cv" style="color:var(--bad);font-weight:700;">—</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-sep"></div>
            <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(255,71,87,0.08);border-radius:6px;padding:6px 10px;margin:6px 0 4px;border-left:3px solid var(--bad);">
              <span style="font-size:11px;font-weight:700;color:var(--bad);white-space:nowrap;">CARGA VIVA TOTAL</span>
              <span style="display:flex;align-items:center;gap:4px;"><span id="r_losa_cv_total" style="color:var(--bad);font-size:15px;font-weight:900;">—</span><span class="ru">t/m\u00b2</span></span>
            </div>
            <div style="font-size:10px;color:var(--muted);text-align:right;margin-top:5px;">* Valor m\u00ednimo seg\u00fan NEC-SE-CG-2015</div>
          </div>
        </div>
        <div class="mini-card diagram-mini">
          <div class="mini-header"><span style="color:var(--accent)">&#9658;</span> Inercia Teorema Steiner'''

c = c.replace(old_steiner_card, new_steiner_card, 1)

# 3. Add CV JS calculation inside recalcLosa, just before closing }
# Find where setResult for cm_total is and add CV calcs after it
old_js_end = "setResult('r_losa_cm_total', C_total, 2);"
new_js_end = """setResult('r_losa_cm_total', C_total, 2);

      // Carga Viva NEC-15
      const cvSel = document.getElementById('losa_cv');
      const cv_val = parseFloat(cvSel ? cvSel.value : 0.200);
      const cv_uso = cvSel ? cvSel.options[cvSel.selectedIndex].text : 'Vivienda';
      setResult('r_losa_cv', cv_val, 2);
      setResult('r_losa_cv_total', cv_val, 2);
      const usoEl = document.getElementById('r_losa_uso_txt');
      if (usoEl) usoEl.textContent = cv_uso;"""

c = c.replace(old_js_end, new_js_end, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('CV card added OK')
