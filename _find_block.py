path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the combined card start (the line with 'ANÁLISIS DE CARGAS MUERTAS')
start_idx = None
end_idx = None
for i, l in enumerate(lines):
    if 'ANÁLISIS DE CARGAS MUERTAS' in l or 'AN\u00c1LISIS DE CARGAS MUERTAS' in l:
        # Search backwards to find the opening div
        for j in range(i, max(i-5, 0), -1):
            if '<div class="mini-card"' in lines[j]:
                start_idx = j
                break
    if start_idx is not None and i > start_idx and '        </div>' in lines[i]:
        # Find the closing div at same level
        end_idx = i
        break

print(f'start={start_idx}, end={end_idx}')
if start_idx is not None and end_idx is not None:
    print('Lines to replace:')
    for i in range(start_idx, end_idx+1):
        print(f'{i+1}: {repr(lines[i][:80])}')
