def calculate_synthetic_borrower_probability(contradictions, shadow_score):
    probability = 0
    reasons = []

    for issue in contradictions:
        issue_type = issue["Type"]

        if "PAN" in issue_type:
            probability += 30
            reasons.append("PAN mismatch indicates identity inconsistency.")

        elif "Name" in issue_type:
            probability += 15
            reasons.append("Name mismatch indicates possible identity stitching.")

        elif "Address" in issue_type:
            probability += 15
            reasons.append("Address mismatch indicates unstable applicant profile.")

        elif "GST" in issue_type:
            probability += 25
            reasons.append("GSTIN mismatch indicates business identity inconsistency.")

        elif "Financial" in issue_type:
            probability += 25
            reasons.append("Financial mismatch indicates income or turnover inflation.")

    if shadow_score["shadow_score"] < 550:
        probability += 15
        reasons.append("Low shadow credit score increases synthetic borrower risk.")

    if probability > 100:
        probability = 100

    if probability >= 70:
        risk_label = "High Synthetic Borrower Risk"
    elif probability >= 40:
        risk_label = "Medium Synthetic Borrower Risk"
    else:
        risk_label = "Low Synthetic Borrower Risk"

    return {
        "probability": probability,
        "risk_label": risk_label,
        "reasons": reasons
    }