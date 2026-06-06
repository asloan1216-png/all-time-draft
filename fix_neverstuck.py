# Whitespace-tolerant anti-stuck fix for BOTH spin paths.
#   1) Main spin: 50-attempt retry -> 200 + exhaustive fallback over all valid combos
#      (respects a locked decade, then opens all decades as a last resort).
#   2) Reroll button: currently random with NO needs check -> picks only from
#      team/decade combos that can supply a still-needed position.
# Uses regex with flexible whitespace so it matches regardless of indentation/CRLF.
import re

PATH='src/App.jsx'
code=open(PATH,encoding='utf-8').read()
n_main=n_rr=0

# ---- FIX 1: main spin retry ----
pat_main = re.compile(
    r"\}\s*while\s*\(\s*attempts\s*<\s*50\s*&&\s*!poolHasNeeded\(\s*res\.team\s*,\s*res\.decade\s*\)\s*\)\s*;"
)
repl_main = (
    "} while(attempts<200 && !poolHasNeeded(res.team, res.decade));\n"
    "        if(!poolHasNeeded(res.team,res.decade)){\n"
    "          const _decs=(decadeMode&&lockedDecade)?[lockedDecade]:DECADES;\n"
    "          const _all=[];_decs.forEach(d=>(TEAMS_BY_DECADE[d]||[]).forEach(t=>_all.push({team:t,decade:d})));\n"
    "          let _v=_all.find(c=>poolHasNeeded(c.team,c.decade));\n"
    "          if(!_v&&decadeMode&&lockedDecade){const _a2=[];DECADES.forEach(d=>(TEAMS_BY_DECADE[d]||[]).forEach(t=>_a2.push({team:t,decade:d})));_v=_a2.find(c=>poolHasNeeded(c.team,c.decade));}\n"
    "          if(_v)res=_v;\n"
    "        }"
)
if "const _decs=(decadeMode&&lockedDecade)?[lockedDecade]:DECADES;" in code:
    print("FIX 1: SKIP (already applied)")
    n_main=1
else:
    code, c = pat_main.subn(repl_main, code, count=1)
    if c: print("FIX 1: OK — main spin now 200 + exhaustive fallback"); n_main=1
    else: print("FIX 1: MISS — couldn't find the 50-attempt while loop")

# ---- FIX 2: reroll button needs-aware selection ----
# Match: let res; if(decadeMode&&lockedDecade){ ... } else res=randTeamDecade();
pat_rr = re.compile(
    r"let res;\s*"
    r"if\s*\(\s*decadeMode\s*&&\s*lockedDecade\s*\)\s*\{\s*"
    r"const teams\s*=\s*TEAMS_BY_DECADE\[lockedDecade\]\|\|\[\];\s*"
    r"res\s*=\s*\{\s*team:\s*teams\[Math\.floor\(Math\.random\(\)\*teams\.length\)\]\s*,\s*decade:\s*lockedDecade\s*\};\s*"
    r"\}\s*else\s+res\s*=\s*randTeamDecade\(\);"
)
repl_rr = (
    "let res;\n"
    "                      {\n"
    "                        const _dIds=new Set(Object.values(roster).filter(Boolean).map(p=>p.id));\n"
    "                        const _dNames=new Set(Object.values(roster).filter(Boolean).map(p=>(p.displayName||p.name||'').replace(/ \\d-yr$/,'')));\n"
    "                        const _notD=p=>{if(_dIds.has(p.id))return false;const dn=(p.displayName||p.name||'').replace(/ \\d-yr$/,'');return !_dNames.has(dn);};\n"
    "                        const _need=getNeededPositions(roster);\n"
    "                        const _has=(team,decade)=>players.some(p=>{if(!_notD(p)||p.team!==team||p.decade!==decade)return false;if(p.type==='pitcher')return (p.role==='SP'&&_need.sp>0)||(p.role==='RP'&&_need.rp>0);return _need.hitter.length>0&&p.eligiblePositions.some(pos=>_need.hitter.includes(pos));});\n"
    "                        const _decs=(decadeMode&&lockedDecade)?[lockedDecade]:DECADES;\n"
    "                        let _combos=[];_decs.forEach(d=>(TEAMS_BY_DECADE[d]||[]).forEach(t=>_combos.push({team:t,decade:d})));\n"
    "                        let _valid=_combos.filter(c=>_has(c.team,c.decade));\n"
    "                        if(_valid.length===0){let _a=[];DECADES.forEach(d=>(TEAMS_BY_DECADE[d]||[]).forEach(t=>_a.push({team:t,decade:d})));_valid=_a.filter(c=>_has(c.team,c.decade));}\n"
    "                        res=_valid.length>0?_valid[Math.floor(Math.random()*_valid.length)]:((decadeMode&&lockedDecade)?{team:(TEAMS_BY_DECADE[lockedDecade]||[])[0],decade:lockedDecade}:randTeamDecade());\n"
    "                      }"
)
if "const _has=(team,decade)=>players.some" in code:
    print("FIX 2: SKIP (already applied)")
    n_rr=1
else:
    code, c = pat_rr.subn(lambda m: repl_rr, code, count=1)
    if c: print("FIX 2: OK — reroll button now picks only valid combos"); n_rr=1
    else: print("FIX 2: MISS — couldn't find the reroll random selection")

open(PATH,'w',encoding='utf-8').write(code)
print(f"\n{n_main+n_rr}/2 applied. If 2/2 and it compiles: commit & push.")
