path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# I will replace the entire initSync() JS with event delegation which is 100% fail-proof
old_sync_start = c.find("function initSync() {")
old_sync_end = c.find("} // end initSync", old_sync_start)
if old_sync_start > -1 and old_sync_end > -1:
    old_sync = c[old_sync_start:old_sync_end + len("} // end initSync")]
    
    new_sync = """
      // --- EVENT DELEGATION GLOBAL SYNC ---
      document.addEventListener('input', function(e) {
          const t = e.target;
          if (!t.classList) return;
          const cls = Array.from(t.classList).find(c => c.startsWith('sync-'));
          if (cls) {
              document.querySelectorAll('.' + cls).forEach(s => {
                  if (s !== t && s.value !== t.value) {
                      s.value = t.value;
                      s.style.backgroundColor = "rgba(0,229,255,0.2)";
                      setTimeout(() => s.style.backgroundColor = "", 500);
                      
                      const id = s.id;
                      if (id.startsWith('losa_')) { if(typeof recalcLosa === 'function') recalcLosa(); }
                      else if (id.startsWith('col_')) { if(typeof recalcCol === 'function') recalcCol(); }
                      else { if(typeof recalc === 'function') recalc(); }
                  }
              });
              if (cls === 'sync-uso') {
                  const cv_viga = document.getElementById('Cv');
                  if (cv_viga) {
                      cv_viga.value = t.value;
                      cv_viga.style.backgroundColor = "rgba(0,229,255,0.2)";
                      setTimeout(() => cv_viga.style.backgroundColor = "", 500);
                      if(typeof recalc === 'function') recalc();
                  }
                  
                  // Also manually sync it for CV in Losas
                  const elCv = document.getElementById('r_losa_cv');
                  const elCvTot = document.getElementById('r_losa_cv_total');
                  const elUso = document.getElementById('r_losa_uso_txt');
                  if (elCv) elCv.textContent = parseFloat(t.value).toFixed(2);
                  if (elCvTot) elCvTot.textContent = parseFloat(t.value).toFixed(2);
                  if (elUso && t.options) elUso.textContent = t.options[t.selectedIndex].text;
              }
          }
      });
      document.addEventListener('change', function(e) {
          // just trigger an input event to catch select changes
          if (e.target.tagName === 'SELECT' && Array.from(e.target.classList).find(c => c.startsWith('sync-'))) {
              e.target.dispatchEvent(new Event('input', {bubbles: true}));
          }
      });
"""
    c = c.replace(old_sync, new_sync)

# Remove `initSync();` completely, as it's no longer needed
c = c.replace("try { initSync(); }", "// delegated sync")

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Sync upgraded to Delegation!")
