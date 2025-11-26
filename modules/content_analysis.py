import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render(df):
    """Render Content Analysis page"""
    st.header("Content Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Posts", f"{len(df):,}")
    with col2:
        if "Tanggal Upload" in df.columns:
            days = (
                df["Tanggal Upload"].max() - df["Tanggal Upload"].min()
            ).days
            if days > 0:
                st.metric("Avg Posts/Day", f"{len(df)/days:.2f}")
    with col3:
        if "Description" in df.columns:
            total_hashtags = df["Description"].astype(str).str.count("#").sum()
            st.metric("Avg Hashtags/Post", f"{total_hashtags/len(df):.2f}")

    st.write("---")

    col1, col2 = st.columns(2)

    with col1:
        # Upload Frequency
        if "Tanggal Upload" in df.columns:
            st.subheader("Upload Frequency by Day")
            df["Day_of_Week"] = df["Tanggal Upload"].dt.day_name()
            day_freq = df["Day_of_Week"].value_counts()
            fig = px.bar(
                x=day_freq.index,
                y=day_freq.values,
                labels={"x": "Day", "y": "Number of Posts"},
                title="Posts by Day of Week",
            )
            fig.update_traces(marker_color="#1E50A0")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Category Performance
        if "Kategori" in df.columns:
            st.subheader("Category Performance")

            cat_perf = (
                df.groupby("Kategori")
                .agg({"Views": "sum", "Engagement": "sum"})
                .reset_index()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    name="Views",
                    x=cat_perf["Kategori"],
                    y=cat_perf["Views"],
                    marker_color="#1E50A0",
                    offsetgroup=0,
                )
            )

            fig.add_trace(
                go.Bar(
                    name="Engagement",
                    x=cat_perf["Kategori"],
                    y=cat_perf["Engagement"],
                    marker_color="#FFC107",
                    yaxis="y2",
                    offsetgroup=1,
                )
            )

            fig.update_layout(
                barmode="group",
                title="Views & Engagement by Category",
                xaxis_title="Category",
                yaxis=dict(
                    title=dict(text="Views", font=dict(color="#1E50A0")),
                    tickfont=dict(color="#1E50A0"),
                    side="left",
                ),
                yaxis2=dict(
                    title=dict(text="Engagement", font=dict(color="#FFC107")),
                    tickfont=dict(color="#FFC107"),
                    overlaying="y",
                    side="right",
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                ),
            )

            st.plotly_chart(fig, use_container_width=True)

    # Best Time to Post
    if "Tanggal Upload" in df.columns:
        st.subheader("Best Time to Post")
        df["Hour"] = df["Tanggal Upload"].dt.hour
        df["Day_of_Week"] = df["Tanggal Upload"].dt.day_name()

        hourly_performance = (
            df.groupby("Hour")
            .agg({"Views": "mean", "Engagement_Rate": "mean"})
            .reset_index()
        )

        best_day = df.groupby("Day_of_Week")["Engagement_Rate"].mean().idxmax()
        best_hour = df.groupby("Hour")["Engagement_Rate"].mean().idxmax()

        col1, col2 = st.columns([3.5, 1])

        with col1:
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=hourly_performance["Hour"],
                    y=hourly_performance["Views"],
                    name="Avg Views",
                    mode="lines+markers",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=hourly_performance["Hour"],
                    y=hourly_performance["Engagement_Rate"],
                    name="Avg Engagement Rate",
                    mode="lines+markers",
                    yaxis="y2",
                )
            )
            fig.update_layout(
                title="Performance by Hour of Day",
                xaxis_title="Hour",
                yaxis_title="Avg Views",
                yaxis2=dict(
                    title="Avg Engagement Rate", overlaying="y", side="right"
                ),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown(
                """
            <style>
            .insight-card {
                background: linear-gradient(135deg, #1E50A0 0%, #4A90E2 100%);
                border-radius: 15px;
                padding: 25px 20px;
                color: white;
                text-align: center;
                height: 300px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-top: 50px;
            }
            .insight-title {
                font-size: 14px;
                opacity: 0.9;
                margin-bottom: 8px;
                font-weight: 500;
            }
            .insight-value {
                font-size: 36px;
                font-weight: 700;
                margin: 8px 0;
            }
            .insight-subtitle {
                font-size: 14px;
                opacity: 0.9;
                margin-top: 20px;
                margin-bottom: 8px;
                font-weight: 500;
            }
            </style>
            """,
                unsafe_allow_html=True,
            )

            insight_html = f"""
            <div class="insight-card">
                <div class="insight-title">Day with Highest Engagement</div>
                <div class="insight-value">{best_day}</div>
                <div class="insight-subtitle">Hour with Highest Engagement</div>
                <div class="insight-value">{best_hour} PM</div>
            </div>
            """
            st.markdown(insight_html, unsafe_allow_html=True)

    # Top Performing Posts
    st.subheader("Top 10 Performing Posts")

    top_posts = df.nlargest(10, "Views")[
        ["Judul", "Views", "Likes", "Comments", "Engagement_Rate", "Channel"]
    ].reset_index(drop=True)

    for idx, row in top_posts.iterrows():
        rank = idx + 1

        if rank == 1:
            gradient = "linear-gradient(135deg, #a8edea 0%, #74d0ff 100%)"
        elif rank == 2:
            gradient = "linear-gradient(135deg, #74d0ff 0%, #4facfe 100%)"
        elif rank == 3:
            gradient = "linear-gradient(135deg, #4facfe 0%, #3366C2 100%)"
        else:
            gradient = "linear-gradient(135deg, #2e86de 0%, #1e50a0 100%)"

        card_html = f"""
        <div class="post-card" style="background: {gradient}; position: relative;">
            <div class="rank-badge">#{rank}</div>
            <div class="post-title">{row['Judul']}</div>
            <div class="post-channel">
                📺 Channel: {row['Channel']}
            </div>
            <div class="post-stats">
                <div class="stat-item">
                    👁️ {row['Views']:,.0f} views
                </div>
                <div class="stat-item">
                    ❤️ {row['Likes']:,.0f}
                </div>
                <div class="stat-item">
                    💬 {row['Comments']:,.0f}
                </div>
                <div class="stat-item">
                    📊 {row['Engagement_Rate']:.2f}%
                </div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)