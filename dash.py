import streamlit as st
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(page_title="Hospital Data Analysis", page_icon=":hospital:", layout="wide")

st.title(":hospital: Hospital Data Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# File uploader
fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    df = pd.read_csv(fl, encoding="ISO-8859-1")

    # Preprocess dataset
    df["appointmentdate"] = pd.to_datetime(df["appointmentdate"])
    df["diagnosisdate"] = pd.to_datetime(df["diagnosisdate"])

    # Sidebar filters
    st.sidebar.header("Choose your filter:")
    city = st.sidebar.multiselect("Pick the City", df["city"].unique())
    if not city:
        filtered_df = df.copy()
    else:
        filtered_df = df[df["city"].isin(city)]

    # Layout for the dashboard
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8 = st.columns(2)

    # Age Distribution
    with col1:
        st.subheader("Age Distribution")
        fig = px.histogram(filtered_df, x="age", nbins=20, title="Age Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # Appointment Status
    with col2:
        st.subheader("Appointment Status")
        status_df = filtered_df.groupby(["appointmentdate", "status"]).size().reset_index(name='counts')
        fig = px.bar(status_df, x="appointmentdate", y="counts", color="status", title="Appointment Status")
        st.plotly_chart(fig, use_container_width=True)

    # Appointment Frequency
    with col3:
        st.subheader("Appointment Frequency")
        freq_df = filtered_df["appointmentdate"].value_counts().reset_index()
        freq_df.columns = ["appointmentdate", "count"]
        fig = px.line(freq_df, x="appointmentdate", y="count", title="Appointment Frequency")
        st.plotly_chart(fig, use_container_width=True)

    # Doctor Utilization
    with col4:
        st.subheader("Doctor Utilization")
        doctor_df = filtered_df["doctor_firstname"].value_counts().reset_index()
        doctor_df.columns = ["doctor_firstname", "count"]
        fig = px.bar(doctor_df, x="doctor_firstname", y="count", title="Doctor Utilization")
        st.plotly_chart(fig, use_container_width=True)

    # Payment Status
    with col5:
        st.subheader("Payment Status")
        fig = px.pie(filtered_df, names="paymentstatus", hole=0.5, title="Payment Status")
        st.plotly_chart(fig, use_container_width=True)

    # Billing Amounts
    with col6:
        st.subheader("Billing Amounts")
        fig = px.box(filtered_df, y="amount", title="Billing Amounts")
        st.plotly_chart(fig, use_container_width=True)

    # Common Diagnoses
    with col7:
        st.subheader("Common Diagnoses")
        diagnosis_df = filtered_df["treatmentname"].value_counts().reset_index()
        diagnosis_df.columns = ["treatmentname", "count"]
        fig = px.bar(diagnosis_df, x="treatmentname", y="count", title="Common Diagnoses")
        st.plotly_chart(fig, use_container_width=True)

    # Treatment Outcomes
    with col8:
        st.subheader("Treatment Outcomes")
        outcome_df = filtered_df.groupby(["treatmentname", "status"]).size().reset_index(name='counts')
        fig = px.bar(outcome_df, x="treatmentname", y="counts", color="status", title="Treatment Outcomes")
        st.plotly_chart(fig, use_container_width=True)

    # Department Utilization
    st.subheader("Department Utilization")
    department_df = filtered_df.groupby(["departmentname", "doctor_firstname"]).size().reset_index(name='counts')
    fig = px.treemap(department_df, path=["departmentname", "doctor_firstname"], values="counts", title="Department Utilization")
    st.plotly_chart(fig, use_container_width=True)

    # Specialization Demand
    st.subheader("Specialization Demand")
    specialization_df = filtered_df["specialization"].value_counts().reset_index()
    specialization_df.columns = ["specialization", "count"]
    fig = px.pie(specialization_df, names="specialization", title="Specialization Demand")
    st.plotly_chart(fig, use_container_width=True)

    # Common Symptoms
    st.subheader("Common Symptoms")
    symptom_df = filtered_df["symptomname"].value_counts().reset_index()
    symptom_df.columns = ["symptomname", "count"]
    fig = px.bar(symptom_df, x="symptomname", y="count", title="Common Symptoms")
    st.plotly_chart(fig, use_container_width=True)

    # Nurse Workload
    st.subheader("Nurse Workload")
    nurse_df = filtered_df["nurse_firstname"].value_counts().reset_index()
    nurse_df.columns = ["nurse_firstname", "count"]
    fig = px.bar(nurse_df, x="nurse_firstname", y="count", title="Nurse Workload")
    st.plotly_chart(fig, use_container_width=True)

    # Diagnosis Date Analysis
    st.subheader("Diagnosis Date Analysis")
    diagnosis_freq_df = filtered_df["diagnosisdate"].value_counts().reset_index()
    diagnosis_freq_df.columns = ["diagnosisdate", "count"]
    fig = px.line(diagnosis_freq_df, x="diagnosisdate", y="count", title="Diagnosis Date Analysis")
    st.plotly_chart(fig, use_container_width=True)

    # Download original dataset
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button('Download Data', data=csv, file_name="hospital_data.csv", mime="text/csv")

else:
    st.warning("Please upload a file to analyze.")
