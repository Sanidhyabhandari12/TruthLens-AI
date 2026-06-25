def calculate_fraud_score(contradictions, metadata_results=None):
    score = 0

    for issue in contradictions:
        score += issue["Score"]

    if metadata_results:
        for doc_name, result in metadata_results.items():
            warnings = result.get("warnings", [])

            for warning in warnings:
                if "modified after creation" in warning.lower():
                    score += 20

                elif "suspicious metadata" in warning.lower():
                    score += 15

                elif "missing pdf creation date" in warning.lower():
                    score += 10

                else:
                    score += 5

    if score > 100:
        score = 100

    if score <= 30:
        risk_level = "Low Risk"
        recommendation = "APPROVE"

    elif score <= 60:
        risk_level = "Medium Risk"
        recommendation = "MANUAL REVIEW"

    else:
        risk_level = "High Risk"
        recommendation = "REJECT / ESCALATE"

    return {
        "score": score,
        "risk_level": risk_level,
        "recommendation": recommendation
    }