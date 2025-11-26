import streamlit as st
import pandas as pd
import plotly.express as px


def render(df):
    """Render Engagement Analytics page"""
    st.header("Engagement Analytics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Engagement", f"{df['Engagement'].sum():,.0f}")
    with col2:
        st.metric("Avg Engagement", f"{df['Engagement'].mean():,.0f}")
    with col3:
        st.metric("Avg Engagement Rate", f"{df['Engagement_Rate'].mean():.2f}%")
    with col4:
        if "Tanggal Upload" in df.columns:
            days = (
                df["Tanggal Upload"].max() - df["Tanggal Upload"].min()
            ).days
            if days > 0:
                st.metric(
                    "Avg Engagement/Day", f"{df['Engagement'].sum()/days:,.0f}"
                )

    st.write("---")

    col1, col2 = st.columns(2)

    with col1:
        # Engagement Distribution
        st.subheader("Engagement Distribution")
        engagement_data = pd.DataFrame(
            {
                "Type": ["Likes", "Comments"],
                "Count": [df["Likes"].sum(), df["Comments"].sum()],
            }
        )
        fig = px.pie(
            engagement_data,
            values="Count",
            names="Type",
            title="Likes vs Comments",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Top Engagement Videos
        st.subheader("Top 10 Videos by Engagement")

        top10 = df.nlargest(10, "Engagement")[
            ["Judul", "Engagement", "Engagement_Rate"]
        ]
        top10 = top10.sort_values("Engagement", ascending=True)

        fig = px.bar(
            top10,
            x="Engagement",
            y="Judul",
            orientation="h",
            text="Engagement",
            title="Top 10 Engagement Videos",
        )

        fig.update_traces(textposition="outside")
        fig.update_layout(
            yaxis_title="Video Title",
            xaxis_title="Engagement",
            yaxis=dict(categoryorder="total ascending"),
        )

        st.plotly_chart(fig, use_container_width=True)

    # Engagement vs Views
    st.subheader("Engagement vs Views")
    fig = px.scatter(
        df,
        x="Views",
        y="Engagement",
        hover_data=["Judul"],
        title="Engagement vs Views Correlation",
        trendline="ols",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Duration vs Performance
    if "Duration_Seconds" in df.columns:
        st.subheader("Duration vs Engagement")
        df["Duration_Minutes"] = df["Duration_Seconds"] / 60
        fig = px.scatter(
            df,
            x="Duration_Minutes",
            y="Engagement_Rate",
            hover_data=["Judul"],
            title="Video Duration vs Engagement Rate",
        )
        st.plotly_chart(fig, use_container_width=True)