path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the previous block with a simple native-style reference
old_ref_block = '''          <div style="font-size:10px; color:var(--muted); margin-top:10px; padding:8px; background:rgba(255,255,255,0.03); border-radius:4px; border-left:2px solid var(--accent2);">
            <div style="color:var(--accent2); font-weight:bold; margin-bottom:4px; font-size:9px; letter-spacing:0.5px; text-transform:uppercase;">Extracto NEC-SE-CG (Cargas Vivas)</div>
            <table style="width:100%; border-collapse:collapse; line-height:1.4;">
              <tr><td style="padding:1px 0;">Vivienda / Dormitorios</td><td style="text-align:right;">2.0 kN/m² (0.20 t/m²)</td></tr>
              <tr><td style="padding:1px 0;">Oficinas</td><td style="text-align:right;">2.4 kN/m² (0.24 t/m²)</td></tr>
              <tr><td style="padding:1px 0;">Aulas / Escuelas</td><td style="text-align:right;">3.0 kN/m² (0.30 t/m²)</td></tr>
              <tr><td style="padding:1px 0;">Comercios (Plantas Altas)</td><td style="text-align:right;">3.6 kN/m² (0.36 t/m²)</td></tr>
              <tr><td style="padding:1px 0;">Garajes (Vehículos < 4t)</td><td style="text-align:right;">3.0 kN/m² (0.30 t/m²)</td></tr>
            </table>
          </div>'''

new_ref_line = '''          <div style="font-size:10px; color:var(--muted); text-align:right; margin-top:5px; opacity:0.8;">(Cap\u00edtulo 1, Tabla 1 - NEC-SE-CG 2015)</div>'''

if old_ref_block in c:
    c = c.replace(old_ref_block, new_ref_line, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('Simplified NEC Reference applied OK')
else:
    print('NOT FOUND')
