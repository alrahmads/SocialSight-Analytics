import pandas as pd
import re


def calculate_engagement_rate(df):
    """Calculate engagement rate"""
    if "Likes" in df.columns and "Comments" in df.columns and "Views" in df.columns:
        df["Engagement"] = df["Likes"] + df["Comments"]
        df["Engagement_Rate"] = (df["Engagement"] / df["Views"] * 100).fillna(0)
    return df


def clean_duration(duration_str):
    """Convert duration string to seconds"""
    try:
        if pd.isna(duration_str):
            return 0
        duration_str = str(duration_str).strip()
        if duration_str.startswith("PT"):
            duration_str = duration_str[2:]

        hours = minutes = seconds = 0
        if "H" in duration_str:
            hours = int(duration_str.split("H")[0])
            duration_str = duration_str.split("H")[1]
        if "M" in duration_str:
            minutes = int(duration_str.split("M")[0])
            duration_str = duration_str.split("M")[1]
        if "S" in duration_str:
            seconds = int(duration_str.replace("S", ""))

        return hours * 3600 + minutes * 60 + seconds
    except:
        return 0


def parse_date(date_str):
    """Parse date string"""
    try:
        return pd.to_datetime(date_str)
    except:
        return pd.NaT


def split_comments(comment_string):
    """Split multiple comments separated by ||"""
    if pd.isna(comment_string):
        return []
    comments = re.split(r"\s\|\|\s", str(comment_string))
    return [c.strip() for c in comments if c.strip()]


def generate_insights(df):
    """Generate automatic insights"""
    insights = []

    if "Engagement" in df.columns:
        total_engagement = df["Engagement"].sum()
        insights.append(
            f"Total engagement mencapai {total_engagement:,.0f} interaksi (likes + comments)"
        )

    if "Channel" in df.columns and "Subscribers" in df.columns:
        top_channel = df.groupby("Channel")["Subscribers"].first().idxmax()
        top_subscribers = df.groupby("Channel")["Subscribers"].first().max()
        insights.append(
            f"Channel dengan subscribers terbanyak: {top_channel} ({top_subscribers:,.0f} subscribers)"
        )

    if "Engagement_Rate" in df.columns:
        avg_engagement = df["Engagement_Rate"].mean()
        insights.append(f"Rata-rata engagement rate per video: {avg_engagement:.2f}%")

    if "Kategori" in df.columns:
        top_category = df["Kategori"].value_counts().idxmax()
        insights.append(f"Kategori terpopuler: {top_category}")

    if "Tanggal Upload" in df.columns:
        recent_uploads = df[
            df["Tanggal Upload"] >= df["Tanggal Upload"].max() - pd.Timedelta(days=7)
        ]
        insights.append(f"Upload 7 hari terakhir: {len(recent_uploads)} video")

    return insights