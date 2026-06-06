# Re-sync known-correct eligibility into your real file (some earlier fixes
# never landed), then re-derive each primary `position` label from eligibility.
import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Ground-truth eligibility for players we've corrected before (and a few extras).
# Keyed by displayName. Value = correct eligiblePositions list.
TRUTH = {
    "Julio Rodríguez":   ['CF','LF','RF','DH'],
    "Michael Harris II":  ['CF','LF','RF','DH'],
    "Jazz Chisholm Jr.":  ['2B','CF','3B','SS','DH'],
    "Daulton Varsho":     ['C','LF','CF','RF','DH'],
    "Jeremy Peña":        ['SS','DH'],
    "Jose Siri":          ['CF','LF','RF','DH'],
    "Pete Crow-Armstrong":['CF','LF','RF','DH'],
    "Shea Langeliers":    ['C','DH'],
    "Jackson Merrill":    ['CF','LF','RF','DH'],
    "Andy Pages":         ['RF','LF','DH'],
    "Drake Baldwin":      ['C','DH'],
    "Yainer Diaz":        ['C','DH'],
    "Wilyer Abreu":       ['LF','CF','RF','DH'],
    "Ryan Jeffers":       ['C','DH'],
    "Zach Neto":          ['SS','DH'],
    "Colson Montgomery":  ['SS','DH'],
    "Brice Turang":       ['2B','SS','DH'],
    "Caleb Durbin":       ['2B','SS','DH'],
    "Elly De La Cruz":    ['SS','3B','DH'],
    "Ha-Seong Kim":       ['SS','2B','3B','DH'],
    "Anthony Volpe":      ['SS','DH'],
    "Bobby Witt Jr.":     ['SS','3B','DH'],
    "Wander Franco":      ['SS','2B','DH'],
    "Bryson Stott":       ['2B','SS','DH'],
    "Wyatt Langford":     ['LF','CF','RF','DH'],
    "Jarren Duran":       ['CF','LF','RF','DH'],
    "Brandon Marsh":      ['CF','LF','RF','DH'],
    "Isaac Paredes":      ['3B','2B','DH'],
    "Nolan Jones":        ['LF','3B','RF','DH'],
    "Royce Lewis":        ['SS','3B','DH'],
    "Jordan Westburg":    ['2B','3B','SS','DH'],
    "Steven Kwan":        ['LF','CF','RF','DH'],
    "Luis Robert Jr.":    ['CF','LF','RF','DH'],
    "Jonathan India":     ['2B','3B','DH'],
    "Noelvi Marte":       ['3B','SS','DH'],
    "Spencer Torkelson":  ['1B','3B','DH'],
    "Riley Greene":       ['LF','CF','RF','DH'],
    "Oneil Cruz":         ['SS','LF','DH'],
    "Jackson Holliday":   ['2B','SS','DH'],
    "CJ Abrams":          ['SS','DH'],
    "Gunnar Henderson":   ['SS','3B','DH'],
    "Masyn Winn":         ['SS','DH'],
    "Matt McLain":        ['SS','2B','DH'],
    "Brayan Rocchio":     ['SS','2B','DH'],
    "Corbin Carroll":     ['CF','LF','RF','DH'],
}

resynced = []
for name, elig in TRUTH.items():
    new_elig = ','.join(f"'{p}'" for p in elig)
    # Build both the literal name and its JS \uXXXX-escaped variant,
    # since the file stores accented chars as escapes (e.g. Rodr\u00edguez).
    variants = {name}
    esc_name = ''.join(c if ord(c) < 128 else "\\u%04x" % ord(c) for c in name)
    variants.add(esc_name)
    n = 0
    for v in variants:
        pat = re.compile(r'(displayName:"' + re.escape(v) + r'"[^}]*?eligiblePositions:\[)[^\]]+(\])')
        code, cnt = pat.subn(lambda m: m.group(1) + new_elig + m.group(2), code)
        n += cnt
    if n > 0:
        resynced.append((name, n, elig))

print("Eligibility re-synced:")
for name, n, elig in resynced:
    print(f"  {name} ({n} card(s)) -> {elig}")
print(f"  [{len(resynced)}/{len(TRUTH)} names found in file]\n")

# Now re-derive primary position = first non-DH eligible, for ALL hitters
def fix(m):
    head, pos, elig = m.group(1), m.group(2), m.group(3)
    eligset = [e.strip().strip("'") for e in elig.split(',')]
    if eligset in (['SP'],['RP']): return m.group(0)
    primary = next((e for e in eligset if e != 'DH'), eligset[0])
    return f"{head}position:'{primary}',eligiblePositions:[{elig}]"
pattern = r"(id:'[^']+',name:\"[^\"]+\"[^}]*?)position:'([^']+)',eligiblePositions:\[([^\]]+)\]"
code, total = re.subn(pattern, fix, code)

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

# verify
jm = re.search(r'displayName:"Julio Rodr[^}]*?position:\'([^\']+)\',eligiblePositions:\[([^\]]+)\]', code)
print(f"Position labels re-derived on {total} hitter cards")
if jm:
    print(f"Julio Rodriguez now: position '{jm.group(1)}', eligible [{jm.group(2)}]")
print("\nIf Julio shows CF: git add . && git commit -m 'resync eligibility + position labels' && git push")
