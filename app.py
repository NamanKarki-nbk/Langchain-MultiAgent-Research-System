"""
LangChain Multi-Agent Research System - Streamlit User Interface
================================================================
A modern, intuitive dashboard for orchestrating autonomous research agents:
- Search Agent: Real-time intelligence gathering via Tavily
- Reader Agent: Deep content extraction and scraping via Trafilatura
- Writer Agent: Structured executive report synthesis via Google Gemini
- Critic Agent: Strict peer review, scoring & actionable feedback
"""

import os
import sys
import time
import re
import json
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the existing pipeline without modifying any underlying code
from src.pipeline.pipeline import run_research_pipeline


# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="NexusAgent • Multi-Agent Research System",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==============================================================================
# Custom CSS Styling
# ==============================================================================
st.markdown(
    """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    code, pre, .stCode {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1350px;
    }

    /* Hero Header */
    .hero-container {
        position: relative;
        padding: 2rem 2.2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(168, 85, 247, 0.05) 50%, rgba(6, 182, 212, 0.08) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.15);
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        line-height: 1.15;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.4rem;
        letter-spacing: -0.02em;
    }

    .hero-desc {
        color: #64748B;
        font-size: 1.02rem;
        max-width: 780px;
        line-height: 1.5;
        margin-bottom: 1.2rem;
    }

    /* Agent Architecture Flow */
    .agent-pipeline-flow {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-top: 1.2rem;
    }

    @media (max-width: 900px) {
        .agent-pipeline-flow {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    .agent-pill-card {
        padding: 0.85rem 1rem;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.25s ease;
    }

    .agent-pill-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }

    .agent-pill-name {
        font-weight: 700;
        font-size: 0.88rem;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 3px;
    }

    .agent-pill-role {
        font-size: 0.74rem;
        color: #94A3B8;
        line-height: 1.3;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 1.1rem 1.2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }

    .metric-val {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
        margin: 0.3rem 0;
    }

    .metric-lbl {
        font-size: 0.78rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }

    /* Critic Evaluation Card */
    .critic-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 16px;
        padding: 1.4rem;
        margin-bottom: 1.5rem;
    }

    .verdict-banner {
        border-left: 4px solid #8B5CF6;
        background: rgba(139, 92, 246, 0.08);
        padding: 0.9rem 1.2rem;
        border-radius: 0 10px 10px 0;
        font-size: 1rem;
        font-style: italic;
        margin: 1rem 0;
        color: #DDD6FE;
    }

    /* Source Link Cards */
    .source-card {
        padding: 0.9rem 1.1rem;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.07);
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
    }

    .source-card:hover {
        border-color: rgba(6, 182, 212, 0.4);
        background: rgba(6, 182, 212, 0.03);
    }

    .source-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #38BDF8;
        margin-bottom: 4px;
        text-decoration: none;
    }

    .source-snippet {
        font-size: 0.82rem;
        color: #94A3B8;
        line-height: 1.4;
    }

    /* Terminal Console */
    .terminal-container {
        background: #0B0F19;
        color: #E2E8F0;
        border-radius: 12px;
        border: 1px solid #1E293B;
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        max-height: 380px;
        overflow-y: auto;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 8px 18px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# Helper Classes & Utilities
# ==============================================================================
class StdoutCapture:
    """Captures stdout from run_research_pipeline to provide real-time updates and logs."""
    def __init__(self, status_widget=None, log_placeholder=None):
        self.status_widget = status_widget
        self.log_placeholder = log_placeholder
        self.lines = []
        self._stdout = sys.stdout

    def write(self, text):
        self._stdout.write(text)
        if text.strip():
            clean = text.strip()
            self.lines.append(clean)
            if self.status_widget:
                if "step 1" in clean.lower():
                    self.status_widget.update(
                        label="🔍 Step 1/4: Search Agent querying Tavily for web intelligence...",
                        state="running",
                    )
                elif "step 2" in clean.lower():
                    self.status_widget.update(
                        label="📑 Step 2/4: Reader Agent scraping and extracting top resources...",
                        state="running",
                    )
                elif "step 3" in clean.lower():
                    self.status_widget.update(
                        label="✍️ Step 3/4: Writer Agent drafting comprehensive synthesis report...",
                        state="running",
                    )
                elif "step 4" in clean.lower():
                    self.status_widget.update(
                        label="⚖️ Step 4/4: Critic Agent conducting strict peer review & evaluation...",
                        state="running",
                    )

    def flush(self):
        self._stdout.flush()

    def get_logs(self):
        return "\n".join(self.lines)


def to_string(content) -> str:
    """Safely converts message content (str, list of dicts/strings, or any object) into a string."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                # LangChain & Gemini format: [{'type': 'text', 'text': '...'}]
                if "text" in item and item["text"]:
                    parts.append(str(item["text"]))
                elif "content" in item and item["content"]:
                    parts.append(str(item["content"]))
                else:
                    parts.append(str(item))
            elif hasattr(item, "text"):
                parts.append(str(item.text))
            elif hasattr(item, "content"):
                parts.append(to_string(item.content))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    if isinstance(content, dict):
        if "text" in content:
            return str(content["text"])
        if "content" in content:
            return str(content["content"])
        return json.dumps(content, indent=2)
    if hasattr(content, "content"):
        return to_string(content.content)
    return str(content)


def parse_critic_feedback(feedback_text):
    """Parses structured feedback into Score, Strengths, Areas to Improve, and Verdict."""
    feedback_text = to_string(feedback_text)
    data = {
        "score": None,
        "strengths": [],
        "improvements": [],
        "verdict": "",
        "raw": feedback_text,
    }
    if not feedback_text.strip():
        return data

    # Extract score
    score_match = re.search(r"Score:\s*([0-9]+(?:\.[0-9]+)?)\s*/\s*10", feedback_text, re.IGNORECASE)
    if score_match:
        try:
            data["score"] = float(score_match.group(1))
        except ValueError:
            data["score"] = None

    # Extract Strengths
    strengths_match = re.search(
        r"Strengths:\s*\n((?:[\s*-].*\n?)+?)(?=\n\s*(?:Areas to Improve|One line verdict|\Z))",
        feedback_text,
        re.IGNORECASE,
    )
    if strengths_match:
        items = [
            line.strip().lstrip("-*• ")
            for line in strengths_match.group(1).split("\n")
            if line.strip().lstrip("-*• ")
        ]
        data["strengths"] = items

    # Extract Areas to Improve
    improve_match = re.search(
        r"Areas to Improve:\s*\n((?:[\s*-].*\n?)+?)(?=\n\s*(?:One line verdict|\Z))",
        feedback_text,
        re.IGNORECASE,
    )
    if improve_match:
        items = [
            line.strip().lstrip("-*• ")
            for line in improve_match.group(1).split("\n")
            if line.strip().lstrip("-*• ")
        ]
        data["improvements"] = items

    # Extract Verdict
    verdict_match = re.search(
        r"One line verdict:\s*\n?(.*)", feedback_text, re.IGNORECASE | re.DOTALL
    )
    if verdict_match:
        data["verdict"] = verdict_match.group(1).strip()

    return data


def parse_search_results(raw_search):
    """Parses raw Tavily string or agent output into structured search items."""
    raw_search = to_string(raw_search)
    items = []
    if not raw_search.strip():
        return items

    # Strategy 1: Delimited by "-----" as formatted by web_search tool
    if "-----" in raw_search:
        blocks = raw_search.split("-----")
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            title = ""
            url = ""
            snippet = ""

            title_m = re.search(r"Ttile:\s*(.*?)(?=\nURL:|$)", block, re.DOTALL | re.IGNORECASE)
            url_m = re.search(r"URL:\s*(https?://[^\s\n]+)", block, re.IGNORECASE)
            snip_m = re.search(r"Snippit:\s*(.*?)$", block, re.DOTALL | re.IGNORECASE)

            if title_m:
                title = title_m.group(1).strip()
            if url_m:
                url = url_m.group(1).strip()
            if snip_m:
                snippet = snip_m.group(1).strip()

            if url or title:
                items.append({
                    "title": title or "Source Reference",
                    "url": url,
                    "snippet": snippet or block[:200],
                })

    # Strategy 2: Extract markdown links [Title](https://...) from agent's response
    if not items:
        md_links = re.findall(r"\[([^\]]+)\]\((https?://[^\s\)]+)\)", raw_search)
        for t, u in md_links:
            items.append({
                "title": t.strip(),
                "url": u.strip(),
                "snippet": "Discovered source reference",
            })

    # Strategy 3: Extract bare URLs if still no links found
    if not items:
        bare_urls = re.findall(r"(https?://[^\s\)\],\"'>]+)", raw_search)
        seen = set()
        for u in bare_urls:
            if u not in seen:
                seen.add(u)
                domain = u.split("/")[2] if "//" in u else u
                items.append({
                    "title": domain,
                    "url": u,
                    "snippet": "Web source discovered by Search Agent",
                })
            if len(items) >= 5:
                break

    return items


# ==============================================================================
# Session State Initialization
# ==============================================================================
if "history" not in st.session_state:
    st.session_state["history"] = []

if "current_results" not in st.session_state:
    st.session_state["current_results"] = None

if "current_topic" not in st.session_state:
    st.session_state["current_topic"] = ""

if "current_time" not in st.session_state:
    st.session_state["current_time"] = 0.0

if "current_logs" not in st.session_state:
    st.session_state["current_logs"] = ""

if "input_topic_value" not in st.session_state:
    st.session_state["input_topic_value"] = "The impact of AI on the job market in 2026"


# ==============================================================================
# Sidebar
# ==============================================================================
with st.sidebar:
    st.markdown("### 🧬 NexusAgent System")
    st.caption("Autonomous LangChain Multi-Agent Architecture")
    st.markdown("---")

    # API Keys Health Check
    gemini_key = os.getenv("GEMINI_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")

    st.markdown("#### 🔌 Connection Status")
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        if gemini_key:
            st.success("Gemini API\nConnected", icon="🟢")
        else:
            st.error("Gemini API\nMissing Key", icon="🔴")
    with col_k2:
        if tavily_key:
            st.success("Tavily API\nConnected", icon="🟢")
        else:
            st.error("Tavily API\nMissing Key", icon="🔴")

    if not gemini_key or not tavily_key:
        st.warning("⚠️ Verify your `.env` file contains valid `GEMINI_API_KEY` and `TAVILY_API_KEY`.")

    st.markdown("---")

    # Architecture Overview
    st.markdown("#### 🤖 Agent Hierarchy")
    with st.expander("Explore Agent Roles", expanded=False):
        st.markdown(
            """
            - **🔍 Search Agent**
              - *Tool:* `web_search` (Tavily Client)
              - *Role:* Finds top reliable sources, recent developments & snippets.
            
            - **📑 Reader Agent**
              - *Tool:* `scrape_url` (Trafilatura & Readability)
              - *Role:* Scrapes deep content from the most authoritative URL.
            
            - **✍️ Writer Agent**
              - *Model:* Gemini 3.5 Flash Lite
              - *Role:* Synthesizes findings into Introduction, Key Findings, Conclusion & Sources.
            
            - **⚖️ Critic Agent**
              - *Model:* Gemini 3.5 Flash Lite
              - *Role:* Rigorous peer evaluation: 10-point score, strengths & areas to improve.
            """
        )

    st.markdown("---")

    # Research History
    st.markdown("#### 📚 Session History")
    if st.session_state["history"]:
        st.caption(f"{len(st.session_state['history'])} research reports in this session:")
        for idx, item in enumerate(reversed(st.session_state["history"])):
            hist_title = item["topic"]
            if len(hist_title) > 34:
                hist_title = hist_title[:31] + "..."
            
            score_badge = ""
            if item.get("score") is not None:
                score_badge = f" • ⭐ {item['score']}/10"

            if st.button(
                f"📄 {hist_title}{score_badge}",
                key=f"hist_{idx}",
                use_container_width=True,
            ):
                st.session_state["current_topic"] = item["topic"]
                st.session_state["current_results"] = item["results"]
                st.session_state["current_time"] = item.get("time", 0.0)
                st.session_state["current_logs"] = item.get("logs", "")
                st.rerun()

        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state["history"] = []
            st.rerun()
    else:
        st.info("No prior research runs yet. Launch a topic to start building history.")

    st.markdown("---")
    st.caption("Engineered with LangChain · Google Gemini · Streamlit")


# ==============================================================================
# Hero Section & Architectural Pipeline
# ==============================================================================
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-badge">Autonomous Multi-Agent Intelligence</div>
        <div class="hero-title">NexusAgent Research System</div>
        <div class="hero-desc">
            Orchestrate collaborative AI agents to autonomously research complex topics, scrape authoritative sources, draft comprehensive reports, and perform rigorous peer critique.
        </div>
        <div class="agent-pipeline-flow">
            <div class="agent-pill-card">
                <div class="agent-pill-name" style="color: #60A5FA;"><span>🔍</span> 1. Search Agent</div>
                <div class="agent-pill-role">Tavily Web Search · Source Discovery</div>
            </div>
            <div class="agent-pill-card">
                <div class="agent-pill-name" style="color: #34D399;"><span>📑</span> 2. Reader Agent</div>
                <div class="agent-pill-role">Deep Page Scraping · Multi-Strategy</div>
            </div>
            <div class="agent-pill-card">
                <div class="agent-pill-name" style="color: #C084FC;"><span>✍️</span> 3. Writer Agent</div>
                <div class="agent-pill-role">Gemini Synthesis · Executive Report</div>
            </div>
            <div class="agent-pill-card">
                <div class="agent-pill-name" style="color: #FBBF24;"><span>⚖️</span> 4. Critic Agent</div>
                <div class="agent-pill-role">Evaluation Rubric · 10-Point Scorecard</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# Interactive Topic Input & Presets
# ==============================================================================
st.markdown("### 🎯 Enter Research Topic")

# Example Preset Buttons
st.caption("💡 Quick Suggestions:")
preset_cols = st.columns(4)
presets = [
    "The impact of AI on the job market in 2026",
    "Quantum computing breakthroughs in drug discovery",
    "Commercial viability of solid-state EV batteries",
    "Autonomous AI agent frameworks in enterprise automation",
]

for p_col, preset_text in zip(preset_cols, presets):
    with p_col:
        short_label = preset_text if len(preset_text) <= 32 else preset_text[:29] + "..."
        if st.button(short_label, help=preset_text, use_container_width=True):
            st.session_state["input_topic_value"] = preset_text
            st.rerun()

topic_input = st.text_input(
    label="Topic or Question to Investigate",
    value=st.session_state.get("input_topic_value", ""),
    placeholder="e.g. Current status of nuclear fusion energy commercialization in 2026",
    label_visibility="collapsed",
)

col_btn, col_empty = st.columns([1, 3])
with col_btn:
    run_clicked = st.button("🚀 Launch Research Pipeline", type="primary", use_container_width=True)


# ==============================================================================
# Pipeline Execution Handler
# ==============================================================================
if run_clicked:
    if not topic_input.strip():
        st.warning("⚠️ Please provide a topic before launching the research pipeline.")
    else:
        topic = topic_input.strip()
        status_box = st.status("Initializing Multi-Agent Pipeline...", expanded=True)
        capture = StdoutCapture(status_widget=status_box)
        orig_stdout = sys.stdout

        start_time = time.time()
        try:
            sys.stdout = capture
            # Invoke the user's existing pipeline function directly
            raw_state = run_research_pipeline(topic)
            elapsed = time.time() - start_time
            sys.stdout = orig_stdout

            # Safely normalize all fields to strings
            result_state = {
                "report": to_string(raw_state.get("report", "")),
                "feedback": to_string(raw_state.get("feedback", "")),
                "search_results": to_string(raw_state.get("search_results", "")),
                "scraped_content": to_string(raw_state.get("scraped_content", "")),
            }

            status_box.update(
                label=f"✅ Research Pipeline Complete in {elapsed:.1f}s!",
                state="complete",
                expanded=False,
            )

            # Parse critic feedback for scoring
            feedback_parsed = parse_critic_feedback(result_state["feedback"])

            # Update session state
            st.session_state["current_topic"] = topic
            st.session_state["current_results"] = result_state
            st.session_state["current_time"] = elapsed
            st.session_state["current_logs"] = capture.get_logs()

            # Record in history
            st.session_state["history"].append({
                "topic": topic,
                "results": result_state,
                "score": feedback_parsed.get("score"),
                "time": elapsed,
                "logs": capture.get_logs(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })

            st.toast("🎉 Multi-agent research completed successfully!", icon="✅")

        except Exception as ex:
            sys.stdout = orig_stdout
            status_box.update(label="❌ Pipeline Execution Encountered an Error", state="error")
            st.error(f"**Execution Error:** {str(ex)}")
            st.info("💡 Ensure your internet connection is active and that your API keys in `.env` are valid.")


# ==============================================================================
# Results Presentation
# ==============================================================================
if st.session_state["current_results"]:
    results = st.session_state["current_results"]
    topic = st.session_state["current_topic"]
    elapsed_time = st.session_state["current_time"]
    logs = st.session_state["current_logs"]

    report_text = to_string(results.get("report", ""))
    critic_text = to_string(results.get("feedback", ""))
    search_text = to_string(results.get("search_results", ""))
    scraped_text = to_string(results.get("scraped_content", ""))

    # Parse details
    parsed_critic = parse_critic_feedback(critic_text)
    parsed_sources = parse_search_results(search_text)

    word_count = len(report_text.split())
    char_count = len(report_text)
    read_time_mins = max(1, round(word_count / 200))

    st.markdown("---")
    st.markdown(f"## 📊 Research Dossier: *{topic}*")

    # Metrics Summary Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        score_val = parsed_critic.get("score")
        score_display = f"{score_val:.0f}/10" if score_val is not None else "Reviewed"
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">Critic Score</div>
                <div class="metric-val" style="color: {'#10B981' if (score_val or 0) >= 8 else '#F59E0B'};">
                    {score_display}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">Report Length</div>
                <div class="metric-val" style="color: #6366F1;">{word_count:,} <span style="font-size: 1rem; color: #94A3B8;">words</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">Est. Reading Time</div>
                <div class="metric-val" style="color: #06B6D4;">~{read_time_mins} <span style="font-size: 1rem; color: #94A3B8;">min</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-lbl">Execution Duration</div>
                <div class="metric-val" style="color: #8B5CF6;">{elapsed_time:.1f} <span style="font-size: 1rem; color: #94A3B8;">sec</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs for structured viewing
    tab_report, tab_critic, tab_search, tab_scrape, tab_logs = st.tabs([
        "📄 Executive Report",
        "⚖️ Critic Evaluation",
        "🔍 Search Intelligence",
        "📑 Deep Scraped Content",
        "💻 Terminal Logs",
    ])

    # --------------------------------------------------------------------------
    # Tab 1: Executive Report (Writer Agent)
    # --------------------------------------------------------------------------
    with tab_report:
        col_rep_head, col_rep_actions = st.columns([2, 1])
        with col_rep_head:
            st.markdown("### ✍️ Final Synthesized Report")
            st.caption("Drafted by Writer Chain (Gemini 3.5 Flash Lite) using aggregated research")
        with col_rep_actions:
            # Download options
            st.download_button(
                label="📥 Download Markdown (.md)",
                data=report_text,
                file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
            )

        st.markdown("---")
        # Display the formatted report
        st.markdown(report_text)

        # Download plain text button
        st.markdown("---")
        col_dl1, col_dl2 = st.columns([1, 4])
        with col_dl1:
            st.download_button(
                label="📥 Download as Text (.txt)",
                data=report_text,
                file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
            )

    # --------------------------------------------------------------------------
    # Tab 2: Critic Evaluation (Critic Agent)
    # --------------------------------------------------------------------------
    with tab_critic:
        st.markdown("### ⚖️ Critic Review & Quality Scorecard")
        st.caption("Strict independent evaluation conducted by Critic Chain")

        if parsed_critic.get("verdict"):
            st.markdown(
                f"""
                <div class="verdict-banner">
                    <strong>Verdict:</strong> {parsed_critic['verdict']}
                </div>
                """,
                unsafe_allow_html=True,
            )

        col_crit_left, col_crit_right = st.columns(2)

        with col_crit_left:
            st.markdown("#### ✅ Identified Strengths")
            if parsed_critic["strengths"]:
                for s in parsed_critic["strengths"]:
                    st.markdown(f"- 🟢 **{s}**")
            else:
                st.info("No explicit strengths enumerated in the critic feedback.")

        with col_crit_right:
            st.markdown("#### 🎯 Areas to Improve")
            if parsed_critic["improvements"]:
                for imp in parsed_critic["improvements"]:
                    st.markdown(f"- 🟠 {imp}")
            else:
                st.info("No specific areas for improvement noted.")

        st.markdown("---")
        with st.expander("🔍 View Raw Critic Response"):
            st.code(critic_text, language="markdown")

    # --------------------------------------------------------------------------
    # Tab 3: Search Intelligence (Search Agent)
    # --------------------------------------------------------------------------
    with tab_search:
        st.markdown("### 🔍 Search Agent Discoveries")
        st.caption("Real-time web intelligence gathered via Tavily Search API")

        if parsed_sources:
            st.markdown(f"**Found {len(parsed_sources)} primary source documents:**")
            for idx, item in enumerate(parsed_sources, start=1):
                url = item.get("url", "#")
                st.markdown(
                    f"""
                    <div class="source-card">
                        <div style="font-size: 0.76rem; color: #64748B; font-weight: 600;">SOURCE #{idx}</div>
                        <a href="{url}" target="_blank" class="source-title">{item['title']}</a>
                        <div style="font-size: 0.78rem; color: #64748B; margin-bottom: 6px; word-break: break-all;">🔗 {url}</div>
                        <div class="source-snippet">{item['snippet']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                """
                <div class="source-card">
                    <div style="font-size: 0.76rem; color: #64748B; font-weight: 600;">SEARCH AGENT SYNTHESIS</div>
                    <div class="source-snippet">Detailed search findings are displayed below:</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(search_text)

        with st.expander("View Raw Search Agent Output"):
            st.code(search_text, language="markdown")

    # --------------------------------------------------------------------------
    # Tab 4: Deep Scraped Content (Reader Agent)
    # --------------------------------------------------------------------------
    with tab_scrape:
        st.markdown("### 📑 Reader Agent Scraped Content")
        st.caption("Clean text extracted via Trafilatura & Readability from the top selected URL")

        scrape_len = len(scraped_text)
        st.markdown(f"**Extracted Text Volume:** `{scrape_len:,}` characters")

        st.text_area(
            label="Scraped Deep Content Preview",
            value=scraped_text,
            height=380,
            disabled=True,
        )

    # --------------------------------------------------------------------------
    # Tab 5: Terminal Logs
    # --------------------------------------------------------------------------
    with tab_logs:
        st.markdown("### 💻 Multi-Agent Execution Stream")
        st.caption("Console traces and communication between Search, Reader, Writer, and Critic agents")

        if logs:
            st.markdown(f'<div class="terminal-container"><pre>{logs}</pre></div>', unsafe_allow_html=True)
        else:
            st.code("No terminal logs captured for this run.")

        st.download_button(
            label="📥 Download Full Research Bundle (JSON)",
            data=json.dumps({
                "topic": topic,
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": elapsed_time,
                "search_results": search_text,
                "scraped_content": scraped_text,
                "report": report_text,
                "critic_feedback": critic_text,
            }, indent=2),
            file_name=f"research_bundle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
        )
