path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Wrap lines 134-161 (0-indexed 133-160) in a 2-column flex row
# Card 1: lines 134-145 (0-indexed 133-144)
# Card 2: lines 146-161 (0-indexed 145-160)

card1 = lines[133:145]   # "Peso del hormigon" card
card2 = lines[145:161]   # "Cargas Muertas Adicionales" card

# We'll wrap them in a flex row container, each taking 50%
# Reduce font size a bit to help fit
def shrink(lines_list):
    result = []
    for l in lines_list:
        # Remove outer indentation of 8 spaces, add inside wrapper
        result.append(l)
    return result

wrapper = (
    '        <div style="display:flex;gap:8px;align-items:stretch;">\n'
    '          <div style="flex:1;min-width:0;">\n'
)
mid = (
    '          </div>\n'
    '          <div style="flex:1;min-width:0;">\n'
)
close_wrapper = (
    '          </div>\n'
    '        </div>\n'
)

new_block = [wrapper] + card1 + [mid] + card2 + [close_wrapper]

new_lines = lines[:133] + new_block + lines[161:]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Side-by-side applied OK')
