import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import json
from collections import Counter
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from utils.helpers import split_comments


# ==================== SENTIMENT HELPER FUNCTIONS ====================
@st.cache_resource
def load_stopwords():
    """Load stopword mappings from file"""
    try:
        with open(
            "data/combined_stop_words.txt", "r", encoding="utf-8"
        ) as f:
            stopwords = json.load(f)
        return stopwords
    except:
        return {}


@st.cache_resource
def load_sentiment_mappings():
    """Load all informal-formal mappings"""
    mappings = {}

    try:
        file_1 = pd.read_csv("data/informal_formal_1.csv")
        file_1_map = dict(
            zip(
                file_1["transformed"].astype(str).str.lower(),
                file_1["original-for"].astype(str).str.lower(),
            )
        )
        mappings.update(file_1_map)
    except:
        pass

    try:
        with open("data/informal_formal_2.txt", "r", encoding="utf-8") as f:
            mappings.update(json.load(f))
    except:
        pass

    try:
        with open(
            "data/update_combined_slang_words.txt", "r", encoding="utf-8"
        ) as f:
            mappings.update(json.load(f))
    except:
        pass

    custom_map = {
        "apkh": "apakah",
        "gak": "tidak",
        "ga": "tidak",
        "gk": "tidak",
        "nggk": "tidak",
        "agar": "supaya",
        "o on": "bodoh",
        "blo on": "bodoh",
        "lekas": "segera",
        "sbr": "sabar",
        "nggan": "tidak mau"
    }
    mappings.update(custom_map)

    return mappings


@st.cache_resource
def load_sentiment_model():
    """Load sentiment analysis model"""
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            "./models/sentiment_analysis"
        )
        model = AutoModelForSequenceClassification.from_pretrained(
            "./models/sentiment_analysis"
        )
        sentiment_pipeline = pipeline(
            "sentiment-analysis", model=model, tokenizer=tokenizer
        )
        return sentiment_pipeline
    except Exception as e:
        st.warning(f"Sentiment model not available: {str(e)}")
        return None


def normalize_text(text, mappings):
    """Normalize text by converting informal/slang to formal"""
    text = str(text)

    def replace_match(match):
        word = match.group(0)
        lower_word = word.lower()
        if lower_word in mappings:
            replacement = mappings[lower_word]
            if word.isupper():
                return replacement.upper()
            elif word[0].isupper():
                return replacement.capitalize()
            else:
                return replacement
        return word

    pattern = r"\b(" + "|".join(map(re.escape, mappings.keys())) + r")\b"
    normalized = re.sub(pattern, replace_match, text, flags=re.IGNORECASE)
    return normalized


def analyze_sentiment(text, sentiment_pipeline):
    """Analyze sentiment of text"""
    try:
        if sentiment_pipeline is None:
            return "NEUTRAL"
        result = sentiment_pipeline(str(text)[:512])
        return result[0]["label"] if result else "NEUTRAL"
    except:
        return "NEUTRAL"


