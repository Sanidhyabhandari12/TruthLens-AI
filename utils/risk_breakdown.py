def generate_risk_breakdown(contradictions, metadata_results):
    breakdown = {
        "Identity Risk": 0,
        "GST Risk": 0,
        "Financial Risk": 0,
        "Metadata Risk": 0
    }

    for issue in contradictions:
        issue_type = issue["Type"]

        if "Name" in issue_type or "PAN" in issue_type:
            breakdown["Identity Risk"] += issue["Score"]

        elif "GST" in issue_type:
            breakdown["GST Risk"] += issue["Score"]

        elif "Financial" in issue_type:
            breakdown["Financial Risk"] += issue["Score"]

    for doc_name, result in metadata_results.items():
        warnings = result.get("warnings", [])
        breakdown["Metadata Risk"] += len(warnings) * 10

    for key in breakdown:
        if breakdown[key] > 100:
            breakdown[key] = 100

    return breakdown