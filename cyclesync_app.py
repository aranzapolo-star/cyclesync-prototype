import streamlit as st

st.set_page_config(
    page_title="CycleSync",
    page_icon="🌸",
    layout="centered"
)

st.title("🌸 CycleSync")
st.subheader("Whole-Cycle Wellness Tracker")

st.write(
    "Welcome to CycleSync! Track your menstrual cycle, "
    "physical symptoms, emotional experiences, and wellbeing."
)

st.info(
    "CycleSync is an educational tracking tool, not a "
    "diagnostic tool. Cycle and ovulation estimates may be uncertain."
)

st.header("Welcome!")

st.write(
    "This prototype will help you record daily experiences "
    "and explore your personal patterns over time."
)

name = st.text_input("Choose a nickname (optional)")

if st.button("Continue"):
    if name.strip():
        st.success(f"Welcome to CycleSync, {name}!")
    else:
        st.success("Welcome to CycleSync!")

st.caption("University prototype | CycleSync")
