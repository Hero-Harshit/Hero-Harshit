import base64
import os
import re

files = {
    'card-nxt-health.svg': 'Nxt Health Logo.png',
    'card-memory-marbles.svg': 'Memory Marbles Logo.png',
    'card-monever.svg': 'Monever Logo.png'
}

d = r'd:\All Codes ✔️\Readme'

for svg_file, png_file in files.items():
    svg_path = os.path.join(d, svg_file)
    png_path = os.path.join(d, png_file)
    
    with open(png_path, 'rb') as f:
        png_data = f.read()
        b64_str = base64.b64encode(png_data).decode('utf-8')
        
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
        
    # First try replacing existing base64 string
    svg_content, count = re.subn(r'href="data:image/png;base64,[a-zA-Z0-9+/=]+"', f'href="data:image/png;base64,{b64_str}"', svg_content)
    
    if count == 0:
        # If no base64 string is found, try replacing the url-encoded file name
        encoded_png_name = png_file.replace(" ", "%20")
        svg_content = svg_content.replace(f'href="{encoded_png_name}"', f'href="data:image/png;base64,{b64_str}"')
    
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
        
print("Successfully embedded base64 images")
