import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import joblib


def render(df):
    """Render Topic Analysis page"""
    st.header("Topic Analysis")

    # Load NMF Model
    try:
        nmf_package = joblib.load("models/topic_modeling/nmf_model.pkl")
        nmf_model = nmf_package["nmf_model"]
        tfidf_vectorizer = nmf_package["tfidf"]
        feature_names = nmf_package["feature_names"]
        n_topics = nmf_package["n_topics"]
        model_loaded = True
    except:
        model_loaded = False

    st.write("---")

    # Word Cloud from Titles
    if "Judul" in df.columns:
        st.subheader("Word Cloud - Video Titles")
        all_titles = " ".join(df["Judul"].astype(str).values)

        try:
            wordcloud = WordCloud(
                width=1200,
                height=400,
                background_color="white",
                colormap="viridis",
            ).generate(all_titles)

            fig, ax = plt.subplots(figsize=(15, 5))
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
        except:
            st.warning(
                "Unable to generate word cloud. Install wordcloud library."
            )
            st.write("---")

    # ================== NMF TOPIC MODELING ==================
    if model_loaded:
        st.subheader(
            "Topic Modeling Results - Non Negative Matrix Factorization (NMF)"
        )

        # Display Topics
        st.markdown("#### Discovered Topics")

        n_words = 10
        topic_data = []

        for i, comp in enumerate(nmf_model.components_):
            top_idx = comp.argsort()[-n_words:][::-1]
            top_words = [feature_names[j] for j in top_idx]
            topic_data.append(
                {"Topic": f"Topic {i+1}", "Keywords": ", ".join(top_words[:10])}
            )

        # Display as cards
        cols = st.columns(2)
        for idx, topic in enumerate(topic_data):
            with cols[idx % 2]:
                st.markdown(
                    f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            border-radius: 10px; padding: 20px; margin-bottom: 15px; color: white; 
                            min-height: 180px; display: flex; flex-direction: column; 
                            justify-content: flex_start; height: 100%;">
                    <h4 style="color: white; margin-bottom: 10px;">{topic['Topic']}</h4>
                    <p style="font-size: 16px; line-height: 1.6;">{topic['Keywords']}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        st.write("---")

        # Apply NMF to current data
        try:
            # Preprocess current data
            def preprocess_text(text):
                if pd.isna(text):
                    return ""
                text = str(text).lower()
                text = re.sub(r"http\S+|www\S+|https\S+", "", text)
                text = re.sub(r"[^a-zA-Z\s]", " ", text)
                text = " ".join(text.split())
                return text

            df_temp = df.copy()
            df_temp["combined_text"] = (
                df_temp["Judul"].fillna("")
                + " "
                + (
                    df_temp["Total Video Cha Tags"].fillna("")
                    if "Total Video Cha Tags" in df_temp.columns
                    else ""
                )
            )
            df_temp["processed_text"] = df_temp["combined_text"].apply(
                preprocess_text
            )

            # Transform with loaded vectorizer
            tfidf_matrix = tfidf_vectorizer.transform(df_temp["processed_text"])
            nmf_topics = nmf_model.transform(tfidf_matrix)

            df_temp["topic"] = nmf_topics.argmax(axis=1)
            df_temp["topic_confidence"] = nmf_topics.max(axis=1)

            # Topic Distribution
            st.markdown("#### Topic Distribution")
            col1, col2 = st.columns(2)

            with col1:
                topic_dist = df_temp["topic"].value_counts().sort_index()
                topic_labels = [f"Topic {i+1}" for i in topic_dist.index]

                fig = px.pie(
                    values=topic_dist.values,
                    names=topic_labels,
                    title="Video Distribution by Topic",
                    color_discrete_sequence=px.colors.qualitative.Set3,
                )
                fig.update_traces(
                    textposition="inside", textinfo="percent+label"
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Topic Performance
                if "Views" in df_temp.columns:
                    topic_perf = (
                        df_temp.groupby("topic")["Views"]
                        .agg(["sum", "mean", "count"])
                        .reset_index()
                    )
                    topic_perf["topic"] = topic_perf["topic"].apply(
                        lambda x: f"Topic {x+1}"
                    )
                    topic_perf.columns = [
                        "Topic",
                        "Total Views",
                        "Avg Views",
                        "Video Count",
                    ]

                    st.markdown("**Topic Performance**")
                    st.dataframe(
                        topic_perf.style.format(
                            {
                                "Total Views": "{:,.0f}",
                                "Avg Views": "{:,.0f}",
                                "Video Count": "{:.0f}",
                            }
                        ),
                        use_container_width=True,
                    )

            st.write("---")

            # Most Frequent Topics
            st.markdown("#### Top Videos by Topic")

            selected_topic = st.selectbox(
                "Select Topic to View Top Videos",
                [f"Topic {i+1}" for i in range(n_topics)],
            )

            topic_idx = int(selected_topic.split()[1]) - 1
            topic_videos = (
                df_temp[df_temp["topic"] == topic_idx]
                .nlargest(5, "Views")[
                    ["Judul", "Views", "Likes", "Comments", "topic_confidence"]
                ]
                .reset_index(drop=True)
            )

            if len(topic_videos) > 0:
                for idx, row in topic_videos.iterrows():
                    st.markdown(
                        f"""
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; 
                                margin-bottom: 10px; border-left: 4px solid #1E50A0;">
                        <div style="font-weight: 600; font-size: 15px; color: #1E50A0; margin-bottom: 8px;">
                            {row['Judul']}
                        </div>
                        <div style="display: flex; gap: 20px; font-size: 13px; color: #666;">
                            <span>👁️ {row['Views']:,.0f} views</span>
                            <span>❤️ {row['Likes']:,.0f} likes</span>
                            <span>💬 {row['Comments']:,.0f} comments</span>
                            <span>🎯 {row['topic_confidence']:.2%} confidence</span>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No videos found for this topic")

        except Exception as e:
            st.error(f"Error applying topic model: {str(e)}")

        st.write("---")