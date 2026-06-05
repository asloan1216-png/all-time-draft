with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

# The starters line needs to use spOrder instead of raw Object.values
old = "const starters=Object.values(roster).filter(p=>p&&p.role==='SP');\n  const relievers=Object.values(roster).filter(p=>p&&p.role==='RP');\n  const feedback=getLineupFeedback(lineup);"

new = "const allSPs=Object.values(roster).filter(p=>p&&p.role==='SP');\n  const starters=spOrder.slice(0,allSPs.length).map(i=>allSPs[i]).filter(Boolean);\n  const relievers=Object.values(roster).filter(p=>p&&p.role==='RP');\n  const feedback=getLineupFeedback(lineup);"

if old in code:
    code = code.replace(old, new, 1)
    print("Fixed: starters now uses spOrder")
else:
    print("Not found - checking what's there...")
    idx = code.find("const starters=Object.values(roster)")
    while idx > 0:
        print(repr(code[idx:idx+150]))
        idx = code.find("const starters=Object.values(roster)", idx+1)

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Done — run: git add . && git commit -m 'fix SP arrows starters order' && git push")
