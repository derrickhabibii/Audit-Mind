# AuditMind — PRD.md
## Product Requirements Document

---

## Problem Statement

Internal audit teams have no fast, structured starting point for scoping a Shadow AI review. Traditional security controls (DLP, CASB, SIEM) were not designed to detect unauthorized AI tool usage. An employee pasting sensitive data into ChatGPT on a personal account leaves no footprint in any corporate security system.

Before an audit team can go internal, they need to know: how exposed is this company to Shadow AI risk, and what external signals exist that governance is or isn't keeping pace with AI adoption?

That pre-screening layer does not exist as a packaged product. AuditMind is it.

---

## What Done Looks Like

### Phase 1 — Portfolio-Ready (current sprint)

**Definition of done:**
- [ ] `requirements.txt` exists and is accurate
- [ ] `app.py` runs end-to-end with no errors on a fresh install
- [ ] Deployed on Streamlit Cloud with a public URL
- [ ] README includes: what it does, how to run it, screenshots of UI and report output, live demo link, and link to case study
- [ ] `docs/` folder contains case study docx and one sample PDF report
- [ ] SESSION_LOG.md is up to date
- [ ] All files are pushed to GitHub main branch

**Success criterion:** A hiring manager or technical interviewer clicks the GitHub link, reads the README in 60 seconds, clicks the Streamlit demo link, and can see the tool running without installing anything.

---

### Phase 2 — Malaysian Regulatory Context Mode (next sprint, after Phase 1 deployed)

**Why this feature:** Every job Derrick is applying to in Malaysia involves data governance or AI compliance. PDPA, Bank Negara's AI governance guidelines, SC guidelines on algorithmic trading. Adding a Malaysia-specific context mode makes AuditMind directly relevant to every target company — Farben, Cleverus, any BFSI player in KL.

**What it does:**
- Adds a country context selector in the UI (Global / Malaysia)
- When Malaysia is selected, the SYSTEM_PROMPT includes PDPA requirements, Bank Negara RMiT framework references, and SC guidelines
- Scoring rubric remains the same — criteria weights stay fixed
- Report output notes Malaysian regulatory context in the findings section

**Definition of done:**
- [ ] Country context selector renders in UI
- [ ] SYSTEM_PROMPT correctly injects Malaysian regulatory context when selected
- [ ] Tested on at least one Malaysian company (Maybank, CIMB, or a fintech)
- [ ] Results documented in SESSION_LOG.md

---

### Phase 3 — Batch Scanning (stretch goal)

- [ ] UI accepts multiple URLs (text area, one per line)
- [ ] Runs assessments sequentially with progress indicator
- [ ] Produces a comparison table across all companies scanned
- [ ] Exportable as single combined PDF

---

## Non-Goals (What This Is Not)

- Not an anomaly detection tool (AuditBoard does this)
- Not an internal monitoring tool (requires network access we don't have)
- Not a real-time alert system
- Not a replacement for internal audit — it is a pre-screen and starting point
- Does not access any internal company systems

---

## Constraints

- Scores may vary across runs due to live web search variability — this is documented and acceptable at prototype stage
- Scoring rubric criteria are fixed and must not be changed
- Model must remain `claude-sonnet-4-20250514`
- Web search tool must remain `web_search_20250305`
- Free tier Streamlit Cloud deployment (100 app instances, usage limits apply)
- Anthropic API costs real money — demo should not be abused

---

## Users

**Primary — Internal audit practitioner:**
Question: Where do we stand on AI governance? Are we ready if a government client or audit committee asks us to prove it?
Use: Planning input — decides whether AI governance belongs in the next audit cycle and which areas to prioritize.

**Secondary — Government IT director / procurement:**
Question: Is this vendor mature enough on AI governance to trust with citizen data before I renew this contract?
Use: Vendor pre-screen — identifies which vendors warrant deeper due diligence and what specific evidence to request.

**Tertiary (job hunt context) — Technical hiring manager:**
Question: Can this candidate actually build something useful with AI?
Use: Portfolio demonstration — shows real engineering, real methodology, real results on real companies.

---

## Key Metrics (for portfolio positioning)

- 4 companies assessed in peer comparison
- 9-section case study documenting methodology
- Two-score system with gap analysis (more sophisticated than single-score tools)
- Full audit pack output (findings, controls, interview questions, evidence requests)
- Government software sector focus (highest data sensitivity use case)