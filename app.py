import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Import dari file terpisah
from utils.styles import apply_custom_css, render_header
from utils.helpers import (
    calculate_engagement_rate,
    clean_duration,
    parse_date,
    split_comments,
    generate_insights
)
from utils.sidebar import render_sidebar
from modules import (
    executive_summary,
    engagement_analytics,
    content_analysis,
    view_reach_analytics,
    sentiment_comment_analysis,
    topic_analysis,
    data_explorer
)

# ================== PAGE CONFIG ==================
st.set_page_config(page_title="SocialSight Analytics", layout="wide")

# ================== APPLY STYLES ==================
apply_custom_css()
render_header()

# ================== SIDEBAR ==================
menu, uploaded_file = render_sidebar()

# ================== LOAD DATA ==================
if "df" not in st.session_state:
    st.session_state.df = None

if uploaded_file is not None:
    file_id = f"{uploaded_file.name}_{uploaded_file.size}"

    if (
        "current_file_id" not in st.session_state
        or st.session_state.current_file_id != file_id
    ):
        try:
            if uploaded_file.name.endswith(".csv"):
                try:
                    df = pd.read_csv(
                        uploaded_file, encoding="utf-8", on_bad_lines="skip"
                    )
                except UnicodeDecodeError:
                    try:
                        uploaded_file.seek(0)
                        df = pd.read_csv(
                            uploaded_file, encoding="latin-1", on_bad_lines="skip"
                        )
                    except UnicodeDecodeError:
                        uploaded_file.seek(0)
                        df = pd.read_csv(
                            uploaded_file, encoding="cp1252", on_bad_lines="skip"
                        )
                except Exception as e:
                    uploaded_file.seek(0)
                    df = pd.read_csv(
                        uploaded_file,
                        encoding="utf-8",
                        sep=",",
                        quotechar='"',
                        escapechar="\\",
                        on_bad_lines="skip",
                        engine="python",
                    )
            else:
                df = pd.read_excel(uploaded_file)

            if "Tanggal Upload" in df.columns:
                df["Tanggal Upload"] = df["Tanggal Upload"].apply(parse_date)

            if "Durasi" in df.columns:
                df["Duration_Seconds"] = df["Durasi"].apply(clean_duration)

            df = calculate_engagement_rate(df)

            if "Komentar Lengkap" in df.columns:
                df["Comments"] = df["Komentar Lengkap"].apply(lambda x: len(split_comments(x)))
                st.sidebar.info("📝 Comment counts updated based on split comments")

            st.session_state.df = df
            st.session_state.current_file_id = file_id

            st.sidebar.success(f"✅ Data loaded: {len(df)} records")
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            st.info("Please make sure your file has the correct format and columns.")
    else:
        st.sidebar.success(f"✅ Data loaded: {len(st.session_state.df)} records")

# ================== ROUTING ==================
if st.session_state.df is not None:
    df = st.session_state.df

    try:
        if menu == "Executive Summary":
            executive_summary.render(df)
        elif menu == "Engagement Analytics":
            engagement_analytics.render(df)
        elif menu == "Content Analysis":
            content_analysis.render(df)
        elif menu == "View & Reach Analytics":
            view_reach_analytics.render(df)
        elif menu == "Sentiment & Comment Analysis":
            sentiment_comment_analysis.render(df)
        elif menu == "Topic Analysis":
            topic_analysis.render(df)
        elif menu == "Data Explorer":
            data_explorer.render(df)

    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.info("Please make sure your file has the correct format and columns.")

else:
    st.markdown(
        """
        <div style="
            background-color:#eef3fa;
            padding:15px;
            border-radius:8px;
            border:1px solid #d1d9e6;
        ">
            <strong>Please upload a CSV or Excel file to begin analysis.</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Expected Data Structure")
    st.write("Your dataset should contain the following example columns:")

    example_data = {
        "Video ID": ["abc123", "def456"],
        "Judul": ["Video Title 1", "Video Title 2"],
        "Tanggal Upload": ["2025-01-15", "2025-01-16"],
        "Channel": ["Channel A", "Channel B"],
        "Country": ["ID", "ID"],
        "Subscribers": [1000000, 500000],
        "Total Video Cha Tags": ["tag1, tag2", "tag3, tag4"],
        "Kategori": ["News & Politics", "Entertainment"],
        "Views": [10000, 5000],
        "Likes": [500, 250],
        "Comments": [50, 25],
        "Durasi": ["PT5M30S", "PT3M45S"],
        "Definition": ["hd", "hd"],
        "Dimension": ["2d", "2d"],
    }

    example_df = pd.DataFrame(example_data)
    st.dataframe(example_df, use_container_width=True)

    st.write("---")

    st.markdown(
        """
    <h3 style='margin-bottom:10px;'>Features Available</h3>

    <div style="
        line-height:1.7;
        background-color:#f8f9fc;
        padding:18px;
        border-radius:8px;
        border:1px solid #e3e8f0;
    ">

    <ol>
        <li><strong>Executive Summary</strong>: Overview of key metrics and insights.</li>
        <li><strong>View & Reach Analytics</strong>: Analysis of performance metrics such as views, impressions, and reach patterns.</li>
        <li><strong>Engagement Analytics</strong>: Analysis of likes, comments, and engagement rate.</li>
        <li><strong>Content Analysis</strong>: Performance patterns based on category, timing, and content attributes.</li>
        <li><strong>Sentiment & Comment Analysis</strong>: Audience sentiment, keyword themes, and comment trends.</li>
        <li><strong>Topic Analysis</strong>: Keyword extraction, word clouds, and correlation analysis.</li>
        <li><strong>Data Explorer</strong>: Explore, filter, and download raw or processed data.</li>
    </ol>

    <p style="margin-top:10px;">
        Upload your dataset to begin the analysis workflow.
    </p>

    </div>
    """,
        unsafe_allow_html=True,
    )