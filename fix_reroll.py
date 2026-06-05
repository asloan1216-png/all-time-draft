import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

# ─── FIX 1: Replace two reroll buttons with single 4-use button ───────────────

# Replace state declarations
old_states = [
    "const [teamRerolls,setTeamRerolls]=useState(0);    // how many times team has been rerolled\n  const [decadeRerolls,setDecadeRerolls]=useState(0); // how many times decade has been rerolled",
    "const [teamRerolls,setTeamRerolls]=useState(0); // how many times team has been rerolled\n  const [decadeRerolls,setDecadeRerolls]=useState(0); // how many times decade has been rerolled",
    "const [teamRerolls,setTeamRerolls]=useState(0);\n  const [decadeRerolls,setDecadeRerolls]=useState(0);",
]
for old in old_states:
    if old in code:
        code = code.replace(old, "const [rerollsUsed,setRerollsUsed]=useState(0); // total rerolls (max 4)", 1)
        print("Fix 1a: state declarations replaced")
        fixes += 1
        break

# Replace teamRerolls/decadeRerolls references
replacements = [
    ("setTeamRerolls(0);setDecadeRerolls(0);", "setRerollsUsed(0);"),
    ("setTeamRerolls(0); setDecadeRerolls(0);", "setRerollsUsed(0);"),
    ("setTeamRerolls(r=>r+1)", "setRerollsUsed(r=>r+1)"),
    ("setDecadeRerolls(r=>r+1)", ""),
    ("teamRerolls>=2", "rerollsUsed>=4"),
    ("decadeRerolls>=2", "rerollsUsed>=4"),
]
for old, new in replacements:
    if old in code:
        code = code.replace(old, new)
        print(f"Fix 1b: replaced '{old[:40]}'")
        fixes += 1

# Find and replace the two-button div with single button
# Find the comment that starts the reroll section
start_marker = '{/* Reroll buttons'
end_marker = '</div>\n            </>\n          )}'
start = code.find(start_marker)
if start > 0:
    end = code.find(end_marker, start)
    if end > 0:
        end += len(end_marker)
        new_buttons = """{/* Single reroll button — 4 uses per round */}
              <div style={{display:'flex',gap:8,marginTop:12,justifyContent:'center',width:'100%',maxWidth:500}}>
                <button
                  disabled={rerollsUsed>=4}
                  onClick={()=>{
                    if(rerollsUsed>=4) return;
                    setRerollsUsed(r=>r+1);
                    setPool([]);
                    setSpinning(true);
                    setTimeout(()=>{
                      let res;
                      if(decadeMode&&lockedDecade){
                        const teams=TEAMS_BY_DECADE[lockedDecade]||[];
                        res={team:teams[Math.floor(Math.random()*teams.length)],decade:lockedDecade};
                      } else res=randTeamDecade();
                      setSpinRes(res);setSpinning(false);
                      const dIds=new Set(Object.values(roster).filter(Boolean).map(p=>p.id));
                      const dNames=new Set(Object.values(roster).filter(Boolean).map(p=>(p.displayName||p.name||'').replace(/ \\d-yr$/,'')));
                      const notD=p=>{if(dIds.has(p.id))return false;const dn=(p.displayName||p.name||'').replace(/ \\d-yr$/,'');return !dNames.has(dn);};
                      const strict=players.filter(p=>notD(p)&&p.team===res.team&&p.decade===res.decade).sort((a,b)=>(b.avgWARperYear||0)-(a.avgWARperYear||0));
                      const fallback=strict.length>0?strict:players.filter(p=>notD(p)&&p.decade===res.decade).sort((a,b)=>(b.avgWARperYear||0)-(a.avgWARperYear||0)).slice(0,8);
                      setPool(fallback);
                    },1600);
                  }}
                  style={{background:rerollsUsed>=4?'rgba(30,42,58,0.4)':'rgba(245,158,11,0.06)',border:`1px solid ${rerollsUsed>=4?'#0f1f35':'rgba(245,158,11,0.3)'}`,color:rerollsUsed>=4?'#1e3a5f':'#f59e0b',borderRadius:8,padding:'8px 22px',cursor:rerollsUsed>=4?'not-allowed':'pointer',fontSize:12,fontWeight:700,transition:'all .15s'}}>
                  🎰 Spin Again {rerollsUsed>=4?'(used)':`(${4-rerollsUsed} left)`}
                </button>
              </div>
            </>
          )}"""
        code = code[:start] + new_buttons + code[end:]
        print("Fix 1c: two buttons replaced with single Spin Again button")
        fixes += 1

# ─── FIX 2: Add up/down arrows to reorder starting pitchers ──────────────────

old_sp_map = """starters.map((sp,i)=>(
            <div key={i} style={{display:'flex',alignItems:'center',gap:8,background:'rgba(8,16,32,0.7)',border:'1px solid #0f1f35',borderRadius:10,padding:'8px 10px',marginBottom:6}}>
              <span style={{fontSize:13,fontWeight:700,color:'#60a5fa',width:28,flexShrink:0}}>SP{i+1}</span>
              <span style={{flex:1,fontSize:13,fontWeight:600,overflow:'hidden',whiteSpace:'nowrap',textOverflow:'ellipsis'}}>{sp.name}</span>
              <span style={{fontSize:10,color:'#475569',flexShrink:0}}>{sp.decade}</span>
              <span style={{fontSize:10,color:'#94a3b8',flexShrink:0}}>{sp.stats?.era} ERA</span>
            </div>
          ))}"""

