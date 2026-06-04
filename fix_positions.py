import re

with open('src/App.jsx','r', encoding='utf-8') as f:
    code = f.read()

fixes = {
    'Jazz Chisholm Jr.':  ['2B','CF','3B','SS','DH'],
    'Michael Harris II':  ['CF','LF','RF','DH'],
    'Daulton Varsho':     ['C','LF','CF','RF','DH'],
    'Shea Langeliers':    ['C','DH'],
    'Jackson Merrill':    ['CF','LF','RF','DH'],
    'Drake Baldwin':      ['C','DH'],
    'Yainer Diaz':        ['C','DH'],
    'Wilyer Abreu':       ['LF','CF','RF','DH'],
    'Colson Montgomery':  ['SS','DH'],
    'Brice Turang':       ['2B','SS','DH'],
    'Elly De La Cruz':    ['SS','3B','DH'],
    'Ha-Seong Kim':       ['SS','2B','3B','DH'],
    'Anthony Volpe':      ['SS','DH'],
    'Bobby Witt Jr.':     ['SS','3B','DH'],
    'Wander Franco':      ['SS','2B','DH'],
    'Bryson Stott':       ['2B','SS','DH'],
    'Wyatt Langford':     ['LF','CF','RF','DH'],
    'Jarren Duran':       ['CF','LF','RF','DH'],
    'Brandon Marsh':      ['CF','LF','RF','DH'],
    'Isaac Paredes':      ['3B','2B','DH'],
    'Nolan Jones':        ['LF','3B','RF','DH'],
    'Julio Rodr\u00edguez': ['CF','LF','RF','DH'],
    'Jeremy Pe\u00f1a':   ['SS','DH'],
    'Jose Siri':          ['CF','LF','RF','DH'],
    'Pete Crow-Armstrong':['CF','LF','RF','DH'],
    'Andy Pages':         ['RF','LF','DH'],
    'Ryan Jeffers':       ['C','DH'],
    'Zach Neto':          ['SS','DH'],
    'Caleb Durbin':       ['2B','SS','DH'],
    'Royce Lewis':        ['SS','3B','DH'],
    'Jordan Westburg':    ['2B','3B','SS','DH'],
    'Steven Kwan':        ['LF','CF','RF','DH'],
    'Luis Robert Jr.':    ['CF','LF','RF','DH'],
    'Jonathan India':     ['2B','3B','DH'],
    'Noelvi Marte':       ['3B','SS','DH'],
    'Spencer Torkelson':  ['1B','3B','DH'],
    'Riley Greene':       ['LF','CF','RF','DH'],
    'Oneil Cruz':         ['SS','LF','DH'],
    'Jackson Holliday':   ['2B','SS','DH'],
    'CJ Abrams':          ['SS','DH'],
    'Gunnar Henderson':   ['SS','3B','DH'],
    'Masyn Winn':         ['SS','DH'],
    'Matt McLain':        ['SS','2B','DH'],
    'Brayan Rocchio':     ['SS','2B','DH'],
    'Corbin Carroll':     ['CF','LF','RF','DH'],
    'Joe Morgan':         ['2B','DH'],
    'Luis Gonzalez':      ['LF','DH'],
}

fixed = 0
for name, correct_elig in fixes.items():
    new_elig_str = ','.join(f"'{p}'" for p in correct_elig)
    name_escaped = re.escape(name)
    pattern = fr'(displayName:"{name_escaped}"[^}}]*?eligiblePositions:\[)[^\]]+(\])'
    new_code = re.sub(pattern, fr'\g<1>{new_elig_str}\2', code, flags=re.DOTALL)
    if new_code != code:
        code = new_code
        fixed += 1
        print(f"Fixed: {name}")

# Fix decade reroll to keep same team
old_dec = "// Keep same team concept, roll a new decade (pick a decade where this team exists)"
new_dec = "// Roll a new decade only — keep the same team, freeze it in the animation"
if old_dec in code:
    code = code.replace(old_dec, new_dec, 1)
    # Also fix the team selection logic
    old_team = """                    const teamsInDec=TEAMS_BY_DECADE[newDec]||[];
                    const newTeam=teamsInDec[Math.floor(Math.random()*teamsInDec.length)];
                    const newRes={team:newTeam,decade:newDec};
                    // Pick team from new decade upfront before spinning"""
    new_team = """                    const teamsInNewDec=TEAMS_BY_DECADE[newDec]||[];
                    const currentTeam=spinRes.team;"""
    if old_team in code:
        code = code.replace(old_team, new_team, 1)
        print("Fixed: decade reroll keeps same team")

with open('src/App.jsx','w', encoding='utf-8') as f:
    f.write(code)

print(f"\nTotal fixed: {fixed}")
print("Done — now run: git add . && git commit -m 'fix positions and decade reroll' && git push")
