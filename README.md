# Barcode_sorting

Program is used for barcode sorting.
Checks the scanned suspected barcode against a list of known NOK barcodes, then writes the scanned barcode into a txt file depending on the result.
Warns the user if input language is hungarian (scans "ö" instead of "0"), character count doesnt match, or the barcode has previously been scanned before.
Keeps count of OK/NOK barcodes.
