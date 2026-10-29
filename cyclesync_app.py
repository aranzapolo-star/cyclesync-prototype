import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="CycleSync", page_icon="🌸", layout="centered")

st.title("🌸 CycleSync")
st.subheader("Whole-Cycle Wellness Tracker")
st.write("Track your menstrual cycle, physical symptoms, emotional experiences, and wellbeing over time.")
st.info("CycleSync is an educational prototype, not a diagnostic tool. Cycle and ovulation estimates can be uncertain.")
st.warning("Prototype privacy notice: Do not enter your real name or identifying information. This version has no individual accounts or secure long-term storage. Use fictional test data only; do not use it with study participants yet.")

if "records" not in st.session_state:
    st.session_state.records = []

st.header("Daily check-in")
st.caption("Fields marked optional can be left blank.")

participant_code = st.text_input("Participant nickname or code (optional)", placeholder="For example: P001 — do not use your real name")
record_date = st.date_input("Date of check-in", value=date.today())

st.subheader("Menstrual cycle")
period_started = st.radio("Did your period start today?", ["No", "Yes", "Not sure"], horizontal=True)
bleeding = st.selectbox("Bleeding today", ["None", "Spotting", "Light", "Moderate", "Heavy", "Not sure"])
period_ended = st.radio("Did your period end today?", ["No", "Yes", "Not applicable / not sure"], horizontal=True)

blood_amount = "Not applicable"
product_changes = "Not recorded"
product_saturation = "Not recorded"
clots = "Not recorded"
blood_color = "Not recorded"
flow_leakage = "Not recorded"

if bleeding in ["Spotting", "Light", "Moderate", "Heavy"]:
    st.markdown("#### Period flow details")
    st.caption("These details are optional. Choose the options that fit your experience.")
    blood_amount = st.selectbox("How would you describe the amount of blood?", ["Not sure", "Very little", "A little", "Moderate amount", "A lot"])
    product_changes = st.selectbox("How often did you change your menstrual product? (optional)", ["Not applicable / did not use a product", "Not recorded", "Less often than every 4 hours", "Every 3–4 hours", "Every 1–2 hours", "Every hour or more often"])
    product_saturation = st.selectbox("How full was your menstrual product when you changed it? (optional)", ["Not applicable", "Not recorded", "Not full / lightly stained", "Partly full", "Mostly full", "Completely saturated"])
    clots = st.selectbox("Did you notice blood clots? (optional)", ["Not recorded", "No", "Yes, small clots", "Yes, larger clots", "Not sure"])
    blood_color = st.selectbox("What color was the blood? (optional)", ["Not recorded", "Bright red", "Dark red", "Brown", "Pink", "Mixed / changed during the day", "Not sure"])
    flow_leakage = st.selectbox("Did bleeding leak through your menstrual product or clothes? (optional)", ["Not recorded", "No", "Yes, once", "Yes, more than once"])

st.subheader("Physical symptoms")
physical_symptoms = st.multiselect("Which physical symptoms did you experience today?", ["Cramps / pelvic pain", "Headache", "Bloating", "Breast tenderness", "Fatigue / low energy", "Acne / skin changes", "Nausea", "Digestive changes", "Back pain", "Muscle or joint pain", "Increased appetite", "Changes in sleep", "No physical symptoms", "Other"])
pain_level = st.slider("Overall pain intensity (0 = none, 10 = worst imaginable)", min_value=0, max_value=10, value=0)

st.subheader("Emotional wellbeing")
emotions = st.multiselect("How did you feel emotionally today?", ["Calm / content", "Happy / positive", "Anxious / worried", "Irritable", "Sad / low mood", "Sensitive / tearful", "Stressed", "Motivated / energetic", "Difficulty concentrating", "No noticeable emotional changes", "Other"])
wellbeing = st.select_slider("Overall wellbeing today", options=["Very poor", "Poor", "Okay", "Good", "Very good"], value="Okay")

