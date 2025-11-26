import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render(df):
    """Render View & Reach Analytics page"""
    st.header("View & Reach Analytics")

    # Key Metrics Section
    st.markdown("### Key Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Views", f"{df['Views'].sum():,.0f}")
    with col2:
        st.metric("Avg Views/Video", f"{df['Views'].mean():,.0f}")
    with col3:
        st.metric("Max Views", f"{df['Views'].max():,.0f}")
    with col4:
        median_views = df["Views"].median()
        st.metric("Median Views", f"{median_views:,.0f}")

    st.write("")
    st.markdown("---")
    st.write("")

    # Views Distribution & Top Videos
    st.markdown("### Views Analysis")
    col1, col2 = st.columns([1.2, 0.8])

    with col1:
        st.markdown("#### Views Distribution")
        fig = px.histogram(
            df,
            x="Views",
            nbins=30,
            labels={"Views": "Views", "count": "Number of Videos"},
        )
        fig.update_traces(
            marker_color="#1E50A0",
            marker_line_color="white",
            marker_line_width=1,
        )
        fig.update_layout(
            showlegend=False, height=380, margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Top 10 Videos by Views")
        top_videos = df.nlargest(10, "Views")[
            ["Judul", "Views", "Channel"]
        ].reset_index(drop=True)
        top_videos.index = top_videos.index + 1
        top_videos.columns = ["Title", "Views", "Channel"]
        top_videos["Views"] = top_videos["Views"].apply(lambda x: f"{x:,.0f}")
        st.dataframe(
            top_videos, use_container_width=True, height=380, hide_index=False
        )

    st.write("")
    st.markdown("---")
    st.write("")

    # Views Over Time
    if "Tanggal Upload" in df.columns:
        st.markdown("### Views Growth Trends")

        daily_views = (
            df.groupby(df["Tanggal Upload"].dt.date)["Views"]
            .sum()
            .reset_index()
        )
        daily_views.columns = ["Date", "Total Views"]
        daily_views["Date"] = pd.to_datetime(daily_views["Date"])
        daily_views = daily_views.sort_values("Date")
        daily_views["Cumulative Views"] = daily_views["Total Views"].cumsum()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Daily Views Over Time")
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=daily_views["Date"],
                    y=daily_views["Total Views"],
                    name="Daily Views",
                    mode="lines",
                    line=dict(color="#1E50A0", width=2),
                    fill="tozeroy",
                    fillcolor="rgba(30, 80, 160, 0.1)",
                    hovertemplate="<b>Date:</b> %{x|%Y-%m-%d}<br><b>Views:</b> %{y:,.0f}<extra></extra>",
                )
            )
            fig.update_layout(
                showlegend=False,
                height=350,
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis_title="Date",
                yaxis_title="Total Views",
                hovermode="x unified",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Cumulative Views Growth")
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=daily_views["Date"],
                    y=daily_views["Cumulative Views"],
                    name="Cumulative Views",
                    mode="lines",
                    line=dict(color="#4A90E2", width=3),
                    hovertemplate="<b>Date:</b> %{x|%Y-%m-%d}<br><b>Total:</b> %{y:,.0f}<extra></extra>",
                )
            )
            fig.update_layout(
                showlegend=False,
                height=350,
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis_title="Date",
                yaxis_title="Cumulative Views",
                hovermode="x unified",
            )
            st.plotly_chart(fig, use_container_width=True)

    st.write("")
    st.markdown("---")
    st.write("")

    # Monthly Views
    if "Tanggal Upload" in df.columns:
        st.markdown("### Monthly Total Views Analysis")

        monthly_views = (
            df.groupby(df["Tanggal Upload"].dt.to_period("M"))["Views"]
            .sum()
            .reset_index()
        )
        monthly_views.columns = ["Month", "Total Views"]
        monthly_views["Month"] = monthly_views["Month"].astype(str)

        fig = px.line(
            monthly_views,
            x="Month",
            y="Total Views",
            markers=True,
            labels={"Total Views": "Total Views", "Month": "Month"},
        )

        fig.update_traces(
            line=dict(width=3, color="#1E50A0"),
            marker=dict(size=8, color="#1E50A0", line=dict(color="white", width=1.5)),
            text=[f"{v:,.0f}" for v in monthly_views["Total Views"]],
            textposition="top center"
        )

        fig.update_layout(
            showlegend=False,
            height=350,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Month",
            yaxis_title="Total Views",
        )

        st.plotly_chart(fig, use_container_width=True)

    st.write("")
    st.markdown("---")
    st.write("")

    # View Spikes Detection
    if "Tanggal Upload" in df.columns:
        st.markdown("### View Spikes Detection")

        mean_views = daily_views["Total Views"].mean()
        std_views = daily_views["Total Views"].std()
        spike_threshold = mean_views + (2 * std_views)

        spikes = daily_views[
            daily_views["Total Views"] > spike_threshold
        ].copy()

        if len(spikes) > 0:
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown("#### View Spikes Over Time")
                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=daily_views["Date"],
                        y=daily_views["Total Views"],
                        name="Daily Views",
                        mode="lines",
                        line=dict(color="#1E50A0", width=2),
                        hovertemplate="<b>Date:</b> %{x|%Y-%m-%d}<br><b>Views:</b> %{y:,.0f}<extra></extra>",
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=spikes["Date"],
                        y=spikes["Total Views"],
                        name="Detected Spikes",
                        mode="markers",
                        marker=dict(
                            color="#FF4444",
                            size=14,
                            symbol="circle",
                            line=dict(color="white", width=2),
                        ),
                        hovertemplate="<b>SPIKE</b><br><b>Date:</b> %{x|%Y-%m-%d}<br><b>Views:</b> %{y:,.0f}<extra></extra>",
                    )
                )

                fig.add_hline(
                    y=spike_threshold,
                    line_dash="dash",
                    line_color="#FF4444",
                    line_width=2,
                    annotation_text=f"Threshold: {spike_threshold:,.0f}",
                    annotation_position="right",
                    annotation_font_size=11,
                    annotation_font_color="#FF4444",
                )

                fig.update_layout(
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1,
                    ),
                    height=400,
                    margin=dict(l=10, r=10, t=40, b=10),
                    xaxis_title="Date",
                    yaxis_title="Total Views",
                    hovermode="closest",
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("#### Spike Statistics")

                st.markdown("**Spike Statistics**")
                st.metric("Spike Threshold", f"{spike_threshold:,.0f} views")
                st.metric("Total Spikes", len(spikes))

                st.write("")
                st.markdown("**Top 5 Spike Dates**")

                top_spikes = spikes.nlargest(5, "Total Views")[
                    ["Date", "Total Views"]
                ].reset_index(drop=True)

                for idx, row in top_spikes.iterrows():
                    date_str = row["Date"].strftime("%Y-%m-%d")
                    views_str = f"{row['Total Views']:,.0f}"
                    rank = idx + 1

                    st.markdown(
                        f"""
                    <div style="background-color: #f8f9fa; padding: 12px; margin-bottom: 8px; 
                                border-radius: 8px; border-left: 4px solid #1E50A0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-weight: 600; color: #1E50A0; font-size: 13px;">#{rank} {date_str}</div>
                                <div style="font-size: 12px; color: #666; margin-top: 2px;">{views_str} views</div>
                            </div>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
        else:
            st.info("No significant view spikes detected in the dataset.")

    st.write("")
    st.markdown("---")
    st.write("")

    # Views by Channel
    if "Channel" in df.columns:
        st.markdown("### Channel Performance Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Top 10 Channels by Total Views")
            channel_views = (
                df.groupby("Channel")["Views"].sum().nlargest(10).sort_values()
            )
            fig = px.bar(
                x=channel_views.values,
                y=channel_views.index,
                orientation="h",
                labels={"x": "Total Views", "y": "Channel"},
            )
            fig.update_traces(
                marker_color="#1E50A0",
                marker_line_color="white",
                marker_line_width=1,
                texttemplate="%{x:,.0f}",
                textposition="outside",
            )
            fig.update_layout(
                showlegend=False,
                height=400,
                margin=dict(l=10, r=80, t=10, b=10),
                xaxis_title="Total Views",
                yaxis_title="",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Top 10 Channels by Average Views")
            channel_avg_views = (
                df.groupby("Channel")["Views"].mean().nlargest(10).sort_values()
            )
            fig = px.bar(
                x=channel_avg_views.values,
                y=channel_avg_views.index,
                orientation="h",
                labels={"x": "Average Views", "y": "Channel"},
            )
            fig.update_traces(
                marker_color="#4A90E2",
                marker_line_color="white",
                marker_line_width=1,
                texttemplate="%{x:,.0f}",
                textposition="outside",
            )
            fig.update_layout(
                showlegend=False,
                height=400,
                margin=dict(l=10, r=80, t=10, b=10),
                xaxis_title="Average Views",
                yaxis_title="",
            )
            st.plotly_chart(fig, use_container_width=True)

    st.write("")
    st.markdown("---")
    st.write("")

    # Reach Metrics
    st.markdown("### Reach Metrics Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_reach = df["Views"].sum()
        st.metric(
            "Total Reach",
            f"{total_reach:,.0f}",
            help="Total views across all videos",
        )

    with col2:
        unique_viewers_estimate = df["Views"].sum() * 0.7
        st.metric(
            "Est. Unique Viewers",
            f"{unique_viewers_estimate:,.0f}",
            help="Estimated 70% of total views",
        )

    with col3:
        if "Subscribers" in df.columns:
            total_potential_reach = (
                df.groupby("Channel")["Subscribers"].first().sum()
            )
            st.metric(
                "Potential Reach",
                f"{total_potential_reach:,.0f}",
                help="Total subscribers across channels",
            )

    with col4:
        avg_views_per_subscriber = (
            (
                df["Views"].sum()
                / df.groupby("Channel")["Subscribers"].first().sum()
                * 100
            )
            if "Subscribers" in df.columns
            else 0
        )
        st.metric(
            "Reach Rate",
            f"{avg_views_per_subscriber:.2f}%",
            help="Views / Subscribers ratio",
        )

    st.write("")
    st.markdown("---")
    st.write("")

    # Video Performance Categories
    st.markdown("### Video Performance Categories")

    percentile_25 = df["Views"].quantile(0.25)
    percentile_75 = df["Views"].quantile(0.75)

    def categorize_performance(views):
        if views >= percentile_75:
            return "High Performance"
        elif views >= percentile_25:
            return "Medium Performance"
        else:
            return "Low Performance"

    df["Performance Category"] = df["Views"].apply(categorize_performance)

    performance_dist = df["Performance Category"].value_counts()

    fig = px.pie(
        values=performance_dist.values,
        names=performance_dist.index,
        color=performance_dist.index,
        color_discrete_map={
            "High Performance": "#1E50A0",
            "Medium Performance": "#4A90E2",
            "Low Performance": "#7FB3D5",
        },
        hole=0.4,
    )
    fig.update_traces(
        textposition="outside",
        textinfo="label+percent",
        textfont_size=13,
        marker=dict(line=dict(color="white", width=2)),
        pull=[0.05, 0, 0],
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
    )
    fig.update_layout(
        showlegend=False,
        height=350,
        margin=dict(l=20, r=20, t=10, b=10),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial"),
    )
    st.plotly_chart(fig, use_container_width=True)