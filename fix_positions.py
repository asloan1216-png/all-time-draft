import re

with open('src/App.jsx','r', encoding='utf-8') as f:
    code = f.read()

fixed = 0

# Fix 1: Decade reroll animation - freeze team immediately
old_dec_anim = "      } else if(rerollMode==='decade'){\n        // Decade reroll: keep current team visible, only cycle decades\n        ref.current=setInterval(()=>setDisp(d=>({team:d.team,decade:DECADES[Math.floor(Math.random()*DECADES.length)]})),80);"
new_dec_anim = "      } else if(rerollMode==='decade'){\n        // Decade reroll: freeze team from result, only cycle decades\n        const frozenTeam=result?.team||disp.team;\n        setDisp(d=>({...d,team:frozenTeam})); // lock team immediately\n        ref.current=setInterval(()=>setDisp(d=>({team:frozenTeam,decade:DECADES[Math.floor(Math.random()*DECADES.length)]})),80);"
if old_dec_anim in code:
    code = code.replace(old_dec_anim, new_dec_anim, 1)
    fixed += 1
    print("Fixed: decade reroll freezes team in animation")

# Fix 2: Team reroll animation - freeze decade immediately  
old_team_anim = "      } else if(rerollMode==='team'){\n        // Team reroll: keep current decade, only cycle teams\n        const dec=result?.decade||disp.decade;\n        const teams=TEAMS_BY_DECADE[dec]||[];\n        ref.current=setInterval(()=>setDisp(d=>({team:teams[Math.floor(Math.random()*teams.length)],decade:dec})),80);"
new_team_anim = "      } else if(rerollMode==='team'){\n        // Team reroll: freeze decade from result, only cycle teams\n        const dec=result?.decade||disp.decade;\n        const teams=TEAMS_BY_DECADE[dec]||[];\n        setDisp(d=>({...d,decade:dec})); // lock decade immediately\n        ref.current=setInterval(()=>setDisp(d=>({team:teams[Math.floor(Math.random()*teams.length)],decade:dec})),80);"
if old_team_anim in code:
    code = code.replace(old_team_anim, new_team_anim, 1)
    fixed += 1
    print("Fixed: team reroll freezes decade in animation")

with open('src/App.jsx','w', encoding='utf-8') as f:
    f.write(code)

print(f"\nTotal fixed: {fixed}")
print("Done — now run: git add . && git commit -m 'fix reroll animations' && git push")
