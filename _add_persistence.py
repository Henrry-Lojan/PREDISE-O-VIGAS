path = r'D:\Users\USUARIO%202023\Desktop\INTERFAZ\make_unified.py'
import re

# We will add a persistence script to the tabs_html or a separate js block
with open(r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py', 'r', encoding='utf-8') as f:
    c = f.read()

persistence_js = """
      // --- PERSISTENCIA DE DATOS (LocalStorage) ---
      function saveAllData() {
        const data = {};
        document.querySelectorAll('input, select').forEach(el => {
          if (el.id) data[el.id] = el.value;
        });
        localStorage.setItem('structural_suite_data', JSON.stringify(data));
      }

      function loadAllData() {
        const saved = localStorage.getItem('structural_suite_data');
        if (!saved) return;
        const data = JSON.parse(saved);
        Object.keys(data).forEach(id => {
          const el = document.getElementById(id);
          if (el) {
            el.value = data[id];
            // Trigger UI styling for specialized elements if they were active
            if (el.tagName === 'INPUT' && el.style.backgroundColor) {
               // optional: handle highlighting here if needed
            }
          }
        });
      }

      // Add persistence triggers
      document.addEventListener('input', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {
          saveAllData();
        }
      });
      document.addEventListener('change', (e) => {
        if (e.target.tagName === 'SELECT') {
          saveAllData();
        }
      });
"""

# Inject persistence_js inside the script tag of tabs_html or anywhere global
# Let's put it in tabs_html script block
old_tabs_script = "function openTab(tabId, btn) {"
new_tabs_script = persistence_js + "\\n      function openTab(tabId, btn) {"

c = c.replace(old_tabs_script, new_tabs_script)

# Modify window.onload to load data BEFORE recalcs
old_onload = """      window.onload = function() {
          if (originalOnload) originalOnload();
          recalcLosa();
          recalcCol();
          recalcSis();
      };"""

new_onload = """      window.onload = function() {
          if (originalOnload) originalOnload();
          try { loadAllData(); } catch(e) { console.error('Error loading data', e); }
          recalcLosa();
          if (typeof recalc === 'function') recalc(); // Vigas
          recalcCol();
          recalcSis();
      };"""

c = c.replace(old_onload, new_onload)

with open(r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py', 'w', encoding='utf-8') as f:
    f.write(c)

print('Persistence system added OK')
