with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

old = "} while(attempts<50 && !poolHasNeeded(res.team, res.decade));\n      }\n\n      setSpinRes(res);setSpinning(fal"

new = """} while(attempts<200 && !poolHasNeeded(res.team, res.decade));
        // Exhaustive fallback: try every team+decade combo until one works
        if(!poolHasNeeded(res.team, res.decade)){
          const allCombos=[];
          DECADES.forEach(dec=>(TEAMS_BY_DECADE[dec]||[]).forEach(team=>allCombos.push({team,decade:dec})));
          const valid=allCombos.find(c=>poolHasNeeded(c.team,c.decade));
          if(valid) res=valid;
        }
      }

      setSpinRes(res);setSpinning(fal"""

if old in code:
    code = code.replace(old, new, 1)
    print("Fixed: exhaustive search added to initial spin")
else:
    print("Not matched")

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Done — run: git add . && git commit -m 'fix initial spin exhaustive search' && git push")
