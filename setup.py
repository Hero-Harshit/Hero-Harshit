import os

files = ['github-stats.svg', 'streak-stats.svg', 'top-langs.svg', 'trophies.svg', 'productivity.svg']
for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        dark_name = file.replace('.svg', '-dark.svg')
        light_name = file.replace('.svg', '-light.svg')
        
        with open(dark_name, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Create light version
        light_content = content
        light_content = light_content.replace('fill="#151515"', 'fill="#ffffff"')
        light_content = light_content.replace('fill="#fff"', 'fill="#333333"')
        light_content = light_content.replace('fill="#ffffff"', 'fill="#333333"')
        light_content = light_content.replace('fill="#fffefe"', 'fill="#333333"')
        light_content = light_content.replace('fill="#000000"', 'fill="#f0f0f0"')
        
        with open(light_name, 'w', encoding='utf-8') as f:
            f.write(light_content)
        print(f'Created {dark_name} and {light_name}')
