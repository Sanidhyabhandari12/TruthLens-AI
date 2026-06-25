def generate_shadow_credit_score(contradictions, metadata_results):
    identity_score = 100
    business_score = 100
    financial_score = 100
    metadata_score = 100

    for issue in contradictions:
        issue_type = issue["Type"]

        if "PAN" in issue_type:
            identity_score -= 40
        elif "Name" in issue_type:
            identity_score -= 20
        elif "Address" in issue_type:
            identity_score -= 20
        elif "GST" in issue_type:
            business_score -= 35
        elif "Financial" in issue_type:
            financial_score -= 50

    metadata_penalty = 0

    for _, result in metadata_results.items():
        metadata_penalty += len(result.get("warnings", [])) * 10

    metadata_score -= metadata_penalty

    identity_score = max(identity_score, 0)
    business_score = max(business_score, 0)
    financial_score = max(financial_score, 0)
    metadata_score = max(metadata_score, 0)

    final_score = (
        identity_score * 0.30
        + business_score * 0.25
        + financial_score * 0.30
        + metadata_score * 0.15
    )

    shadow_score = int(300 + (final_score * 6))

    if shadow_score >= 750:
        tier = "Prime"
    elif shadow_score >= 650:
        tier = "Near Prime"
    elif shadow_score >= 550:
        tier = "Sub Prime"
    else:
        tier = "High Risk"

    return {
        "shadow_score": shadow_score,
        "tier": tier,
        "identity_score": identity_score,
        "business_score": business_score,
        "financial_score": financial_score,
        "metadata_score": metadata_score,
    }