import pandas as pd

# Read the cpus database
cpus = pd.read_csv('cpus.csv', on_bad_lines='skip')

# Search for the CPUs that are showing as generic
test_cpus = [
    'AMD RYZEN 5 PRO 8540U',
    'AMD RYZEN AI 9 365',
    'AMD RYZEN 9 HX 370',
    'AMD RYZEN 5 PRO 2500U'
]

for cpu in test_cpus:
    # Extract key number
    import re
    number_match = re.search(r'\d{3,4}', cpu)
    if number_match:
        number = number_match.group()
        matches = cpus[cpus['name'].str.contains(number, case=False, na=False)]
        print(f'\n{cpu}:')
        print(f'  Searching for "{number}" in database...')
        print(f'  Found {len(matches)} matches')
        if len(matches) > 0:
            print('  Sample matches:')
            for name in matches['name'].head(5):
                print(f'    - {name}')
        else:
            print('  ❌ NOT FOUND in database - will use Generic')
