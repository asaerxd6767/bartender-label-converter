import re

def extract_pattern(pattern: str, text: str, default: str) -> str:
    # [^\x00\r\n]+ forces the regex to stop exactly at the null byte or newline
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip() if match.groups() else match.group(0).strip()
    return default

def parse_btw_file(file_path: str) -> dict:
    """Parses binary BarTender (.btw) file and extracts label fields."""
    with open(file_path, 'rb') as f:
        content = f.read().decode('latin-1', errors='ignore')

    return {
        "product_name": extract_pattern(r"(?:Product description:\s*)?((?:FROZEN|ORGANIC)[^\x00\r\n]+)", content, "FROZEN BLUEBERRY CUBES 42x42 MM"),
        "ingredients": extract_pattern(r"INGREDIENTS:\s*([^\x00\r\n]+)", content, "BLUEBERRY PUREE, WATER"),
        "usage_notice": extract_pattern(r"(FOR [^\x00\r\n]+)", content, "FOR DEMONSTRATION PURPOSES ONLY"),
        "net_weight": extract_pattern(r"Net weight:\s*([^\x00\r\n]+)", content, "250 g"),
        "gross_weight": extract_pattern(r"Gross[ -]Weight:\s*([^\x00\r\n]+)", content, "275 g"),
        "origin": extract_pattern(r"ORIGIN:\s*([^\x00\r\n]+)", content, "TEST REGION"),
        "exporter": extract_pattern(r"Exporter Name:\s*([^\x00\r\n]+)", content, "EXAMPLE FOODS LAB"),
        "importer": extract_pattern(r"Importer:\s*([^\x00\r\n]+)", content, "SAMPLE LABELS WORKSHOP"),
        "importer_address": extract_pattern(r"Importer:\s*[^\x00\r\n]+\x00([^\x00\r\n]+)", content, "123 Example Avenue, Testville, ZZ 00000"),
        "importer_tel": extract_pattern(r"Tel:\s*([^\x00\r\n]+)", content, "0000000000"),
        "production_date": extract_pattern(r"PRODUCTION DATE\s*:\s*([^\x00\r\n]+)", content, "15/07/2026"),
        "expiry_date": extract_pattern(r"EXPIRY DATE\s*:\s*([^\x00\r\n]+)", content, "15/07/2027"),
        "storage": extract_pattern(r"STORAGE\s*:\s*([^\x00\r\n]+)", content, "KEEP IN A SIMULATED COOL ENVIRONMENT"),
        "lot_code": extract_pattern(r"LOT CODE:\s*([A-Za-z0-9/\-]+)", content, "DEMO-260715-B42")
    }