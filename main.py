import argparse
import os
from src.parser import parse_btw_file
from src.pdf_generator import generate_label_pdf

def main():
    parser = argparse.ArgumentParser(description="BarTender (.btw) Label Extractor & PDF Renderer")
    parser.add_argument("-i", "--input", required=True, help="Path to input .btw file")
    parser.add_argument("-o", "--output", default="output_label.pdf", help="Output PDF file path")
    parser.add_argument("--html", action="store_true", help="Save intermediate HTML preview file")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[-] Error: File '{args.input}' not found.")
        return

    print(f"[+] Parsing BarTender file: {args.input}")
    parsed_data = parse_btw_file(args.input)

    html_path = args.output.replace(".pdf", ".html") if args.html else None

    print("[+] Rendering PDF Label...")
    generate_label_pdf(parsed_data, args.output, html_path)
    print(f"[✔] Successfully generated label: {args.output}")

if __name__ == "__main__":
    main()