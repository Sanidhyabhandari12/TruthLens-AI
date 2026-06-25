from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os
from datetime import datetime


def generate_pdf_report(
    fraud_result,
    underwriter_report,
    contradictions,
    risk_breakdown,
    metadata_results
):
    os.makedirs("reports", exist_ok=True)

    report_path = os.path.join(
        "reports",
        "TruthLens_Investigation_Report.pdf"
    )

    doc = SimpleDocTemplate(report_path)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("TruthLens AI Investigation Report", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Executive Summary", styles["Heading2"]))

    summary_data = [
        ["Fraud Score", f"{fraud_result['score']} / 100"],
        ["Risk Level", fraud_result["risk_level"]],
        ["Decision", underwriter_report["decision"]],
        ["Confidence", f"{underwriter_report['confidence']}%"],
    ]

    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 16))

    story.append(Paragraph("AI Underwriter Summary", styles["Heading2"]))
    story.append(Paragraph(underwriter_report["summary"], styles["Normal"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Risk Category Breakdown", styles["Heading2"]))

    risk_data = [["Risk Category", "Score"]]

    for category, score in risk_breakdown.items():
        risk_data.append([category, str(score)])

    risk_table = Table(risk_data)
    risk_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    story.append(risk_table)
    story.append(Spacer(1, 16))

    story.append(Paragraph("Contradictions Detected", styles["Heading2"]))

    if contradictions:
        contradiction_data = [["Issue", "Severity", "Score"]]

        for issue in contradictions:
            contradiction_data.append([
                issue["Type"],
                issue["Severity"],
                str(issue["Score"])
            ])

        contradiction_table = Table(contradiction_data)
        contradiction_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("PADDING", (0, 0), (-1, -1), 8),
        ]))

        story.append(contradiction_table)

    else:
        story.append(Paragraph("No contradictions detected.", styles["Normal"]))

    story.append(Spacer(1, 16))

    story.append(Paragraph("Document Fingerprints", styles["Heading2"]))

    for doc_name, metadata in metadata_results.items():
        story.append(Paragraph(f"Document: {doc_name}", styles["Heading3"]))
        story.append(Paragraph(f"SHA-256: {metadata['sha256']}", styles["Normal"]))

        warnings = metadata.get("warnings", [])

        if warnings:
            for warning in warnings:
                story.append(Paragraph(f"Warning: {warning}", styles["Normal"]))
        else:
            story.append(Paragraph("No metadata warning detected.", styles["Normal"]))

        story.append(Spacer(1, 8))

    doc.build(story)

    return report_path