def render(df):
    """Render Sentiment & Comment Analysis page"""
    st.header("Sentiment & Comment Analysis")

    # Load resources
    sentiment_mappings = load_sentiment_mappings()
    sentiment_pipeline = load_sentiment_model()

    st.write("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Comments", f"{df['Comments'].sum():,.0f}")
    with col2:
        st.metric("Avg Comments/Video", f"{df['Comments'].mean():.0f}")
    with col3:
        comment_rate = df["Comments"].sum() / df["Views"].sum() * 100
        st.metric("Comment Rate", f"{comment_rate:.3f}%")

    st.write("---")

    col1, col2 = st.columns(2)

    with col1:
        # Most Commented Videos
        st.subheader("Most Commented Videos")
        top_comments = df.nlargest(10, "Comments")[
            ["Judul", "Comments", "Views", "Channel"]
        ]
        st.dataframe(top_comments, use_container_width=True)

    with col2:
        # Comments vs Likes Ratio
        st.subheader("Engagement Breakdown")
        df["Like_Rate"] = (df["Likes"] / df["Views"] * 100).fillna(0)
        df["Comment_Rate"] = (df["Comments"] / df["Views"] * 100).fillna(0)

        fig = go.Figure()
        fig.add_trace(go.Box(y=df["Like_Rate"], name="Like Rate %"))
        fig.add_trace(go.Box(y=df["Comment_Rate"], name="Comment Rate %"))
        fig.update_layout(title="Like Rate vs Comment Rate Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # Comment Trends Over Time
    if "Tanggal Upload" in df.columns:
        st.subheader("Comment Trends Over Time")
        comment_trend = df.groupby(df["Tanggal Upload"].dt.date)[
            "Comments"
        ].sum()
        fig = px.line(
            x=comment_trend.index,
            y=comment_trend.values,
            labels={"x": "Date", "y": "Total Comments"},
            title="Comments Over Time",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.write("---")

    # ==================== SENTIMENT ANALYSIS ====================
    if sentiment_pipeline is not None:
        if "Komentar Lengkap" in df.columns:
            # Auto-process sentiment analysis
            if "sentiment_results_cache" not in st.session_state:
                with st.spinner(
                    "Processing comments and analyzing sentiment..."
                ):
                    sentiment_results = []

                    for idx, row in df.iterrows():
                        if pd.isna(row.get("Komentar Lengkap")):
                            continue

                        comments_list = split_comments(row["Komentar Lengkap"])

                        for comment in comments_list:
                            normalized = normalize_text(
                                comment, sentiment_mappings
                            )
                            sentiment = analyze_sentiment(
                                normalized, sentiment_pipeline
                            )

                            sentiment_results.append(
                                {
                                    "video_id": row.get("Video ID", idx),
                                    "tanggal_upload": row.get(
                                        "Tanggal Upload", None
                                    ),
                                    "comment_raw": comment,
                                    "comment_normalized": normalized,
                                    "sentiment": sentiment,
                                }
                            )

                    if sentiment_results:
                        st.session_state.sentiment_results_cache = pd.DataFrame(
                            sentiment_results
                        )
                    else:
                        st.session_state.sentiment_results_cache = None

            # Get results from cache
            results_df = st.session_state.sentiment_results_cache

            if results_df is not None and len(results_df) > 0:
                st.success(f"Analyzed {len(results_df)} comments")

                # ==================== 1. TOTAL SENTIMENT OVERVIEW ====================
                st.subheader("Total Sentiment Overview")

                sentiment_colors = {
                    "Positive": "#4A90E2",
                    "Negative": "#e74c3c",
                    "Neutral": "#95a5a6",
                }

                sentiment_counts = results_df["sentiment"].value_counts()

                for sentiment in ["Positive", "Negative", "Neutral"]:
                    count = sentiment_counts.get(sentiment, 0)
                    st.markdown(
                        f"""
                        <div style="padding:10px; border-radius:8px; margin-bottom:8px;
                                    background-color:{sentiment_colors[sentiment]}; 
                                    color:white; font-weight:bold;">
                            {sentiment}: {count}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.write("---")

                # ==================== 2. SENTIMENT DISTRIBUTION ====================
                st.subheader("Sentiment Distribution")

                col1, col2 = st.columns(2)

                with col1:
                    # PIE CHART
                    fig = px.pie(
                        values=[sentiment_counts.get(s, 0) for s in ["Positive", "Negative", "Neutral"]],
                        names=["Positive", "Negative", "Neutral"],
                        title="Sentiment Composition",
                        color=["Positive", "Negative", "Neutral"],
                        color_discrete_map=sentiment_colors,
                    )
                    fig.update_traces(textposition="inside", textinfo="percent+label", textfont_color="white")
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    # BAR CHART
                    fig = px.bar(
                        x=["Positive", "Negative", "Neutral"],
                        y=[sentiment_counts.get(s, 0) for s in ["Positive", "Negative", "Neutral"]],
                        labels={"x": "Sentiment", "y": "Count"},
                        title="Sentiment Count Distribution",
                        color=["Positive", "Negative", "Neutral"],
                        color_discrete_map=sentiment_colors,
                    )
                    fig.update_traces(texttemplate="%{y}", textposition="outside")
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)

                st.write("---")

                # ==================== 3. MOST FREQUENT WORDS ====================
                st.subheader("Most Frequent Words in Comments")

                all_words = []
                for comment in results_df["comment_normalized"]:
                    words = re.findall(r"\b\w+\b", str(comment).lower())
                    all_words.extend(words)

                word_counts = Counter(all_words)
                stop_words = load_stopwords()
                filtered_words = {
                    word: count
                    for word, count in word_counts.items()
                    if len(word) > 2 and word not in stop_words
                }
                top_words = dict(
                    sorted(
                        filtered_words.items(),
                        key=lambda x: x[1],
                        reverse=True,
                    )[:15]
                )

                fig = px.bar(
                    x=list(top_words.values()),
                    y=list(top_words.keys()),
                    orientation="h",
                    title="Top 15 Most Frequent Words",
                    labels={"x": "Frequency", "y": "Word"},
                )
                fig.update_traces(marker_color="#1E50A0")
                fig.update_layout(height=400, margin=dict(l=100))
                st.plotly_chart(fig, use_container_width=True)

                st.write("---")

                # ==================== 4. SENTIMENT TRENDS OVER TIME ====================
                if (
                    "tanggal_upload" in results_df.columns
                    and results_df["tanggal_upload"].notna().any()
                ):
                    st.subheader("Sentiment Trends Over Time")

                    results_df_copy = results_df.copy()
                    results_df_copy["tanggal_upload"] = pd.to_datetime(
                        results_df_copy["tanggal_upload"],
                        errors="coerce",
                    )
                    results_df_copy = results_df_copy[
                        results_df_copy["tanggal_upload"].notna()
                    ]

                    if len(results_df_copy) > 0:
                        sentiment_over_time = (
                            results_df_copy.groupby(
                                [
                                    results_df_copy["tanggal_upload"].dt.date,
                                    "sentiment",
                                ]
                            )
                            .size()
                            .reset_index(name="count")
                        )

                        fig = px.line(
                            sentiment_over_time,
                            x="tanggal_upload",
                            y="count",
                            color="sentiment",
                            title="Sentiment Trends Over Time",
                            labels={
                                "tanggal_upload": "Date",
                                "count": "Number of Comments",
                            },
                            color_discrete_map={
                                "Positive": "#2ecc71",
                                "Negative": "#e74c3c",
                                "Neutral": "#95a5a6",
                            },
                            markers=True,
                        )
                        fig.update_layout(hovermode="x unified")
                        st.plotly_chart(fig, use_container_width=True)

                        st.write("---")

                # ==================== 5. COMMENT-LEVEL ANALYSIS ====================
                st.subheader("Comment-Level Sentiment Analysis")

                col1, col2 = st.columns([2, 1])
                with col1:
                    selected_sentiment = st.selectbox(
                        "Filter by Sentiment",
                        ["All", "Positive", "Negative", "Neutral"],
                        key="sentiment_filter",
                    )
                with col2:
                    num_samples = st.number_input(
                        "Number of comments to show",
                        min_value=5,
                        max_value=50,
                        value=10,
                    )

                if selected_sentiment == "All":
                    filtered_results = results_df.head(num_samples)
                else:
                    filtered_results = results_df[
                        results_df["sentiment"] == selected_sentiment
                    ].head(num_samples)

                if len(filtered_results) > 0:
                    for idx, row in filtered_results.iterrows():
                        color_map = {
                            "Positive": "#2ecc71",
                            "Negative": "#e74c3c",
                            "Neutral": "#95a5a6",
                        }
                        sentiment_color = color_map.get(
                            row["sentiment"], "#1E50A0"
                        )

                        st.markdown(
                            f"""
                            <div style="background-color: #f8f9fa; padding: 12px; border-radius: 8px; 
                                        margin-bottom: 10px; border-left: 4px solid {sentiment_color};">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                    <div style="font-weight: 600; font-size: 12px; color: {sentiment_color};">
                                        {row['sentiment']}
                                    </div>
                                </div>
                                <div style="font-size: 13px; color: #333; margin-bottom: 8px; font-style: italic;">
                                    "{row['comment_raw']}"
                                </div>
                                <div style="font-size: 11px; color: #999; border-top: 1px solid #e0e0e0; padding-top: 6px;">
                                    <b>Normalized:</b> {row['comment_normalized'][:150]}...
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.info(
                        f"No comments found with sentiment: {selected_sentiment}"
                    )

                st.write("---")

                # Download Results
                st.subheader("📥 Export Results")
                csv = results_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Sentiment Analysis Results (CSV)",
                    data=csv,
                    file_name="sentiment_analysis_results.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            else:
                st.info("No comments found for analysis")
        else:
            st.info(
                "Upload data with 'Komentar Lengkap' column to perform sentiment analysis"
            )
    else:
        st.warning(
            "⚠️ Sentiment model not loaded. Ensure model files exist at ./models/sentiment_analysis"
        )

    st.write("---")

    # Sentiment Proxy
    st.subheader("Audience Reception (Like/Comment Ratio)")
    df["Engagement_Quality"] = (df["Likes"] / (df["Comments"] + 1)).fillna(0)

    bins = [0, 10, 50, 100, float("inf")]
    labels = ["Low", "Medium", "High", "Very High"]
    df["Quality_Category"] = pd.cut(
        df["Engagement_Quality"], bins=bins, labels=labels
    )

    quality_dist = df["Quality_Category"].value_counts()
    fig = px.bar(
        x=quality_dist.index,
        y=quality_dist.values,
        labels={"x": "Engagement Quality", "y": "Number of Videos"},
        title="Distribution of Engagement Quality",
    )
    st.plotly_chart(fig, use_container_width=True)