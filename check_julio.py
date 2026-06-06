import re
with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Find ALL Julio Rodriguez occurrences and show their full card
print("All 'Julio Rodr' cards in your file:\n")
for m in re.finditer(r"\{id:'[^']*'[^{]*?Julio Rodr[^}]*?\}", code):
    seg = m.group(0)
    pos = re.search(r"position:'([^']+)'", seg)
    elig = re.search(r"eligiblePositions:\[([^\]]+)\]", seg)
    print(f"  position: {pos.group(1) if pos else '?'}")
    print(f"  eligible: {elig.group(1) if elig else '?'}")
    print(f"  raw: {seg[:160]}")
    print()

# Count mismatches that remain
bad = []
for m in re.finditer(r"name:\"([^\"]+)\"[^}]*?position:'([^']+)',eligiblePositions:\[([^\]]+)\]", code):
    name, pos = m.group(1), m.group(2)
    elig = [e.strip().strip("'") for e in m.group(3).split(',')]
    if elig in (['SP'],['RP']): continue
    if pos not in elig: bad.append((name,pos,elig))
print(f"Cards still mismatched: {len(bad)}")
for n,p,e in bad[:15]:
    print(f"  {n}: shows '{p}', eligible {e}")
