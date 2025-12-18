import streamlit as st
import csv
import json
import httpx
import sys
from io import StringIO
from pathlib import Path

# 1. إضافة المسار لضمان رؤية المجلد المصدري
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from csv_profiler.profile import basic_profile
from csv_profiler.render import render_markdown

st.set_page_config(page_title="CSV Profiler Pro", layout="wide")
st.title("📊 CSV Profiler & Analyzer")

# --- قسم جلب البيانات ---
st.sidebar.header("Data Source")
use_url = st.sidebar.checkbox("Load from URL", value=False)

rows = None

if use_url:
    url = st.sidebar.text_input("CSV URL", placeholder="https://.../data.csv")
    if url:
        try:
            with st.spinner("Downloading data..."):
                r = httpx.get(url, timeout=10.0)
                r.raise_for_status()
                text = r.text
                rows = list(csv.DictReader(StringIO(text)))
        except Exception as e:
            st.error(f"Failed to load URL: {e}")
    else:
        st.info("Paste a URL in the sidebar.")
else:
    uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        text = uploaded.getvalue().decode("utf-8-sig")
        rows = list(csv.DictReader(StringIO(text)))

# --- قسم معالجة وعرض البيانات ---
if rows:
 st.subheader("📋 Data Preview")
 st.dataframe(rows[:10]) 
    
    # إدارة حالة التقرير ليبقى ظاهراً بعد التحميل
if 'show_report' not in st.session_state:
        st.session_state.show_report = False

if st.button("🚀 Generate Full Profile"):
        st.session_state.show_report = True

if st.session_state.show_report:
     report_obj = basic_profile(rows)
     report_dict = report_obj.to_dict()
     md_report = render_markdown(report_obj)
        
     st.divider()
     st.subheader("📝 Analysis Report")
     st.markdown(md_report)
        
     st.subheader("📥 Export Report")
     col1, col2 = st.columns(2)
        
     with col1:
         st.download_button(
                label="Download JSON",
                data=json.dumps(report_dict, indent=4),
                file_name="report.json",
                mime="application/json"
            )
            
     with col2:
            st.download_button(
                label="Download Markdown",
                data=md_report,
                file_name="report.md",
                mime="text/markdown"
            )
else:
    st.warning("Please upload a file or provide a URL to start.")