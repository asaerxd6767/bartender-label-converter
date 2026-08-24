from weasyprint import HTML
from .barcode import generate_code39_base64

def generate_label_pdf(data: dict, output_pdf_path: str, output_html_path: str = None):
    """Renders extracted data into a printable HTML & PDF label."""
    barcode_b64 = generate_code39_base64(data.get("lot_code", "000000"))

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Label Preview</title>
    <style>
        @page {{ size: 105mm 150mm; margin: 0; background-color: #ffffff; }}
        body {{ margin: 0; padding: 5mm; font-family: Arial, sans-serif; color: #000000; background-color: #ffffff; }}
        * {{ box-sizing: border-box; }}
        .label-container {{ width: 95mm; height: 140mm; margin: 0 auto; border: 2px solid #000; padding: 4mm; }}
        .header-box {{ border-bottom: 2px solid #000; padding-bottom: 3mm; margin-bottom: 2mm; text-align: center; }}
        .product-title {{ font-size: 13pt; font-weight: 900; text-transform: uppercase; margin: 0 0 2mm 0; }}
        .subtitle {{ font-size: 9.5pt; font-weight: bold; margin: 1mm 0; text-transform: uppercase; }}
        .badge-use {{ background-color: #000; color: #fff; text-align: center; font-weight: bold; font-size: 8pt; padding: 1.5mm 0; margin: 2mm 0 0 0; text-transform: uppercase; }}
        .section-box {{ border-bottom: 1.5px solid #000; padding: 2mm 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        td {{ width: 50%; font-size: 9pt; font-weight: bold; vertical-align: top; }}
        .row {{ margin: 1.5mm 0; font-size: 9pt; line-height: 1.4; }}
        .label-title {{ font-weight: bold; }}
        .storage-box {{ background-color: #f2f2f2; border: 1px dashed #000; padding: 2mm; margin: 2mm 0; text-align: center; font-size: 8.5pt; font-weight: bold; }}
        .barcode-container {{ text-align: center; margin-top: 2mm; }}
        .barcode-container img {{ max-width: 95%; height: auto; }}
    </style>
</head>
<body>
    <div class="label-container">
        <div class="header-box">
            <div class="product-title">{data.get('product_name')}</div>
            <div class="subtitle">INGREDIENTS: {data.get('ingredients')}</div>
            <div class="badge-use">{data.get('usage_notice')}</div>
        </div>

        <div class="section-box">
            <table>
                <tr>
                    <td>Net weight: {data.get('net_weight')}</td>
                    <td>Gross Weight: {data.get('gross_weight')}</td>
                </tr>
            </table>
        </div>

        <div class="section-box">
            <div class="row"><span class="label-title">ORIGIN:</span> {data.get('origin')}</div>
            <div class="row"><span class="label-title">Exporter:</span> {data.get('exporter')}</div>
            <div class="row" style="margin-top: 1.5mm;">
                <span class="label-title">Importer:</span><br>
                {data.get('importer')}<br>
                {data.get('importer_address')}<br>
                Tel: {data.get('importer_tel')}
            </div>
        </div>

        <div class="section-box">
            <table>
                <tr>
                    <td>PRODUCTION DATE:<br><span style="font-size:10pt; font-weight:900;">{data.get('production_date')}</span></td>
                    <td>EXPIRY DATE:<br><span style="font-size:10pt; font-weight:900;">{data.get('expiry_date')}</span></td>
                </tr>
            </table>
        </div>

        <div class="storage-box">
            STORAGE: {data.get('storage')}
        </div>

        <div class="barcode-container">
            <div style="font-size: 8.5pt; font-weight: bold; margin-bottom: 1mm;">LOT CODE: {data.get('lot_code')}</div>
            <img src="data:image/svg+xml;base64,{barcode_b64}" alt="Barcode">
        </div>
    </div>
</body>
</html>
"""

    if output_html_path:
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    HTML(string=html_content).write_pdf(output_pdf_path)