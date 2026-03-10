import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Student Productivity Tracker",
    page_icon="📚",
    layout="wide"
)

# ---------- SIDEBAR ----------
st.sidebar.title("📚 Productivity App")
page = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Study Tracker", "Dashboard", "About"]
)

st.sidebar.info("Track your study habits and productivity!")

# ---------- HOME ----------
if page == "Home":

    st.title("📚 Student Productivity Tracker")

    st.markdown("### Improve your focus, track your study, and analyze productivity.")

    col1, col2 = st.columns(2)

    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135755.png", width=200)

    with col2:
        st.success("Start tracking your study sessions today!")

        st.progress(70)

        st.metric("Average Focus Level", "78%", "+5%")

        if st.button("Start Tracking"):
            st.balloons()

# ---------- TRACKER ----------
elif page == "Study Tracker":

    st.title("📝 Study Tracker")

    tab1, tab2, tab3 = st.tabs(["Student Info", "Study Details", "Submit"])

    with tab1:

        st.subheader("Student Information")

        name = st.text_input("Student Name")

        age = st.number_input("Age", 10, 40)

        study_date = st.date_input("Study Date", datetime.date.today())

        mood = st.select_slider(
            "Mood",
            ["Very Bad","Bad","Okay","Good","Excellent"]
        )

    with tab2:

        st.subheader("Study Session Details")

        col1, col2 = st.columns(2)

        with col1:

            subject = st.selectbox(
                "Main Subject",
                ["Math","Science","Programming","English","History"]
            )

            subjects = st.multiselect(
                "Other Subjects",
                ["AI","Cybersecurity","Networking","Web Dev"]
            )

            hours = st.slider("Study Hours",0,12)

        with col2:

            focus = st.radio(
                "Focus Level",
                ["Low","Medium","High"]
            )

            productivity = st.slider("Productivity Level",0,100)

            break_time = st.number_input("Break Time (minutes)",0,120)

    with tab3:

        st.subheader("Final Step")

        notes = st.text_area("Notes")

        upload = st.file_uploader("Upload Study Material")

        agree = st.checkbox("I confirm the information is correct")

        if st.button("Submit Study Record"):

            st.success("Study record saved!")

            st.balloons()

            data = {
                "Name":[name],
                "Subject":[subject],
                "Study Hours":[hours],
                "Focus":[focus],
                "Productivity":[productivity]
            }

            df = pd.DataFrame(data)

            st.dataframe(df)

# ---------- DASHBOARD ----------
elif page == "Dashboard":

    st.title("📊 Productivity Dashboard")

    st.metric("Weekly Study Hours","25 hrs","+3 hrs")

    chart_data = pd.DataFrame({
        "Day":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        "Hours":[3,4,2,5,6,3,2]
    })

    st.line_chart(chart_data.set_index("Day"))

    st.bar_chart(chart_data.set_index("Day"))

    with st.expander("Study Tips"):

        st.write("""
        • Study in focused intervals  
        • Avoid distractions  
        • Take short breaks  
        • Review your notes daily  
        """)

# ---------- ABOUT ----------
elif page == "About":

    st.title("ℹ About This App")

    st.subheader("What the App Does")

    st.write("""
    This application helps students monitor their study sessions,
    evaluate productivity levels, and analyze their learning habits.
    """)

    st.subheader("Target Users")

    st.write("""
    The target users are high school and college students
    who want to improve their study routine and focus.
    """)

    st.subheader("Inputs and Outputs")

    st.write("""
    Inputs include student name, subjects studied, study hours,
    productivity level, focus level, and notes.

    Outputs include study summaries, charts, and productivity insights.
    """)
