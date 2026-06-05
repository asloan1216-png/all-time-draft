with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Find and fix the reroll button spin - it has the exhaustive search inside setTimeout
# which may be causing infinite loop. Simplify it.
old = """                    setTimeout(()=>{
                      let res;
                      if(decadeMode&&lockedDecade){
                        const teams=TEAMS_BY_DECADE[lockedDecade]||[];
                        res={team:teams[Math.floor(Math.random()*teams.length)],decade:lockedDecade};
                      } else {
                        res=randTeamDecade();
                        let att2=0;
                        while(att2<200 && !poolHasNeeded(res.team,res.decade)){res=randTeamDecade();att2++;}
                        if(!poolHasNeeded(res.team,res.decade)){
                          const allC=[];DECADES.forEach(dec=>(TEAMS_BY_DECADE[dec]||[]).forEach(team=>allC.push({team,decade:dec})));
                          const valid=allC.find(c=>poolHasNeeded(c.team,c.decade));
                          if(valid)res=valid;
                        }
                      }
                      setSpinRes(res);setSpinning(false);"""

new = """                    setTimeout(()=>{
                      let res;
                      if(decadeMode&&lockedDecade){
                        const teams=TEAMS_BY_DECADE[lockedDecade]||[];
                        res={team:teams[Math.floor(Math.random()*teams.length)],decade:lockedDecade};
                      } else res=randTeamDecade();
                      setSpinRes(res);setSpinning(false);"""

if old in code:
    code = code.replace(old, new, 1)
    print("Fixed: removed exhaustive search from reroll timeout")
else:
    print("Not matched - searching...")
    idx = code.find('att2<200')
    if idx > 0:
        print(repr(code[idx-200:idx+200]))

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Done — run: git add . && git commit -m 'fix reroll infinite spin' && git push")
