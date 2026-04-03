path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Lower Yc result font size a bit too
old_yc = 'font-size:14px"></span>'
new_yc = 'font-size:13px"></span>'
c = c.replace(old_yc, new_yc, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Yc font size lowered OK')
