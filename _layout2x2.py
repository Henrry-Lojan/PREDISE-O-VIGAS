path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

def extract_card(text, start_idx):
    depth = 0
    i = start_idx
    while i < len(text):
        if text[i:i+4] == '<div':
            depth += 1
            i += 4
        elif text[i:i+6] == '</div>':
            depth -= 1
            i += 6
            if depth == 0:
                return text[start_idx:i], i
        else:
            i += 1
    return text[start_idx:], len(text)

# Use text patterns that are unique and present in file
marker_A = 'Predimensionamiento de Losa'
marker_B = 'lbl_losa_graf_title'
marker_C = 'Peso del hormig\u00f3n'         # "Peso del hormigón"
marker_D = 'Cargas Muertas Adicionales y Totales'
marker_E = 'Inercia Teorema Steiner'

def find_card_start(text, marker):
    idx = text.index(marker)
    # Walk back to find the opening <div
    i = idx
    while i >= 0:
        if text[i:i+4] == '<div':
            return i
        i -= 1
    return 0

idx_A = find_card_start(content, marker_A)
card_A, end_A = extract_card(content, idx_A)

idx_B = find_card_start(content, marker_B)
card_B, end_B = extract_card(content, idx_B)

idx_C = find_card_start(content, marker_C)
card_C, end_C = extract_card(content, idx_C)

# For D, start search after C ends to avoid potential duplicates
idx_D_text = content.index(marker_D, end_C)
idx_D = find_card_start(content, marker_D)   # safe since unique
card_D, end_D = extract_card(content, idx_D)

idx_E = find_card_start(content, marker_E)
card_E, end_E = extract_card(content, idx_E)

print(f'A:{idx_A}-{end_A}')
print(f'B:{idx_B}-{end_B}')
print(f'C:{idx_C}-{end_C}')
print(f'D:{idx_D}-{end_D}')
print(f'E:{idx_E}-{end_E}')

# Validate order: A < B < C < D < E
assert idx_A < idx_B < idx_C < idx_D < idx_E, f'Order mismatch! {idx_A} {idx_B} {idx_C} {idx_D} {idx_E}'

# Build new 2-column grid
new_layout = (
    '        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:start;">\n'
    '          <div style="display:flex;flex-direction:column;gap:8px;">\n'
    + card_A + '\n'
    + card_C + '\n'
    + '          </div>\n'
    + '          <div style="display:flex;flex-direction:column;gap:8px;">\n'
    + card_D + '\n'
    + card_B + '\n'
    + '          </div>\n'
    + '        </div>\n'
    + card_E + '\n'
)

new_content = content[:idx_A] + new_layout + content[end_E:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('2x2 grid OK')
