path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

old = "wToDraw >= 15 ? 'Bloque (' + bb + ' cmX' + hw + 'cm)' : ''"
new = "wToDraw >= 15 ? 'Bloque<br>(' + bb + 'x' + hw + 'cm)' : ''"

# Also need to allow HTML in the div — change display to block and text-align center
# The div already has display:flex and align-items:center so <br> should work
# but we need flex-direction:column for line break to work visually
old2 = "display:flex; justify-content:center; align-items:center; height:${h_hw}px;\">"
new2 = "display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; height:${h_hw}px;\">"

c = c.replace(old, new, 1)
c = c.replace(old2, new2, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('OK')
