import os

dummy_btw_bytes = (
    b"Synthetic BarTender Fixture (c) Test Data Only \x00\x01\x02\x00"
    b"Edition: Test, Version: 99.00 Build Number: 4242 Format Version: 99001\x00\x00"
    b"Fixture Printer (300 dpi) - SYNTHETIC-USB\x00"
    b"Product description: FROZEN BLUEBERRY CUBES 42x42 MM\x00"
    b"INGREDIENTS: BLUEBERRY PUREE, WATER\x00"
    b"FOR DEMONSTRATION PURPOSES ONLY\x00"
    b"Net weight: 250 g\x00"
    b"Gross Weight: 275 g\x00"
    b"ORIGIN: TEST REGION\x00"
    b"Exporter Name: EXAMPLE FOODS LAB\x00"
    b"Importer: SAMPLE LABELS WORKSHOP\x00"
    b"123 Example Avenue, Testville, ZZ 00000\x00"
    b"Tel: 0000000000\x00"
    b"PRODUCTION DATE : 15/07/2026\x00"
    b"EXPIRY DATE : 15/07/2027\x00"
    b"STORAGE : KEEP IN A SIMULATED COOL ENVIRONMENT\x00"
    b"LOT CODE: DEMO-260715-B42\x00"
)

os.makedirs("samples", exist_ok=True)

with open("samples/sample_label.btw", "wb") as f:
    f.write(dummy_btw_bytes)

print("[✔] Successfully created dummy file: 'samples/sample_label.btw'")