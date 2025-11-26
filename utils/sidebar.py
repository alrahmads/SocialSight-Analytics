import streamlit as st


def render_sidebar():
    """Render sidebar menu and file uploader"""
    
    # Logo
    st.sidebar.image("assets/SocialSight.png", width=300)

    st.sidebar.markdown("**Menu Analisis**")

    if "menu" not in st.session_state:
        st.session_state["menu"] = "Executive Summary"

    # Menu items
    menu_items = [
        ("Executive Summary", "m1"),
        ("Engagement Analytics", "m2"),
        ("Content Analysis", "m3"),
        ("View & Reach Analytics", "m4"),
        ("Sentiment & Comment Analysis", "m5"),
        ("Topic Analysis", "m6"),
        ("Data Explorer", "m7"),
    ]

    # Render menu buttons
    for label, key in menu_items:
        is_active = st.session_state["menu"] == label
        button_type = "primary" if is_active else "secondary"

        if st.sidebar.button(label, key=key, type=button_type, use_container_width=True):
            st.session_state["menu"] = label
            st.rerun()

    menu = st.session_state["menu"]

    st.sidebar.write("---")
    uploaded_file = st.sidebar.file_uploader("Upload File Data", type=["csv", "xlsx"])

    return menu, uploaded_file