import re

file = 'card-memory-marbles.svg'

with open(file, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the background rect entirely
content = re.sub(r'<!-- Icon Container -->\s*<rect[^>]+>\s*', '<!-- Icon Container -->\n    ', content)

with open(file, 'w', encoding='utf-8') as f:
    f.write(content)
    
print('Successfully removed background rect from memory marbles svg')
