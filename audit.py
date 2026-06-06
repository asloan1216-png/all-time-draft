# READ-ONLY full audit of the deployed file. Changes nothing.
# Reports the true state of every major fix + data integrity check.
import re, sys

PATH = 'src/App.jsx'
with open(PATH, 'r', encoding='utf-8') as f:
    code = f.read()

P=0; F=0; W=0
def ok(label, cond, detail=""):
    global P,F
    print(("  PASS  " if cond else "  FAIL  ") + label + (("  — "+detail) if detail and not cond else ""))
    if cond: P+=1
    else: F+=1
def warn(label, detail=""):
    global W
    print("  WARN  " + label + (("  — "+detail) if detail else "")); W+=1

print("="*64)
print("ALL-TIME DRAFT — FULL FILE AUDIT (read-only)")
print(f"File: {PATH}  ({len(code):,} bytes)")
print("="*64)

# ---- ENGINE ----
print("\n[ENGINE]")
ok("Pitching staff read with lowercase keys (sp)", "toLowerCase().startsWith('sp')" in code)
ok("Pitching staff read with lowercase keys (rp)", "toLowerCase().startsWith('rp')" in code)
ok("No leftover uppercase startsWith('SP')", "startsWith('SP')" not in code)
ok("No leftover uppercase startsWith('RP')", "startsWith('RP')" not in code)
ok("Variance: 1000-season Monte Carlo", "length:1000" in code and "seasons" in code)
ok("Variance: headline is one real season", "seasons[Math.floor(Math.random()*" in code)
ok("Variance: winRange in result", "winRange" in code)
ok("Variance: expectedWins in result", "expectedWins" in code)
ok("Staff breakdown returns spRA9/rpRA9", "spRA9: Math.round(spRA" in code)
ok("Result carries spRA9", "spRA9: staff.spRA9" in code)
ok("Result carries rpRA9", "rpRA9: staff.rpRA9" in code)
ok("Results screen shows Rotation RA9", "Rotation RA9" in code)
ok("Results screen shows Bullpen RA9", "Bullpen RA9" in code)
ok("Replay Season button present", "Replay Season" in code)
ok("Replay wired to re-simulate", "onReplay={()=>" in code)
ok("Expected-range line shown", "Expected range:" in code)

# ---- ANTI-STUCK ----
print("\n[ANTI-STUCK SPIN]")
ok("Deterministic comboPickable present", "comboPickable" in code)
ok("Pool guaranteed non-empty safety net", "decadePool=players.filter(p=>notDrafted(p))" in code)
# the old fragile retry should be gone
if "attempts<50 && !poolHasNeeded" in code:
    warn("Old 50-attempt retry still present (may be replaced or coexisting)")
else:
    ok("Old fragile 50-attempt retry removed", True)

# ---- DATA INTEGRITY: positions ----
print("\n[DATA — POSITION LABELS]")
mismatch=[]
for m in re.finditer(r'name:"([^"]+)"[^}]*?position:\'([^\']+)\',eligiblePositions:\[([^\]]+)\]', code):
    name,pos = m.group(1),m.group(2)
    elig=[e.strip().strip("'") for e in m.group(3).split(',')]
    if elig in (['SP'],['RP']): continue
    if pos not in elig: mismatch.append((name,pos,elig))
ok(f"Every hitter's label is a position they can play", len(mismatch)==0,
   f"{len(mismatch)} mismatches e.g. {mismatch[:3]}")

# ---- DATA INTEGRITY: known players ----
print("\n[DATA — KNOWN PLAYER ELIGIBILITY]")
def elig_of(disp_substr):
    # match escaped-unicode or plain
    m=re.search(r'displayName:"'+disp_substr+r'[^"]*"[^}]*?eligiblePositions:\[([^\]]+)\]', code)
    if not m: return None
    return [e.strip().strip("'") for e in m.group(1).split(',')]
checks_known = {
    "Julio Rodr": ['CF','LF','RF','DH'],
    "Jazz Chisholm": ['2B','CF','3B','SS','DH'],
    "Joe Morgan": ['2B','DH'],
    "Brooks Robinson": ['3B','DH'],
    "Jeremy Pe": ['SS','DH'],
    "Michael Harris": ['CF','LF','RF','DH'],
}
for sub,exp in checks_known.items():
    got=elig_of(sub)
    ok(f"{sub.strip()} eligibility", got==exp, f"got {got}, expected {exp}")

# ---- DATA: special cards ----
print("\n[DATA — MANUAL CARDS]")
ok("Sheffield FLA 1990s card", "gary-sheffield-1990s" in code and re.search(r"gary-sheffield-1990s'[^}]*team:'FLA'", code) is not None)
ok("Kevin Brown FLA 1990s card", re.search(r"kevin-brown-1990s-sp'[^}]*team:'FLA'", code) is not None)
ok("Vlad Guerrero ANA 2000s card", "vladimir-guerrero-ana-2000s" in code)

# ---- DATA: duplicate IDs ----
print("\n[DATA — STRUCTURAL]")
ids=re.findall(r"\{id:'([^']+)'", code)
dupes={i for i in ids if ids.count(i)>1}
ok(f"No duplicate card IDs ({len(ids)} cards total)", len(dupes)==0, f"dupes: {list(dupes)[:5]}")

# ---- CONFIG ----
print("\n[CONFIG]")
m=re.search(r"SALARY_CAP_BUDGET\s*=\s*(\d+)", code)
ok("Salary cap = 250", m is not None and m.group(1)=="250", f"found {m.group(1) if m else 'none'}")
ok("Single reroll (rerollsUsed) present", "rerollsUsed" in code)
ok("No leftover teamRerolls state", "const [teamRerolls" not in code)
ok("No leftover decadeRerolls state", "const [decadeRerolls" not in code)
ok("SP reorder arrows present", "spKeys=['sp1','sp2','sp3','sp4','sp5']" in code or "onRosterChange(nr)" in code)

# ---- STRUCTURAL SANITY ----
print("\n[SYNTAX SANITY]")
ok("Balanced braces", code.count('{')==code.count('}'), f"{code.count('{')} open vs {code.count('}')} close")
ok("Balanced parens", code.count('(')==code.count(')'), f"{code.count('(')} open vs {code.count(')')} close")
ok("Balanced square brackets", code.count('[')==code.count(']'), f"{code.count('[')} open vs {code.count(']')} close")

print("\n"+"="*64)
print(f"RESULT:  {P} passed, {F} failed, {W} warnings")
print("="*64)
if F==0:
    print("ALL CHECKS PASSED ✓  — engine + data integrity verified.")
else:
    print("SOME CHECKS FAILED ✗  — paste this output back; do not assume deployed state is correct.")
