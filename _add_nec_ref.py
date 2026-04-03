path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Add reference section below the select in the input-group
old_cv_end = '            </select>\n          </div></div>\n        </div>'
new_cv_end = '''            </select>
          </div></div>
          <div style="font-size:10px; color:var(--muted); margin-top:10px; padding:8px; background:rgba(255,255,255,0.03); border-radius:4px; border-left:2px solid var(--accent2);">
            <div style="color:var(--accent2); font-weight:bold; margin-bottom:4px; font-size:9px; letter-spacing:0.5px; text-transform:uppercase;">Extracto NEC-SE-CG (Cargas Vivas)</div>
            <table style="width:100\u0025; border-collapse:collapse; line-height:1.4;">
              <tr><td style="padding:1px 0;">Vivienda / Dormitorios</td><td style="text-align:right;">2.0 kN/m\u00b2 (0.20 t/m\u00b2)</td></tr>
              <tr><td style="padding:1px 0;">Oficinas</td><td style="text-align:right;">2.4 kN/m\u00b2 (0.24 t/m\u00b2)</td></tr>
              <tr><td style="padding:1px 0;">Aulas / Escuelas</td><td style="text-align:right;">3.0 kN/m\u00b2 (0.30 t/m\u00b2)</td></tr>
              <tr><td style="padding:1px 0;">Comercios (Plantas Altas)</td><td style="text-align:right;">3.6 kN/m\u00b2 (0.36 t/m\u00b2)</td></tr>
              <tr><td style="padding:1px 0;">Garajes (Veh\u00edculos < 4t)</td><td style="text-align:right;">3.0 kN/m\u00b2 (0.30 t/m\u00b2)</td></tr>
            </table>
          </div>
        </div>'''

if old_cv_end in c:
    c = c.replace(old_cv_end, new_cv_end, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('NEC Reference added OK')
else:
    print('NOT FOUND')
