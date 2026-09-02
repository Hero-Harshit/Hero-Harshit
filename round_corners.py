from PIL import Image, ImageDraw

files = [
    'Nxt Health Logo.png',
    'Monever Logo.png'
]

# 10% corner radius is usually nice for squares
def add_rounded_corners(im, rad):
    mask = Image.new('L', im.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + im.size, radius=rad, fill=255)
    
    # We create a new image to ensure it has an alpha channel
    result = im.copy()
    if result.mode != 'RGBA':
        result = result.convert('RGBA')
    
    result.putalpha(mask)
    return result

for filename in files:
    img = Image.open(filename).convert('RGBA')
    
    # Let's apply a 20px radius, assuming the image is ~200-256px
    # Or proportionally, 15% of width
    rad = int(img.size[0] * 0.15)
    
    rounded_img = add_rounded_corners(img, rad)
    rounded_img.save(filename, optimize=True)
    print(f'Applied {rad}px rounded corners to {filename}')
