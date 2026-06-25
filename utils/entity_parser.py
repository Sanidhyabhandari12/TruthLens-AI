import re


def clean_value(value):
    value = str(value)
    value = value.replace("\n", " ")
    value = value.replace("\t", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip(" :-")


def unique_list(items):
    cleaned = []

    for item in items:
        item = clean_value(item)

        if item and item not in cleaned:
            cleaned.append(item)

    return cleaned


def extract_pan(text):
    pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
    return unique_list(re.findall(pattern, text.upper()))


def extract_gstin(text):
    pattern = r"\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]\b"
    return unique_list(re.findall(pattern, text.upper()))


def extract_dates(text):
    patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b"
    ]

    dates = []

    for pattern in patterns:
        dates.extend(re.findall(pattern, text))

    return unique_list(dates)


def extract_amounts(text):
    patterns = [
        r"(?:₹|Rs\.?|INR)\s?\d{1,3}(?:,\d{2,3})*(?:\.\d+)?",
        r"\b\d{1,3}(?:,\d{2,3})+(?:\.\d+)?\b"
    ]

    amounts = []

    for pattern in patterns:
        amounts.extend(re.findall(pattern, text, flags=re.IGNORECASE))

    return unique_list(amounts)


def extract_names(text):
    names = []

    lines = text.split("\n")

    name_keywords = [
        "name",
        "applicant name",
        "customer name",
        "borrower name",
        "owner name",
        "property owner name",
        "account holder",
        "account holder name"
    ]

    stop_words = [
        "pan",
        "gstin",
        "address",
        "date",
        "amount",
        "turnover",
        "bank",
        "loan",
        "property",
        "account",
        "mobile",
        "email"
    ]

    for line in lines:
        original_line = line.strip()
        lower_line = original_line.lower()

        for keyword in name_keywords:
            if lower_line.startswith(keyword):
                parts = re.split(r":|-", original_line, maxsplit=1)

                if len(parts) > 1:
                    name = clean_value(parts[1])

                    for stop in stop_words:
                        pattern = r"\b" + re.escape(stop) + r"\b"
                        name = re.split(pattern, name, flags=re.IGNORECASE)[0]

                    name = clean_value(name)

                    if len(name.split()) >= 2:
                        names.append(name.title())

    return unique_list(names)


def extract_addresses(text):
    addresses = []

    lines = text.split("\n")

    address_keywords = [
        "address",
        "residential address",
        "permanent address",
        "communication address",
        "property address",
        "office address",
        "business address"
    ]

    stop_words = [
        "pan",
        "gstin",
        "date",
        "amount",
        "turnover",
        "loan",
        "mobile",
        "email",
        "account"
    ]

    for line in lines:
        original_line = line.strip()
        lower_line = original_line.lower()

        for keyword in address_keywords:
            if lower_line.startswith(keyword):
                parts = re.split(r":|-", original_line, maxsplit=1)

                if len(parts) > 1:
                    address = clean_value(parts[1])

                    for stop in stop_words:
                        pattern = r"\b" + re.escape(stop) + r"\b"
                        address = re.split(pattern, address, flags=re.IGNORECASE)[0]

                    address = clean_value(address)

                    if len(address) >= 8:
                        addresses.append(address.title())

    return unique_list(addresses)


def extract_entities(text):
    return {
        "names": extract_names(text),
        "addresses": extract_addresses(text),
        "pan": extract_pan(text),
        "gstin": extract_gstin(text),
        "amounts": extract_amounts(text),
        "dates": extract_dates(text)
    }