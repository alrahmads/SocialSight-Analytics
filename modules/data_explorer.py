import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO


def render(df):
    """Render Data Explorer page"""
    st.header("Data Explorer")

    st.subheader("Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        if "Channel" in df.columns:
            channels = list(df["Channel"].unique())
            selected_channels = st.multiselect(
                "Select Channels", channels, default=[]
            )

    with col2:
        if "Kategori" in df.columns:
            categories = list(df["Kategori"].unique())
            selected_categories = st.multiselect(
                "Select Categories", categories, default=[]
            )

    with col3:
        min_views = st.number_input(
            "Min Views", min_value=0, value=0, step=1000
        )

    # Apply Filters
    filtered_df = df.copy()

    if selected_channels:
        filtered_df = filtered_df[
            filtered_df["Channel"].isin(selected_channels)
        ]

    if selected_categories:
        filtered_df = filtered_df[
            filtered_df["Kategori"].isin(selected_categories)
        ]

    if min_views > 0:
        filtered_df = filtered_df[filtered_df["Views"] >= min_views]

    st.write(f"**Showing {len(filtered_df)} of {len(df)} records**")

    st.write("---")

    # Numeric Summary dan Category Breakdown
    col1, col2 = st.columns(2)

    with col1:
        # Numeric Summary
        st.subheader("Numeric Summary")
        numeric_cols = filtered_df.select_dtypes(
            include=[np.number]
        ).columns.tolist()
        key_metrics = ["Views", "Likes", "Comments", "Subscribers"]
        display_cols = [col for col in key_metrics if col in numeric_cols]

        if display_cols:
            summary_stats = filtered_df[display_cols].describe()
            summary_stats.loc["sum"] = filtered_df[display_cols].sum()

            # Format angka
            summary_stats_formatted = summary_stats.copy()
            for col in summary_stats_formatted.columns:
                summary_stats_formatted[col] = summary_stats_formatted[
                    col
                ].apply(lambda x: f"{x:,.2f}" if pd.notnull(x) else "")

            # Rename index
            summary_stats_formatted.index = [
                "Count",
                "Mean",
                "Std",
                "Min",
                "25%",
                "50%",
                "75%",
                "Max",
                "Sum",
            ]

            st.dataframe(
                summary_stats_formatted, use_container_width=True, height=350
            )

    with col2:
        # Category Breakdown
        st.subheader("Category Breakdown")
        if "Kategori" in filtered_df.columns:
            category_breakdown = filtered_df.groupby("Kategori").agg(
                {"Views": ["count", "sum"], "Likes": "sum", "Comments": "sum"}
            )

            category_breakdown.columns = [
                "Video Count",
                "Total Views",
                "Total Likes",
                "Total Comments",
            ]

            st.dataframe(
                category_breakdown, use_container_width=True, height=350
            )
    st.write("---")

    # Data Table
    st.subheader("Filtered Data Table")

    # Column selector
    all_columns = filtered_df.columns.tolist()
    default_columns = [
        "Judul",
        "Channel",
        "Views",
        "Likes",
        "Comments",
        "Engagement_Rate",
        "Kategori",
    ]
    default_columns = [col for col in default_columns if col in all_columns]

    selected_columns = st.multiselect(
        "Select columns to display", all_columns, default=default_columns
    )

    if selected_columns:
        display_df = filtered_df[selected_columns]
        st.dataframe(display_df, use_container_width=True, height=400)
    else:
        st.warning("Please select at least one column to display")

    # Download Options
    st.subheader("Download Data")

    # CSV Download
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="filtered_social_media_data.csv",
        mime="text/csv",
        use_container_width=True,
    )

    # Excel Download
    filtered_df_export = filtered_df.copy()
    for col in filtered_df_export.columns:
        if pd.api.types.is_datetime64_any_dtype(filtered_df_export[col]):
            filtered_df_export[col] = filtered_df_export[col].dt.tz_localize(
                None
            )

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        filtered_df_export.to_excel(writer, index=False, sheet_name="Data")
    excel_data = output.getvalue()

    st.download_button(
        label="📥 Download as Excel",
        data=excel_data,
        file_name="filtered_social_media_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )