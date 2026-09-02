import os

files = ['header.svg', 'quote.svg', 'card-nxt-health.svg', 'card-memory-marbles.svg', 'card-monever.svg']

light_css = '''
    @media (prefers-color-scheme: light) {
        rect[fill="#151515"] { fill: #ffffff !important; stroke: #e1e4e8 !important; }
        .name-title { fill: #24292f !important; }
        .sub-primary, .quote-body { fill: #24292f !important; }
        .sub-secondary, .quote-line, .author-tag { fill: #57606a !important; }
        .terminal-title { fill: #57606a !important; }
        text[fill="#f0f6fc"] { fill: #24292f !important; }
        text[fill="#8b949e"] { fill: #57606a !important; }
    }
'''

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'prefers-color-scheme: light' not in content:
            if '</style>' in content:
                content = content.replace('</style>', light_css + '\n</style>')
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {file}")
