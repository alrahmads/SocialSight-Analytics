import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import generate_insights


def render(df):
    """Render Executive Summary page"""
    st.header("Executive Summary")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Videos", f"{len(df):,}")
    with col2:
        if "Views" in df.columns:
            st.metric("Total Views", f"{df['Views'].sum():,.0f}")
    with col3:
        if "Likes" in df.columns:
            st.metric("Total Likes", f"{df['Likes'].sum():,.0f}")
    with col4:
        if "Comments" in df.columns:
            st.metric("Total Comments", f"{df['Comments'].sum():,.0f}")
    with col5:
        if "Engagement_Rate" in df.columns:
            st.metric(
                "Avg Engagement Rate", f"{df['Engagement_Rate'].mean():.2f}%"
            )

    st.write("---")

    # Top Channels by Subscribers
    if "Channel" in df.columns and "Subscribers" in df.columns:
        st.subheader("Top 10 Channels by Subscribers")
        top_channels = (
            df.groupby("Channel")["Subscribers"]
            .first()
            .sort_values(ascending=True)
            .tail(10)
        )
        fig = px.bar(
            x=top_channels.values,
            y=top_channels.index,
            orientation="h",
            labels={"x": "Subscribers", "y": "Channel"},
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Subscribers",
            yaxis_title="Channel",
        )
        fig.update_traces(
            texttemplate="%{x:,.0f}",
            textposition="outside",
            marker=dict(
                color=top_channels.values,
                colorscale="Blues",
                showscale=False,
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Category Performance
    if "Kategori" in df.columns:
        st.subheader("Category Account Performance Analysis")
        cat_analysis = (
            df.groupby("Kategori")
            .agg(
                {
                    "Views": ["sum", "mean"],
                    "Engagement_Rate": "mean",
                    "Judul": "count",
                }
            )
            .round(2)
        )
        cat_analysis.columns = [
            "Total Views",
            "Avg Views",
            "Avg Eng Rate",
            "Video Count",
        ]
        cat_analysis = cat_analysis.sort_values("Total Views", ascending=False)
        st.dataframe(cat_analysis, use_container_width=True)

    # Recent Upload Trends
    if "Tanggal Upload" in df.columns:
        st.subheader("Upload Trends (Last 30 Days)")
        df_recent = df[
            df["Tanggal Upload"]
            >= df["Tanggal Upload"].max() - pd.Timedelta(days=30)
        ]
        upload_trend = df_recent.groupby(
            df_recent["Tanggal Upload"].dt.date
        ).size()
        fig = px.line(
            x=upload_trend.index,
            y=upload_trend.values,
            labels={"x": "Date", "y": "Number of Uploads"},
            title="Upload Activity",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Key Insights
    st.subheader("💡 Key Insights")
    insights = generate_insights(df)
    for insight in insights:
        st.info(insight)