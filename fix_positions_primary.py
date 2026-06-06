# Fix stale primary-position labels. ~642 hitter cards had a `position` field
# (the headline label shown on the card) that wasn't even in their own
# eligiblePositions list — e.g. Julio Rodriguez showed "2B" but can only play
# CF/LF/RF, catchers like Javy Lopez showed "3B", etc. We earlier fixed the
# eligibility lists but never synced the display label.
#
# Fix: set each hitter card's `position` to the first non-DH entry of its own
# eligiblePositions. Pitchers (['SP'] / ['RP']) are left untouched.
import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

def fix(m):
    head, pos, elig = m.group(1), m.group(2), m.group(3)
    eligset = [e.strip().strip("'") for e in elig.split(',')]
    if eligset == ['SP'] or eligset == ['RP']:
        return m.group(0)  # pitcher, leave alone
    primary = next((e for e in eligset if e != 'DH'), eligset[0])
    return f"{head}position:'{primary}',eligiblePositions:[{elig}]"

pattern = r"(id:'[^']+',name:\"[^\"]+\"[^}]*?)position:'([^']+)',eligiblePositions:\[([^\]]+)\]"
new_code, n = re.subn(pattern, fix, code)

# verify no hitter mismatches remain
bad = 0
for m in re.finditer(r"name:\"[^\"]+\"[^}]*?position:'([^']+)',eligiblePositions:\[([^\]]+)\]", new_code):
    pos = m.group(1); elig = [e.strip().strip("'") for e in m.group(2).split(',')]
    if elig in (['SP'], ['RP']): continue
    if pos not in elig: bad += 1

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(new_code)

print(f"Rewrote {n} position fields")
print(f"Remaining mismatches: {bad}")
jm = re.search(r"displayName:\"Julio Rodr[^}]*?position:'([^']+)'", new_code)
if jm: print(f"Julio Rodriguez now shows: {jm.group(1)}")
if bad == 0 and n > 1000:
    print("SUCCESS — every hitter's label is now a position they can actually play.")
    print("Run: git add . && git commit -m 'fix stale primary position labels (642 cards)' && git push")
else:
    print("Unexpected result — do NOT push, report back.")
