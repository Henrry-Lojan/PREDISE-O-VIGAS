path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find start of the merged card (line with mini-card + gradient background on same line)
start_idx = None
end_idx = None
for i, l in enumerate(lines):
    if '<div class="mini-card"' in l and 'linear-gradient' in l:
        start_idx = i
        break

if start_idx is None:
    print('ERROR: start not found')
    exit(1)

# Find the matching closing </div> at the same nesting level
depth = 0
for i in range(start_idx, len(lines)):
    depth += lines[i].count('<div')
    depth -= lines[i].count('</div>')
    if depth <= 0:
        end_idx = i
        break

print(f'Block from line {start_idx+1} to {end_idx+1}')

# The two original separate cards to restore
restored = """\
        <div class="mini-card">
          <div class="mini-header"><span style="color:var(--accent2)">&#9658;</span> Peso del hormig\u00f3n</div>
          <div class="mini-body">
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_vtot" data-eq-title="Vol. Total" data-eq-body="V_{tot} = \\\\frac{100 \\\\times 100}{10000} \\\\times \\\\frac{Hl}{100}">Volumen total en funci\u00f3n de geometr\u00eda</span><span class="rv" id="r_losa_vtot">\u2014</span><span class="ru">m\u00b3</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_vbloq" data-eq-title="Vol. Bloques" data-eq-body="V_{bloq} = \\\\frac{bb^2 \\\\times (Hl-tc) \\\\times 4}{10^6}">Volumen del bloque en funci\u00f3n de geometr\u00eda</span><span class="rv" id="r_losa_vbloq">\u2014</span><span class="ru">m\u00b3</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_vhorm" data-eq-title="Vol. Hormig\u00f3n" data-eq-body="V_{horm} = V_{tot} - V_{bloq}">Volumen del hormig\u00f3n</span><span class="rv" id="r_losa_vhorm">\u2014</span><span class="ru">m\u00b3</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_peso" data-eq-title="Peso Hormig\u00f3n" data-eq-body="P_{h} = V_{horm} \\\\times 2.4">Peso del hormig\u00f3n en funci\u00f3n del peso espec\u00edfico</span><span class="rv" id="r_losa_peso">\u2014</span><span class="ru">t</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_area" data-eq-title="\u00c1rea" data-eq-body="A = \\\\frac{100 \\\\times 100}{10000}">El \u00c1rea</span><span class="rv" id="r_losa_area">\u2014</span><span class="ru">m\u00b2</span></div>
            <div class="mini-sep"></div>
            <div class="mini-row"><span class="rl" style="color:var(--accent3);font-weight:700">CARGA MUERTA DE LA LOSA</span><span class="rv accent-v" id="r_losa_phorm_final">\u2014</span><span class="ru">t/m\u00b2</span></div>
          </div>
        </div>
        <div class="mini-card diagram-mini">
          <div class="mini-header"><span style="color:var(--warn)">&#9658;</span> Cargas Muertas Adicionales y Totales</div>
          <div class="mini-body" style="padding:15px;">
            <div class="mini-row"><span class="rl" id="lbl_losa_cpared">Paredes / Tabiquer\u00eda equivalentes</span><span class="rv" id="r_losa_cpared">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl" id="lbl_losa_caliv">Alivianador de losa</span><span class="rv" id="r_losa_caliv">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl">Masillado</span><span class="rv" id="r_losa_cmasillado">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl">Acabados</span><span class="rv" id="r_losa_cacabados">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl">Instalaciones</span><span class="rv" id="r_losa_cinstal">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-sep"></div>
            <div class="mini-row"><span class="rl" style="color:var(--accent2);font-weight:700">CARGAS MUERTAS INSTALACIONES</span><span class="rv" id="r_losa_csuper">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl" style="color:var(--accent2);font-weight:700">CARGA MUERTA LOSA</span><span class="rv" id="r_losa_cmlosa">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-sep"></div>
            <div class="mini-row"><span class="rl" style="color:var(--warn);font-weight:800;font-size:13px">CARGA MUERTA TOTAL</span><span class="rv" style="color:var(--warn);font-size:15px" id="r_losa_cm_total">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div style="font-size:10px; color:var(--muted); text-align:right; margin-top:4px;">* Suma transferida din\u00e1micamente al m\u00f3dulo Vigas</div>
          </div>
        </div>
"""

# Also remove any r_losa_csuper2 setResult injections from JS
new_lines = lines[:start_idx] + [restored] + lines[end_idx+1:]

# Remove r_losa_csuper2 line if it was added to JS
clean_lines = [l for l in new_lines if "r_losa_csuper2" not in l]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(clean_lines)

print('Restored OK')
