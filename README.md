# 🧬 LangChain Multi-Agent Research System

An autonomous multi-agent research intelligence system powered by **LangChain**, **Google Gemini**, **Tavily Web Search**, and **Trafilatura**.

---

## 🏗️ Architecture Overview

The pipeline orchestrates 4 specialized agents working in sequence:

```
[User Topic]
      │
      ▼
┌───────────────────────────┐
│ 🔍 1. Search Agent        │ ➔ Tavily Search API gathers recent, authoritative sources
└─────────────┬─────────────┘
              ▼
┌───────────────────────────┐
│ 📑 2. Reader Agent        │ ➔ Trafilatura & Readability deep-scrape top target URL
└─────────────┬─────────────┘
              ▼
┌───────────────────────────┐
│ ✍️ 3. Writer Agent         │ ➔ Gemini 3.5 synthesizes structured executive research report
└─────────────┬─────────────┘
              ▼
┌───────────────────────────┐
│ ⚖️ 4. Critic Agent        │ ➔ Gemini 3.5 evaluates strictly: 10-point score & review
└─────────────┬─────────────┘
              ▼
[Final Research Dossier & Scorecard]
```

---

## 🚀 Quick Start

### 1. Configure Environment Variables
Create or verify your `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Web UI
Launch the interactive dashboard:

```bash
streamlit run app.py
```
*(Or on Windows, simply double-click `run_app.bat`)*

### 4. Run via Terminal / CLI
To execute the pipeline directly in the console:

```bash
python main.py
```

---

## 🌟 Streamlit UI Features

- **Interactive Topic Launcher:** Quick-select trending research presets or input custom queries.
- **Live Agent Pipeline Status:** Real-time visual progress tracker across the 4 stages.
- **Executive Report View:** Fully styled markdown with word counts and reading estimates.
- **Critic Scorecard:** Visual 10-point score badge, enumerated strengths, improvements, and verdict banner.
- **Search Intelligence Inspector:** Source cards linking directly to retrieved articles with snippets.
- **Deep Scraped Preview:** Review extracted content volume and full text processed by the Reader Agent.
- **Session History:** Retain and compare multiple research runs during your session.
- **Export Options:** Download as Markdown (`.md`), Plain Text (`.txt`), or Full Research Bundle (`.json`).
