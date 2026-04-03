path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Lower the table font size from 12px to 11px
old_table = '<table style="width:100%; text-align:right; font-size:12px; border-collapse:collapse; margin-top:5px;">'
new_table = '<table style="width:100%; text-align:right; font-size:11px; border-collapse:collapse; margin-top:5px;">'
c = c.replace(old_table, new_table, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Table font size lowered OK')
