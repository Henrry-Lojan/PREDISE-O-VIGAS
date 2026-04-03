path = r'D:\Users\USUARIO 2023\Desktop\INTERFAZ\make_unified.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. We need to find the Sync JS block and wrap it in a function.
old_sync = """      // --- SYNCHRONIZE INPUTS ACROSS TABS ---
      const syncClasses = ['sync-L1', 'sync-L2', 'sync-L3', 'sync-L4', 'sync-pisos', 'sync-He', 'sync-uso'];
      syncClasses.forEach(cls => {"""

new_sync = """      // --- SYNCHRONIZE INPUTS ACROSS TABS ---
      function initSync() {
          const syncClasses = ['sync-L1', 'sync-L2', 'sync-L3', 'sync-L4', 'sync-pisos', 'sync-He', 'sync-uso'];
          syncClasses.forEach(cls => {"""

# Also need to close the `initSync()` function.
old_sync_end = """              el.addEventListener('change', handleSync);
          });
      });"""

new_sync_end = """              el.addEventListener('change', handleSync);
          });
      });
      } // end initSync
"""

c = c.replace(old_sync, new_sync)
c = c.replace(old_sync_end, new_sync_end)

# 2. Add `initSync()` to `window.onload`
old_onload = "try { loadAllData(); } catch(e) { console.error('Error loading data', e); }"
new_onload = "try { loadAllData(); initSync(); } catch(e) { console.error('Error loading data', e); }"
c = c.replace(old_onload, new_onload)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Sync fixed!")
