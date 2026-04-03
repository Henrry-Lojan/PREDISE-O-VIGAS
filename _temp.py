import re

path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# I will replace the Losas Arquitectónicos block string AND modify how it parses Vigas
# Actually, the easiest way instead of over-complicating `make_unified.py` is to literally inject the unified logic into the assembled HTML, OR modify `make_unified.py` to do it.

# Let's write the `make_unified.py` patches:

new_make_unified = """
import re

viga_path = r'D:\\Users\\USUARIO 2023\\Desktop\\INTERFAZ\\Predimensionamiento_vigas.html'
with open(viga_path, 'r', encoding='utf-8') as f:
    viga_content = f.read()

head_match = re.search(r'(<!DOCTYPE html>.*?<title>).*?(</title>.*?</style>)', viga_content, re.DOTALL)
if head_match:
    head_html = head_match.group(1) + "Dashboard Unificado - Ingeniería" + head_match.group(2)
else:
    head_html = ""

layout_match = re.search(r'<div class="layout">(.*?)</div><!-- end layout -->', viga_content, re.DOTALL)
viga_layout = layout_match.group(1) if layout_match else ""

script_match = re.search(r'<script>(.*?)</script>', viga_content, re.DOTALL)
viga_script = script_match.group(1) if script_match else ""

viga_script = viga_script.replace(
    "const cuEl = document.getElementById('cu_display'); if (cuEl) cuEl.textContent = Cu.toFixed(2);",
    '''const cuEl = document.getElementById('cu_display'); if (cuEl) cuEl.textContent = Cu.toFixed(2);
      const colCuInput = document.getElementById('col_cu');
      if (colCuInput && Math.abs((parseFloat(colCuInput.value)||0) - Cu) > 0.01) {
          colCuInput.value = Cu.toFixed(2);
          colCuInput.style.backgroundColor = "rgba(127,255,107,0.3)";
          setTimeout(() => { colCuInput.style.backgroundColor = ""; }, 1000);
          if (typeof recalcCol === 'function') recalcCol();
      }
      const colBvigInput = document.getElementById('col_bvig');
      if (colBvigInput && colBvigInput.value != b) {
          colBvigInput.value = b;
      }
    '''
)

def build_arch_block(prefix=''):
    return f'''        <div class="input-group arch-group">
          <div class="input-group-title"><span style="color:var(--accent)">◈</span> Datos Arquitectónicos</div>
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
          <div style="font-size:10px; color:var(--muted); text-align:right; margin-top:5px; opacity:0.8;">(Sección 4.2 - Tabla 9 - NEC-SE-CG 2015)</div>
        </div>'''

# --- VIGAS LAYOUT modifications
# Remove the existing "ARQUITECTONICOS" from viga_layout and replace it with our dynamic one
vig_arch_regex = r'<!-- ARQUITECTÓNICOS -->.*?<!-- CARGAS -->'
viga_layout = re.sub(vig_arch_regex, "<!-- ARQUITECTÓNICOS -->\n" + build_arch_block('') + "\n<!-- CARGAS -->", viga_layout, flags=re.DOTALL)


# --- LOSAS UI
losa_inputs = build_arch_block('losa_') + '''
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
'''
# NOTE: Removed the separate "Carga Viva NEC" block, because it is now inside the unified arch block for Losas!
"""
# Get the rest of the python code directly as a continuation
with open(r'X_temp.py', 'r') # wait I'll embed the rest manually.
"""
