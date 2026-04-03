path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Insert CV JS block just before the closing brace of recalcLosa (before line 450's "    }")
old_close = """       if (typeof recalc === 'function') recalc(); // Actualiza viga
       }
     }
     document.querySelectorAll('[id^=losa_]').forEach(el => el.addEventListener('input', recalcLosa));"""

new_close = """       if (typeof recalc === 'function') recalc(); // Actualiza viga
       }

      // === CARGA VIVA NEC-SE-CG 2015 ===
      const cvSel = document.getElementById('losa_cv');
      if (cvSel) {
        const cv_val = parseFloat(cvSel.value);
        const cv_uso = cvSel.options[cvSel.selectedIndex].text;
        const elCv = document.getElementById('r_losa_cv');
        const elCvTot = document.getElementById('r_losa_cv_total');
        const elUso = document.getElementById('r_losa_uso_txt');
        if (elCv) elCv.textContent = cv_val.toFixed(2);
        if (elCvTot) elCvTot.textContent = cv_val.toFixed(2);
        if (elUso) elUso.textContent = cv_uso;
      }
     }
     document.querySelectorAll('[id^=losa_]').forEach(el => el.addEventListener('input', recalcLosa));
     document.querySelectorAll('[id^=losa_]').forEach(el => el.addEventListener('change', recalcLosa));"""

if old_close in c:
    c = c.replace(old_close, new_close, 1)
    print('Replaced OK')
else:
    print('NOT FOUND - searching...')
    idx = c.find('if (typeof recalc')
    print(repr(c[idx-20:idx+200]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
