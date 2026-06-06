# Two features:
#   #5 — Show staff quality (rotation + bullpen RA9) on the results screen so the
#        now-working pitching is visible to players.
#   #6 — "Replay Season" button: re-simulate the SAME roster to chase a better
#        year, leaning into the new variance.
import re

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

fixes = 0
def report(name, ok):
    global fixes
    print(("OK  " if ok else "MISS") + " — " + name)
    if ok: fixes += 1

# ─────────────────────────────────────────────────────────────────────
# #5a — staffRunsAllowedPerGame returns a breakdown instead of just a number
# ─────────────────────────────────────────────────────────────────────
old_ret_staff = "  // Hard floor 2.4 — still better than any real team's full season, but reachable only by a perfect staff.\n  return Math.max(2.4, ra);"
new_ret_staff = ("  // Hard floor 2.4 — still better than any real team's full season, but reachable only by a perfect staff.\n"
                 "  return { ra: Math.max(2.4, ra), spRA9: Math.round(spRA*100)/100, rpRA9: Math.round(rpRA*100)/100 };")
ok = old_ret_staff in code
if ok:
    code = code.replace(old_ret_staff, new_ret_staff, 1)
report("#5a staff function returns breakdown", ok)

# #5b — update the call site in simulate() to read .ra and capture breakdown
old_call = "  let rapg = staffRunsAllowedPerGame(starters, relievers, hitters);"
new_call = ("  const staff = staffRunsAllowedPerGame(starters, relievers, hitters);\n"
            "  let rapg = staff.ra;")
ok = old_call in code
if ok:
    code = code.replace(old_call, new_call, 1)
report("#5b simulate reads staff.ra", ok)

# #5c — add spRA9/rpRA9 to the result object
old_obj = "    wins, losses:162-wins, winPct, rawWinPct,"
new_obj = "    wins, losses:162-wins, winPct, rawWinPct,\n    spRA9: staff.spRA9, rpRA9: staff.rpRA9,"
ok = old_obj in code
if ok:
    code = code.replace(old_obj, new_obj, 1)
report("#5c result carries spRA9/rpRA9", ok)

# #5d — show two rows on the results screen (Rotation RA9 + Bullpen RA9)
old_rows = "              ['Team wRC+', `${result.avgWRC} (${result.avgWRC>=100?'+':''}${result.avgWRC-100}% offense)`],"
new_rows = ("              ['Team wRC+', `${result.avgWRC} (${result.avgWRC>=100?'+':''}${result.avgWRC-100}% offense)`],\n"
            "              ...(result.spRA9!=null ? [['Rotation RA9', result.spRA9.toFixed(2)]] : []),\n"
            "              ...(result.rpRA9!=null ? [['Bullpen RA9', result.rpRA9.toFixed(2)]] : []),")
ok = old_rows in code
if ok:
    code = code.replace(old_rows, new_rows, 1)
report("#5d results screen shows rotation/bullpen RA9", ok)

# ─────────────────────────────────────────────────────────────────────
# #6 — Replay Season button
# ─────────────────────────────────────────────────────────────────────
# 6a — reset the count-up animation whenever a NEW result object arrives,
#      so replay re-triggers the dramatic count.
old_anim = "  },[result.wins]);"
new_anim = "  },[result]);  // re-run the count-up on every fresh sim (incl. replays)"
ok = old_anim in code
if ok:
    code = code.replace(old_anim, new_anim, 1)
report("#6a animation re-triggers on replay", ok)

# Also reset 'show' at the start of the effect so stats fade in fresh each replay
old_eff = "  useEffect(()=>{\n    let n=0;const t=result.wins;"
new_eff = "  useEffect(()=>{\n    setShow(false); setAnim(0);\n    let n=0;const t=result.wins;"
ok = old_eff in code
if ok:
    code = code.replace(old_eff, new_eff, 1)
report("#6b animation state resets each replay", ok)

# 6c — add onReplay prop to ResultsScreen signature
old_sig = "function ResultsScreen({result,roster,lineup,onReset,onShare}){"
new_sig = "function ResultsScreen({result,roster,lineup,onReset,onShare,onReplay}){"
ok = old_sig in code
if ok:
    code = code.replace(old_sig, new_sig, 1)
report("#6c ResultsScreen accepts onReplay", ok)

# 6d — add the Replay button next to Draft Again / Copy
old_btns = """        <div style={{display:'flex',gap:10}}>
          <button onClick={onReset} style={{flex:1,background:'linear-gradient(135deg,#f59e0b,#d97706)',color:'#000',border:'none',borderRadius:12,padding:'14px 8px',fontWeight:900,fontSize:14,cursor:'pointer',letterSpacing:0,whiteSpace:'nowrap'}}>DRAFT AGAIN</button>
          <button onClick={onShare} style={{flex:1,background:'rgba(96,165,250,0.08)',border:'1px solid #3b82f6',color:'#93c5fd',borderRadius:12,padding:'15px',fontWeight:700,fontSize:13,cursor:'pointer'}}>📋 Copy</button>
        </div>"""
new_btns = """        {show&&onReplay&&(
          <button onClick={onReplay} style={{width:'100%',marginBottom:10,background:'rgba(74,222,128,0.07)',border:'1px solid rgba(74,222,128,0.35)',color:'#4ade80',borderRadius:12,padding:'13px',fontWeight:700,fontSize:13,cursor:'pointer',letterSpacing:0.5}}>🔄 Replay Season <span style={{color:'#475569',fontWeight:400}}>· same roster, new luck</span></button>
        )}
        <div style={{display:'flex',gap:10}}>
          <button onClick={onReset} style={{flex:1,background:'linear-gradient(135deg,#f59e0b,#d97706)',color:'#000',border:'none',borderRadius:12,padding:'14px 8px',fontWeight:900,fontSize:14,cursor:'pointer',letterSpacing:0,whiteSpace:'nowrap'}}>DRAFT AGAIN</button>
          <button onClick={onShare} style={{flex:1,background:'rgba(96,165,250,0.08)',border:'1px solid #3b82f6',color:'#93c5fd',borderRadius:12,padding:'15px',fontWeight:700,fontSize:13,cursor:'pointer'}}>📋 Copy</button>
        </div>"""
ok = old_btns in code
if ok:
    code = code.replace(old_btns, new_btns, 1)
report("#6d Replay button added", ok)

# 6e — wire onReplay where ResultsScreen is rendered (re-run simulate on same roster)
old_render = "<ResultsScreen result={result} roster={roster} lineup={lineup} onReset={reset}"
new_render = "<ResultsScreen result={result} roster={roster} lineup={lineup} onReplay={()=>{const r=simulate(roster,lineup,decadeMode); if(r){ if(salaryMode){r.salaryMode=true;r.budgetSpent=budgetSpent;r.budgetTotal=SALARY_CAP_BUDGET;} if(decadeMode)r.decadeMode=true; setResult(r);} }} onReset={reset}"
ok = old_render in code
if ok:
    code = code.replace(old_render, new_render, 1)
report("#6e onReplay wired to re-simulate same roster", ok)

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

print(f"\n{fixes}/10 applied")
if fixes == 10:
    print("SUCCESS — staff quality shown + replay button live.")
else:
    print("Some hunks missed — do NOT push; report the MISS lines back.")
print("If 10/10: git add . && git commit -m 'show staff RA9 + replay season button' && git push")
