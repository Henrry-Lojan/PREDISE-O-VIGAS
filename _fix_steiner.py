path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

old = '        <div class="mini-card diagram-mini">\n          <div class="mini-header"><span style="color:var(--accent)">&#9658;</span> Inercia Teorema Steiner'
new = '        <div class="mini-card">\n          <div class="mini-header"><span style="color:var(--accent)">&#9658;</span> Inercia Teorema Steiner'

if old in c:
    c = c.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('OK')
else:
    print('NOT FOUND, searching...')
    idx = c.find('Inercia Teorema Steiner')
    print(repr(c[idx-150:idx+50]))
