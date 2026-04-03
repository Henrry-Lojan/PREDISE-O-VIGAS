path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Fix color: replace --bad with a nice purple/accent2 color for CV card in results
c = c.replace(
    '<div class="mini-header"><span style="color:var(--bad)">&#9670;</span> Carga Viva &mdash; NEC-SE-CG 2015</div>',
    '<div class="mini-header"><span style="color:var(--accent2)">&#9670;</span> Cargas Vivas &mdash; NEC-SE-CG 2015</div>',
    1
)
c = c.replace(
    "font-size:10px;font-weight:700;letter-spacing:1px;color:var(--bad);margin-bottom:8px;padding-bottom:4px;border-bottom:1px dashed rgba(255,71,87,0.3);",
    "font-size:10px;font-weight:700;letter-spacing:1px;color:var(--accent2);margin-bottom:8px;padding-bottom:4px;border-bottom:1px dashed rgba(0,229,255,0.3);",
    1
)
c = c.replace(
    'style="color:var(--bad);font-weight:700;">—</span><span class="ru">t/m\u00b2</span></div>',
    'style="color:var(--accent2);font-weight:700;">—</span><span class="ru">t/m\u00b2</span></div>',
    1
)
c = c.replace(
    'background:rgba(255,71,87,0.08);border-radius:6px;padding:6px 10px;margin:6px 0 4px;border-left:3px solid var(--bad)',
    'background:rgba(0,229,255,0.07);border-radius:6px;padding:6px 10px;margin:6px 0 4px;border-left:3px solid var(--accent2)',
    1
)
c = c.replace(
    '<span style="font-size:11px;font-weight:700;color:var(--bad);white-space:nowrap;">CARGA VIVA TOTAL</span>',
    '<span style="font-size:11px;font-weight:700;color:var(--accent2);white-space:nowrap;">CARGA VIVA TOTAL</span>',
    1
)
c = c.replace(
    '<span id="r_losa_cv_total" style="color:var(--bad);font-size:15px;font-weight:900;">—</span>',
    '<span id="r_losa_cv_total" style="color:var(--accent2);font-size:15px;font-weight:900;">—</span>',
    1
)
c = c.replace(
    '<span class="rv" id="r_losa_cv" style="color:var(--bad);font-weight:700;">—</span>',
    '<span class="rv" id="r_losa_cv" style="color:var(--accent2);font-weight:700;">—</span>',
    1
)
# Fix input section color too
c = c.replace(
    '<span style="color:var(--bad)">&#9670;</span> Carga Viva &mdash; NEC-SE-CG 2015',
    '<span style="color:var(--accent2)">&#9670;</span> Carga Viva &mdash; NEC-SE-CG 2015',
    1
)

# 2. Fix JS: make sure CV is read correctly and valores se muestran
# The current JS code might have wrong function name or not finding element
# Replace the CV JS block entirely
old_cv_js = """      // Carga Viva NEC-15
      const cvSel = document.getElementById('losa_cv');
      const cv_val = parseFloat(cvSel ? cvSel.value : 0.200);
      const cv_uso = cvSel ? cvSel.options[cvSel.selectedIndex].text : 'Vivienda';
      setResult('r_losa_cv', cv_val, 2);
      setResult('r_losa_cv_total', cv_val, 2);
      const usoEl = document.getElementById('r_losa_uso_txt');
      if (usoEl) usoEl.textContent = cv_uso;"""

new_cv_js = """      // Carga Viva NEC-15
      const cvSel = document.getElementById('losa_cv');
      const cv_val = cvSel ? parseFloat(cvSel.value) : 0.200;
      const cv_uso = cvSel ? cvSel.options[cvSel.selectedIndex].text : 'Vivienda / Departamentos';
      const cvEl = document.getElementById('r_losa_cv');
      if (cvEl) cvEl.textContent = cv_val.toFixed(2);
      const cvTotEl = document.getElementById('r_losa_cv_total');
      if (cvTotEl) cvTotEl.textContent = cv_val.toFixed(2);
      const usoEl = document.getElementById('r_losa_uso_txt');
      if (usoEl) usoEl.textContent = cv_uso;"""

c = c.replace(old_cv_js, new_cv_js, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('CV fixed OK')
