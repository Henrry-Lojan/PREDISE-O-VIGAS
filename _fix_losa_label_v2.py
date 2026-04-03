path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Change title back to descriptive but formatted
old_vlbl = 'vlbl.innerHTML = `<span style="color:var(--accent);font-weight:bold;font-size:14px">${hl} cm</span>'
new_vlbl = 'vlbl.innerHTML = `<span style="color:var(--accent);font-weight:bold;font-size:13px">Losa alivianada de ${hl} cm</span>'

if old_vlbl in c:
    c = c.replace(old_vlbl, new_vlbl, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('OK')
else:
    print('NOT FOUND')
