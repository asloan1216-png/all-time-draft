# Finisher: applies the 3 fixes the audit found missing from the deployed file.
#   A) Win variance + expected range (162-0 reachable)
#   B) Bulletproof anti-stuck spin
#   C) Vlad Guerrero ANA 2000s card
# Idempotent: each step detects if already applied and skips. Read the report.
import re

PATH='src/App.jsx'
code=open(PATH,encoding='utf-8').read()

def has(s): return s in code

# ───────────────────────── A) VARIANCE ─────────────────────────
print("[A] Win variance + expected range")
if has("length:1000") and has("winRange"):
    print("  SKIP — already present")
else:
    a=0
    old_sim="""  // Monte-Carlo a 162-game season, median of 7 runs for stability
  const sims = Array.from({length:7}, () => {
    let w=0; for(let i=0;i<162;i++) if(Math.random()<winPct) w++; return w;
  }).sort((a,b)=>a-b);
  const wins = sims[3];"""
    new_sim="""  // Monte-Carlo 1000 full seasons to capture real baseball variance.
  // Headline = ONE actual simulated season (same roster varies; a perfect
  // roster has a genuine rare shot at 162-0). Range = where it lands typically.
  const seasons = Array.from({length:1000}, () => {
    let w=0; for(let i=0;i<162;i++) if(Math.random()<winPct) w++; return w;
  });
  const wins = seasons[Math.floor(Math.random()*seasons.length)];
  const sortedSeasons = [...seasons].sort((a,b)=>a-b);
  const winRange = [sortedSeasons[Math.floor(1000*0.10)], sortedSeasons[Math.floor(1000*0.90)]];
  const expectedWins = Math.round(winPct*162);"""
    if old_sim in code: code=code.replace(old_sim,new_sim,1); a+=1; print("  OK  sim block -> variance season")
    else: print("  MISS sim block (median-of-7 not found)")

    old_ret="    wins, losses:162-wins, winPct, rawWinPct,"
    new_ret="    wins, losses:162-wins, winPct, rawWinPct, winRange, expectedWins,"
    if old_ret in code and "winRange, expectedWins" not in code:
        code=code.replace(old_ret,new_ret,1); a+=1; print("  OK  result carries winRange/expectedWins")
    else: print("  MISS/SKIP return object")

    old_hero="""          <span style={{fontSize:64,fontWeight:700,color:'#1e3a5f',fontFamily:'Georgia,serif'}}>{162-anim}</span>
        </div>
        
        {show&&("""
    new_hero="""          <span style={{fontSize:64,fontWeight:700,color:'#1e3a5f',fontFamily:'Georgia,serif'}}>{162-anim}</span>
        </div>
        {show&&result.winRange&&(
          <div style={{fontSize:12,color:'#475569',marginBottom:26,marginTop:2,letterSpacing:0.5}}>
            Expected range: <span style={{color:'#94a3b8',fontWeight:600}}>{result.winRange[0]}\u2013{result.winRange[1]} wins</span> in a typical season
          </div>
        )}
        {show&&("""
    if old_hero in code: code=code.replace(old_hero,new_hero,1); a+=1; print("  OK  expected-range line added")
    else: print("  MISS hero block (layout differs)")
    print(f"  -> {a}/3 variance hunks")

# ───────────────────────── B) ANTI-STUCK ─────────────────────────
print("\n[B] Bulletproof anti-stuck spin")
if has("comboPickable"):
    print("  SKIP — already present")
