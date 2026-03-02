import re
import json


def load_receipt(file_path):
    """Load a receipt text file, guessing or falling back to a sensible encoding.

    The example data is in Cyrillic (Windows-1251), so opening as UTF-8
    results in mojibake.  Try a quick detection and decode accordingly,
    but default to cp1251 if detection is inconclusive.
    """

    # read raw bytes first so we can detect the encoding
    with open(file_path, 'rb') as f:
        raw = f.read()

    # simple heuristic: if utf-8 decoding works, use it; otherwise use cp1251
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        # receipts in our tests are Windows‑1251 encoded
        return raw.decode('cp1251')


def parse_products(text):
    """
    Извлекает:
    - название
    - количество
    - цену за единицу
    - итог по позиции
    """

    pattern = r'''
        \d+\.\n
        (?P<name>.+?)\n
        (?P<qty>\d+,\d+)\s*x\s*
        (?P<unit_price>[\d\s]+,\d{2})\n
        (?P<total>[\d\s]+,\d{2})
    '''

    matches = re.finditer(pattern, text, re.VERBOSE)

    products = []

    for m in matches:
        qty = float(m.group("qty").replace(",", "."))
        unit_price = float(m.group("unit_price").replace(" ", "").replace(",", "."))
        total = float(m.group("total").replace(" ", "").replace(",", "."))

        products.append({
            "name": m.group("name").strip(),
            "quantity": qty,
            "unit_price": unit_price,
            "total_price": total
        })

    return products


def extract_total(text):
    match = re.search(r'ИТОГО:\n([\d\s]+,\d{2})', text)
    if match:
        return float(match.group(1).replace(" ", "").replace(",", "."))
    return None


def extract_datetime(text):
    match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})', text)
    if match:
        return {
            "date": match.group(1),
            "time": match.group(2)
        }
    return None


def extract_payment_method(text):
    match = re.search(r'(Банковская карта|Наличные)', text)
    return match.group(1) if match else "Unknown"


def main():
    import sys
    import os

    # make sure the output stream is capable of emitting utf-8 characters
    # (PowerShell / Windows default encoding is often cp1252 which will
    # mangle Cyrillic).  ``reconfigure`` is available on Python 3.7+.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # ``raw.txt`` lives next to this module so build an absolute path; it
    # makes running the script from elsewhere (or via full python.exe
    # invocation) more reliable.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    receipt_path = os.path.join(script_dir, "raw.txt")

    try:
        text = load_receipt(receipt_path)
    except FileNotFoundError:
        sys.stderr.write(f"receipt file not found: {receipt_path}\n")
        sys.exit(1)

    products = parse_products(text)
    receipt_total = extract_total(text)

    calculated_total = round(sum(p["total_price"] for p in products), 2)

    output = {
        "products": products,
        "items_count": len(products),
        "calculated_total": calculated_total,
        "receipt_total": receipt_total,
        "totals_match": calculated_total == receipt_total,
        "date_time": extract_datetime(text),
        "payment_method": extract_payment_method(text)
    }

    print(json.dumps(output, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()