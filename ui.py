
import streamlit as st

class UI:
    @staticmethod
    def inject_css():
        pass

    @staticmethod
    def logo():
        st.markdown("<h1 style='text-align:center;color:white;'>Elixir</h1>", unsafe_allow_html=True)

    @staticmethod
    def nav():
        pages = ["Dashboard","Upload","Notes","Study Plan","Profile"]
        cols = st.columns(len(pages))

        if "nav" not in st.session_state:
            st.session_state.nav = "Dashboard"

        for i,p in enumerate(pages):
            if cols[i].button(p, use_container_width=True):
                st.session_state.nav = p

        return st.session_state.nav

    @staticmethod
    def dashboard():
        st.write("Dashboard")

    @staticmethod
    def profile():
        st.write("Profile")
