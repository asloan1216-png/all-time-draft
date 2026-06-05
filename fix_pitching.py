# CRITICAL FIX: simulate() was filtering roster keys with uppercase 'SP'/'RP',
# but slots are stored lowercase ('sp1'..'sp5', 'rp1'..'rp4'). Result: the
# pitching staff was ALWAYS empty and every team allowed a flat ~4.22 RA/G
# regardless of which pitchers were drafted. This makes pitching actually count.

import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

old_sp = "const starters  = Object.entries(roster).filter(([k])=>k.startsWith('SP')).map(([,v])=>v).filter(Boolean);"
new_sp = "const starters  = Object.entries(roster).filter(([k])=>k.toLowerCase().startsWith('sp')).map(([,v])=>v).filter(Boolean);"
if old_sp in code:
    code = code.replace(old_sp, new_sp, 1)
    print("Fix 1: starters now correctly read from sp1-sp5 slots")
    fixes += 1
else:
    print("Fix 1: starters line NOT matched - checking...")
    m = re.search(r"const starters\s*=.*startsWith\('SP'\).*", code)
    if m: print("  Found:", m.group(0))

old_rp = "const relievers = Object.entries(roster).filter(([k])=>k.startsWith('RP')).map(([,v])=>v).filter(Boolean);"
new_rp = "const relievers = Object.entries(roster).filter(([k])=>k.toLowerCase().startsWith('rp')).map(([,v])=>v).filter(Boolean);"
if old_rp in code:
    code = code.replace(old_rp, new_rp, 1)
    print("Fix 2: relievers now correctly read from rp1-rp4 slots")
    fixes += 1
else:
    print("Fix 2: relievers line NOT matched - checking...")
    m = re.search(r"const relievers\s*=.*startsWith\('RP'\).*", code)
    if m: print("  Found:", m.group(0))

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\nTotal fixes: {fixes}/2")
if fixes == 2:
    print("SUCCESS — pitching now affects the simulation.")
print("Run: git add . && git commit -m 'CRITICAL: fix pitching staff being ignored in sim' && git push")
