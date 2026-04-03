path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_card = """\
        <div class="mini-card" style="background:linear-gradient(160deg,rgba(0,229,255,0.04),rgba(123,97,255,0.06),rgba(255,167,38,0.04));border:1px solid rgba(123,97,255,0.3);border-radius:10px;">
          <div class="mini-header" style="font-size:12px;letter-spacing:1.5px;padding-bottom:8px;border-bottom:1px solid rgba(123,97,255,0.3);">&#x2B21;&nbsp;AN\u00c1LISIS DE CARGAS MUERTAS</div>
          <div class="mini-body" style="padding:12px 15px;">
            <div style="font-size:10px;font-weight:700;letter-spacing:1px;color:var(--accent2);margin:4px 0 8px 0;padding-bottom:4px;border-bottom:1px dashed rgba(0,229,255,0.25);">&#9312; PESO PROPIO &mdash; LOSA DE HORMIG\u00d3N</div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_vtot" data-eq-title="Vol. Total" data-eq-body="V_{{tot}} = \\frac{{100 \\times 100}}{{10000}} \\times \\frac{{Hl}}{{100}}">Volumen total por geometr\u00eda</span><span class="rv" id="r_losa_vtot">\u2014</span><span class="ru">m\u00b3</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_vbloq" data-eq-title="Vol. Bloques" data-eq-body="V_{{bloq}} = \\frac{{bb^2 \\times (Hl-tc) \\times 4}}{{10^6}}">Volumen bloques alivianantes</span><span class="rv" id="r_losa_vbloq">\u2014</span><span class="ru">m\u00b3</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_vhorm" data-eq-title="Vol. Hormig\u00f3n" data-eq-body="V_{{horm}} = V_{{tot}} - V_{{bloq}}">Volumen hormig\u00f3n real</span><span class="rv" id="r_losa_vhorm">\u2014</span><span class="ru">m\u00b3</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_peso" data-eq-title="Peso Hormig\u00f3n" data-eq-body="P_{{h}} = V_{{horm}} \\times 2.4">Peso hormig\u00f3n (\u03b3 = 2.4 t/m\u00b3)</span><span class="rv" id="r_losa_peso">\u2014</span><span class="ru">t</span></div>
            <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_area" data-eq-title="\u00c1rea" data-eq-body="A = 1.0 \\text{{ m}}^2">\u00c1rea unitaria (1m\u00d71m)</span><span class="rv" id="r_losa_area">\u2014</span><span class="ru">m\u00b2</span></div>
            <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(0,229,255,0.09);border-radius:5px;padding:5px 10px;margin:6px 0 12px;border-left:3px solid var(--accent2);">
              <span style="font-size:11px;font-weight:700;color:var(--accent2);">CARGA MUERTA DE LA LOSA</span>
              <span style="display:flex;align-items:center;gap:4px;"><span class="rv accent-v" id="r_losa_phorm_final" style="font-size:14px;">\u2014</span><span class="ru">t/m\u00b2</span></span>
            </div>
            <div style="font-size:10px;font-weight:700;letter-spacing:1px;color:var(--accent3);margin:4px 0 8px 0;padding-bottom:4px;border-bottom:1px dashed rgba(127,255,107,0.25);">&#9313; CARGAS SUPERIMPUESTAS</div>
            <div class="mini-row"><span class="rl" id="lbl_losa_cpared">Paredes / Tabiquer\u00eda equiv.</span><span class="rv" id="r_losa_cpared">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl" id="lbl_losa_caliv">Alivianador de losa</span><span class="rv" id="r_losa_caliv">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl">Masillado</span><span class="rv" id="r_losa_cmasillado">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl">Acabados</span><span class="rv" id="r_losa_cacabados">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl">Instalaciones</span><span class="rv" id="r_losa_cinstal">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(127,255,107,0.07);border-radius:5px;padding:5px 10px;margin:6px 0 12px;border-left:3px solid var(--accent3);">
              <span style="font-size:11px;font-weight:700;color:var(--accent3);">CARGAS MUERTAS INSTALACIONES</span>
              <span style="display:flex;align-items:center;gap:4px;"><span class="rv" id="r_losa_csuper" style="color:var(--accent3);font-size:14px;">\u2014</span><span class="ru">t/m\u00b2</span></span>
            </div>
            <div style="font-size:10px;font-weight:700;letter-spacing:1px;color:var(--warn);margin:4px 0 8px 0;padding-bottom:4px;border-bottom:1px dashed rgba(255,167,38,0.3);">&#9314; RESUMEN FINAL</div>
            <div class="mini-row"><span class="rl" style="color:var(--accent2);font-weight:600;">Carga muerta losa (peso propio)</span><span class="rv" id="r_losa_cmlosa" style="color:var(--accent2);">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-row"><span class="rl" style="color:var(--accent3);font-weight:600;">Cargas superimpuestas</span><span class="rv" id="r_losa_csuper2" style="color:var(--accent3);">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(255,167,38,0.10);border-radius:6px;padding:8px 12px;margin:8px 0 4px;border:1px solid rgba(255,167,38,0.4);">
              <span style="font-size:13px;font-weight:800;color:var(--warn);letter-spacing:0.5px;">CARGA MUERTA TOTAL</span>
              <span style="display:flex;align-items:center;gap:6px;"><span id="r_losa_cm_total" style="color:var(--warn);font-size:18px;font-weight:900;">\u2014</span><span style="color:var(--muted);font-size:11px;">t/m\u00b2</span></span>
            </div>
            <div style="font-size:10px;color:var(--muted);text-align:right;margin-top:5px;">* Valor transferido din\u00e1micamente al m\u00f3dulo Vigas \u2193</div>
          </div>
        </div>
"""

# Also need setResult for r_losa_csuper2 in JS — find and patch
# Replace lines 134-161 (0-indexed: 133 to 160)
new_lines = lines[:133] + [new_card] + lines[161:]

# Patch JS: add setResult for r_losa_csuper2 right after r_losa_csuper
patched = []
for line in new_lines:
    patched.append(line)
    if "setResult('r_losa_csuper'," in line and 'r_losa_csuper2' not in line:
        indent = line[:len(line) - len(line.lstrip())]
        patched.append(indent + "setResult('r_losa_csuper2', C_superimpuesta, 2);\n")

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(patched)

print('Patch applied OK')
