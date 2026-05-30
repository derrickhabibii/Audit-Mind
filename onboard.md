# AuditMind — ONBOARD.md
## Cold Start Document

Read this first. Whether you are Hans, Exo, a collaborator, or a hiring manager who cloned the repo — this tells you what this project is, what is done, and what is next.

---

## 30-Second Version

AuditMind is a Shadow AI risk scanner. You give it a company URL. It researches the company's public profile using Claude AI with live web search, scores it on two dimensions (how exposed they are to AI risk vs. how much governance they visibly demonstrate), and produces an internal audit-style report with findings, recommended controls, and an evidence request list.

It was built to address a real gap that a VP of Internal Audit identified as his biggest concern. It has been tested on four real government software companies. The methodology is documented in a 9-section case study.

---

## The Problem It Solves

**Shadow AI** = employees using AI tools (ChatGPT, Copilot, Gemini, Notion AI) that their organization has not approved, with sensitive company data, leaving no audit trail and no way for IT or compliance to know it happened.

Traditional security controls — firewalls, DLP, CASB tools, SIEM dashboards — were not designed for this threat vector. An employee pasting a confidential contract into ChatGPT on a personal account does not trigger a single alert in any of those systems.

AuditMind gives an audit team a fast, structured starting point for scoping a Shadow AI review before going internal. It tells you where to look. The internal audit does the verification.

---

## What the Tool Produces

Given a company URL, AuditMind returns:

**Two scores:**
- **Exposure Score (0–100):** How much does this company need strong AI governance? Based on data sensitivity, regulatory environment, AI product presence, workforce distribution, and security incident history.
- **Visible Governance Score (0–100):** How much external evidence of AI governance exists? Named deliberately — the tool only measures what is publicly observable.
- **Shadow AI Gap:** Exposure minus Visible Governance. This is the headline number.

**A full report containing:**
- Executive Summary (CFO/Board-level narrative)
- Scoring Breakdown (every criterion scored with cited evidence or explicitly flagged as not found)
- Audit Findings (3–5 findings in formal internal audit language with priority and confidence ratings)
- Recommended Controls (4–6 controls with timeline and owner)
- Audit Pack (department risk zones, 7 interview questions, 10 evidence requests)
- PDF export via download button

---

## Known Results (Reference)

These scores were generated April 27, 2026 using publicly available information:

| Company | Exposure | Visible Gov | Gap | Risk Level | Confidence |
|---|---|---|---|---|---|
| Tyler Technologies | 85 | 35 | 50 | High | Medium |
| CentralSquare Technologies | 90 | 25 | 65 | Critical | Medium |
| Accela | 85 | 10 | 75 | Critical | Medium |
| OpenGov | 70 | 0 | 70 | Critical | Low |

Note: Scores may vary slightly across runs due to live web search variability. The scoring rubric criteria are fixed. This variability is documented as a known limitation in the case study.

---

## File Structure

```
AuditMind/
├── app.py              ← main Streamlit app, all logic in one file
├── requirements.txt    ← pip install from here
├── CLAUDE.md           ← full project mastermind brief (agents read this)
├── ONBOARD.md          ← this file
├── PRD.md              ← product requirements and phase plan
├── SESSION_LOG.md      ← running log of what changed and when
├── README.md           ← public-facing repo description
└── docs/
    ├── AuditMind_CaseStudy_v2.docx   ← full methodology and peer comparison
    └── sample_report_tyler.pdf        ← sample output for Tyler Technologies
```

---

## Tech Stack

| Component | Detail |
|---|---|
| Language | Python |
| UI | Streamlit |
| AI | Anthropic API — `claude-sonnet-4-20250514` |
| Web search | `web_search_20250305` tool |
| PDF export | ReportLab |
| Deployment | Streamlit Cloud (free tier) |

---

## How to Run Locally

```bash
# 1. Clone
git clone https://github.com/derrickhabibii/Audit-Mind.git
cd Audit-Mind

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API key
export ANTHROPIC_API_KEY="sk-ant-..."   # Mac/Linux
# set ANTHROPIC_API_KEY=sk-ant-...      # Windows

# 4. Run
streamlit run app.py
# Opens at http://localhost:8501
```

Test with: `https://www.tylertech.com`

Expected result: Exposure 85, Visible Governance ~35, Gap ~50, High Risk.

---

## If You Are Hans

Your job is to review `app.py` and validate it is correct before Exo touches anything. Check:

- SYSTEM_PROMPT is present and complete
- `extract_json()` function is present and uses `rfind` for closing brace
- `run_assessment()` has a proper tool-use loop (max 5 iterations, does not exit early on tool_use blocks without final text)
- Streamlit UI renders all tabs correctly
- Model is exactly `claude-sonnet-4-20250514`
- Web search tool name is exactly `web_search_20250305`
- `max_tokens` is at least 4000

Flag anything wrong immediately. Do not let Exo start until you have verified the file.

Full project context is in CLAUDE.md.

---

## If You Are Exo

Your job is to build. Hans tells you what to fix or add. You implement it.

Rules:
- One task at a time
- Confirm with Derrick before starting each new task
- Update SESSION_LOG.md when you finish
- Do not change the scoring rubric
- Do not change the model name or tool name

Current Phase 1 tasks (in order):
1. Create `requirements.txt`
2. Verify `app.py` runs end-to-end (Hans signs off first)
3. Deploy to Streamlit Cloud
4. Take screenshots for README
5. Upgrade README

Full project context is in CLAUDE.md.

---

## If You Are a Human Reading This Repo

The full methodology, scoring rubric, and peer comparison across four government software companies is in `docs/AuditMind_CaseStudy_v2.docx`.

A sample output report for Tyler Technologies is in `docs/sample_report_tyler.pdf`.

The live tool is deployed at: [Streamlit Cloud link — to be added after deployment]

Built by Derrick Chua Jingye | William Jewell College | May 2026