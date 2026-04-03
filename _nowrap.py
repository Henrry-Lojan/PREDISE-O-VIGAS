path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the flex wrapper + both cards (lines 134-167)
# Use the unique opening tag of the wrapper as anchor
old_wrapper_start = '        <div style="display:flex;gap:8px;align-items:stretch;">\r\n          <div style="flex:1;min-width:0;">\r\n        <div class="mini-card">'
new_wrapper_start = '        <div style="display:flex;gap:8px;align-items:flex-start;flex-wrap:nowrap;">\r\n          <div style="flex:0 0 auto;">\r\n        <div class="mini-card">'

content = content.replace(old_wrapper_start, new_wrapper_start, 1)

# Change the mid-divider between the two cards
old_mid = '          </div>\r\n          <div style="flex:1;min-width:0;">\r\n        <div class="mini-card diagram-mini">'
new_mid  = '          </div>\r\n          <div style="flex:0 0 auto;">\r\n        <div class="mini-card diagram-mini">'

content = content.replace(old_mid, new_mid, 1)

# Add white-space:nowrap to .rl within the "Peso del hormigon" card labels
# These are the clickable-label spans — add nowrap style inline
old_vtot = 'id="lbl_losa_vtot" data-eq-title="Vol. Total" data-eq-body="V_{tot} = \\\\frac{100 \\\\times 100}{10000} \\\\times \\\\frac{Hl}{100}">Volumen total en funci\u00f3n de geometr\u00eda</span>'
new_vtot = 'id="lbl_losa_vtot" data-eq-title="Vol. Total" data-eq-body="V_{tot} = \\\\frac{100 \\\\times 100}{10000} \\\\times \\\\frac{Hl}{100}" style="white-space:nowrap">Volumen total en funci\u00f3n de geometr\u00eda</span>'
content = content.replace(old_vtot, new_vtot, 1)

old_vbloq = 'id="lbl_losa_vbloq" data-eq-title="Vol. Bloques" data-eq-body="V_{bloq} = \\\\frac{bb^2 \\\\times (Hl-tc) \\\\times 4}{10^6}">Volumen del bloque en funci\u00f3n de geometr\u00eda</span>'
new_vbloq = 'id="lbl_losa_vbloq" data-eq-title="Vol. Bloques" data-eq-body="V_{bloq} = \\\\frac{bb^2 \\\\times (Hl-tc) \\\\times 4}{10^6}" style="white-space:nowrap">Volumen del bloque en funci\u00f3n de geometr\u00eda</span>'
content = content.replace(old_vbloq, new_vbloq, 1)

old_vhorm = 'id="lbl_losa_vhorm" data-eq-title="Vol. Hormig\u00f3n" data-eq-body="V_{horm} = V_{tot} - V_{bloq}">Volumen del hormig\u00f3n</span>'
new_vhorm = 'id="lbl_losa_vhorm" data-eq-title="Vol. Hormig\u00f3n" data-eq-body="V_{horm} = V_{tot} - V_{bloq}" style="white-space:nowrap">Volumen del hormig\u00f3n</span>'
content = content.replace(old_vhorm, new_vhorm, 1)

old_peso_lbl = 'id="lbl_losa_peso" data-eq-title="Peso Hormig\u00f3n" data-eq-body="P_{h} = V_{horm} \\\\times 2.4">Peso del hormig\u00f3n en funci\u00f3n del peso espec\u00edfico</span>'
new_peso_lbl = 'id="lbl_losa_peso" data-eq-title="Peso Hormig\u00f3n" data-eq-body="P_{h} = V_{horm} \\\\times 2.4" style="white-space:nowrap">Peso hormig\u00f3n (\u03b3 = 2.4 t/m\u00b3)</span>'
content = content.replace(old_peso_lbl, new_peso_lbl, 1)

old_area_lbl = 'id="lbl_losa_area" data-eq-title="\u00c1rea" data-eq-body="A = \\\\frac{100 \\\\times 100}{10000}">El \u00c1rea</span>'
new_area_lbl = 'id="lbl_losa_area" data-eq-title="\u00c1rea" data-eq-body="A = \\\\frac{100 \\\\times 100}{10000}" style="white-space:nowrap">\u00c1rea unitaria</span>'
content = content.replace(old_area_lbl, new_area_lbl, 1)

# Add nowrap to the summary rows in card 1
old_cm_losa = '<span class="rl" style="color:var(--accent3);font-weight:700">CARGA MUERTA DE LA LOSA</span>'
new_cm_losa = '<span class="rl" style="color:var(--accent3);font-weight:700;white-space:nowrap">CARGA MUERTA DE LA LOSA</span>'
content = content.replace(old_cm_losa, new_cm_losa, 1)

# Add nowrap to all .rl spans in the second card (Cargas Muertas)
# The mini-body of card 2 starts with lbl_losa_cpared
# We replace just the inner spans systematically
for old, new in [
    ('<span class="rl" id="lbl_losa_cpared">',       '<span class="rl" id="lbl_losa_cpared" style="white-space:nowrap">'),
    ('<span class="rl" id="lbl_losa_caliv">',        '<span class="rl" id="lbl_losa_caliv" style="white-space:nowrap">'),
    ('<span class="rl">Masillado</span>',              '<span class="rl" style="white-space:nowrap">Masillado</span>'),
    ('<span class="rl">Acabados</span>',               '<span class="rl" style="white-space:nowrap">Acabados</span>'),
    ('<span class="rl">Instalaciones</span>',          '<span class="rl" style="white-space:nowrap">Instalaciones</span>'),
    ('<span class="rl" style="color:var(--accent2);font-weight:700">CARGAS MUERTAS INSTALACIONES</span>',
     '<span class="rl" style="color:var(--accent2);font-weight:700;white-space:nowrap">CARGAS MUERTAS INSTALACIONES</span>'),
    ('<span class="rl" style="color:var(--accent2);font-weight:700">CARGA MUERTA LOSA</span>',
     '<span class="rl" style="color:var(--accent2);font-weight:700;white-space:nowrap">CARGA MUERTA LOSA</span>'),
    ('<span class="rl" style="color:var(--warn);font-weight:800;font-size:13px">CARGA MUERTA TOTAL</span>',
     '<span class="rl" style="color:var(--warn);font-weight:800;font-size:13px;white-space:nowrap">CARGA MUERTA TOTAL</span>'),
]:
    content = content.replace(old, new, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('nowrap + flex auto applied OK')
