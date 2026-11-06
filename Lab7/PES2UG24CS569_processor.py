import math
import re

def verify_isbn10_format(isbn_str):
    """Return a summary of a well-formed ISBN-10, or None if the input is not one."""
    if not isinstance(isbn_str, str):
        return None
    cleaned = isbn_str.replace('-', '').strip()
    # ASCII-only on purpose: str.isdigit() accepts characters like '²' that int() rejects.
    if not re.fullmatch(r"[0-9]{9}[0-9Xx]", cleaned):
        return None
    first_digit = int(cleaned[0])
    group_code = cleaned[1:4]
    check_char = cleaned[9].upper()
    return f"Group {group_code}: Starts {first_digit}, Checksum {check_char}"

def calculate_depreciation_factor(book_age_str):
    """Return a factor in [0.1, 1.0] for 'age/lifespan', or None if the input is invalid."""
    if not isinstance(book_age_str, str):
        return None
    parts = book_age_str.split('/')
    if len(parts) != 2:
        return None
    try:
        age = float(parts[0])
        life = float(parts[1])
    except ValueError:
        return None
    # Reject nan/inf, negative ages and zero/negative lifespans (division by zero).
    if not (math.isfinite(age) and math.isfinite(life)) or age < 0 or life <= 0:
        return None
    depreciation = 1.0 - (age / life)
    return round(max(0.1, depreciation), 2)

def lookup_condition_multiplier(condition_code):
    """Return the multiplier for a known condition grade, or None if unknown."""
    if not isinstance(condition_code, str):
        return None
    grade = condition_code.strip().upper()
    multipliers = {
        "MINT": 1.25,
        "LIKE_NEW": 1.00,
        "VERY_GOOD": 0.80,
        "GOOD": 0.60,
        "POOR": 0.30
    }
    return multipliers.get(grade)

def main():
    print("==== Running verify_isbn10_format ====")
    isbn_in = input("Enter ISBN-10 (e.g. 0-306-40615-2): ")
    result = verify_isbn10_format(isbn_in)
    print(result if result is not None else "Invalid ISBN-10 format")

    print("\n==== Running calculate_depreciation_factor ====")
    age_in = input("Enter age/lifespan in years (e.g. 3/10): ")
    factor = calculate_depreciation_factor(age_in)
    print("Depreciation Factor:", factor if factor is not None else "Invalid age/lifespan")

    print("\n==== Running lookup_condition_multiplier ====")
    cond_in = input("Enter condition (e.g. MINT, GOOD, POOR): ")
    multiplier = lookup_condition_multiplier(cond_in)
    print("Multiplier:", multiplier if multiplier is not None else "Unknown condition")

if __name__ == "__main__":
    main()
