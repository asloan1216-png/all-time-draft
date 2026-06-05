with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

# Fix 1: Increase retry attempts and use exhaustive search as final fallback
old_retry = """      do {
        res = randTeamDecade();
        attempts++;
      } while (attempts<50 && !poolHasNeeded(res.team, res.decade));"""

new_retry = """      // Try random spins first
      do {
        res = randTeamDecade();
        attempts++;
      } while (attempts<200 && !poolHasNeeded(res.team, res.decade));
      // If still not found, exhaustively search ALL team+decade combos
      if (!poolHasNeeded(res.team, res.decade)) {
        const allCombos = [];
        DECADES.forEach(dec => (TEAMS_BY_DECADE[dec]||[]).forEach(team => allCombos.push({team,decade:dec})));
        const validCombo = allCombos.find(c => poolHasNeeded(c.team, c.decade));
        if (validCombo) res = validCombo;
      }"""

if old_retry in code:
    code = code.replace(old_retry, new_retry, 1)
    print("Fix 1: exhaustive search fallback added")
    fixes += 1
else:
    print("Fix 1: not matched")

# Fix 2: Same for the reroll button spin
old_reroll_spin = """                    setTimeout(()=>{
                      let res;
                      if(decadeMode&&lockedDecade){
                        const teams=TEAMS_BY_DECADE[lockedDecade]||[];
                        res={team:teams[Math.floor(Math.random()*teams.length)],decade:lockedDecade};
                      } else res=randTeamDecade();
                      setSpinRes(res);setSpinning(false);"""

new_reroll_spin = """                    setTimeout(()=>{
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

if old_reroll_spin in code:
    code = code.replace(old_reroll_spin, new_reroll_spin, 1)
    print("Fix 2: reroll button also uses exhaustive search")
    fixes += 1
else:
    print("Fix 2: not matched")

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\nTotal fixes: {fixes}")
print("Done — run: git add . && git commit -m 'fix stuck spin exhaustive search' && git push")
