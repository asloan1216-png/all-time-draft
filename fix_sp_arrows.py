with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

# 1. Add spOrder state to App (next to lineup state)
old_lineup_state = "const [lineup,setLineup]=useState(Array(9).fill(null));"
new_lineup_state = "const [lineup,setLineup]=useState(Array(9).fill(null));\n  const [spOrder,setSpOrder]=useState([0,1,2,3,4]);"
if old_lineup_state in code:
    code = code.replace(old_lineup_state, new_lineup_state, 1)
    print("Fix 1: spOrder state added to App")
    fixes += 1

# 2. Pass spOrder/setSpOrder into LineupBuilder
old_lb = "<LineupBuilder roster={roster} lineup={lineup} onLineupChange={setLineup} rpRoles={rpRoles} onRpRolesChange={setRpRoles} onSimulate={runSim}/>"
new_lb = "<LineupBuilder roster={roster} lineup={lineup} onLineupChange={setLineup} rpRoles={rpRoles} onRpRolesChange={setRpRoles} onSimulate={runSim} spOrder={spOrder} onSpOrderChange={setSpOrder}/>"
if old_lb in code:
    code = code.replace(old_lb, new_lb, 1)
    print("Fix 2: spOrder props passed to LineupBuilder")
    fixes += 1

# 3. Reset spOrder when new game starts
old_reset = "setLineup(Array(9).fill(null));"
new_reset = "setLineup(Array(9).fill(null)); setSpOrder([0,1,2,3,4]);"
if old_reset in code:
    code = code.replace(old_reset, new_reset)
    print("Fix 3: spOrder reset on new game")
    fixes += 1

# 4. Update LineupBuilder function signature to accept spOrder prop
old_sig = "function LineupBuilder({roster,lineup,onLineupChange,rpRoles,onRpRolesChange,onSimulate})"
new_sig = "function LineupBuilder({roster,lineup,onLineupChange,rpRoles,onRpRolesChange,onSimulate,spOrder=[0,1,2,3,4],onSpOrderChange})"
if old_sig in code:
    code = code.replace(old_sig, new_sig, 1)
    print("Fix 4: LineupBuilder signature updated")
    fixes += 1
else:
    # Try finding it differently
    import re
    m = re.search(r'function LineupBuilder\(\{[^}]+\}\)', code)
    if m:
        print(f"Found signature: {m.group(0)}")

# 5. Replace internal spOrder state with prop-based version
old_sp_state = """const allSPs=Object.values(roster).filter(p=>p&&p.role==='SP');
  const [spOrder,setSpOrder]=useState(()=>allSPs.map((_,i)=>i));
  const starters=spOrder.map(i=>allSPs[i]).filter(Boolean);"""

new_sp_state = """const allSPs=Object.values(roster).filter(p=>p&&p.role==='SP');
  const starters=spOrder.slice(0,allSPs.length).map(i=>allSPs[i]).filter(Boolean);"""

if old_sp_state in code:
    code = code.replace(old_sp_state, new_sp_state, 1)
    print("Fix 5: internal spOrder state replaced with prop")
    fixes += 1

# 6. Replace setSpOrder in arrow buttons with onSpOrderChange
code = code.replace(
    "const o=[...spOrder];[o[i-1],o[i]]=[o[i],o[i-1]];setSpOrder(o);",
    "const o=[...spOrder];[o[i-1],o[i]]=[o[i],o[i-1]];onSpOrderChange(o);"
)
code = code.replace(
    "const o=[...spOrder];[o[i],o[i+1]]=[o[i+1],o[i]];setSpOrder(o);",
    "const o=[...spOrder];[o[i],o[i+1]]=[o[i+1],o[i]];onSpOrderChange(o);"
)
print("Fix 6: arrow buttons use onSpOrderChange")
fixes += 1

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\nTotal fixes: {fixes}")
print("Done — run: git add . && git commit -m 'fix SP reorder arrows' && git push")
