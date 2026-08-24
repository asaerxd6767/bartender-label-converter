import os

dummy_btw_bytes = (
    b"Bar Tender Format File (c) 1992-2001 Seagull Scientific, Inc \x00\x01\x02\x00"
    b"Edition: Enterprise, Version: 7.00 Build Number: 934 Format Version: 70005\x00\x00"
    b"iDPRT iF4 (203 dpi) - TSPL USB001\x00"
    b"Product description: ORGANIC FROZEN STRAWBERRIES 15x15 MM\x00"
    b"INGREDIENTS: STRAWBERRY FRUIT\x00"
    b"FOR MANUFACTURING & CATERING USE\x00"
    b"Net weight: 12 Kg\x00"
    b"Gross Weight: 12.8 kg\x00"
    b"ORIGIN: EGYPT\x00"
    b"Exporter Name: ACME EXPORT & TRADING CO\x00"
    b"Importer: GLOBAL FOOD IMPORTS LLC\x00"
    b"Sharjah, P.O. Box 99999, United Arab Emirates\x00"
    b"Tel: 0097140000000\x00"
    b"PRODUCTION DATE : 01/01/2026\x00"
    b"EXPIRY DATE : 01/01/2028\x00"
    b"STORAGE : DRY AND COOL CONDITIONS (-18 degree C)\x00"
    b"LOT CODE: ST20260101-LOT1\x00"
)

os.makedirs("samples", exist_ok=True)

with open("samples/sample_label.btw", "wb") as f:
    f.write(dummy_btw_bytes)

print("[✔] Successfully created dummy file: 'samples/sample_label.btw'")