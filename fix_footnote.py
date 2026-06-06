# Adds a muted footnote below the Draft Again / Copy buttons explaining that the
# win total reflects a computed talent level + real season variance (not luck/guessing).
import re

PATH='src/App.jsx'
code=open(PATH,encoding='utf-8').read()

if "true talent level calculated from real career stats" in code:
    print("SKIP — footnote already present")
else:
    pat = re.compile(r"(Copy</button>\s*</div>)")
    def repl(m):
        return (m.group(1) +
            "\n        <div style={{fontSize:11,color:'#475569',lineHeight:1.5,marginTop:16,fontStyle:'italic',textAlign:'center',maxWidth:440,marginLeft:'auto',marginRight:'auto'}}>"
            "Every roster has a true talent level calculated from real career stats. "
            "Each season simulates 162 games around that talent \u2014 so just like real baseball, a great team won\u2019t post the exact same record twice. "
            "The expected range shows where this roster lands in a typical year."
            "</div>")
    code, n = pat.subn(repl, code, count=1)
    if n:
        open(PATH,'w',encoding='utf-8').write(code)
        print("OK — footnote added below Draft Again / Copy")
    else:
        print("MISS — Copy button anchor not found")
