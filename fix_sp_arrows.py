with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Simple approach: swap sp slot values directly in roster
# Replace the starters.map with version that swaps roster['sp1'] <-> roster['sp2'] etc.

old_sp_map = """starters.map((sp,i)=>(
            <div key={i} style={{display:'flex',alignItems:'center',gap:8,background:'rgba(8,16,32,0.7)',border:'1px solid #0f1f35',borderRadius:10,padding:'8px 10px',marginBottom:6}}>
              <span style={{fontSize:13,fontWeight:700,color:'#60a5fa',width:28,flexShrink:0}}>SP{i+1}</span>
              <span style={{flex:1,fontSize:13,fontWeight:600,overflow:'hidden',whiteSpace:'nowrap',textOverflow:'ellipsis'}}>{sp.name}</span>
              <span style={{fontSize:10,color:'#475569',flexShrink:0}}>{sp.decade}</span>
              <span style={{fontSize:10,color:'#94a3b8',flexShrink:0}}>{sp.stats?.era} ERA</span>
              <div style={{display:'flex',flexDirection:'column',gap:1,flexShrink:0}}>
                <button onClick={()=>{if(i===0)return;const o=[...spOrder];[o[i-1],o[i]]=[o[i],o[i-1]];onSpOrderChange(o);}} disabled={i===0} style={{background:'none',border:'none',cursor:i===0?'default':'pointer',color:i===0?'#1e3a5f':'#60a5fa',fontSize:11,lineHeight:1,padding:'1px 3px'}}>▲</button>
                <button onClick={()=>{if(i===starters.length-1)return;const o=[...spOrder];[o[i],o[i+1]]=[o[i+1],o[i]];onSpOrderChange(o);}} disabled={i===starters.length-1} style={{background:'none',border:'none',cursor:i===starters.length-1?'default':'pointer',color:i===starters.length-1?'#1e3a5f':'#60a5fa',fontSize:11,lineHeight:1,padding:'1px 3px'}}>▼</button>
              </div>
            </div>
          ))}"""

new_sp_map = """starters.map((sp,i)=>(
            <div key={i} style={{display:'flex',alignItems:'center',gap:8,background:'rgba(8,16,32,0.7)',border:'1px solid #0f1f35',borderRadius:10,padding:'8px 10px',marginBottom:6}}>
              <span style={{fontSize:13,fontWeight:700,color:'#60a5fa',width:28,flexShrink:0}}>SP{i+1}</span>
              <span style={{flex:1,fontSize:13,fontWeight:600,overflow:'hidden',whiteSpace:'nowrap',textOverflow:'ellipsis'}}>{sp.name}</span>
              <span style={{fontSize:10,color:'#475569',flexShrink:0}}>{sp.decade}</span>
              <span style={{fontSize:10,color:'#94a3b8',flexShrink:0}}>{sp.stats?.era} ERA</span>
              <div style={{display:'flex',flexDirection:'column',gap:1,flexShrink:0}}>
                <button onClick={()=>{
                  if(i===0)return;
                  const spKeys=['sp1','sp2','sp3','sp4','sp5'].filter(k=>roster[k]);
                  const a=spKeys[i-1],b=spKeys[i];
                  onLineupChange&&onLineupChange(lineup);
                  const nr={...roster};const tmp=nr[a];nr[a]=nr[b];nr[b]=tmp;
                  onRosterChange(nr);
                }} disabled={i===0} style={{background:'none',border:'none',cursor:i===0?'default':'pointer',color:i===0?'#1e3a5f':'#60a5fa',fontSize:11,lineHeight:1,padding:'1px 3px'}}>▲</button>
                <button onClick={()=>{
                  if(i===starters.length-1)return;
                  const spKeys=['sp1','sp2','sp3','sp4','sp5'].filter(k=>roster[k]);
                  const a=spKeys[i],b=spKeys[i+1];
                  const nr={...roster};const tmp=nr[a];nr[a]=nr[b];nr[b]=tmp;
                  onRosterChange(nr);
                }} disabled={i===starters.length-1} style={{background:'none',border:'none',cursor:i===starters.length-1?'default':'pointer',color:i===starters.length-1?'#1e3a5f':'#60a5fa',fontSize:11,lineHeight:1,padding:'1px 3px'}}>▼</button>
              </div>
            </div>
          ))}"""

if old_sp_map in code:
    code = code.replace(old_sp_map, new_sp_map, 1)
    print("Fixed: arrows now swap sp1/sp2/sp3 keys directly")
else:
    print("SP map not matched")
    import re
    idx = code.find('starters.map((sp,i)=>')
    print(repr(code[idx:idx+200]))

# Add onRosterChange to LineupBuilder signature
old_sig = "function LineupBuilder({roster,lineup,onLineupChange,rpRoles,onRpRolesChange,onSimulate,spOrder=[0,1,2,3,4],onSpOrderChange})"
new_sig = "function LineupBuilder({roster,lineup,onLineupChange,rpRoles,onRpRolesChange,onSimulate,onRosterChange,spOrder=[0,1,2,3,4],onSpOrderChange})"
if old_sig in code:
    code = code.replace(old_sig, new_sig, 1)
    print("Fixed: onRosterChange added to signature")

# Pass onRosterChange into LineupBuilder call
old_lb = "<LineupBuilder roster={roster} lineup={lineup} onLineupChange={setLineup} rpRoles={rpRoles} onRpRolesChange={setRpRoles} onSimulate={runSim} spOrder={spOrder} onSpOrderChange={setSpOrder}/>"
new_lb = "<LineupBuilder roster={roster} lineup={lineup} onLineupChange={setLineup} rpRoles={rpRoles} onRpRolesChange={setRpRoles} onSimulate={runSim} onRosterChange={setRoster} spOrder={spOrder} onSpOrderChange={setSpOrder}/>"
if old_lb in code:
    code = code.replace(old_lb, new_lb, 1)
    print("Fixed: onRosterChange passed to LineupBuilder")

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Done — run: git add . && git commit -m 'fix SP arrows swap slots' && git push")
