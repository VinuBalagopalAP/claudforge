import streamlit as st
import json
import time
from pathlib import Path
import pandas as pd

# --- CONFIG ---
st.set_page_config(
    page_title="ClaudForge Live ⚒️", page_icon="⚒️", layout="wide", initial_sidebar_state="expanded"
)

# --- THEME (Glassmorphism) ---
st.markdown(
    """
    <style>
    .main {
        background-color: #0E1117;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    .status-card {
        background: linear-gradient(135deg, #1e1e2f 0%, #11111d 100%);
        padding: 30px;
        border-radius: 20px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 25px;
    }
    .highlight {
        color: #ff4b4b;
        font-weight: bold;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    /* Hide the running spinner */
    [data-testid="stStatusWidget"] {
        display: none;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# --- DATA LOADING ---
def load_session(path: Path):
    if not path.exists():
        return None
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None


# --- UI LOGIC ---
def run_app():
    # Get path from CLI args passed to streamlit
    import sys

    # Extract path if passed after --
    try:
        idx = sys.argv.index("--")
        batch_path_str = sys.argv[idx + 1]
    except (ValueError, IndexError):
        batch_path_str = "."

    batch_path = Path(batch_path_str).resolve()
    session_file = batch_path / ".claudforge_session.json"

    st.title("ClaudForge Live Monitor ⚒️")

    placeholder = st.empty()

    while True:
        data = load_session(session_file)

        with placeholder.container():
            if not data:
                st.warning(f"Waiting for session data at {batch_path.name}...")
                st.info("Start an upload in the terminal to see live progress.")
            else:
                # 1. METRICS ROW
                col1, col2, col3, col4 = st.columns(4)

                total = data["total_folders"]
                history = data["history_count"]
                current_session_done = len(data["results"])
                limit = data["limit"] or total

                global_progress = (
                    ((history + current_session_done) / total) * 100 if total > 0 else 0
                )
                session_progress = (current_session_done / limit) * 100 if limit > 0 else 0

                col1.metric(
                    "Global Progress",
                    f"{global_progress:.1f}%",
                    f"{history + current_session_done}/{total}",
                )
                col2.metric(
                    "Current Session", f"{session_progress:.1f}%", f"{current_session_done}/{limit}"
                )

                # ETR Calculation
                elapsed = time.time() - data["session_start"]
                if current_session_done > 0:
                    avg_time = elapsed / current_session_done
                    remaining = (limit - current_session_done) * avg_time
                    etr_min = int(remaining // 60)
                    etr_sec = int(remaining % 60)
                    col3.metric("ETR", f"{etr_min}m {etr_sec}s", f"Avg: {avg_time:.1f}s/skill")
                else:
                    col3.metric("ETR", "Calculating...")

                col4.metric("Status", data["status"])

                # 2. ACTIVE UPLOAD
                if data["status"] == "RUNNING" and data["current_skill"]:
                    st.markdown(
                        f"""
                        <div class="status-card">
                            <h3 style='margin:0'>🚀 Now Uploading</h3>
                            <p style='font-size: 24px; color: #00d4ff; margin-top:10px;'>
                                {data["current_skill"]}
                            </p>
                            <p style='font-size: 14px; opacity: 0.7;'>
                                Processing skill {data["current_index"]} 
                                of session limit {limit}
                            </p>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )
                elif data["status"] == "FINISHED":
                    st.success("🎉 Batch Complete! All skills successfully processed.")

                # 3. RESULTS TABLE
                if data["results"]:
                    st.subheader("Recent Activity")
                    df = pd.DataFrame(data["results"], columns=["Skill", "Status", "Details"])
                    # Reverse to show newest at top
                    st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)

                # 4. LIVE ENGINE LOGS
                if "log_file" in data:
                    st.subheader("🛠 Live Engine Logs")
                    log_path = Path(data["log_file"])
                    if log_path.exists():
                        try:
                            with open(log_path, "r") as f:
                                # Get last 20 lines
                                lines = f.readlines()
                                tail = "".join(lines[-20:])
                                st.code(tail, language="text", wrap_lines=True)
                        except Exception:
                            st.warning("Could not read engine logs.")

        time.sleep(1)


if __name__ == "__main__":
    run_app()
