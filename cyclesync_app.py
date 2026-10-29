import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="CycleSync",
    page_icon="🌸",
    layout="centered"
)

st.title("🌸 CycleSync")
st.subheader("Whole-Cycle Wellness Tracker")
st.write(
    "Track your menstrual cycle, physical symptoms, emotional experiences, "
    "and wellbeing over time."
)
st.info(
    "CycleSync is an educational prototype, not a diagnostic tool. "
    "Cycle and ovulation estimates can be uncertain."
)

st.warning(
    "Prototype privacy notice: Do not enter your real name or information that "
    "identifies you. This version does not have individual accounts or secure "
    "long-term storage. Use fictional test data only; do not use it with study "
    "participants yet."
)

if "records" not in st.session_state:
    st.session_state.records = []

st.header("Daily check-in")
st.caption("Fields marked optional can be left blank.")

with st.form("daily_checkin"):
    participant_code = st.text_input(
        "Participant nickname or code (optional)",
        placeholder="For example: P001 — do not use your real name"
    )
    record_date = st.date_input("Date of check-in", value=date.today())

    st.subheader("Menstrual cycle")
    period_started = st.radio(
        "Did your period start today?",
        options=["No", "Yes", "Not sure"],
        horizontal=True
    )
    bleeding = st.selectbox(
        "Bleeding today",
        ["None", "Spotting", "Light", "Moderate", "Heavy", "Not sure"]
    )
    period_ended = st.radio(
        "Did your period end today?",
        options=["No", "Yes", "Not applicable / not sure"],
        horizontal=True
    )

    st.subheader("Physical symptoms")
    physical_symptoms = st.multiselect(
        "Which physical symptoms did you experience today?",
        [
            "Cramps / pelvic pain",
            "Headache",
            "Bloating",
"Breast tenderness",
            "Fatigue / low energy",
            "Acne / skin changes",
            "Nausea",
            "Digestive changes",
            "Back pain",
            "Muscle or joint pain",
            "Increased appetite",
            "Changes in sleep",
            "No physical symptoms",
            "Other"
        ]
    )
    pain_level = st.slider(
        "Overall pain intensity (0 = none, 10 = worst imaginable)",
        min_value=0,
        max_value=10,
        value=0
    )

    st.subheader("Emotional wellbeing")
    emotions = st.multiselect(
        "How did you feel emotionally today?",
        [
            "Calm / content",
            "Happy / positive",
            "Anxious / worried",
            "Irritable",
            "Sad / low mood",
            "Sensitive / tearful",
            "Stressed",
            "Motivated / energetic",
            "Difficulty concentrating",
            "No noticeable emotional changes",
            "Other"
        ]
    )
    wellbeing = st.select_slider(
        "Overall wellbeing today",
        options=["Very poor", "Poor", "Okay", "Good", "Very good"],
        value="Okay"
    )

    st.subheader("Discharge and other observations")
    discharge = st.selectbox(
        "Vaginal discharge (optional)",
        [
            "Not recorded",
            "None noticed",
            "Dry",
            "Sticky",
            "Creamy",
            "Watery",
            "Slippery / stretchy",
            "Unusual change",
            "Prefer not to say"
        ]
    )
    spotting = st.radio(
        "Spotting outside your period?",
        ["Not sure / not recorded", "No", "Yes"],
        horizontal=True
    )
    daily_impact = st.selectbox(
        "How much did symptoms affect your daily activities?",
        ["Not at all", "A little", "Moderately", "A lot", "Unable to do usual activities"]
    )
    notes = st.text_area(
        "Additional notes (optional)",
        placeholder="Avoid names or identifying details."
    )

    submitted = st.form_submit_button("Save this check-in", type="primary")

if submitted:
    st.session_state.records.append({
        "participant_code": participant_code.strip(),
        "date": record_date.isoformat(),
        "period_started": period_started,
        "bleeding": bleeding,
        "period_ended": period_ended,
        "physical_symptoms": "; ".join(physical_symptoms),
        "pain_level_0_10": pain_level,
        "emotions": "; ".join(emotions),
        "wellbeing": wellbeing,
        "discharge": discharge,
        "spotting_outside_period": spotting,
        "daily_impact": daily_impact,
        "notes": notes.strip()
    })
    st.success("Check-in saved for this browser session.")

st.divider()
st.header("Your check-ins")

records = st.session_state.records
if records:
    df = pd.DataFrame(records)
    st.write(f"Check-ins in this session: **{len(df)}**")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.download_button(
        label="Download check-ins as CSV",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="cyclesync_test_records.csv",
        mime="text/csv"
    )

    st.caption(
        "Download your records before leaving this session. They are kept only "
        "in the current app session and may disappear when the session resets."
    )
else:
    st.write("Your saved check-ins will appear here.")
    st.caption("Try a fictional entry to test the form.")

st.divider()
st.caption("CycleSync | University prototype | Educational use only")

