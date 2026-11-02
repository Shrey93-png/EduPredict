
import streamlit as st
import pandas as pd

from predictor import (
    validate_inputs,
    predict_performance,
    generate_suggestions
)

st.set_page_config(
    page_title="EduPredict | Student Intelligence",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CUSTOM DARK THEME ----------------

st.markdown("""
<style>

.stApp {
    background: #0b1120;
    color: #e5e7eb;
}

[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #263247;
}

[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #f8fafc !important;
}

p, label, span {
    color: #cbd5e1;
}

[data-testid="stMetric"] {
    background: #151f32;
    border: 1px solid #263650;
    padding: 20px;
    border-radius: 14px;
}

[data-testid="stMetricValue"] {
    color: #60a5fa !important;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 9px;
    padding: 0.55rem 1rem;
    font-weight: 600;
}

.stButton > button:hover {
    background: #1d4ed8;
    color: white;
    border: none;
}

.stDownloadButton > button {
    background: #1e293b;
    color: #93c5fd;
    border: 1px solid #334155;
    border-radius: 9px;
}

.stDownloadButton > button:hover {
    background: #334155;
    color: white;
}

[data-testid="stFileUploader"] {
    background: #151f32;
    border: 1px dashed #475569;
    border-radius: 12px;
    padding: 15px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #263650;
    border-radius: 10px;
}

input, textarea {
    background-color: #151f32 !important;
    color: white !important;
}

[data-baseweb="select"] > div {
    background-color: #151f32;
    border-color: #334155;
    color: white;
}

hr {
    border-color: #263650;
}

.hero {
    background: linear-gradient(120deg, #172554, #312e81, #1e1b4b);
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #3730a3;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 34px;
    margin-bottom: 8px;
}

.hero p {
    color: #c7d2fe;
    font-size: 15px;
}

.section-card {
    background: #151f32;
    border: 1px solid #263650;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 15px;
}

.small-text {
    color: #94a3b8;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>🎓 EduPredict</h1>
    <p>Intelligent Student Performance Prediction System</p>
    <p>Academic analytics • Performance prediction • Student insights</p>
</div>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

st.sidebar.markdown("## 🎓 EduPredict")

st.sidebar.markdown(
    "<p style='color:#94a3b8;font-size:13px;'>"
    "STUDENT ANALYTICS PLATFORM</p>",
    unsafe_allow_html=True
)

st.sidebar.divider()

option = st.sidebar.radio(
    "NAVIGATION",
    ["Dashboard", "Bulk Upload", "Manual Entry"]
)

st.sidebar.divider()

st.sidebar.markdown(
    "<p style='color:#64748b;font-size:12px;'>"
    "Powered by Python & Streamlit</p>",
    unsafe_allow_html=True
)


# ---------------- PROCESS STUDENTS ----------------

def process_students(data):

    required_columns = [
        "Name",
        "Attendance",
        "Assignment",
        "Internal",
        "Study Hours"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        st.error(
            "Missing columns: " + ", ".join(missing_columns)
        )
        return None

    results = []
    errors = []

    for index, student in data.iterrows():

        try:
            if pd.isna(student["Name"]):
                name = ""
            else:
                name = str(student["Name"]).strip()

            attendance = float(student["Attendance"])
            assignment = float(student["Assignment"])
            internal = float(student["Internal"])
            study_hours = float(student["Study Hours"])

            validation_errors = validate_inputs(
                name,
                attendance,
                assignment,
                internal,
                study_hours
            )

            if validation_errors:
                errors.append({
                    "Row": index + 2,
                    "Student": name,
                    "Error": " ".join(validation_errors)
                })
                continue

            performance = predict_performance(
                attendance,
                assignment,
                internal,
                study_hours
            )

            suggestions = generate_suggestions(
                attendance,
                assignment,
                internal,
                study_hours
            )

            results.append({
                "Name": name,
                "Attendance": attendance,
                "Assignment": assignment,
                "Internal": internal,
                "Study Hours": study_hours,
                "Performance": performance,
                "Suggestions": suggestions
            })

        except (ValueError, TypeError):
            errors.append({
                "Row": index + 2,
                "Student": str(student.get("Name", "")),
                "Error": "Invalid or missing numeric value."
            })

    if errors:
        st.warning(
            f"{len(errors)} invalid record(s) were skipped."
        )
        st.dataframe(
            pd.DataFrame(errors),
            use_container_width=True
        )

    if not results:
        st.error("No valid student records found.")
        return None

    return pd.DataFrame(results)


# ---------------- RESULTS DASHBOARD ----------------

def show_results(results):

    if results is None or results.empty:
        return

    st.markdown("## 📊 Class Performance Overview")

    total = len(results)

    excellent = (
        results["Performance"] == "Excellent"
    ).sum()

    good = (
        results["Performance"] == "Good"
    ).sum()

    average = (
        results["Performance"] == "Average"
    ).sum()

    poor = (
        results["Performance"] == "Poor"
    ).sum()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Students", total)
    col2.metric("Excellent", int(excellent))
    col3.metric("Good", int(good))
    col4.metric("Average", int(average))
    col5.metric("Poor", int(poor))

    st.divider()

    # Performance chart

    st.markdown("### 📈 Performance Distribution")

    chart_data = pd.DataFrame({
        "Performance": [
            "Excellent",
            "Good",
            "Average",
            "Poor"
        ],
        "Students": [
            int(excellent),
            int(good),
            int(average),
            int(poor)
        ]
    })

    st.bar_chart(
        chart_data.set_index("Performance")
    )

    st.divider()

    # Student records

    st.markdown("### 👨‍🎓 Student Records")

    col1, col2 = st.columns(2)

    with col1:
        search = st.text_input(
            "🔍 Search student",
            placeholder="Enter student name..."
        )

    with col2:
        selected_category = st.selectbox(
            "Filter performance",
            [
                "All",
                "Excellent",
                "Good",
                "Average",
                "Poor"
            ]
        )

    filtered = results.copy()

    if search:
        filtered = filtered[
            filtered["Name"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if selected_category != "All":
        filtered = filtered[
            filtered["Performance"] == selected_category
        ]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Downloads

    st.markdown("### 📥 Download Reports")

    csv_data = results.to_csv(
        index=False
    ).encode("utf-8")

    from io import BytesIO

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:
        results.to_excel(
            writer,
            index=False,
            sheet_name="Student Results"
        )

    excel_data = output.getvalue()

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "⬇ Download CSV Report",
            data=csv_data,
            file_name="student_performance_report.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        st.download_button(
            "⬇ Download Excel Report",
            data=excel_data,
            file_name="student_performance_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


# ---------------- DASHBOARD ----------------

if option == "Dashboard":

    st.markdown("## Welcome to EduPredict 👋")

    st.markdown("""
    <div class="section-card">
        <h3>Student Performance Intelligence</h3>
        <p class="small-text">
        Analyse student performance, identify academic weaknesses
        and generate performance reports through a single platform.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚡ Available Modules")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="section-card">
            <h3>📁 Bulk Upload</h3>
            <p class="small-text">
            Upload an entire class list using Excel or CSV
            and automatically analyse student records.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="section-card">
            <h3>✍ Manual Entry</h3>
            <p class="small-text">
            Enter individual student details and
            instantly generate performance predictions.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.info(
        "Select a module from the sidebar to get started."
    )


# ---------------- BULK UPLOAD ----------------

elif option == "Bulk Upload":

    st.markdown("## 📁 Bulk Student Data Upload")

    st.markdown("""
    <div class="section-card">
        <h3>Upload your class list</h3>
        <p class="small-text">
        Upload an Excel (.xlsx) or CSV (.csv) file.
        The system will automatically process every valid student record.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "Required columns: Name, Attendance, Assignment, Internal, Study Hours"
    )

    uploaded_file = st.file_uploader(
        "Choose your class file",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:

        try:

            if uploaded_file.name.endswith(".csv"):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)

            st.success("File uploaded successfully!")

            st.markdown("### 📋 Uploaded Student Data")

            st.dataframe(
                data,
                use_container_width=True,
                hide_index=True
            )

            if st.button(
                "🚀 Predict All Students",
                use_container_width=True
            ):

                results = process_students(data)

                if results is not None:

                    st.success(
                        f"Successfully analysed {len(results)} students."
                    )

                    show_results(results)

        except Exception as error:
            st.error(
                f"Unable to process file: {error}"
            )


# ---------------- MANUAL ENTRY ----------------

elif option == "Manual Entry":

    st.markdown("## ✍ Individual Student Analysis")

    st.markdown("""
    <div class="section-card">
        <p class="small-text">
        Enter the student's academic details below
        to generate an instant performance prediction.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("student_form"):

        name = st.text_input(
            "Student Name",
            placeholder="Enter student name"
        )

        col1, col2 = st.columns(2)

        with col1:
            attendance = st.number_input(
                "Attendance Percentage",
                min_value=0.0,
                max_value=100.0,
                value=75.0
            )

            assignment = st.number_input(
                "Assignment Marks",
                min_value=0.0,
                max_value=100.0,
                value=70.0
            )

        with col2:
            internal = st.number_input(
                "Internal Marks",
                min_value=0.0,
                max_value=100.0,
                value=70.0
            )

            study_hours = st.number_input(
                "Daily Study Hours",
                min_value=0.0,
                max_value=24.0,
                value=2.0
            )

        submitted = st.form_submit_button(
            "🚀 Predict Performance",
            use_container_width=True
        )

    if submitted:

        errors = validate_inputs(
            name,
            attendance,
            assignment,
            internal,
            study_hours
        )

        if errors:

            for error in errors:
                st.error(error)

        else:

            performance = predict_performance(
                attendance,
                assignment,
                internal,
                study_hours
            )

            suggestions = generate_suggestions(
                attendance,
                assignment,
                internal,
                study_hours
            )

            st.divider()

            st.markdown("### 📊 Prediction Result")

            st.metric(
                "Predicted Performance",
                performance
            )

            st.markdown("### 💡 Improvement Suggestions")

            st.info(suggestions)

