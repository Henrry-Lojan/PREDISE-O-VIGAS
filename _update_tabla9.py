path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update the select options with Gimnasios and more accurate Tabla 9 values
old_select = '''            <select id="losa_cv" onchange="recalcLosa()">
              <option value="0.200">Vivienda / Departamentos</option>
              <option value="0.240">Oficinas</option>
              <option value="0.300">Aulas / Escuelas</option>
              <option value="0.300">Corredores (resid.)</option>
              <option value="0.300">Escaleras</option>
              <option value="0.300">Garajes (< 4 t)</option>
              <option value="0.480">Salas de reuni\u00f3n</option>
              <option value="0.290">Biblioteca - lectura</option>
              <option value="0.720">Biblioteca - dep\u00f3sito</option>
              <option value="0.200">Hospital - salas</option>
              <option value="0.380">Hospital - corredores</option>
              <option value="0.200">Hotel - cuartos</option>
              <option value="0.380">Hotel - corredores</option>
              <option value="0.480">Comercial planta baja</option>
              <option value="0.360">Comercial plantas sup.</option>
              <option value="0.180">Cubierta accesible</option>
              <option value="0.070">Cubierta no accesible</option>
            </select>'''

new_select = '''            <select id="losa_cv" onchange="recalcLosa()">
              <option value="0.200">Vivienda / Departamentos</option>
              <option value="0.240">Oficinas</option>
              <option value="0.480">Gimnasios / \u00c1reas de baile</option>
              <option value="0.480">\u00c1reas de reuni\u00f3n / Teatros</option>
              <option value="0.480">Comercial (Primer piso)</option>
              <option value="0.360">Comercial (Pisos sup.)</option>
              <option value="0.300">Escuelas (Aulas)</option>
              <option value="0.480">Escuelas (Corredores p. sup)</option>
              <option value="0.300">Garajes (Livianos < 4t)</option>
              <option value="0.180">Cubierta accesible (Terrazas)</option>
              <option value="0.070">Cubierta no accesible</option>
              <option value="0.480">Balcones</option>
            </select>'''

c = c.replace(old_select, new_select, 1)

# 2. Update the reference line to mention Tabla 9
old_ref = '''(Cap\u00edtulo 1, Tabla 1 - NEC-SE-CG 2015)'''
new_ref = '''(Secci\u00f3n 4.2 - Tabla 9 - NEC-SE-CG 2015)'''

c = c.replace(old_ref, new_ref, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated to Tabla 9 with Gimnasios OK')
