# AuditMind — SESSION_LOG.md

Log every session here. Format: date, who worked, what was done, what changed, what is next.

---

## Session 001 — 2026-04-27 | Derrick
**What happened:** Built initial version of `app.py` as alternative assignment for Data Analytics in Business Accounting (Prof. Mark Satterfield, VP Internal Audit, Tyler Technologies). Single-file Streamlit app with Anthropic API, web search tool-use loop, two-score system (Exposure + Visible Governance), PDF export via ReportLab.

**What was tested:** Four companies in the government software sector.
- Tyler Technologies: Exposure 85, Visible Gov 35, Gap 50, High Risk
- CentralSquare Technologies: Exposure 90, Visible Gov 25, Gap 65, Critical
- Accela: Exposure 85, Visible Gov 10, Gap 75, Critical
- OpenGov: Exposure 70, Visible Gov 0, Gap 70, Critical

**What was created:** `app.py`, `README.md`, `CLAUDE.md` (initial Hans brief), `AuditMind_CaseStudy_v2.docx`

**Status:** Assignment submitted. App functional locally.

---

## Session 002 — 2026-05-29 | Derrick + Claude (mastermind)
**What happened:** Decided to properly engineer AuditMind as a portfolio piece for Malaysia job hunt. Read full case study, assessed current file structure, determined Phase 1 scope.

**What was created:**
- `CLAUDE.md` — full rewrite, mastermind brief for two-agent workflow
- `ONBOARD.md` — cold start doc for Hans, Exo, and human readers
- `PRD.md` — product requirements, phase plan, success criteria
- `SESSION_LOG.md` — this file

**What is next (Phase 1 tasks for Exo, in order):**
1. Hans reviews `app.py` — validate tool-use loop, JSON extraction, tab rendering, model/tool names
2. Exo creates `requirements.txt`
3. Deploy to Streamlit Cloud
4. Take screenshots of UI and sample report
5. Upgrade README with screenshots, live link, case study reference
6. Create `docs/` folder, add case study docx
7. Generate and add one sample PDF report (Tyler Technologies)
8. Push everything to GitHub main

**Status:** Governance docs complete. Awaiting Hans review of app.py.

---

## Session 003 — 2026-05-29 | Derrick + Exo

**What happened:** Created `requirements.txt`. Read `app.py` and identified all imports. Three third-party packages: `streamlit`, `anthropic`, `reportlab`. All standard library imports (`json`, `re`, `time`, `io`, `datetime`) excluded. No version constraints per Derrick's instruction.

**What was created:**
- `requirements.txt` — three packages, no version pins

**What is next (Phase 1, continuing in order):**
1. ~~Hans reviews `app.py`~~ — complete (Hans signed off)
2. ~~Create `requirements.txt`~~ — complete (this session)
3. Deploy to Streamlit Cloud
4. Take screenshots of UI and sample report
5. Upgrade README with screenshots, live link, case study reference
6. Create `docs/` folder, add case study docx
7. Generate and add one sample PDF report (Tyler Technologies)
8. Push everything to GitHub main

**Status:** requirements.txt done. Next task is Streamlit Cloud deployment — awaiting Derrick's go-ahead.

---

## Session 004 — 2026-05-29 | Derrick + Exo

**What happened:** Built out the full docs/ folder structure and upgraded README to portfolio-grade.

**What was done:**
- Created `docs/` and `docs/screenshots/` folders
- Moved `AuditMind_CaseStudy_v2.docx` into `docs/`
- Copied `AuditMind_Tyler_Technologies_20260530.pdf` from Downloads into `docs/`
- Copied and renamed 4 screenshots into `docs/screenshots/`:
  - `score_cards.png` — score cards hero view (Exposure/Gap/Visible Gov/Confidence)
  - `audit_findings.png` — all 3 audit findings with priority + confidence badges
  - `recommended_controls.png` — 4 recommended actions with owner and timeline
  - `scoring_breakdown.png` — visible governance breakdown with progress bars
- Replaced `README.md` with portfolio-grade version (Derrick-authored)
- Note: screenshot filenames used Unicode narrow no-break space ` ` before "PM" — required Python shutil to copy correctly

**What is next (Phase 1, continuing in order):**
1. ~~Hans reviews `app.py`~~ — complete
2. ~~Create `requirements.txt`~~ — complete
3. ~~Docs folder + screenshots + README upgrade~~ — complete (this session)
4. Deploy to Streamlit Cloud — get public URL, add to README
5. Push everything to GitHub main

**Status:** Repo is portfolio-ready locally. Awaiting Streamlit Cloud deployment and final GitHub push.

---

<!-- Add new sessions below this line -->