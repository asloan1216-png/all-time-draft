import re

with open('src/App.jsx','r', encoding='utf-8') as f:
    code = f.read()

fixed = 0

# Replace the two reroll buttons (team + decade) with a single reroll button (4 uses)
# First update state: replace teamRerolls + decadeRerolls with single rerollsUsed

# 1. Replace useState declarations
old_states = "  const [teamRerolls,setTeamRerolls]=useState(0);    // how many times team has been rerolled\n  const [decadeRerolls,setDecadeRerolls]=useState(0); // how many times decade has been rerolled"
new_states = "  const [rerollsUsed,setRerollsUsed]=useState(0); // total rerolls used (max 4 per round)"
if old_states in code:
    code = code.replace(old_states, new_states, 1)
    fixed += 1
    print("Fixed: state declarations")

# 2. Reset in startGame
old_sg_reset = "    setTeamRerolls(0);setDecadeRerolls(0);"
new_sg_reset = "    setRerollsUsed(0);"
if old_sg_reset in code:
    code = code.replace(old_sg_reset, new_sg_reset, 1)
    fixed += 1
    print("Fixed: startGame reset")

# 3. Reset in reset()
old_reset = "setTeamRerolls(0);setDecadeRerolls(0);"
new_reset = "setRerollsUsed(0);"
if old_reset in code:
    code = code.replace(old_reset, new_reset, 1)
    fixed += 1
    print("Fixed: reset() function")

# 4. Remove reset from pick() if present
old_pick_reset = "      setTeamRerolls(0); setDecadeRerolls(0);\n"
if old_pick_reset in code:
    code = code.replace(old_pick_reset, "", 1)
    print("Fixed: removed reset from pick()")

# 5. Replace the two reroll buttons with one
old_buttons = """              {/* Reroll buttons — 2 team rerolls + 2 decade rerolls per round */}
              <div style={{display:'flex',gap:8,marginTop:12,flexWrap:'wrap',justifyContent:'center',width:'100%',maxWidth:500}}>
                <button
                  disabled={teamRerolls>=2}
                  onClick={()=>{
                    if(teamRerolls>=2) return;
                    const dec=lockedDecade||spinRes.decade;
                    // Pick the best team upfront before spinning
                    const draftedIds=new Set(Object.values(roster).filter(Boolean).map(p=>p.id));
                    const draftedNames=new Set(Object.values(roster).filter(Boolean).map(p=>(p.displayName||p.name||'').replace(/ \\d-yr$/,'')));
                    const notDrafted=p=>{if(draftedIds.has(p.id))return false;const dn=(p.displayName||p.name||'').replace(/ \\d-yr$/,'');return !draftedNames.has(dn);};
                    const neededNow2=getNeededPositions(roster);
                    const otherTeams=(TEAMS_BY_DECADE[dec]||[]).filter(t=>t!==spinRes.team);
                    const eligible2=otherTeams.filter(t=>players.some(p=>notDrafted(p)&&p.team===t&&p.decade===dec));
                    const pool2=eligible2.length>0?eligible2:otherTeams;
                    const finalTeam=pool2[Math.floor(Math.random()*pool2.length)]||spinRes.team;
                    const finalRes={team:finalTeam,decade:dec};
                    setTeamRerolls(r=>r+1);
                    setPool([]);setRerollMode('team');
                    setSpinning(true);
                    setTimeout(()=>{
                      setSpinRes(finalRes);setSpinning(false);setRerollMode(null);
                      const strict=players.filter(p=>notDrafted(p)&&p.team===finalTeam&&p.decade===dec).sort((a,b)=>(b.avgWARperYear||0)-(a.avgWARperYear||0));
                      const fallback=strict.length>0?strict:players.filter(p=>notDrafted(p)&&p.decade===dec).sort((a,b)=>(b.avgWARperYear||0)-(a.avgWARperYear||0)).slice(0,8);
                      setPool(fallback);
                    },800);
                  }}
                  style={{background:teamRerolls>=2?'rgba(30,42,58,0.4)':'rgba(245,158,11,0.06)',border:`1px solid ${teamRerolls>=2?'#0f1f35':'rgba(245,158,11,0.3)'}`,color:teamRerolls>=2?'#1e3a5f':'#f59e0b',borderRadius:8,padding:'8px 18px',cursor:teamRerolls>=2?'not-allowed':'pointer',fontSize:12,fontWeight:700,transition:'all .15s'}}>
                  🔄 New Team {teamRerolls>=2?'(used)':teamRerolls>0?`(${2-teamRerolls} left)`:'(2 left)'}
                </button>
                {!decadeMode&&<button
                  disabled={decadeRerolls>=2}
                  onClick={()=>{
                    if(decadeRerolls>=2) return;
                    // Roll a new decade only — keep the same team, freeze it in the animation
                    const currentDec=spinRes.decade;
                    const currentTeam=spinRes.team;
                    const allDecs=DECADES.filter(d=>d!==currentDec&&(TEAMS_BY_DECADE[d]||[]).length>0);
                    const newDec=allDecs[Math.floor(Math.random()*allDecs.length)];
                    // Keep same team if it exists in new decade, otherwise pick best available
                    const draftedIds2=new Set(Object.values(roster).filter(Boolean).map(p=>p.id));
                    const draftedNames2=new Set(Object.values(roster).filter(Boolean).map(p=>(p.displayName||p.name||'').replace(/ \\d-yr$/,'')));
                    const notDrafted2=p=>{if(draftedIds2.has(p.id))return false;const dn=(p.displayName||p.name||'').replace(/ \\d-yr$/,'');return !draftedNames2.has(dn);};
                    const teamsInNewDec=TEAMS_BY_DECADE[newDec]||[];
                    // Use same team if available, else pick a random one from new decade
                    const finalTeam2=teamsInNewDec.includes(currentTeam)?currentTeam:teamsInNewDec[Math.floor(Math.random()*teamsInNewDec.length)];
                    const finalRes2={team:finalTeam2,decade:newDec};
                    setDecadeRerolls(r=>r+1);
                    setPool([]);setRerollMode('decade');
                    setSpinning(true);
                    setTimeout(()=>{
                      setSpinRes(finalRes2);setSpinning(false);setRerollMode(null);
                      const strict=players.filter(p=>notDrafted2(p)&&p.team===finalTeam2&&p.decade===newDec).sort((a,b)=>(b.avgWARperYear||0)-(a.avgWARperYear||0));
                      const fallback=strict.length>0?strict:players.filter(p=>notDrafted2(p)&&p.decade===newDec).sort((a,b)=>(b.avgWARperYear||0)-(a.avgWARperYear||0)).slice(0,8);
                      setPool(fallback);
                    },800);
                  }}
                  style={{background:decadeRerolls>=2?'rgba(30,42,58,0.4)':'rgba(96,165,250,0.06)',border:`1px solid ${decadeRerolls>=2?'#0f1f35':'rgba(96,165,250,0.3)'}`,color:decadeRerolls>=2?'#1e3a5f':'#60a5fa',borderRadius:8,padding:'8px 18px',cursor:decadeRerolls>=2?'not-allowed':'pointer',fontSize:12,fontWeight:700,transition:'all .15s'}}>
                  📅 New Decade {decadeRerolls>=2?'(used)':decadeRerolls>0?`(${2-decadeRerolls} left)`:'(2 left)'}
                </button>}
              </div>"""

