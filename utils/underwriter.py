def generate_underwriter_report(contradictions, fraud_result):
    reasons = []

    for issue in contradictions:
        reasons.append({
            "issue": issue["Type"],
            "severity": issue["Severity"],
            "details": issue["Details"],
            "score": issue["Score"]
        })

    score = fraud_result["score"]

    if score <= 30:
        decision = "APPROVE"
        summary = "Documents appear largely consistent. Application may be considered for approval."

    elif score <= 60:
        decision = "MANUAL REVIEW"
        summary = "Moderate risk detected. Human verification is recommended before loan approval."

    else:
        decision = "REJECT / ESCALATE"
        summary = "High risk detected. Application should be rejected or escalated to fraud investigation team."

    return {
        "decision": decision,
        "confidence": score,
        "summary": summary,
        "reasons": reasons
    }