else:
    old="""      // Normal spin or decade mode subsequent spins (team only, decade locked)
      // Re-roll up to 50 times to find a team with eligible players for current needs
      let attempts=0;
      if(isDaily&&dailyRolls.length>0){
        res=dailyRolls[dailyIdx]||randTeamDecade();setDailyIdx(i=>i+1);
      } else {
        do {
          if(decadeMode && lockedDecade){
            const teams=TEAMS_BY_DECADE[lockedDecade]||[];
            const team=teams[Math.floor(Math.random()*teams.length)];
            res={team,decade:lockedDecade};
          } else {
            res=randTeamDecade();
          }
          attempts++;
        } while(attempts<50 && !poolHasNeeded(res.team, res.decade));
      }"""
    new="""      // Deterministic, never-stuck selection: pick from the set of combos that
      // can actually supply a needed player (using the SAME decade-wide pool the
      // user sees), so a "valid" spin can never show an unpickable pool.
      function comboPickable(team, decade){
        const inPool = players.filter(p => notDrafted(p) && p.team===team && p.decade===decade);
        const usePool = inPool.length>0 ? inPool : players.filter(p => notDrafted(p) && p.decade===decade);
        return usePool.some(p => {
          if (p.type==='pitcher') return (p.role==='SP'&&needsSP)||(p.role==='RP'&&needsRP);
          return needsH && p.eligiblePositions.some(pos=>neededNow.hitter.includes(pos));
        });
      }
      if(isDaily&&dailyRolls.length>0){
        res=dailyRolls[dailyIdx]||randTeamDecade();setDailyIdx(i=>i+1);
      } else {
        const decadesToUse = (decadeMode && lockedDecade) ? [lockedDecade] : DECADES;
        let combos = [];
        decadesToUse.forEach(dec => (TEAMS_BY_DECADE[dec]||[]).forEach(team => combos.push({team,decade:dec})));
        let valid = combos.filter(c => comboPickable(c.team, c.decade));
        if(valid.length===0 && decadeMode && lockedDecade){
          let allCombos=[];
          DECADES.forEach(dec => (TEAMS_BY_DECADE[dec]||[]).forEach(team => allCombos.push({team,decade:dec})));
          valid = allCombos.filter(c => comboPickable(c.team, c.decade));
        }
        if(valid.length>0){ res = valid[Math.floor(Math.random()*valid.length)]; }
        else { res = (decadeMode && lockedDecade)
            ? {team:(TEAMS_BY_DECADE[lockedDecade]||[])[0], decade:lockedDecade}
            : randTeamDecade(); }
      }"""
    if old in code: code=code.replace(old,new,1); print("  OK  deterministic selection")
    else: print("  MISS retry block (spin structure differs)")

    old_pool="""      const decadePool=strictPool.length>0?strictPool:players.filter(p=>
        notDrafted(p)&&p.decade===res.decade
      ).sort((a,b)=>(b.avgWARperYear||0)-(a.avgWARperYear||0)).slice(0,8);

      setPool(decadePool);"""
    new_pool="""      let decadePool=strictPool.length>0?strictPool:players.filter(p=>
        notDrafted(p)&&p.decade===res.decade
      ).sort((a,b)=>(b.avgWARperYear||0)-(a.avgWARperYear||0)).slice(0,8);
      if(decadePool.length===0){
        decadePool=players.filter(p=>notDrafted(p))
          .sort((a,b)=>(b.avgWARperYear||0)-(a.avgWARperYear||0)).slice(0,8);
      }
      setPool(decadePool);"""
    if old_pool in code: code=code.replace(old_pool,new_pool,1); print("  OK  pool never-empty safety net")
    else: print("  MISS pool block")

# ───────────────────────── C) VLAD CARD ─────────────────────────
print("\n[C] Vlad Guerrero ANA 2000s card")
if has("vladimir-guerrero-ana-2000s"):
    print("  SKIP — already present")
else:
    anchor="id:'vladimir-guerrero-2000s'"
    i=code.find(anchor)
    if i>=0:
        end=code.find("},",i)+2
        vlad="\n  {id:'vladimir-guerrero-ana-2000s',name:\"Vladimir Guerrero\",displayName:\"Vladimir Guerrero\",team:'ANA',decade:'2000s',sampleNote:'',position:'RF',eligiblePositions:['RF','DH'],type:'hitter',role:null,peakYears:[2004,2005,2006],avgWARperYear:4.9,stats:{avg:0.328,hr:35,obp:0.389,slg:0.572,wrcPlus:145,bsr:-1.5,dwar:-3.2}},"
        code=code[:end]+vlad+code[end:]; print("  OK  Vlad ANA card added")
    else:
        print("  MISS — vladimir-guerrero-2000s anchor not found")

open(PATH,'w',encoding='utf-8').write(code)
print("\nDone. If no MISS lines above and it compiles, commit & push.")
