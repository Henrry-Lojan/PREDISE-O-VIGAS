path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Simplify title to just '25 cm'
# Searching for the exact string to be safe
old_vlbl = 'vlbl.innerHTML = `<span style="color:var(--accent);font-weight:bold;font-size:13px">Losa Alivianada (Hl = ${hl} cm)</span>'
new_vlbl = 'vlbl.innerHTML = `<span style="color:var(--accent);font-weight:bold;font-size:14px">${hl} cm</span>'

# 2. Add font-size:11px to labels to prevent wrapping
old_span2 = '<span style="display:inline-block;margin-top:4px">Nervio:'
new_span2 = '<span style="display:inline-block;margin-top:4px;font-size:11px">Nervio:'

if old_vlbl in c:
    c = c.replace(old_vlbl, new_vlbl, 1)
    c = c.replace(old_span2, new_span2, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('OK')
else:
    print('NOT FOUND')
