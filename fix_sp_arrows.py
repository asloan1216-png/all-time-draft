import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Find the full starters.map block by position
start = code.find('starters.map((sp,i)=>(')
end = code.find('))}', start) + 3
old_block = code[start:end]
print("Found block, length:", len(old_block))
print("Last 100 chars:", repr(old_block[-100:]))

new_block = """starters.map((sp,i)=>(
            <div key={i} style={{display:'flex',alignItems:'center',gap:8,background:'rgba(8,16,32,0.7)',border:'1px solid #0f1f35',borderRadius:10,padding:'8px 10px',marginBottom:6}}>
              <span style={{fontSize:13,fontWeight:700,color:'#60a5fa',width:28,flexShrink:0}}>SP{i+1}</span>
              <span style={{flex:1,fontSize:13,fontWeight:600,overflow:'hidden',whiteSpace:'nowrap',textOverflow:'ellipsis'}}>{sp.name}</span>
              <span style={{fontSize:10,color:'#475569',flexShrink:0}}>{sp.decade}</span>
              <span style={{fontSize:10,color:'#94a3b8',flexShrink:0}}>{sp.stats?.era} ERA</span>
              <div style={{display:'flex',flexDirection:'column',gap:1,flexShrink:0}}>
                <button onClick={()=>{if(i===0)return;const spKeys=['sp1','sp2','sp3','sp4','sp5'].filter(k=>roster[k]);const a=spKeys[i-1],b=spKeys[i];const nr={...roster};const tmp=nr[a];nr[a]=nr[b];nr[b]=tmp;onRosterChange(nr);}} disabled={i===0} style={{background:'none',border:'none',cursor:i===0?'default':'pointer',color:i===0?'#1e3a5f':'#60a5fa',fontSize:11,lineHeight:1,padding:'1px 3px'}}>▲</button>
                <button onClick={()=>{if(i===starters.length-1)return;const spKeys=['sp1','sp2','sp3','sp4','sp5'].filter(k=>roster[k]);const a=spKeys[i],b=spKeys[i+1];const nr={...roster};const tmp=nr[a];nr[a]=nr[b];nr[b]=tmp;onRosterChange(nr);}} disabled={i===starters.length-1} style={{background:'none',border:'none',cursor:i===starters.length-1?'default':'pointer',color:i===starters.length-1?'#1e3a5f':'#60a5fa',fontSize:11,lineHeight:1,padding:'1px 3px'}}>▼</button>
              </div>
            </div>
          ))})"""

code = code[:start] + new_block + code[end:]
print("Replaced!")

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Done — run: git add . && git commit -m 'fix SP arrows direct swap' && git push")
