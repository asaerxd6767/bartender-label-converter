import base64

def generate_code39_svg(data: str) -> str:
    """Generates a standalone Code 39 Barcode in SVG format."""
    CODE39_DICT = {
        '0': 'bsbSbSbsB', '1': 'BsbSbsbsB', '2': 'bsBSbsbsB', '3': 'BsBSbsbsb',
        '4': 'bsbSBsbsB', '5': 'BsbSBsbsb', '6': 'bsBSBsbsb', '7': 'bsbSbsBsB',
        '8': 'BsbSbsBsb', '9': 'bsBSbsBsb', 'A': 'BsbsbSbsB', 'B': 'bsBsbSbsB',
        'C': 'BsBsbSbsb', 'D': 'bsbsBSbsB', 'E': 'BsbsBSbsb', 'F': 'bsBsBSbsb',
        'G': 'bsbsbSBsB', 'H': 'BsbsbSBsb', 'I': 'bsBsbSBsb', 'J': 'bsbsBSBsb',
        'K': 'BsbsbsbSB', 'L': 'bsBsbsbSB', 'M': 'BsBsbsbSb', 'N': 'bsbsBsbSB',
        'O': 'BsbsBsbSb', 'P': 'bsBsBsbSb', 'Q': 'bsbsbsBSB', 'R': 'BsbsbsBSb',
        'S': 'bsBsbsBSb', 'T': 'bsbsBsBSb', 'U': 'BSbsbsbsB', 'V': 'bSBsbsbsB',
        'W': 'BSBsbsbsb', 'X': 'bSbsBsbsB', 'Y': 'BSbsBsbsb', 'Z': 'bSBsBsbsb',
        '-': 'bSbsbsBsB', '.': 'BSbsbsBsb', ' ': 'bSBsbsBsb', '$': 'bSbSbSbSb',
        '/': 'bSbSbSbsb', '+': 'bSbSbsbSb', '%': 'bsbSbSbSb', '*': 'bSbsBsBsb'
    }
    
    full_data = f"*{data}*"
    narrow, wide, height = 2, 5, 55
    elements = []
    
    for char in full_data:
        pattern = CODE39_DICT.get(char.upper(), CODE39_DICT['*'])
        for el in pattern:
            if el == 'b': elements.append(('bar', narrow))
            elif el == 'B': elements.append(('bar', wide))
            elif el == 's': elements.append(('space', narrow))
            elif el == 'S': elements.append(('space', wide))
        elements.append(('space', narrow))
        
    total_width = sum(w for _, w in elements) + 20
    svg_parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="{height + 25}" viewBox="0 0 {total_width} {height + 25}">']
    svg_parts.append('<rect width="100%" height="100%" fill="white"/>')
    
    x = 10
    for el_type, w in elements:
        if el_type == 'bar':
            svg_parts.append(f'<rect x="{x}" y="5" width="{w}" height="{height}" fill="black"/>')
        x += w
        
    svg_parts.append(f'<text x="{total_width/2}" y="{height + 20}" font-family="Arial, sans-serif" font-size="13" font-weight="bold" text-anchor="middle">{data}</text>')
    svg_parts.append('</svg>')
    
    return "".join(svg_parts)

def generate_code39_base64(data: str) -> str:
    svg = generate_code39_svg(data)
    return base64.b64encode(svg.encode('utf-8')).decode('utf-8')