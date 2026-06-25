import streamlit as st
import os
import pandas as pd

from utils.extractor import extract_text
from utils.entity_parser import extract_entities
from utils.consistency_engine import compare_entities
from utils.fraud_score import calculate_fraud_score
from utils.metadata_checker import check_pdf_metadata
from utils.underwriter import generate_underwriter_report
from utils.risk_breakdown import generate_risk_breakdown
from utils.trust_graph import save_trust_graph_image
from utils.report_generator import generate_pdf_report
from utils.shadow_score import generate_shadow_credit_score
from utils.synthetic_borrower import calculate_synthetic_borrower_probability


UPLOAD_FOLDER = "uploaded_docs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


st.set_page_config(
    page_title="TruthLens AI",
    page_icon="🛡️",
    layout="wide"
)


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #08111f 0%, #101828 45%, #172554 100%);
        color: white;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    h1, h2, h3 {
        color: #f8fafc;
    }

    .hero-card {
        padding: 35px;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(37,99,235,0.35), rgba(14,165,233,0.18));
        border: 1px solid rgba(255,255,255,0.18);
        box-shadow: 0 18px 45px rgba(0,0,0,0.35);
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 20px;
        color: #cbd5e1;
        max-width: 900px;
    }

    .feature-card {
        padding: 22px;
        border-radius: 18px;
        background: rgba(15,23,42,0.82);
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 10px 30px rgba(0,0,0,0.22);
        height: 150px;
    }

    .feature-title {
        font-size: 20px;
        font-weight: 700;
        color: #38bdf8;
    }

    .feature-text {
        font-size: 14px;
        color: #cbd5e1;
        margin-top: 8px;
    }

    .success-box {
        padding: 18px;
        border-radius: 16px;
        background: rgba(22,163,74,0.18);
        border: 1px solid rgba(34,197,94,0.4);
        color: #dcfce7;
    }

    .warning-box {
        padding: 18px;
        border-radius: 16px;
        background: rgba(234,179,8,0.18);
        border: 1px solid rgba(234,179,8,0.4);
        color: #fef9c3;
    }

    .danger-box {
        padding: 18px;
        border-radius: 16px;
        background: rgba(220,38,38,0.20);
        border: 1px solid rgba(248,113,113,0.45);
        color: #fee2e2;
    }

    div[data-testid="stMetric"] {
        background: rgba(15,23,42,0.75);
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }

    .stDownloadButton button {
        background: linear-gradient(90deg, #2563eb, #06b6d4);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 22px;
        font-weight: 700;
    }

    .stButton button {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.markdown("## 🛡️ TruthLens AI")
    st.markdown("### Banking Fraud Intelligence")
    st.divider()

    st.markdown("#### Prototype Modules")
    st.markdown("✅ Multi-document upload")
    st.markdown("✅ Entity extraction")
    st.markdown("✅ Cross-document validation")
    st.markdown("✅ Financial reality check")
    st.markdown("✅ Metadata forensics")
    st.markdown("✅ Trust graph")
    st.markdown("✅ Shadow credit score")
    st.markdown("✅ Synthetic borrower detection")
    st.markdown("✅ Investigation report")

    st.divider()

    st.markdown("#### Demo Tip")
    st.info(
        "Upload clean PDFs first, then upload high-risk PDFs to show how fraud score, shadow credit score, and synthetic borrower probability change."
    )


st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">TruthLens AI 🛡️</div>
        <div class="hero-subtitle">
            Offline Cross-Document Fraud Detection System for Banking Underwriting.
            TruthLens reconstructs an applicant's financial reality and detects identity,
            financial, GST, metadata, shadow credit risk, and synthetic borrower patterns before loan approval.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">🔍 OCR Intelligence</div>
            <div class="feature-text">Extracts useful information from uploaded banking documents.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">🧠 Reality Engine</div>
            <div class="feature-text">Checks whether all documents tell the same financial story.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">🏦 Shadow Score</div>
            <div class="feature-text">Creates an alternative credit score for thin-file borrowers.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">🕵️ Synthetic Risk</div>
            <div class="feature-text">Detects stitched borrower profiles using cross-document inconsistencies.</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("## 📤 Upload Underwriting Documents")

uploaded_files = st.file_uploader(
    "Upload PDF/Image documents",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)


if uploaded_files:

    st.success(f"{len(uploaded_files)} document(s) uploaded successfully.")

    all_docs_entities = {}
    all_metadata_results = {}

    for uploaded_file in uploaded_files:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        extracted_text = extract_text(file_path)
        entities = extract_entities(extracted_text)
        metadata_result = check_pdf_metadata(file_path)

        all_docs_entities[uploaded_file.name] = entities
        all_metadata_results[uploaded_file.name] = metadata_result

        with st.expander(f"📄 Document Analysis: {uploaded_file.name}"):

            tab1, tab2, tab3 = st.tabs(
                ["Extracted Text", "Extracted Entities", "Document DNA"]
            )

            with tab1:
                st.text(extracted_text[:3000])

            with tab2:
                st.json(entities)

            with tab3:
                st.write("### SHA-256 Fingerprint")
                st.code(metadata_result["sha256"])

                st.write("### PDF Metadata")
                st.json(metadata_result["metadata"])

                if metadata_result["warnings"]:
                    st.warning("Tampering / Metadata Warnings:")
                    for warning in metadata_result["warnings"]:
                        st.write(f"- {warning}")
                else:
                    st.success("No suspicious metadata warning found.")

    contradictions = compare_entities(all_docs_entities)

    fraud_result = calculate_fraud_score(
        contradictions,
        all_metadata_results
    )

    underwriter_report = generate_underwriter_report(
        contradictions,
        fraud_result
    )

    risk_breakdown = generate_risk_breakdown(
        contradictions,
        all_metadata_results
    )

    shadow_score = generate_shadow_credit_score(
        contradictions,
        all_metadata_results
    )

    synthetic_result = calculate_synthetic_borrower_probability(
        contradictions,
        shadow_score
    )

    st.markdown("---")

    st.markdown("## 🧾 Underwriting Decision Dashboard")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Fraud Score",
            f"{fraud_result['score']} / 100"
        )

    with m2:
        st.metric(
            "Risk Level",
            fraud_result["risk_level"]
        )

    with m3:
        st.metric(
            "Decision",
            underwriter_report["decision"]
        )

    st.markdown("## 🏦 TruthLens Shadow Credit Score™")

    s1, s2, s3 = st.columns(3)

    with s1:
        st.metric(
            "Shadow Credit Score",
            f"{shadow_score['shadow_score']} / 900"
        )

    with s2:
        st.metric(
            "Credit Tier",
            shadow_score["tier"]
        )

    with s3:
        reality_consistency = round(
            (shadow_score["shadow_score"] - 300) / 6
        )
        st.metric(
            "Reality Consistency",
            f"{reality_consistency}%"
        )

    score_df = pd.DataFrame(
        {
            "Factor": [
                "Identity Consistency",
                "Business Consistency",
                "Financial Consistency",
                "Document Authenticity"
            ],
            "Score": [
                shadow_score["identity_score"],
                shadow_score["business_score"],
                shadow_score["financial_score"],
                shadow_score["metadata_score"]
            ]
        }
    )

    st.bar_chart(
        score_df.set_index("Factor")
    )

    st.markdown("## 🕵️ Synthetic Borrower Probability™")

    b1, b2 = st.columns(2)

    with b1:
        st.metric(
            "Synthetic Borrower Probability",
            f"{synthetic_result['probability']}%"
        )

    with b2:
        st.metric(
            "Synthetic Risk Label",
            synthetic_result["risk_label"]
        )

    if synthetic_result["probability"] >= 70:
        st.markdown(
            """
            <div class="danger-box">
            <h3>🚨 Possible Synthetic Borrower Detected</h3>
            <p>This application shows signs of a stitched or inconsistent borrower profile.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif synthetic_result["probability"] >= 40:
        st.markdown(
            """
            <div class="warning-box">
            <h3>⚠️ Synthetic Borrower Risk Present</h3>
            <p>Some inconsistencies suggest manual borrower verification is needed.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            """
            <div class="success-box">
            <h3>✅ Low Synthetic Borrower Risk</h3>
            <p>The applicant profile appears structurally consistent.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    if synthetic_result["reasons"]:
        st.write("### Why this probability was assigned")
        for reason in synthetic_result["reasons"]:
            st.write(f"- {reason}")
    else:
        st.write("No major synthetic borrower indicators detected.")

    st.markdown("## 🧠 AI Underwriter Summary")

    if fraud_result["score"] <= 30:
        st.markdown(
            f"""
            <div class="success-box">
            <h3>✅ Low Risk Application</h3>
            <p>{underwriter_report["summary"]}</p>
            <b>Confidence:</b> {underwriter_report["confidence"]}%
            </div>
            """,
            unsafe_allow_html=True
        )

    elif fraud_result["score"] <= 60:
        st.markdown(
            f"""
            <div class="warning-box">
            <h3>⚠️ Medium Risk Application</h3>
            <p>{underwriter_report["summary"]}</p>
            <b>Confidence:</b> {underwriter_report["confidence"]}%
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"""
            <div class="danger-box">
            <h3>🚨 High Risk Application</h3>
            <p>{underwriter_report["summary"]}</p>
            <b>Confidence:</b> {underwriter_report["confidence"]}%
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("## 🕸️ Applicant Digital Twin / Trust Graph")

    graph_path = save_trust_graph_image(all_docs_entities)

    st.image(
        graph_path,
        caption="Cross-Document Trust Graph",
        use_container_width=True
    )

    st.markdown("## 📊 Risk Category Breakdown")

    risk_df = pd.DataFrame(
        list(risk_breakdown.items()),
        columns=["Risk Category", "Score"]
    )

    st.bar_chart(
        risk_df.set_index("Risk Category")
    )

    st.dataframe(
        risk_df,
        use_container_width=True
    )

    st.markdown("## 🚩 Contradiction Matrix")

    if contradictions:

        st.error("Contradictions Detected")

        for issue in contradictions:

            with st.expander(f"🚩 {issue['Type']}"):
                st.write(f"**Severity:** {issue['Severity']}")
                st.write(f"**Risk Score Contribution:** +{issue['Score']}")
                st.write("**Evidence Details:**")
                st.json(issue["Details"])

    else:

        st.success("No contradictions found.")

    st.markdown("## 🔎 Explainable Risk Trail")

    if underwriter_report["reasons"]:

        for index, reason in enumerate(
            underwriter_report["reasons"],
            start=1
        ):
            st.write(
                f"**{index}. {reason['issue']}** "
                f"({reason['severity']}) "
                f"→ `+{reason['score']}` risk points"
            )

    else:

        st.write("No major risk factors identified.")

    st.markdown("## 📥 Download Investigation Report")

    report_path = generate_pdf_report(
        fraud_result,
        underwriter_report,
        contradictions,
        risk_breakdown,
        all_metadata_results
    )

    with open(report_path, "rb") as pdf_file:
        st.download_button(
            label="📄 Download TruthLens Investigation Report",
            data=pdf_file,
            file_name="TruthLens_Investigation_Report.pdf",
            mime="application/pdf"
        )

else:

    st.info("Upload documents to begin TruthLens verification.")