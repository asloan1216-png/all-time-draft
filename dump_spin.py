# READ-ONLY: prints the exact spin + reroll code so we can fix the stuck bug precisely.
import re
code = open('src/App.jsx', encoding='utf-8').read()

def show(label, start_pat, span=900):
    i = code.find(start_pat)
    if i < 0:
        print(f"\n### {label}: NOT FOUND ('{start_pat}')")
        return
    print(f"\n### {label} (at char {i})\n" + "-"*60)
    print(code[i:i+span])
    print("-"*60)

# The main spin retry area
show("MAIN SPIN — retry/selection", "What positions do we still need?", 1400)
# The reroll button onClick
show("REROLL BUTTON onClick", "if(rerollsUsed>=4) return;", 1100)
