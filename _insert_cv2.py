path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Insert CV JS block between line 449 and 450 (0-indexed: after line index 448)
cv_js = """
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
"""

# Insert after line 449 (index 448, content "       }\r\n")
new_lines = lines[:449] + [cv_js] + lines[449:]

# Also add 'change' event listener after the 'input' one (line 451, index 450)
# Find the listener line and duplicate it with 'change'
result = []
for i, l in enumerate(new_lines):
    result.append(l)
    if "querySelectorAll('[id^=losa_]').forEach(el => el.addEventListener('input', recalcLosa))" in l:
        result.append("     document.querySelectorAll('[id^=losa_]').forEach(el => el.addEventListener('change', recalcLosa));\n")

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(result)

print('CV JS inserted OK at line 449')
