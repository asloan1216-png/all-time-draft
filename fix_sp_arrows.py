with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0

# 1. Pass roster and lineup into ResultsScreen
old_rs = "<ResultsScreen result={result} onReset={reset} onShare={()=>navigator.clipboard?.writeText(`All-Time Draft\\n${result.wins}-${result.losses} | ${result.benchmark?.label}`).catch(()=>{})}/>"
new_rs = "<ResultsScreen result={result} roster={roster} lineup={lineup} onReset={reset} onShare={()=>navigator.clipboard?.writeText(`All-Time Draft\\n${result.wins}-${result.losses} | ${result.benchmark?.label}`).catch(()=>{})}/>"
if old_rs in code:
    code = code.replace(old_rs, new_rs, 1)
    print("Fix 1: roster+lineup passed to ResultsScreen")
    fixes += 1

# 2. Update ResultsScreen signature and add roster display
old_sig = "function ResultsScreen({result,onReset,onShare}){"
new_sig = "function ResultsScreen({result,roster,lineup,onReset,onShare}){"
if old_sig in code:
    code = code.replace(old_sig, new_sig, 1)
    print("Fix 2: ResultsScreen signature updated")
    fixes += 1

# 3. Add lineup display before the Draft Again button
old_buttons = """        <div style={{display:'flex',gap:10}}>
          <button onClick={onReset} style={{flex:1,background:'linear-gradient(135deg,#f59e0b,#d97706)',color:'#000',border:'none',borderRadius:12,padding:'14px 8px',fontWeight:900,fontSize:14,cursor:'pointer',letterSpacing:0,whiteSpace:'nowrap'}}>DRAFT AGAIN</button>
          <button onClick={onShare} style={{flex:1,background:'rgba(96,165,250,0.08)',border:'1px solid #3b82f6',color:'#93c5fd',borderRadius:12,padding:'15px',fontWeight:700,fontSize:13,cursor:'pointer'}}>📋 Copy</button>
        </div>"""

new_buttons = """        {show&&roster&&(
          <div style={{marginTop:4,marginBottom:24,textAlign:'left'}}>
            <div style={{fontSize:9,letterSpacing:4,color:'#334155',marginBottom:12,textAlign:'center'}}>YOUR ROSTER</div>
            <div style={{fontSize:10,letterSpacing:3,color:'#1e3a5f',marginBottom:6}}>LINEUP</div>
            {lineup&&lineup.filter(Boolean).map((p,i)=>(
              <div key={i} style={{display:'flex',justifyContent:'space-between',padding:'4px 0',borderBottom:'1px solid #080f1e',fontSize:12,gap:8}}>
                <span style={{color:'#475569',width:28,flexShrink:0}}>{p.assignedPos||p.position}</span>
                <span style={{color:'#e2e8f0',flex:1}}>{p.displayName||p.name}</span>
                <span style={{color:'#334155',fontSize:10}}>{p.team} · {p.decade}</span>
              </div>
            ))}
            <div style={{fontSize:10,letterSpacing:3,color:'#1e3a5f',marginBottom:6,marginTop:12}}>ROTATION</div>
            {roster&&['sp1','sp2','sp3','sp4','sp5'].filter(k=>roster[k]).map((k,i)=>{const p=roster[k];return(
              <div key={k} style={{display:'flex',justifyContent:'space-between',padding:'4px 0',borderBottom:'1px solid #080f1e',fontSize:12,gap:8}}>
                <span style={{color:'#60a5fa',width:28,flexShrink:0}}>SP{i+1}</span>
                <span style={{color:'#e2e8f0',flex:1}}>{p.displayName||p.name}</span>
                <span style={{color:'#334155',fontSize:10}}>{p.team} · {p.decade}</span>
              </div>
            );})}
            <div style={{fontSize:10,letterSpacing:3,color:'#1e3a5f',marginBottom:6,marginTop:12}}>BULLPEN</div>
            {roster&&['rp1','rp2','rp3','rp4'].filter(k=>roster[k]).map((k,i)=>{const p=roster[k];return(
              <div key={k} style={{display:'flex',justifyContent:'space-between',padding:'4px 0',borderBottom:'1px solid #080f1e',fontSize:12,gap:8}}>
                <span style={{color:'#a78bfa',width:28,flexShrink:0}}>{p.assignedPos||'RP'}</span>
                <span style={{color:'#e2e8f0',flex:1}}>{p.displayName||p.name}</span>
                <span style={{color:'#334155',fontSize:10}}>{p.team} · {p.decade}</span>
              </div>
            );})}
          </div>
        )}
        <div style={{display:'flex',gap:10}}>
          <button onClick={onReset} style={{flex:1,background:'linear-gradient(135deg,#f59e0b,#d97706)',color:'#000',border:'none',borderRadius:12,padding:'14px 8px',fontWeight:900,fontSize:14,cursor:'pointer',letterSpacing:0,whiteSpace:'nowrap'}}>DRAFT AGAIN</button>
          <button onClick={onShare} style={{flex:1,background:'rgba(96,165,250,0.08)',border:'1px solid #3b82f6',color:'#93c5fd',borderRadius:12,padding:'15px',fontWeight:700,fontSize:13,cursor:'pointer'}}>📋 Copy</button>
        </div>"""

if old_buttons in code:
    code = code.replace(old_buttons, new_buttons, 1)
    print("Fix 3: roster display added to results screen")
    fixes += 1
else:
    print("Fix 3: buttons not matched")

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\nTotal fixes: {fixes}")
print("Done — run: git add . && git commit -m 'show roster on results screen' && git push")
