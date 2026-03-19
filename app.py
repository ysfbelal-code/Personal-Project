
import streamlit as st
from ui import UI
from auth import AuthSystem
from notes import StudyNotesSystem
from planner import StudyPlannerSystem

def main():
    UI.inject_css()

    auth = AuthSystem()
    if auth.handle():
        return

    UI.logo()
    page = UI.nav()

    notes = StudyNotesSystem()
    planner = StudyPlannerSystem()

    if page == "Dashboard":
        UI.dashboard()

    elif page == "Upload":
        notes.upload()

    elif page == "Notes":
        notes.generate()

    elif page == "Study Plan":
        planner.generate_plan()

    elif page == "Profile":
        UI.profile()

if __name__ == "__main__":
    main()
