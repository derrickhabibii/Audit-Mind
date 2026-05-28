import streamlit as st
import anthropic
import json
import re
import time
from io import BytesIO
from datetime import date

st.set_page_config(
    page_title="AuditMind – Shadow AI Risk Scanner",
    page_icon="⬛",
    layout="centered",
)

# ── Styles ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        color: #F5F0E8 !important;
    }

    .main {
        background-color: #0D1B2A !important;
        background-image:
            radial-gradient(ellipse at 15% 40%, rgba(232,168,56,0.04) 0%, transparent 55%),
            radial-gradient(ellipse at 85% 10%, rgba(232,168,56,0.025) 0%, transparent 45%);
    }

    .block-container {
        max-width: 800px;
        padding-top: 4rem;
        padding-bottom: 4rem;
        background: transparent !important;
    }

    /* Hide Streamlit chrome */
    header[data-testid="stHeader"] { display: none !important; }
    footer { display: none !important; }
    #MainMenu { display: none !important; }

    /* Brand */
    .brand-name {
        font-family: 'DM Serif Display', serif;
        font-size: 1.5rem;
        color: #E8A838;
        letter-spacing: 0.5px;
        line-height: 1;
    }
    .brand-tagline {
        font-size: 0.78rem;
        color: rgba(245,240,232,0.3);
        margin-top: 4px;
        letter-spacing: 0.5px;
    }

    /* Page title */
    .page-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2.4rem;
        color: #F5F0E8;
        line-height: 1.2;
        margin-bottom: 10px;
    }
    .page-subtitle {
        font-size: 0.95rem;
        color: rgba(245,240,232,0.45);
        line-height: 1.7;
        max-width: 540px;
    }

    /* Score display */
    .company-name {
        font-family: 'DM Serif Display', serif;
        font-size: 2.4rem;
        color: #F5F0E8;
        line-height: 1.15;
    }
    .score-number {
        font-family: 'DM Serif Display', serif;
        font-size: 7rem;
        font-weight: 400;
        line-height: 1;
    }
    .score-label {
        font-size: 0.72rem;
        color: rgba(245,240,232,0.35);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* Risk badge */
    .risk-badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 3px;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
    }
    .risk-Critical { background: rgba(229,62,62,0.12);  border: 1px solid rgba(229,62,62,0.35);  color: #E53E3E; }
    .risk-High     { background: rgba(232,168,56,0.12); border: 1px solid rgba(232,168,56,0.35); color: #E8A838; }
    .risk-Medium   { background: rgba(236,201,75,0.12); border: 1px solid rgba(236,201,75,0.35); color: #ECC94B; }
    .risk-Low      { background: rgba(56,161,105,0.12); border: 1px solid rgba(56,161,105,0.35); color: #38A169; }

    /* Section headers */
    .section-header {
        font-size: 0.65rem;
        color: rgba(245,240,232,0.3);
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 18px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(245,240,232,0.07);
    }

    /* Executive summary card */
    .exec-card {
        background: rgba(245,240,232,0.04);
        border: 1px solid rgba(245,240,232,0.08);
        border-radius: 8px;
        padding: 32px 36px;
    }
    .exec-text {
        font-size: 1.08rem;
        color: rgba(245,240,232,0.82);
        line-height: 1.95;
    }

    /* Finding cards */
    .finding-card {
        background: rgba(245,240,232,0.02);
        border: 1px solid rgba(245,240,232,0.06);
        border-left: 3px solid;
        border-radius: 0 6px 6px 0;
        padding: 22px 26px;
        margin-bottom: 14px;
    }
    .finding-priority {
        font-size: 0.6rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .finding-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.05rem;
        color: #F5F0E8;
        margin-bottom: 10px;
        line-height: 1.3;
    }
    .finding-observation {
        font-size: 0.9rem;
        color: rgba(245,240,232,0.62);
        line-height: 1.75;
        margin-bottom: 10px;
    }
    .finding-rec {
        font-size: 0.85rem;
        color: rgba(245,240,232,0.42);
        line-height: 1.65;
        font-style: italic;
    }
    .finding-rec::before { content: "→ "; font-style: normal; }

    /* Action items */
    .action-row {
        display: flex;
        gap: 18px;
        align-items: flex-start;
        padding: 16px 0;
        border-bottom: 1px solid rgba(245,240,232,0.05);
    }
    .action-num {
        font-family: 'DM Serif Display', serif;
        font-size: 1.2rem;
        color: #E8A838;
        min-width: 32px;
        padding-top: 1px;
    }
    .action-body { flex: 1; }
    .action-text {
        font-size: 0.9rem;
        color: rgba(245,240,232,0.8);
        line-height: 1.6;
        font-weight: 500;
    }
    .action-meta {
        font-size: 0.75rem;
        color: rgba(245,240,232,0.3);
        margin-top: 4px;
        letter-spacing: 0.3px;
    }

    /* Footer note */
    .footer-note {
        font-size: 0.75rem;
        color: rgba(245,240,232,0.22);
        line-height: 1.7;
        text-align: center;
        padding: 28px 0 8px;
    }

    /* Dividers */
    hr { border-color: rgba(245,240,232,0.07) !important; }

    /* Input */
    .stTextInput > div > div > input {
        background: rgba(245,240,232,0.05) !important;
        border: 1px solid rgba(245,240,232,0.13) !important;
        border-radius: 6px !important;
        color: #F5F0E8 !important;
        font-size: 0.95rem !important;
        padding: 0.7rem 1rem !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(232,168,56,0.5) !important;
        box-shadow: 0 0 0 2px rgba(232,168,56,0.1) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(245,240,232,0.2) !important;
    }

    /* Primary button (Run Assessment) */
    .stButton > button {
        background: #E8A838 !important;
        color: #0D1B2A !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0.65rem 1.6rem !important;
        font-size: 0.92rem !important;
        font-family: 'DM Sans', sans-serif !important;
        width: 100%;
        letter-spacing: 0.3px !important;
        transition: background 0.15s ease !important;
    }
    .stButton > button:hover { background: #D4932A !important; }

    /* Download button */
    .stDownloadButton > button {
        background: transparent !important;
        color: rgba(245,240,232,0.5) !important;
        font-weight: 400 !important;
        border-radius: 6px !important;
        border: 1px solid rgba(245,240,232,0.15) !important;
        padding: 0.55rem 1.4rem !important;
        font-size: 0.85rem !important;
        font-family: 'DM Sans', sans-serif !important;
        letter-spacing: 0.3px !important;
        transition: all 0.15s ease !important;
    }
    .stDownloadButton > button:hover {
        border-color: rgba(232,168,56,0.4) !important;
        color: #E8A838 !important;
    }

    /* Alert */
    div[data-testid="stAlert"] {
        border-radius: 6px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.88rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ── System prompt ───────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """AuditMind is an AI governance pre-screening tool. It identifies external signals that suggest where internal audit should look first. All findings are risk indicators requiring internal verification, not audit conclusions.

You are applying fixed scoring rubrics to publicly available information. Do not use subjective judgment. Only award points for items you can cite specific public evidence for. If you cannot find evidence for a criterion, points = 0. No assumptions.

Use web_search (max 2 searches). Research: industry, sensitive data handling, employee count, work model, AI tools/partnerships, breaches, job postings, certifications, governance policies.

VISIBLE GOVERNANCE SCORE RUBRIC (max 100 — award only for confirmed public evidence):
G1. AI Governance Ownership [15pts]: 15=named person+committee+board oversight confirmed; 10=named person OR committee only; 5=vague reference, no name; 0=none
G2. AI Acceptable Use Policy [15pts]: 15=policy with data restrictions+approved tools+employee duties+escalation process; 10=specific AI policy exists, limited detail; 5=vague responsible AI statement only; 0=none
G3. AI Risk Management Framework [15pts]: 15=detailed framework with specific criteria; 10=published principles with substance; 5=generic ethics or innovation language; 0=none
G4. AI Vendor and Third-Party Risk [15pts]: 15=documented vendor AI review process; 10=general vendor risk management; 5=indirect procurement signals; 0=none
G5. Data Protection & Cybersecurity Maturity [15pts]: 15=named CISO + multiple certs (FedRAMP, SOC2, ISO27001, NIST, CJIS); 10=named CISO OR strong certifications; 5=general security language; 0=none. RULE: Named CISO alone = max 5pts. FedRAMP, SOC2, ISO27001, NIST, CJIS are different standards — award partial credit based on strength and relevance of what is actually confirmed.
G6. Employee Training & Awareness [10pts]: 10=specific AI training program confirmed; 5=general security awareness training only; 0=none
G7. Monitoring, Reporting & Incident Response [10pts]: 10=AI-specific incident response confirmed; 5=general security incident process only; 0=none
G8. Transparency & Customer Assurance [5pts]: 5=specific customer-facing AI disclosures confirmed; 0=none

EXPOSURE SCORE RUBRIC (max 100 — award only for confirmed public evidence):
E1. Sensitive or Regulated Data [25pts]: 25=multiple sensitive types confirmed (govt records, PII, financial, healthcare, legal, criminal justice); 15=one sensitive data type confirmed; 5=general business data, limited sensitivity; 0=none
E2. AI in Products or Customer Workflows [20pts]: 20=AI core to product + multiple AI partnerships confirmed; 10=some AI features, limited integration; 5=general innovation language, no specific AI; 0=none
E3. Regulated Operating Environment [15pts]: 15=multiple strict frameworks confirmed (CJIS, HIPAA, FedRAMP, GDPR, public-sector procurement); 10=one major framework; 5=general compliance language; 0=none
E4. Scale and Operational Complexity [15pts]: 15=10,000+ employees OR 1,000+ customers OR 10+ jurisdictions; 10=1,000-10,000 employees OR 100-1,000 customers; 5=under 1,000 employees; 0=very small. RULE: Data sensitivity outweighs scale. A 900-person company handling court records scores higher than a 5,000-person low-risk software company.
E5. Distributed Workforce Risk [10pts]: 10=fully distributed or fully remote confirmed; 5=hybrid work confirmed; 0=primarily in-office
E6. Security Incident History [10pts]: 10=multiple incidents or major breach in last 5 years; 5=single minor incident; 0=no known incidents. RULE: Absence of known incidents is NOT a positive governance signal. Do not award points here.
E7. Public AI Hiring or Expansion [5pts]: 5=significant AI hiring, AI lab, or AI-related acquisition confirmed; 0=none

CONFIDENCE LEVEL (overall report):
High: multiple specific public artifacts confirmed (policy docs, trust center, named AI role, certifications, training evidence)
Medium: some signals found but mostly general security or privacy evidence
Low: little public disclosure found; score may significantly understate internal maturity

Output ONLY this exact JSON with no markdown, no explanation:
{"companyName":"","industry":"","exposureScore":0,"visibleGovernanceScore":0,"shadowAIGap":0,"confidenceLevel":"High|Medium|Low","executiveSummary":"3-4 sentences for CFO/Board","governanceBreakdown":[{"criterion":"","pointsAwarded":0,"pointsAvailable":0,"evidence":"one line citing specific public evidence or stating none found"}],"exposureBreakdown":[{"criterion":"","pointsAwarded":0,"pointsAvailable":0,"evidence":"one line citing specific public evidence or stating none found"}],"categoryScores":{"AI Governance":0,"Data Sensitivity":0,"Workforce Distribution":0,"IT Controls":0,"Regulatory Exposure":0},"categoryRationale":{"AI Governance":"","Data Sensitivity":"","Workforce Distribution":"","IT Controls":"","Regulatory Exposure":""},"findings":[{"priority":"Critical|High|Medium","confidence":"High|Medium|Low","title":"","observation":"","risk":"","recommendation":""}],"controls":[{"action":"","rationale":"","timeline":"","owner":""}],"dataPoints":[],"limitations":"","departmentRisks":[{"department":"","risk":""}],"auditQuestions":[],"evidenceRequests":[]}

Rules:
governanceBreakdown must have exactly 8 entries (G1-G8 in order). exposureBreakdown must have exactly 7 entries (E1-E7 in order).
shadowAIGap = exposureScore minus visibleGovernanceScore.
3-5 findings. 4-6 controls. Reference specific company facts.
departmentRisks: 5-6 departments tailored to this company's industry and size. Remove departments that clearly do not apply.
auditQuestions: exactly 7 questions tailored to this specific company.
evidenceRequests: exactly 10 document requests tailored to this specific company.
Append to limitations: "The Shadow AI Gap represents the difference between observable AI risk exposure and externally visible governance assurance. It is not proof of internal control failure. A low Visible Governance Score may reflect limited public disclosure rather than weak internal controls." """


def extract_json(text):
    try:
        return json.loads(text.strip())
    except Exception:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(text[start:end + 1])
        except Exception:
            pass
    cleaned = re.sub(r"```json|```", "", text).strip()
    try:
        return json.loads(cleaned)
    except Exception:
        pass
    return None


def _api_call_with_retry(client, status_box, **kwargs):
    for attempt in range(3):
        try:
            return client.messages.create(**kwargs)
        except anthropic.RateLimitError:
            if attempt < 2:
                if status_box:
                    status_box.info(
                        f"Rate limit hit — retrying in 30 seconds "
                        f"(attempt {attempt + 1}/3). Do not close this window..."
                    )
                time.sleep(30)
                if status_box:
                    status_box.empty()
            else:
                raise


def run_assessment(url: str, status_box=None) -> dict:
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": f"Assess: {url}"}]

    for _ in range(5):
        response = _api_call_with_retry(
            client,
            status_box,
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            system=SYSTEM_PROMPT,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=messages,
        )

        all_text = " ".join(b.text for b in response.content if hasattr(b, "text"))

        if response.stop_reason == "end_turn":
            parsed = extract_json(all_text)
            if parsed:
                return parsed
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": "Output raw JSON only."})
            continue

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": getattr(block, "output", "Search executed.")
                    })
            if tool_results:
                messages.append({"role": "user", "content": tool_results})
            continue

    raise ValueError("Could not generate a valid report after multiple attempts.")


def generate_pdf(result: dict) -> bytes:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT

    exposure    = result.get("exposureScore", 0)
    gov         = result.get("visibleGovernanceScore", 0)
    gap, risk   = compute_risk(exposure, gov)
    conf_level  = result.get("confidenceLevel", "Medium")
    company     = result.get("companyName", "Unknown")
    today       = date.today().strftime("%B %d, %Y")

    risk_hex   = {"Critical": "#E53E3E", "High": "#E8A838", "Medium": "#ECC94B", "Low": "#38A169"}.get(risk, "#E8A838")
    risk_color = colors.HexColor(risk_hex)

    navy    = colors.HexColor("#0D1B2A")
    slate   = colors.HexColor("#334155")
    muted   = colors.HexColor("#94a3b8")
    light   = colors.HexColor("#F5F0E8")
    divider = colors.HexColor("#e2e8f0")

    buffer = BytesIO()

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(muted)
        canvas.drawCentredString(letter[0] / 2, 0.45 * inch, f"AuditMind  |  Confidential  |  Page {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=0.9 * inch,
        title=f"AuditMind Shadow AI Risk Assessment — {company}",
        author="AuditMind",
    )

    def style(name, **kw):
        defaults = dict(fontName="Helvetica", fontSize=10, leading=15, textColor=slate, spaceAfter=6)
        defaults.update(kw)
        return ParagraphStyle(name, **defaults)

    s_body        = style("body", fontSize=10, leading=16, spaceAfter=8)
    s_section     = style("section", fontName="Helvetica-Bold", fontSize=7, leading=10,
                          textColor=muted, spaceBefore=20, spaceAfter=10, letterSpacing=1.5)
    s_company     = style("company", fontName="Times-Bold", fontSize=22, leading=26, textColor=navy, spaceAfter=6)
    s_score       = style("score", fontName="Times-Bold", fontSize=40, leading=44, textColor=risk_color, spaceAfter=4)
    s_risk_line   = style("risk_line", fontSize=9, leading=13, textColor=slate, spaceAfter=14)
    s_find_title  = style("find_title", fontName="Times-Bold", fontSize=12, leading=16, textColor=navy, spaceAfter=5)
    s_find_pri    = style("find_pri", fontName="Helvetica-Bold", fontSize=7, leading=10, textColor=risk_color, spaceAfter=4)
    s_label       = style("label", fontName="Helvetica-Bold", fontSize=7, leading=10, textColor=muted, spaceAfter=3)
    s_italic      = style("italic", fontName="Helvetica-Oblique", fontSize=9.5, leading=14, textColor=slate, spaceAfter=6)
    s_ctrl_title  = style("ctrl_title", fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=navy, spaceAfter=3)
    s_ctrl_body   = style("ctrl_body", fontSize=9.5, leading=14, textColor=slate, spaceAfter=2)
    s_ctrl_meta   = style("ctrl_meta", fontSize=8, leading=11, textColor=muted, spaceAfter=8)
    s_dp          = style("dp", fontSize=9.5, leading=14, textColor=slate, spaceAfter=4, leftIndent=14)
    s_disclaimer  = style("disc", fontName="Helvetica-Oblique", fontSize=7.5, leading=11,
                          textColor=muted, alignment=TA_CENTER)
    s_hdr_right   = style("hdr_r", fontSize=9, leading=13, textColor=slate, alignment=TA_RIGHT)
    s_hdr_left    = style("hdr_l", fontName="Helvetica-Bold", fontSize=11, leading=13, textColor=navy)

    hr_heavy  = HRFlowable(width="100%", thickness=1.5, color=navy,   spaceAfter=18)
    hr_light  = HRFlowable(width="100%", thickness=0.4, color=divider, spaceBefore=14, spaceAfter=6)

    els = []

    # ── Header ──
    els.append(Paragraph("AUDITMIND", s_hdr_left))
    els.append(Paragraph(f"Shadow AI Risk Assessment  ·  {today}", s_hdr_right))
    els.append(Spacer(1, 6))
    els.append(hr_heavy)

    # ── Company + Scores ──
    els.append(Paragraph(company, s_company))
    els.append(Paragraph(f"{result.get('industry','')}  ·  <b>{risk.upper()} RISK</b>  ·  Confidence: {conf_level}", s_risk_line))
    score_line = (f"Exposure: {exposure}/100    |    "
                  f"Visible Governance: {gov}/100    |    "
                  f"Shadow AI Gap: {gap}")
    els.append(Paragraph(score_line, ParagraphStyle(
        "score_line", fontName="Times-Bold", fontSize=13, leading=18,
        textColor=risk_color, spaceAfter=4
    )))
    els.append(Paragraph(
        "Visible Governance Score reflects externally observable governance signals only.",
        style("vg_note", fontName="Helvetica-Oblique", fontSize=7.5, leading=11,
              textColor=muted, spaceAfter=12)
    ))
    els.append(hr_light)

    # ── Scoring Breakdown ──
    els.append(Paragraph("HOW THIS SCORE WAS CALCULATED", s_section))

    s_crit_name  = style("cn", fontName="Helvetica-Bold", fontSize=8.5, leading=12, textColor=navy, spaceAfter=1)
    s_crit_pts   = style("cp", fontName="Helvetica-Bold", fontSize=8,   leading=11, textColor=risk_color, spaceAfter=1)
    s_crit_ev    = style("ce", fontName="Helvetica-Oblique", fontSize=8, leading=12, textColor=muted, spaceAfter=6)

    els.append(Paragraph("VISIBLE GOVERNANCE BREAKDOWN:", style("vghdr", fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=slate, spaceAfter=6)))
    gov_total = 0
    for b in result.get("governanceBreakdown", []):
        awarded = b.get("pointsAwarded", 0)
        avail   = b.get("pointsAvailable", 0)
        gov_total += awarded
        els.append(Paragraph(f"{b.get('criterion','')}", s_crit_name))
        els.append(Paragraph(f"{awarded} / {avail} pts", s_crit_pts))
        els.append(Paragraph(b.get("evidence", ""), s_crit_ev))
    els.append(Paragraph(f"TOTAL VISIBLE GOVERNANCE: {gov_total} / 100",
                          style("tot", fontName="Helvetica-Bold", fontSize=9, leading=13, textColor=navy, spaceAfter=10)))

    els.append(Spacer(1, 6))
    els.append(Paragraph("EXPOSURE BREAKDOWN:", style("exhdr", fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=slate, spaceAfter=6)))
    exp_total = 0
    for b in result.get("exposureBreakdown", []):
        awarded = b.get("pointsAwarded", 0)
        avail   = b.get("pointsAvailable", 0)
        exp_total += awarded
        els.append(Paragraph(f"{b.get('criterion','')}", s_crit_name))
        els.append(Paragraph(f"{awarded} / {avail} pts", s_crit_pts))
        els.append(Paragraph(b.get("evidence", ""), s_crit_ev))
    els.append(Paragraph(f"TOTAL EXPOSURE: {exp_total} / 100",
                          style("tot2", fontName="Helvetica-Bold", fontSize=9, leading=13, textColor=navy, spaceAfter=4)))
    els.append(Paragraph(f"SHADOW AI GAP: {gap} — {risk.upper()} RISK",
                          style("gap", fontName="Times-Bold", fontSize=11, leading=15, textColor=risk_color, spaceAfter=4)))
    els.append(hr_light)

    # ── Executive Summary ──
    els.append(Paragraph("EXECUTIVE SUMMARY", s_section))
    els.append(Paragraph(result.get("executiveSummary", ""), s_body))
    els.append(hr_light)

    conf_colors = {
        "High":   colors.HexColor("#38A169"),
        "Medium": colors.HexColor("#E8A838"),
        "Low":    colors.HexColor("#94a3b8"),
    }

    # ── Findings ──
    els.append(Paragraph("AUDIT FINDINGS", s_section))
    findings_list = result.get("findings", [])
    for i, f in enumerate(findings_list):
        p    = f.get("priority", "Medium")
        conf = f.get("confidence", "Medium")
        fc   = colors.HexColor({"Critical": "#E53E3E", "High": "#E8A838", "Medium": "#ECC94B"}.get(p, "#E8A838"))
        cc   = conf_colors.get(conf, colors.HexColor("#94a3b8"))
        pri_style  = ParagraphStyle(f"pri_{i}",  fontName="Helvetica-Bold", fontSize=7,
                                    leading=10, textColor=fc, spaceAfter=2)
        conf_style = ParagraphStyle(f"conf_{i}", fontName="Helvetica",      fontSize=7,
                                    leading=10, textColor=cc, spaceAfter=4)
        els.append(Spacer(1, 10))
        els.append(Paragraph(f"FINDING {i+1:02d}  ·  {p.upper()}", pri_style))
        els.append(Paragraph(f"Confidence: {conf}", conf_style))
        els.append(Paragraph(f.get("title", ""), s_find_title))
        els.append(Paragraph("Observation", s_label))
        els.append(Paragraph(f.get("observation", ""), s_body))
        els.append(Paragraph("Risk", s_label))
        els.append(Paragraph(f.get("risk", ""), s_body))
        els.append(Paragraph("Recommendation", s_label))
        els.append(Paragraph(f.get("recommendation", ""), s_italic))
        if i < len(findings_list) - 1:
            els.append(HRFlowable(width="100%", thickness=0.3, color=divider, spaceBefore=8, spaceAfter=4))

    els.append(hr_light)

    # ── Controls ──
    els.append(Paragraph("RECOMMENDED CONTROLS", s_section))
    for i, c in enumerate(result.get("controls", [])):
        els.append(Paragraph(f"{i+1:02d}.  {c.get('action','')}", s_ctrl_title))
        els.append(Paragraph(c.get("rationale", ""), s_ctrl_body))
        els.append(Paragraph(f"{c.get('owner','')}  ·  {c.get('timeline','')}", s_ctrl_meta))

    els.append(hr_light)

    # ── A: Department Risk Zones ──
    els.append(Paragraph("WHERE SHADOW AI IS MOST LIKELY", s_section))
    s_dept_name = style("dept_name", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
                        textColor=navy, spaceAfter=2)
    s_dept_risk = style("dept_risk", fontSize=9, leading=13, textColor=slate, spaceAfter=8)
    for d in result.get("departmentRisks", []):
        els.append(Paragraph(d.get("department", ""), s_dept_name))
        els.append(Paragraph(d.get("risk", ""), s_dept_risk))

    els.append(hr_light)

    # ── B: Audit Questions ──
    els.append(Paragraph("QUESTIONS INTERNAL AUDIT SHOULD ASK", s_section))
    s_q = style("q", fontSize=9.5, leading=15, textColor=slate, spaceAfter=5, leftIndent=14, firstLineIndent=-14)
    for i, q in enumerate(result.get("auditQuestions", [])):
        els.append(Paragraph(f"{i+1}.  {q}", s_q))

    els.append(hr_light)

    # ── C: Evidence Requests ──
    els.append(Paragraph("DOCUMENTS INTERNAL AUDIT SHOULD REQUEST", s_section))
    s_ev = style("ev", fontSize=9.5, leading=15, textColor=slate, spaceAfter=4, leftIndent=14, firstLineIndent=-14)
    for i, ev in enumerate(result.get("evidenceRequests", [])):
        els.append(Paragraph(f"{i+1:02d}.  {ev}", s_ev))

    els.append(hr_light)

    # ── D: Confidence Key ──
    els.append(Paragraph("ASSESSMENT CONFIDENCE", s_section))
    conf_key_style = style("ck", fontSize=8.5, leading=13, textColor=slate, spaceAfter=4)
    els.append(Paragraph("<b>High</b> — Direct public evidence (breach reports, press releases, job postings, regulatory filings)", conf_key_style))
    els.append(Paragraph("<b>Medium</b> — Inferred from indirect signals (job language, product claims, partnership announcements)", conf_key_style))
    els.append(Paragraph("<b>Low</b> — Assumed based on industry norms; limited public data available", conf_key_style))

    els.append(hr_light)

    # ── Evidence & Data Points ──
    els.append(Paragraph("EVIDENCE & DATA POINTS", s_section))
    for dp in result.get("dataPoints", []):
        els.append(Paragraph(f"• {dp}", s_dp))

    els.append(Spacer(1, 20))
    els.append(HRFlowable(width="100%", thickness=0.4, color=divider, spaceAfter=8))
    els.append(Paragraph(
        "AuditMind measures observable exposure and visible governance signals, not confirmed internal "
        "AI usage. Findings are risk indicators, not audit conclusions.",
        s_disclaimer
    ))
    els.append(Spacer(1, 4))
    els.append(Paragraph(
        "This assessment is based on publicly available information. "
        "Internal audit verification required for formal findings.",
        s_disclaimer
    ))

    doc.build(els, onFirstPage=add_footer, onLaterPages=add_footer)
    return buffer.getvalue()


def get_risk_color(level):
    return {"Critical": "#E53E3E", "High": "#E8A838", "Medium": "#ECC94B", "Low": "#38A169"}.get(level, "#E8A838")


def compute_risk(exposure: int, governance: int):
    """Derive gap and risk level from the two scores."""
    gap = max(0, exposure - governance)
    if gap > 50:   level = "Critical"
    elif gap > 30: level = "High"
    elif gap > 15: level = "Medium"
    else:          level = "Low"
    return gap, level


def gap_explanation(risk: str, exposure: int, governance: int) -> str:
    if exposure >= 60 and governance < 40:
        return ("High exposure with limited visible governance indicates significant Shadow AI risk. "
                "Internal audit verification is recommended.")
    if exposure >= 60 and governance >= 60:
        return ("Strong governance relative to exposure suggests controls are in place. "
                "Periodic review is recommended to maintain this posture.")
    if exposure < 40 and governance < 40:
        return ("Lower exposure limits overall risk, but governance gaps should be addressed "
                "as the organization scales.")
    if risk == "Critical":
        return "Critical gap between exposure and governance. Immediate internal audit action recommended."
    if risk == "High":
        return "Significant gap between exposure level and governance maturity. Prioritize control implementation."
    if risk == "Medium":
        return "Moderate gap detected. Governance improvements should be planned within the next quarter."
    return "Exposure and governance are reasonably aligned. Continue monitoring for changes."


# ── Session state ───────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None

# ── UI Header ──────────────────────────────────────────────────────────────────
st.markdown('<div class="brand-name">AuditMind</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-tagline">Shadow AI Risk Scanner</div>', unsafe_allow_html=True)
st.markdown("---")
st.markdown('<div class="page-title">Shadow AI Risk Assessment</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Enter a company website. AuditMind researches their public profile '
    'and generates a formal Shadow AI exposure assessment.</div>',
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

url = st.text_input("Company Website", placeholder="https://www.tylertech.com", label_visibility="collapsed")

if st.button("Run Assessment"):
    if not url.strip():
        st.error("Please enter a company website URL.")
    else:
        st.session_state.result = None
        status_box = st.empty()
        with st.spinner("Researching company and analyzing Shadow AI exposure..."):
            try:
                st.session_state.result = run_assessment(url.strip(), status_box=status_box)
                status_box.empty()
            except Exception as e:
                st.error(f"Error: {e}")

# ── Results ────────────────────────────────────────────────────────────────────
if st.session_state.result:
    result      = st.session_state.result
    exposure    = result.get("exposureScore", 0)
    gov         = result.get("visibleGovernanceScore", 0)
    gap, risk   = compute_risk(exposure, gov)
    color       = get_risk_color(risk)
    expl        = gap_explanation(risk, exposure, gov)
    conf_level  = result.get("confidenceLevel", "Medium")
    conf_color  = {"High": "#38A169", "Medium": "#E8A838", "Low": "rgba(245,240,232,0.4)"}.get(conf_level, "#E8A838")

    # ── 1. Score header ──
    st.markdown(f"""
    <div style="padding: 44px 0 32px;">
        <div class="company-name">{result.get('companyName','')}</div>
        <div style="font-size:0.85rem; color:rgba(245,240,232,0.3); margin-top:6px; letter-spacing:0.5px;">
            {result.get('industry','')}
        </div>
        <div style="display:flex; gap:14px; margin-top:28px; flex-wrap:wrap;">
            <div style="flex:1; min-width:130px; background:rgba(245,240,232,0.04); border:1px solid rgba(245,240,232,0.08); border-radius:8px; padding:18px 20px;">
                <div style="font-size:0.58rem; color:rgba(245,240,232,0.3); letter-spacing:2.5px; text-transform:uppercase; margin-bottom:10px;">Exposure</div>
                <div style="font-family:'DM Serif Display',serif; font-size:3rem; color:#F5F0E8; line-height:1;">{exposure}</div>
                <div style="font-size:0.68rem; color:rgba(245,240,232,0.22); margin-top:5px;">/ 100</div>
            </div>
            <div style="flex:1; min-width:130px; background:rgba(245,240,232,0.04); border:1px solid rgba(245,240,232,0.08); border-radius:8px; padding:18px 20px;">
                <div style="font-size:0.58rem; color:rgba(245,240,232,0.3); letter-spacing:2.5px; text-transform:uppercase; margin-bottom:10px;">Visible Governance</div>
                <div style="font-family:'DM Serif Display',serif; font-size:3rem; color:#F5F0E8; line-height:1;">{gov}</div>
                <div style="font-size:0.68rem; color:rgba(245,240,232,0.22); margin-top:5px;">/ 100</div>
            </div>
            <div style="flex:1.2; min-width:150px; background:rgba(245,240,232,0.04); border:1px solid rgba(245,240,232,0.08); border-left:3px solid {color}; border-radius:0 8px 8px 0; padding:18px 20px;">
                <div style="font-size:0.58rem; color:rgba(245,240,232,0.3); letter-spacing:2.5px; text-transform:uppercase; margin-bottom:10px;">Shadow AI Gap</div>
                <div style="font-family:'DM Serif Display',serif; font-size:3rem; color:{color}; line-height:1;">{gap}</div>
                <div class="risk-badge risk-{risk}" style="margin-top:10px;">{risk}</div>
            </div>
            <div style="flex:0.8; min-width:110px; background:rgba(245,240,232,0.04); border:1px solid rgba(245,240,232,0.08); border-radius:8px; padding:18px 20px;">
                <div style="font-size:0.58rem; color:rgba(245,240,232,0.3); letter-spacing:2.5px; text-transform:uppercase; margin-bottom:10px;">Confidence</div>
                <div style="font-family:'DM Serif Display',serif; font-size:1.6rem; color:{conf_color}; line-height:1.2;">{conf_level}</div>
                <div style="font-size:0.65rem; color:rgba(245,240,232,0.2); margin-top:8px; line-height:1.4;">External signals only</div>
            </div>
        </div>
        <div style="font-size:0.78rem; color:rgba(245,240,232,0.25); margin-top:14px; font-style:italic;">
            Visible Governance Score reflects externally observable governance signals only.
        </div>
        <div style="font-size:0.88rem; color:rgba(245,240,232,0.45); line-height:1.75; margin-top:12px; max-width:580px;">
            {expl}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── 2. Executive Summary ──
    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="exec-card"><div class="exec-text">{result.get("executiveSummary","")}</div></div>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-top:44px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # ── 3. Top Findings (3 max) ──
    st.markdown('<div class="section-header">Top Audit Findings</div>', unsafe_allow_html=True)
    border_colors = {"Critical": "#E53E3E", "High": "#E8A838", "Medium": "#ECC94B", "Low": "#38A169"}
    conf_styles = {
        "High":   ("rgba(56,161,105,0.12)",  "rgba(56,161,105,0.3)",  "#38A169"),
        "Medium": ("rgba(232,168,56,0.1)",   "rgba(232,168,56,0.3)",  "#E8A838"),
        "Low":    ("rgba(245,240,232,0.05)", "rgba(245,240,232,0.15)","rgba(245,240,232,0.4)"),
    }
    for f in result.get("findings", [])[:3]:
        p    = f.get("priority", "Medium")
        conf = f.get("confidence", "Medium")
        bc   = border_colors.get(p, "#E8A838")
        pc   = get_risk_color(p)
        cbg, cborder, cc = conf_styles.get(conf, conf_styles["Medium"])
        st.markdown(f"""
        <div class="finding-card" style="border-left-color:{bc};">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                <div class="finding-priority" style="color:{pc}; margin-bottom:0;">{p}</div>
                <div style="font-size:0.58rem; font-weight:600; letter-spacing:1.5px; color:{cc}; background:{cbg}; border:1px solid {cborder}; padding:2px 8px; border-radius:3px;">{conf} CONFIDENCE</div>
            </div>
            <div class="finding-title">{f.get('title','')}</div>
            <div class="finding-observation">{f.get('observation','')}</div>
            <div class="finding-rec">{f.get('recommendation','')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:44px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # ── 4. Recommended Actions (4 max) ──
    st.markdown('<div class="section-header">Recommended Actions</div>', unsafe_allow_html=True)
    for i, c in enumerate(result.get("controls", [])[:4]):
        st.markdown(f"""
        <div class="action-row">
            <div class="action-num">{i+1:02d}</div>
            <div class="action-body">
                <div class="action-text">{c.get('action','')}</div>
                <div class="action-meta">{c.get('owner','')} &nbsp;·&nbsp; {c.get('timeline','')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:44px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # ── 5. Audit Pack ──
    st.markdown('<div class="section-header">Audit Pack</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.85rem; color:rgba(245,240,232,0.35); line-height:1.7; margin-bottom:32px; max-width:560px;">'
        'This section converts AuditMind findings into a practical internal audit starting point. '
        'Use these to scope your investigation, prepare interview questions, and build your evidence request list.'
        '</div>',
        unsafe_allow_html=True
    )

    # Department Risk Zones
    st.markdown(
        '<div style="font-size:0.68rem; color:rgba(245,240,232,0.4); font-weight:600; letter-spacing:2px; '
        'text-transform:uppercase; margin-bottom:16px;">Where Shadow AI Is Most Likely</div>',
        unsafe_allow_html=True
    )
    for d in result.get("departmentRisks", []):
        st.markdown(f"""
        <div style="display:flex; gap:20px; padding:13px 0; border-bottom:1px solid rgba(245,240,232,0.05); align-items:flex-start;">
            <div style="font-size:0.88rem; font-weight:600; color:#F5F0E8; min-width:140px; padding-top:1px;">{d.get('department','')}</div>
            <div style="font-size:0.88rem; color:rgba(245,240,232,0.5); line-height:1.65;">{d.get('risk','')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:36px;'></div>", unsafe_allow_html=True)

    # Audit Questions
    st.markdown(
        '<div style="font-size:0.68rem; color:rgba(245,240,232,0.4); font-weight:600; letter-spacing:2px; '
        'text-transform:uppercase; margin-bottom:16px;">Questions Internal Audit Should Ask</div>',
        unsafe_allow_html=True
    )
    for i, q in enumerate(result.get("auditQuestions", [])):
        st.markdown(f"""
        <div style="display:flex; gap:16px; padding:12px 0; border-bottom:1px solid rgba(245,240,232,0.05);">
            <div style="font-size:0.88rem; color:#E8A838; font-weight:600; min-width:22px;">{i+1}.</div>
            <div style="font-size:0.88rem; color:rgba(245,240,232,0.65); line-height:1.7;">{q}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:36px;'></div>", unsafe_allow_html=True)

    # Evidence Requests
    st.markdown(
        '<div style="font-size:0.68rem; color:rgba(245,240,232,0.4); font-weight:600; letter-spacing:2px; '
        'text-transform:uppercase; margin-bottom:16px;">Documents Internal Audit Should Request</div>',
        unsafe_allow_html=True
    )
    for i, ev in enumerate(result.get("evidenceRequests", [])):
        st.markdown(f"""
        <div style="display:flex; gap:16px; padding:11px 0; border-bottom:1px solid rgba(245,240,232,0.05);">
            <div style="font-size:0.78rem; color:rgba(245,240,232,0.22); min-width:28px; padding-top:2px;">{i+1:02d}</div>
            <div style="font-size:0.88rem; color:rgba(245,240,232,0.6); line-height:1.65;">{ev}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:44px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Scoring Breakdown ──
    st.markdown('<div class="section-header">Scoring Breakdown</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.85rem; color:rgba(245,240,232,0.35); line-height:1.7; margin-bottom:28px; max-width:560px;">'
        'Why this company scored this way. Every criterion shows points awarded, points available, '
        'and the specific public evidence used — or lack thereof.'
        '</div>',
        unsafe_allow_html=True
    )

    def render_breakdown(items, total_label):
        running = 0
        for b in items:
            awarded = b.get("pointsAwarded", 0)
            avail   = b.get("pointsAvailable", 0)
            running += awarded
            pct     = awarded / avail if avail else 0
            bar_col = "#38A169" if pct >= 0.7 else "#E8A838" if pct >= 0.35 else "#E53E3E" if pct > 0 else "rgba(245,240,232,0.1)"
            st.markdown(f"""
            <div style="padding:14px 0; border-bottom:1px solid rgba(245,240,232,0.05);">
                <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:6px;">
                    <div style="font-size:0.85rem; font-weight:600; color:#F5F0E8;">{b.get('criterion','')}</div>
                    <div style="font-size:0.88rem; font-weight:700; color:{bar_col}; white-space:nowrap; margin-left:16px;">{awarded} / {avail}</div>
                </div>
                <div style="height:2px; background:rgba(245,240,232,0.07); margin-bottom:7px;">
                    <div style="height:100%; width:{int(pct*100)}%; background:{bar_col};"></div>
                </div>
                <div style="font-size:0.78rem; color:rgba(245,240,232,0.35); line-height:1.6; font-style:italic;">{b.get('evidence','')}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:0.82rem; font-weight:700; color:#F5F0E8; padding:14px 0; '
            f'border-top:1px solid rgba(245,240,232,0.12);">{total_label}: {running} / 100</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div style="font-size:0.68rem; color:rgba(245,240,232,0.4); font-weight:600; letter-spacing:2px; '
        'text-transform:uppercase; margin-bottom:4px;">Visible Governance Score</div>',
        unsafe_allow_html=True
    )
    render_breakdown(result.get("governanceBreakdown", []), "Total Visible Governance")

    st.markdown("<div style='margin-top:32px;'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.68rem; color:rgba(245,240,232,0.4); font-weight:600; letter-spacing:2px; '
        'text-transform:uppercase; margin-bottom:4px;">Exposure Score</div>',
        unsafe_allow_html=True
    )
    render_breakdown(result.get("exposureBreakdown", []), "Total Exposure")

    st.markdown("<div style='margin-top:44px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Footer note ──
    today_str = date.today().strftime("%B %d, %Y")
    st.markdown(
        f'<div class="footer-note">Assessment based on publicly available information as of {today_str}. '
        f'An internal audit would verify these findings directly.</div>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    # ── PDF Export ──
    try:
        pdf_bytes = generate_pdf(result)
        company_slug = result.get("companyName", "Company").replace(" ", "_")
        st.download_button(
            label="Export PDF Report",
            data=pdf_bytes,
            file_name=f"AuditMind_{company_slug}_{date.today().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
        )
    except Exception as e:
        st.warning(f"PDF generation failed: {e}. Run: pip install reportlab")
