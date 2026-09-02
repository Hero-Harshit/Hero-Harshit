import re
import os

files = [
    'card-nxt-health.svg',
    'card-memory-marbles.svg',
    'card-monever.svg'
]

d = r'd:\All Codes ✔️\Readme'

for svg_file in files:
    svg_path = os.path.join(d, svg_file)
    
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
        
    # We want to replace x="2" y="2" width="28" height="28" preserveAspectRatio="xMidYMid meet"
    # with x="0" y="0" width="32" height="32" preserveAspectRatio="xMidYMid slice"
    # We will use regex to find and replace these attributes in the <image tag
    
    svg_content = re.sub(
        r'x="2" y="2" width="28" height="28" preserveAspectRatio="xMidYMid meet"',
        r'x="0" y="0" width="32" height="32" preserveAspectRatio="xMidYMid slice"',
        svg_content
    )
    
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
        
print("Updated image attributes successfully")
