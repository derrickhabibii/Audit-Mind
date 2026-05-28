# AuditMind — Shadow AI Risk Scanner

A web app that takes a company URL and generates a formal Shadow AI exposure assessment using Claude AI with live web research.

**Shadow AI** = employees using unauthorized AI tools (ChatGPT, Copilot, etc.) with sensitive company data, with no visibility, no audit trail, and no controls. It's one of the fastest-growing blind spots in enterprise risk management.

AuditMind scans a company's public profile and produces an audit-style risk report in seconds.

---

## What It Does

1. Takes a company website URL as input
2. Researches the company's public profile via live web search — industry, data sensitivity, workforce model, AI partnerships, breach history, certifications
3. Scores the company across two dimensions using a fixed rubric:
   - **Exposure Score** (0–100) — how much AI risk the company is exposed to based on data sensitivity, regulatory environment, workforce distribution, and AI adoption
   - **Visible Governance Score** (0–100) — how much AI governance the company publicly demonstrates
4. Computes a **Shadow AI Gap** = Exposure minus Visible Governance
5. Generates a full report: executive summary, audit findings, recommended controls, department risk zones, audit interview questions, and evidence requests

---

## Output

| Field | Description |
|---|---|
| Exposure Score | Risk exposure based on data sensitivity, scale, regulatory environment |
| Visible Governance Score | Externally observable governance signals only |
| Shadow AI Gap | The delta — where internal audit should look |
| Risk Level | Critical / High / Medium / Low |
| Confidence | How much public evidence was available |

The report includes:
- **Executive Summary** — CFO/Board-level narrative
- **Audit Findings** — 3–5 findings in formal internal audit language with priority and confidence ratings
- **Recommended Controls** — 4–6 controls with timeline and owner
- **Audit Pack** — department risk zones, 7 interview questions, 10 evidence requests tailored to the company
- **Scoring Breakdown** — every criterion scored with the specific public evidence cited (or explicitly flagged as not found)
- **PDF Export** — download the full report

---

## Tech Stack

- Python
- [Anthropic API](https://www.anthropic.com) (claude-sonnet-4-20250514 with web search)
- Streamlit
- ReportLab (PDF generation)

---

## Setup

**1. Install dependencies**
```bash
pip install anthropic streamlit reportlab
```

**2. Set your API key**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**3. Run**
```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## Example

Input: `https://www.tylertech.com`

Tyler Technologies handles government data for courts, tax systems, and public safety across the US — high exposure, limited publicly visible AI governance signals.

| Score | Value |
|---|---|
| Exposure | 85 / 100 |
| Visible Governance | 35 / 100 |
| Shadow AI Gap | 50 — **High Risk** |
| Confidence | Medium |

---

## Important Notes

- **This tool measures observable signals, not confirmed internal AI usage.** A low Visible Governance Score may reflect limited public disclosure rather than weak internal controls.
- All findings are risk indicators requiring internal verification — not audit conclusions.
- Scores are generated from publicly available information only. Two runs on the same company may produce slightly different scores due to the non-deterministic nature of web search and LLM outputs.

---

## Why This Exists

Built as a practical response to a real gap: Shadow AI governance tooling doesn't exist as a packaged product. Enterprise DLP tools catch data leaving the network. CASB tools monitor cloud app usage. But nothing gives an audit team a fast, structured starting point for scoping a Shadow AI review before they go internal.

This is that starting point.
