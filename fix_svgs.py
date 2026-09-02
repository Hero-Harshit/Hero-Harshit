import re

files = [
    ('card-nxt-health.svg', 'clip-nxt'),
    ('card-monever.svg', 'clip-monever')
]

for file, clip_id in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the background rect entirely
    content = re.sub(r'<!-- Icon Container -->\s*<rect[^>]+>\s*', '<!-- Icon Container -->\n    ', content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
        
print('Successfully removed SVG background rects')