new_buttons = """              {/* Single reroll button — 4 uses per round */}
              <div style={{display:'flex',gap:8,marginTop:12,justifyContent:'center',width:'100%',maxWidth:500}}>
                <button
                  disabled={rerollsUsed>=4}
                  onClick={()=>{
                    if(rerollsUsed>=4) return;
                    setRerollsUsed(r=>r+1);
                    setPool([]);setRerollMode(null);
                    setSpinning(true);
                    setTimeout(()=>{
                      let res;
                      if(decadeMode&&lockedDecade){
                        const teams=TEAMS_BY_DECADE[lockedDecade]||[];
                        res={team:teams[Math.floor(Math.random()*teams.length)],decade:lockedDecade};
                      } else {
                        res=randTeamDecade();
                      }
                      setSpinRes(res);setSpinning(false);
                      const draftedIds=new Set(Object.values(roster).filter(Boolean).map(p=>p.id));
                      const draftedNames=new Set(Object.values(roster).filter(Boolean).map(p=>(p.displayName||p.name||'').replace(/ \\d-yr$/,'')));
                      const notDrafted=p=>{if(draftedIds.has(p.id))return false;const dn=(p.displayName||p.name||'').replace(/ \\d-yr$/,'');return !draftedNames.has(dn);};
                      const strict=players.filter(p=>notDrafted(p)&&p.team===res.team&&p.decade===res.decade).sort((a,b)=>(b.avgWARperYear||0)-(a.avgWARperYear||0));
                      const fallback=strict.length>0?strict:players.filter(p=>notDrafted(p)&&p.decade===res.decade).sort((a,b)=>(b.avgWARperYear||0)-(a.avgWARperYear||0)).slice(0,8);
                      setPool(fallback);
                    },1600);
                  }}
                  style={{background:rerollsUsed>=4?'rgba(30,42,58,0.4)':'rgba(245,158,11,0.06)',border:`1px solid ${rerollsUsed>=4?'#0f1f35':'rgba(245,158,11,0.3)'}`,color:rerollsUsed>=4?'#1e3a5f':'#f59e0b',borderRadius:8,padding:'8px 22px',cursor:rerollsUsed>=4?'not-allowed':'pointer',fontSize:12,fontWeight:700,transition:'all .15s'}}>
                  🎰 Spin Again {rerollsUsed>=4?'(used)':`(${4-rerollsUsed} left)`}
                </button>
              </div>"""

if old_buttons in code:
    code = code.replace(old_buttons, new_buttons, 1)
    fixed += 1
    print("Fixed: replaced 2 buttons with 1 reroll button (4 uses)")
else:
    print("Button block not found!")

with open('src/App.jsx','w', encoding='utf-8') as f:
    f.write(code)

print(f"\nTotal fixed: {fixed}")
print("Done — now run: git add . && git commit -m 'simplify to single reroll button 4 uses' && git push")