st.subheader("Discharge and other observations")
discharge = st.selectbox("Vaginal discharge (optional)", ["Not recorded", "None noticed", "Dry", "Sticky", "Creamy", "Watery", "Slippery / stretchy", "Unusual change", "Prefer not to say"])
spotting = st.radio("Spotting outside your period?", ["Not sure / not recorded", "No", "Yes"], horizontal=True)
daily_impact = st.selectbox("How much did symptoms affect your daily activities?", ["Not at all", "A little", "Moderately", "A lot", "Unable to do usual activities"])
notes = st.text_area("Additional notes (optional)", placeholder="Avoid names or identifying details.")

if st.button("Save this check-in", type="primary"):
    st.session_state.records.append({
        "participant_code": participant_code.strip(),
        "date": record_date.isoformat(),
        "period_started": period_started,
        "bleeding": bleeding,
        "period_ended": period_ended,
        "blood_amount": blood_amount,
        "product_changes": product_changes,
        "product_saturation": product_saturation,
        "blood_clots": clots,
        "blood_color": blood_color,
        "flow_leakage": flow_leakage,
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
    df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.sort_values("date_parsed")

    st.write(f"Check-ins in this session: **{len(df)}**")
    st.dataframe(df.drop(columns=["date_parsed"]), use_container_width=True, hide_index=True)

    st.download_button(
        "Download check-ins as CSV",
        data=df.drop(columns=["date_parsed"]).to_csv(index=False).encode("utf-8-sig"),
        file_name="cyclesync_test_records.csv",
        mime="text/csv"
    )

    st.divider()
    st.header("Statistics and charts")
    st.caption("These summaries use only records currently available in this app session. They are descriptive, not medical conclusions.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Check-ins", len(df))
    col2.metric("Days with bleeding", int(df["bleeding"].isin(["Spotting", "Light", "Moderate", "Heavy"]).sum()))
    col3.metric("Average pain", f'{df["pain_level_0_10"].mean():.1f}/10')

    chart_df = df.set_index("date_parsed")
    pain_chart = chart_df[["pain_level_0_10"]].rename(columns={"pain_level_0_10": "Pain (0–10)"})
    st.subheader("Pain over time")
    st.line_chart(pain_chart, x_label="Date", y_label="Pain intensity")

    bleeding_scale = {"None": 0, "Spotting": 1, "Light": 2, "Moderate": 3, "Heavy": 4, "Not sure": None}
    bleeding_df = chart_df[["bleeding"]].copy()
    bleeding_df["Bleeding level (0–4)"] = bleeding_df["bleeding"].map(bleeding_scale)
    st.subheader("Bleeding level over time")
    st.line_chart(bleeding_df[["Bleeding level (0–4)"]], x_label="Date", y_label="None 0 · Spotting 1 · Light 2 · Moderate 3 · Heavy 4")

    wellbeing_scale = {"Very poor": 1, "Poor": 2, "Okay": 3, "Good": 4, "Very good": 5}
    wellbeing_df = chart_df[["wellbeing"]].copy()
    wellbeing_df["Wellbeing (1–5)"] = wellbeing_df["wellbeing"].map(wellbeing_scale)
    st.subheader("Wellbeing over time")
    st.line_chart(wellbeing_df[["Wellbeing (1–5)"]], x_label="Date", y_label="1 = Very poor · 5 = Very good")

    symptom_counts = {}
    for item in df["physical_symptoms"].fillna(""):
        for symptom in [x.strip() for x in item.split(";") if x.strip()]:
            if symptom != "No physical symptoms":
                symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
    st.subheader("Physical symptoms recorded")
    if symptom_counts:
        symptom_df = pd.DataFrame(
            sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True),
            columns=["Symptom", "Number of check-ins"]
        ).set_index("Symptom")
        st.bar_chart(symptom_df)
    else:
        st.write("No physical symptoms have been recorded in the current session yet.")

    st.caption("The charts are most informative after several check-ins on different dates. They do not predict periods or diagnose a condition.")
else:
    st.write("Your saved check-ins will appear here.")
    st.caption("Try fictional entries on different dates to test the table and charts.")

st.divider()
st.caption("CycleSync | University prototype | Educational use only")




