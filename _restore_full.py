path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find losa_results block and replace it entirely
start_marker = 'losa_results = """\n'
end_marker = '"""\n\nlosa_js'

start_idx = content.index(start_marker) + len(start_marker)
end_idx = content.index(end_marker)

restored_html = r"""        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:start;">
          <!-- Col izquierda: Predimensionamiento + Peso Hormigon -->
          <div style="display:flex;flex-direction:column;gap:8px;">
         <div class="mini-card diagram-mini">
           <div class="mini-header"><span style="color:var(--accent)">&#9658;</span> Predimensionamiento de Losa</div>
           <div class="mini-body" style="padding:15px;">
              <div style="display:flex;gap:10px;">
                 <div id="dcIndicator_losa" style="flex:1;background:rgba(0,229,255,0.1);border:1px solid rgba(0,229,255,0.3);border-radius:8px;padding:10px;text-align:center;margin-bottom:15px;">
                   <div style="font-size:24px;font-weight:700;font-family:var(--sans);" id="r_losa_hmin">—</div>
                   <div style="font-size:10px;color:var(--muted);margin-top:4px;letter-spacing:0.1em">ESPESOR MINIMO CALC. (cm)</div>
                 </div>
                 <div id="status_losa_check" style="flex:1;background:rgba(255,184,48,0.1);border:1px solid rgba(255,184,48,0.3);border-radius:8px;padding:10px;text-align:center;margin-bottom:15px;">
                   <div style="font-size:14px;font-weight:700;font-family:var(--sans);margin-top:5px" id="r_losa_ok">—</div>
                   <div style="font-size:10px;color:var(--muted);margin-top:4px;letter-spacing:0.1em">CHEQUEO ESPESOR</div>
                 </div>
              </div>
             <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_lmax" data-eq-title="Luz M\u00e1xima" data-eq-body="\\text{M\u00e1xima luz entre L1, L2, L3 y L4}">Luz M\u00e1xima Arquitect\u00f3nica (Lm\u00e1x)</span><span class="rv" id="r_losa_lmax">—</span><span class="ru">m</span></div>
             <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_lreal" data-eq-title="Luz C\u00e1lculo" data-eq-body="L_{real} = \\frac{L_{m\\acute{a}x}}{V_{int} + 1}">Luz Efectiva de C\u00e1lculo (Lreal)</span><span class="rv accent-v" id="r_losa_lreal">—</span><span class="ru">m</span></div>
             <div class="mini-sep"></div>
             <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_imin" data-eq-title="Inercia M\u00ednima Requerida" data-eq-body="I_{min} = \\frac{100 \\cdot h_{min}^3}{12}">Inercia m\u00ednima requerida de losa maciza (1m)</span><span class="rv" id="r_losa_imin">—</span><span class="ru">cm4</span></div>
             <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_isteiner" data-eq-title="Inercia Alivianada (Steiner)" data-eq-body="I_{total} = \\sum I_{individuales}">Inercia de la losa alivianada de espesor — cm</span><span class="rv accent-v" id="r_losa_isteiner">—</span><span class="ru">cm4</span></div>
             <div class="mini-sep"></div>
             <div class="mini-row" style="text-align:left;"><span class="rl clickable-label" id="lbl_losa_heq" data-eq-title="Altura Equivalente Losa Maciza" data-eq-body="H_{eq} = \\left( \\frac{12 \\cdot I_t}{100} \\right)^{1/3}">Altura losa maciza equiv. (Heq)</span><span class="rv accent-v" id="r_losa_heq">—</span><span class="ru">cm</span></div>
             <div class="mini-row" style="text-align:left;"><span class="rl clickable-label" id="lbl_losa_lmaxperm" data-eq-title="Longitud M\u00e1x Permitida" data-eq-body="L_{m\\acute{a}x\\,perm} = \\frac{H_{eq}}{0.03 \\cdot 100}">Longitud m\u00e1xima para una losa de — cm</span><span class="rv accent-v" id="r_losa_lmaxperm">—</span><span class="ru">m</span></div>
           </div>
         </div>
         <div class="mini-card">
           <div class="mini-header"><span style="color:var(--accent2)">&#9658;</span> Peso del hormig\u00f3n</div>
           <div class="mini-body">
             <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_vtot" data-eq-title="Vol. Total" data-eq-body="V_{tot} = \\frac{100 \\times 100}{10000} \\times \\frac{Hl}{100}" style="white-space:nowrap">Volumen total en funci\u00f3n de geometr\u00eda</span><span class="rv" id="r_losa_vtot">—</span><span class="ru">m\u00b3</span></div>
             <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_vbloq" data-eq-title="Vol. Bloques" data-eq-body="V_{bloq} = \\frac{bb^2 \\times (Hl-tc) \\times 4}{10^6}" style="white-space:nowrap">Volumen del bloque en funci\u00f3n de geometr\u00eda</span><span class="rv" id="r_losa_vbloq">—</span><span class="ru">m\u00b3</span></div>
             <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_vhorm" data-eq-title="Vol. Hormig\u00f3n" data-eq-body="V_{horm} = V_{tot} - V_{bloq}" style="white-space:nowrap">Volumen del hormig\u00f3n</span><span class="rv" id="r_losa_vhorm">—</span><span class="ru">m\u00b3</span></div>
             <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_peso" data-eq-title="Peso Hormig\u00f3n" data-eq-body="P_{h} = V_{horm} \\times 2.4" style="white-space:nowrap">Peso hormig\u00f3n (\u03b3 = 2.4 t/m\u00b3)</span><span class="rv" id="r_losa_peso">—</span><span class="ru">t</span></div>
             <div class="mini-row"><span class="rl clickable-label" id="lbl_losa_area" data-eq-title="\u00c1rea" data-eq-body="A = \\frac{100 \\times 100}{10000}" style="white-space:nowrap">\u00c1rea unitaria</span><span class="rv" id="r_losa_area">—</span><span class="ru">m\u00b2</span></div>
             <div class="mini-sep"></div>
             <div class="mini-row"><span class="rl" style="color:var(--accent3);font-weight:700;white-space:nowrap">CARGA MUERTA DE LA LOSA</span><span class="rv accent-v" id="r_losa_phorm_final">—</span><span class="ru">t/m\u00b2</span></div>
           </div>
         </div>
          </div>
          <!-- Col derecha: Cargas Muertas + Diagrama Losa -->
          <div style="display:flex;flex-direction:column;gap:8px;">
         <div class="mini-card diagram-mini">
           <div class="mini-header"><span style="color:var(--warn)">&#9658;</span> Cargas Muertas Adicionales y Totales</div>
           <div class="mini-body" style="padding:15px;">
             <div class="mini-row"><span class="rl" id="lbl_losa_cpared" style="white-space:nowrap">Paredes / Tabiquer\u00eda equivalentes</span><span class="rv" id="r_losa_cpared">—</span><span class="ru">t/m\u00b2</span></div>
             <div class="mini-row"><span class="rl" id="lbl_losa_caliv" style="white-space:nowrap">Alivianador de losa</span><span class="rv" id="r_losa_caliv">—</span><span class="ru">t/m\u00b2</span></div>
             <div class="mini-row"><span class="rl" style="white-space:nowrap">Masillado</span><span class="rv" id="r_losa_cmasillado">—</span><span class="ru">t/m\u00b2</span></div>
             <div class="mini-row"><span class="rl" style="white-space:nowrap">Acabados</span><span class="rv" id="r_losa_cacabados">—</span><span class="ru">t/m\u00b2</span></div>
             <div class="mini-row"><span class="rl" style="white-space:nowrap">Instalaciones</span><span class="rv" id="r_losa_cinstal">—</span><span class="ru">t/m\u00b2</span></div>
             <div class="mini-sep"></div>
             <div class="mini-row"><span class="rl" style="color:var(--accent2);font-weight:700;white-space:nowrap">CARGAS MUERTAS INSTALACIONES</span><span class="rv" id="r_losa_csuper">—</span><span class="ru">t/m\u00b2</span></div>
             <div class="mini-row"><span class="rl" style="color:var(--accent2);font-weight:700;white-space:nowrap">CARGA MUERTA LOSA</span><span class="rv" id="r_losa_cmlosa">—</span><span class="ru">t/m\u00b2</span></div>
             <div class="mini-sep"></div>
             <div class="mini-row"><span class="rl" style="color:var(--warn);font-weight:800;font-size:13px;white-space:nowrap">CARGA MUERTA TOTAL</span><span class="rv" style="color:var(--warn);font-size:15px" id="r_losa_cm_total">—</span><span class="ru">t/m\u00b2</span></div>
             <div style="font-size:10px; color:var(--muted); text-align:right; margin-top:4px;">* Suma transferida din\u00e1micamente al m\u00f3dulo Vigas</div>
           </div>
         </div>
         <div class="mini-card diagram-mini">
           <div class="mini-header"><span style="color:var(--accent)">&#9658;</span> <span id="lbl_losa_graf_title">LOSA ALIVIANADA DE — CM</span></div>
           <div class="mini-body" style="padding:15px; text-align:center;">
              <div style="background:rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.08); border-radius:6px; padding:25px 15px 15px 15px; margin-bottom:15px; position:relative;">
                 <div style="display:flex; align-items:center;">
                    <div style="display:flex; flex-direction:column; justify-content:center; align-items:center; border-left:1px solid rgba(255,255,255,0.3); padding-left:5px; margin-right:15px; position:relative;" id="dib_h_cota">
                       <div style="border-top:1px solid rgba(255,255,255,0.3); width:5px; position:absolute; top:0; left:0;"></div>
                       <div style="font-size:10px; color:var(--muted); font-weight:bold; writing-mode:vertical-rl; transform:rotate(180deg); letter-spacing:0.05em; white-space:nowrap;" id="dib_h_val">Hl = 25 cm</div>
                       <div style="border-bottom:1px solid rgba(255,255,255,0.3); width:5px; position:absolute; bottom:0; left:0;"></div>
                    </div>
                    <div style="flex:1;">
                       <div style="display:flex; width:100%; border-bottom:1px solid rgba(255,255,255,0.3); margin-bottom:2px; position:relative;">
                          <div style="position:absolute; top:-16px; width:100%; text-align:center; font-size:10px; color:var(--muted); font-weight:bold; letter-spacing:0.05em;">ANCHO DE AN\u00c1LISIS = 1.00 m</div>
                          <div style="border-left:1px solid rgba(255,255,255,0.3); height:5px; position:absolute; left:0; bottom:0;"></div>
                          <div style="border-right:1px solid rgba(255,255,255,0.3); height:5px; position:absolute; right:0; bottom:0;"></div>
                       </div>
                       
                       <div id="dib_tabla" style="background:var(--accent); width:100%; height:15px; border-radius:2px 2px 0 0; display:flex; align-items:center; justify-content:center; color:rgba(0,0,0,0.7); font-size:11px; font-weight:800; letter-spacing:0.05em;">
                          Tabla de compresi\u00f3n
                       </div>
                       <div id="dib_nervios_container" style="display:flex; width:100%; justify-content:flex-start;">
                          <!-- JS injected webs -->
                       </div>
                    </div>
                 </div>
                 <div id="dib_labels" style="margin-top:15px; font-size:12px; color:var(--text); font-family:var(--sans); background:rgba(0,229,255,0.05); padding:8px; border-radius:4px; border:1px solid rgba(0,229,255,0.2);"></div>
              </div>
           </div>
         </div>
          </div>
        </div>
        <div class="mini-card diagram-mini">
          <div class="mini-header"><span style="color:var(--accent)">&#9658;</span> Inercia Teorema Steiner (1m)</div>
          <div class="mini-body" style="padding:10px;">
             <table style="width:100%; text-align:right; font-size:12px; border-collapse:collapse; margin-top:5px;">
               <thead>
                 <tr style="border-bottom:1px solid rgba(255,255,255,0.1); color:var(--muted);">
                   <th style="padding-bottom:5px;text-align:center">Pieza</th>
                   <th style="padding-bottom:5px">A</th>
                   <th style="padding-bottom:5px">y</th>
                   <th style="padding-bottom:5px">Ay</th>
                   <th style="padding-bottom:5px">Io</th>
                   <th style="padding-bottom:5px">d\u00b2</th>
                   <th style="padding-bottom:5px; color:var(--accent)">It</th>
                 </tr>
               </thead>
               <tbody id="tb_steiner" style="color:var(--text);">
                 <!-- JS -->
               </tbody>
               <tfoot>
                 <tr style="border-top:1px solid rgba(255,255,255,0.1); font-weight:700;">
                   <td style="padding-top:5px;text-align:center;color:var(--accent2)">\u2211</td>
                   <td id="st_A_tot" style="padding-top:5px"></td>
                   <td style="padding-top:5px"></td>
                   <td id="st_Ay_tot" style="padding-top:5px"></td>
                   <td style="padding-top:5px"></td>
                   <td style="padding-top:5px"></td>
                   <td id="st_It_tot" style="padding-top:5px; color:var(--accent)"></td>
                 </tr>
               </tfoot>
             </table>
             <div style="font-size:11px; color:var(--muted); text-align:right; margin-top:15px; border-top:1px dashed rgba(255,255,255,0.1); padding-top:8px;">
               Centroide Real (Yc) = <span id="st_Yc" style="color:var(--text);font-weight:700;font-size:14px"></span> cm
             </div>
          </div>
        </div>
"""

new_content = content[:start_idx] + restored_html + content[end_idx:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('losa_results fully restored and 2x2 layout applied OK')
