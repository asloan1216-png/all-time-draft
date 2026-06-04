import re

with open('src/App.jsx','r', encoding='utf-8') as f:
    code = f.read()

fixed = 0

# The real fix: during decade reroll animation, hide the team entirely
# and only show the decade cycling. Reveal both at the end.
# Do this by making the SlotMachine hide the team when rerollMode='decade'

# Find the SlotMachine display section and add rerollMode awareness
old_display = """  const teamOnly=decadeMode&&lockedDecade;
  const decadeOnly=decadeMode&&!lockedDecade;
  return(
    <div style={{textAlign:'center',background:'rgba(6,12,24,0.95)',border:'2px solid #1e3a5f',borderRadius:16,padding:'16px 24px',width:'100%',maxWidth:360}}>
      <div style={{fontSize:9,letterSpacing:4,color:'#334155',marginBottom:10}}>SLOT MACHINE</div>
      <div style={{display:'flex',alignItems:'center',justifyContent:'center',gap:10}}>
        {!decadeOnly&&<div style={{fontSize:24,fontWeight:900,color:spinning?'#1e3a5f':'#f59e0b',transition:'color .15s',fontFamily:'Georgia,serif'}}>{disp.team||'???'}</div>}
        {!teamOnly&&!decadeOnly&&<div style={{fontSize:18,color:'#0f1f35'}}>·</div>}
        {!teamOnly&&<div style={{fontSize:24,fontWeight:900,color:spinning?'#1e3a5f':'#60a5fa',transition:'color .15s',fontFamily:'Georgia,serif'}}>{disp.decade}</div>}
      </div>"""

new_display = """  const teamOnly=decadeMode&&lockedDecade;
  const decadeOnly=decadeMode&&!lockedDecade;
  const hideTeamDuringAnim=spinning&&rerollMode==='decade';
  return(
    <div style={{textAlign:'center',background:'rgba(6,12,24,0.95)',border:'2px solid #1e3a5f',borderRadius:16,padding:'16px 24px',width:'100%',maxWidth:360}}>
      <div style={{fontSize:9,letterSpacing:4,color:'#334155',marginBottom:10}}>SLOT MACHINE</div>
      <div style={{display:'flex',alignItems:'center',justifyContent:'center',gap:10}}>
        {!decadeOnly&&!hideTeamDuringAnim&&<div style={{fontSize:24,fontWeight:900,color:spinning?'#1e3a5f':'#f59e0b',transition:'color .15s',fontFamily:'Georgia,serif'}}>{disp.team||'???'}</div>}
        {!teamOnly&&!decadeOnly&&!hideTeamDuringAnim&&<div style={{fontSize:18,color:'#0f1f35'}}>·</div>}
        {!teamOnly&&<div style={{fontSize:24,fontWeight:900,color:spinning?'#1e3a5f':'#60a5fa',transition:'color .15s',fontFamily:'Georgia,serif'}}>{disp.decade}</div>}
      </div>"""

if old_display in code:
    code = code.replace(old_display, new_display, 1)
    fixed += 1
    print("Fixed: hide team during decade reroll animation")
else:
    print("Display block not found - checking variant...")

with open('src/App.jsx','w', encoding='utf-8') as f:
    f.write(code)

print(f"\nTotal fixed: {fixed}")
print("Done — now run: git add . && git commit -m 'fix decade reroll animation' && git push")
