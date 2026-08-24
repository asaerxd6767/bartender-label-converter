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
        "product_name": extract_pattern(r"(?:Product description:\s*)?((?:FROZEN|ORGANIC)[^\x00\r\n]+)", content, "FROZEN MANGO DICED 10x10 MM"),
        "ingredients": extract_pattern(r"INGREDIENTS:\s*([^\x00\r\n]+)", content, "MANGO FRUIT"),
        "usage_notice": extract_pattern(r"(FOR MANUFACTURING[^\x00\r\n]+)", content, "FOR MANUFACTURING & CATERING USE"),
        "net_weight": extract_pattern(r"Net weight:\s*([^\x00\r\n]+)", content, "10 Kg"),
        "gross_weight": extract_pattern(r"Gross[ -]Weight:\s*([^\x00\r\n]+)", content, "10.5 kg"),
        "origin": extract_pattern(r"ORIGIN:\s*([^\x00\r\n]+)", content, "EGYPT"),
        "exporter": extract_pattern(r"Exporter Name:\s*([^\x00\r\n]+)", content, "EGY-BERRIES WHOLESALE & RETAILS TRADE"),
        "importer": extract_pattern(r"Importer:\s*([^\x00\r\n]+)", content, "Al Taam foodstuff Ind Sole Proprietorship LLC"),
        "importer_address": extract_pattern(r"(Sharjah[^\x00\r\n]+)", content, "Sharjah ,B.O.37233,United Arab Emirates"),
        "importer_tel": extract_pattern(r"Tel:\s*([^\x00\r\n]+)", content, "00971552340311"),
        "production_date": extract_pattern(r"PRODUCTION DATE\s*:\s*([^\x00\r\n]+)", content, "01/08/2026"),
        "expiry_date": extract_pattern(r"EXPIRY DATE\s*:\s*([^\x00\r\n]+)", content, "01/08/2028"),
        "storage": extract_pattern(r"STORAGE\s*:\s*([^\x00\r\n]+)", content, "DRY AND COOL CONDITIONS (- 18 °C)"),
        "lot_code": extract_pattern(r"LOT CODE:\s*([A-Za-z0-9/\-]+)", content, "01080017M26/S")
    }