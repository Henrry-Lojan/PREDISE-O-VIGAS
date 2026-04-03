path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Make the 2-column inner grid span full width of the parent grid
old_grid = '        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:start;">'
new_grid = '        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:start;grid-column:1/-1;">'
c = c.replace(old_grid, new_grid, 1)

# Also make the Steiner card span full width
old_steiner = '        <div class="mini-card">\n          <div class="mini-header"><span style="color:var(--accent)">&#9658;</span> Inercia Teorema Steiner'
new_steiner = '        <div class="mini-card" style="grid-column:1/-1;">\n          <div class="mini-header"><span style="color:var(--accent)">&#9658;</span> Inercia Teorema Steiner'
c = c.replace(old_steiner, new_steiner, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('OK')
