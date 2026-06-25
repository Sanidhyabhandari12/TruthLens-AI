def clean_amount(amount):
    amount = amount.replace("₹", "")
    amount = amount.replace("Rs", "")
    amount = amount.replace("INR", "")
    amount = amount.replace(",", "")
    amount = amount.strip()

    try:
        return float(amount)
    except:
        return 0


def compare_entities(all_docs_entities):
    contradictions = []

    all_names = set()
    all_pans = set()
    all_gstins = set()
    all_amounts = []

    for doc_name, entities in all_docs_entities.items():
        all_names.update(entities["names"])
        all_pans.update(entities["pan"])
        all_gstins.update(entities["gstin"])

        for amount in entities["amounts"]:
            value = clean_amount(amount)

            if value > 0:
                all_amounts.append({
                    "document": doc_name,
                    "amount": amount,
                    "value": value
                })

    if len(all_names) > 1:
        contradictions.append({
            "Type": "Name Mismatch",
            "Severity": "Medium",
            "Details": list(all_names),
            "Score": 15
        })

    if len(all_pans) > 1:
        contradictions.append({
            "Type": "PAN Mismatch",
            "Severity": "High",
            "Details": list(all_pans),
            "Score": 30
        })

    if len(all_gstins) > 1:
        contradictions.append({
            "Type": "GSTIN Mismatch",
            "Severity": "High",
            "Details": list(all_gstins),
            "Score": 25
        })

    if len(all_amounts) >= 2:
        values = [item["value"] for item in all_amounts]

        max_value = max(values)
        min_value = min(values)

        if min_value > 0 and max_value / min_value >= 10:
            contradictions.append({
                "Type": "Financial Reality Mismatch",
                "Severity": "High",
                "Details": all_amounts,
                "Score": 25
            })

    return contradictions