new_sp_map = """starters.map((sp,i)=>(
            <div key={i} style={{display:'flex',alignItems:'center',gap:8,background:'rgba(8,16,32,0.7)',border:'1px solid #0f1f35',borderRadius:10,padding:'8px 10px',marginBottom:6}}>
              <span style={{fontSize:13,fontWeight:700,color:'#60a5fa',width:28,flexShrink:0}}>SP{i+1}</span>
              <span style={{flex:1,fontSize:13,fontWeight:600,overflow:'hidden',whiteSpace:'nowrap',textOverflow:'ellipsis'}}>{sp.name}</span>
              <span style={{fontSize:10,color:'#475569',flexShrink:0}}>{sp.decade}</span>
              <span style={{fontSize:10,color:'#94a3b8',flexShrink:0}}>{sp.stats?.era} ERA</span>
              <div style={{display:'flex',flexDirection:'column',gap:2,flexShrink:0}}>
                <button onClick={()=>{
                  if(i===0) return;
                  const k=Object.keys(roster).filter(k=>roster[k]?.role==='SP');
                  const newRoster={...roster};
                  const tmp=newRoster[k[i]]; newRoster[k[i]]=newRoster[k[i-1]]; newRoster[k[i-1]]=tmp;
                  setRoster(newRoster);
                }} disabled={i===0} style={{background:'none',border:'none',cursor:i===0?'default':'pointer',color:i===0?'#1e3a5f':'#60a5fa',fontSize:12,lineHeight:1,padding:'1px 4px'}}>▲</button>
                <button onClick={()=>{
                  if(i===starters.length-1) return;
                  const k=Object.keys(roster).filter(k=>roster[k]?.role==='SP');
                  const newRoster={...roster};
                  const tmp=newRoster[k[i]]; newRoster[k[i]]=newRoster[k[i+1]]; newRoster[k[i+1]]=tmp;
                  setRoster(newRoster);
                }} disabled={i===starters.length-1} style={{background:'none',border:'none',cursor:i===starters.length-1?'default':'pointer',color:i===starters.length-1?'#1e3a5f':'#60a5fa',fontSize:12,lineHeight:1,padding:'1px 4px'}}>▼</button>
              </div>
            </div>
          ))}"""

if old_sp_map in code:
    code = code.replace(old_sp_map, new_sp_map, 1)
    print("Fix 2: SP up/down arrows added")
    fixes += 1
else:
    print("Fix 2: SP map block not matched exactly - checking...")
    idx = code.find("starters.map((sp,i)=>")
    if idx > 0:
        print(repr(code[idx:idx+300]))

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\nTotal fixes applied: {fixes}")
print("Done — run: git add . && git commit -m 'single reroll button, SP reorder arrows' && git push")

# ─── FIX 3: Sheffield FLA 1990s card ─────────────────────────────────────────
idx = code.find("gary-sheffield-1990s")
if idx > 0:
    start = code.rfind('{id:', 0, idx)
    end = code.find('},', start) + 2
    old_sheff = code[start:end]
    new_sheff = "{id:'gary-sheffield-1990s',name:\"Gary Sheffield\",displayName:\"Gary Sheffield\",team:'FLA',decade:'1990s',sampleNote:'',position:'RF',eligiblePositions:['3B','SS','LF','RF','DH'],type:'hitter',role:null,peakYears:[1995,1996,1997],avgWARperYear:3.8,stats:{avg:0.296,hr:26,obp:0.452,slg:0.552,wrcPlus:166,bsr:0.0,dwar:-1.8}},"
    if old_sheff != new_sheff:
        code = code.replace(old_sheff, new_sheff, 1)
        print("Fix 3: Sheffield 1990s → FLA 1995-97 (3.8 WAR)")
        fixes += 1
    else:
        print("Fix 3: Sheffield already correct")

# ─── FIX 4: Kevin Brown FLA 1990s card ───────────────────────────────────────
idx = code.find("kevin-brown-1990s-sp")
if idx > 0:
    start = code.rfind('{id:', 0, idx)
    end = code.find('},', start) + 2
    old_brown = code[start:end]
    new_brown = "{id:'kevin-brown-1990s-sp',name:\"Kevin Brown\",displayName:\"Kevin Brown\",team:'FLA',decade:'1990s',sampleNote:'2yr',position:'SP',eligiblePositions:['SP'],type:'pitcher',role:'SP',peakYears:[1996,1997],avgWARperYear:6.1,stats:{era:2.29,fip:2.91,k9:6.96,whip:1.1,ip:235.05,war:6.61,war9:0.2}},"
    if old_brown != new_brown:
        code = code.replace(old_brown, new_brown, 1)
        print("Fix 4: Kevin Brown 1990s → FLA 1996-97 (6.1 WAR)")
        fixes += 1
    else:
        print("Fix 4: Kevin Brown already correct")

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\nTotal fixes applied: {fixes}")
print("Done — run: git add . && git commit -m 'single reroll, SP arrows, Sheffield/Brown FLA fix' && git push")
