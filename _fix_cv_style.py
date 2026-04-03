path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Find and replace the entire CV card in losa_results
old_cv_card = '''        <div class="mini-card">
          <div class="mini-header"><span style="color:var(--accent2)">&#9670;</span> Cargas Vivas &mdash; NEC-SE-CG 2015</div>
          <div class="mini-body" style="padding:12px 15px;">
            <div style="font-size:10px;font-weight:700;letter-spacing:1px;color:var(--accent2);margin-bottom:8px;padding-bottom:4px;border-bottom:1px dashed rgba(0,229,255,0.3);">CARGAS VARIABLES M\u00cdNIMAS (Tabla NEC-SE-CG)</div>
            <div class="mini-row"><span class="rl" id="lbl_losa_uso" style="white-space:nowrap">Uso seleccionado</span><span class="rv" id="r_losa_uso_txt" style="color:var(--bad);font-size:11px;text-align:right;white-space:nowrap">\u2014</span><span class="ru"></span></div>
            <div class="mini-row"><span class="rl" style="white-space:nowrap">Carga viva (CV)</span><span class="rv" id="r_losa_cv" style="color:var(--accent2);font-weight:700;">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-sep"></div>
            <div style="display:flex;justify-content:space-between;align-items:center;background:rgba(0,229,255,0.07);border-radius:6px;padding:6px 10px;margin:6px 0 4px;border-left:3px solid var(--accent2);">
              <span style="font-size:11px;font-weight:700;color:var(--accent2);white-space:nowrap;">CARGA VIVA TOTAL</span>
              <span style="display:flex;align-items:center;gap:4px;"><span id="r_losa_cv_total" style="color:var(--accent2);font-size:15px;font-weight:900;">\u2014</span><span class="ru">t/m\u00b2</span></span>
            </div>
            <div style="font-size:10px;color:var(--muted);text-align:right;margin-top:5px;">* Valor m\u00ednimo seg\u00fan NEC-SE-CG-2015</div>
          </div>
        </div>'''

new_cv_card = '''        <div class="mini-card">
          <div class="mini-header"><span style="color:var(--accent2)">&#9658;</span> Cargas Vivas (NEC-SE-CG 2015)</div>
          <div class="mini-body">
            <div class="mini-row"><span class="rl">Uso seleccionado</span><span class="rv" id="r_losa_uso_txt" style="font-size:11px;text-align:right;">\u2014</span><span class="ru"></span></div>
            <div class="mini-row"><span class="rl">Carga viva (CV)</span><span class="rv accent-v" id="r_losa_cv">\u2014</span><span class="ru">t/m\u00b2</span></div>
            <div class="mini-sep"></div>
            <div class="mini-row"><span class="rl" style="color:var(--accent2);font-weight:700">CARGA VIVA TOTAL</span><span class="rv" id="r_losa_cv_total" style="color:var(--accent2);font-size:15px;font-weight:700">\u2014</span><span class="ru">t/m\u00b2</span></div>
          </div>
        </div>'''

if old_cv_card in c:
    c = c.replace(old_cv_card, new_cv_card, 1)
    print('Replaced OK')
else:
    # Try partial match
    idx = c.find('Cargas Vivas &mdash; NEC-SE-CG 2015')
    if idx >= 0:
        print(f'Found partial at {idx}, manual fix needed')
    else:
        idx = c.find('Cargas Vivas')
        print(f'Found Cargas Vivas at {idx}')
        print(repr(c[idx-100:idx+500]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
