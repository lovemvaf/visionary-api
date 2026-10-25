import re

with open('scripts/build_perfect_presentation.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any occurrence of - 1'00"): or similar
fixed = text.replace('1\'00"):', '1p00s):')
fixed = fixed.replace('1\'05"):', '1p05s):')
fixed = fixed.replace('55s):', '55s):')

with open('scripts/build_perfect_presentation.py', 'w', encoding='utf-8') as f:
    f.write(fixed)

print('Successfully cleaned up quotes in scripts/build_perfect_presentation.py')
