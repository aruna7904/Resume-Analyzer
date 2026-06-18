# Smart AI Resume Analyzer Agent 🤖📄

An advanced, end-to-end Applicant Tracking System (ATS) optimization engine and interactive analytics platform. Built as a final-year CSBS capstone project, this application parses unstructured PDF resumes, executes programmatic keyword extraction, cross-examines applicant profiles against enterprise job descriptions, and renders data-driven feedback through an interactive dashboard.

Powered by a production-stable **Google Gemini LLM pipeline** and supported by a robust **SQLite database backend**.

---

## 🌟 Core Features

* **Automated PDF Ingestion**: Implements `pypdf` stream parsing to dynamically extract raw textual blocks from unstructured document formats.
* **AI Analysis Pipeline**: Orchestrates structured text processing using the `gemini-flash-latest` generative model to analyze profile relevancy.
* **Strict JSON Schema Enforcement**: Programmatically strips LLM markdown syntax and isolates structural payloads using a custom boundary index trimmer.
* **Local Auditing & Persistence**: Saves analysis results locally to an atomic SQLite tracking ledger.
* **Dynamic Analytics UI**: Visualizes matching metrics, exact core skill mappings, missing keyword gaps, granular optimization suggestions, and high-impact summaries.
* **Fault-Tolerant Design**: Features graceful error interceptors to handle external API platform rate limits (`HTTP 429 Quota Exceeded`) seamlessly.

---

## 🛠️ Tech Stack & Architecture

* **Backend Engine**: Python 3.13, Flask (Micro-framework)
* **AI Orchestration**: Google GenAI SDK (`google.generativeai`)
* **Document Parser**: PyPDF
* **Database Ledger**: SQLite 3 (Atomic relational storage)
* **Frontend Interface**: Semantic HTML5, CSS3 Grid/Flexbox Layouts, JavaScript

---

## 📊 Database Schema Structure

The system persists structured analysis logs within an `analysis_history` table:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `analysis_id` | INTEGER (PK) | Auto-incrementing unique tracking identifier. |
| `user_id` | INTEGER | Maps to the internal system profile index (Default: `1`). |
| `job_title` | TEXT | Standardized and cleaned position target title string. |
| `ats_score` | INTEGER | Match metric scalar calculated from 0 to 100. |
| `skills_found` | TEXT (JSON) | Stringified JSON array recording matched core competencies. |
| `missing_skills`| TEXT (JSON) | Stringified JSON array recording critical requirement gaps. |
| `suggestions` | TEXT | Granular, actionable optimization strategies. |
| `summary` | TEXT | Tailored, high-impact narrative resume profile summary copy. |
| `analyzed_at` | TIMESTAMP | Automated server generation chronological log tracker. |

