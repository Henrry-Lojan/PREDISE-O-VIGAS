path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

old_code = "try { loadAllData(); initSync(); } catch(e) { console.error('Error loading data', e); }"
new_code = "try { loadAllData(); } catch(e) { console.error('Error loading data', e); } \\n          try { initSync(); } catch(e) { console.error('Error initSync', e); }"

c = c.replace(old_code, new_code)
with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("initSync isolated")
