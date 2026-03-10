import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import random

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="StudyPulse", layout="wide", initial_sidebar_state="expanded")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:#0f0e17; --surface:#1a1928; --card:#22213a;
    --accent:#f4a261; --accent2:#e76f51; --gold:#ffd166;
    --teal:#06d6a0; --text:#fffffe; --muted:#a7a9be;
    --border:rgba(244,162,97,0.2);
}
html,body,[class*="css"] { font-family:'DM Sans',sans-serif; background:var(--bg); color:var(--text); }
#MainMenu,footer,header { visibility:hidden; }

[data-testid="stSidebar"] { background:linear-gradient(180deg,#12111f,#1a1928); border-right:1px solid var(--border); }
[data-testid="stSidebar"] * { color:var(--text) !important; }

.hero-title { font-family:'Playfair Display',serif; font-size:3.2rem; font-weight:900;
    background:linear-gradient(135deg,#f4a261,#ffd166,#e76f51);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; line-height:1.1; margin-bottom:0.4rem; }
.hero-sub { font-size:1rem; color:var(--muted); letter-spacing:0.04em; margin-bottom:2rem; }

.section-title { font-family:'Playfair Display',serif; font-size:1.35rem; font-weight:700;
    color:var(--gold); border-left:3px solid var(--accent); padding-left:0.65rem; margin:1.5rem 0 0.75rem; }

.stat-card { background:var(--card); border:1px solid var(--border); border-radius:14px;
    padding:1.3rem 1.5rem; text-align:center; height:100%; }
.stat-number { font-family:'Playfair Display',serif; font-size:2rem; font-weight:900; color:var(--gold); }
.stat-label { font-size:0.72rem; text-transform:uppercase; letter-spacing:0.12em; color:var(--muted); margin-top:0.15rem; }
.stat-delta { font-size:0.8rem; color:var(--teal); margin-top:0.25rem; }

.tip-box { background:linear-gradient(135deg,rgba(6,214,160,0.07),rgba(244,162,97,0.04));
    border:1px solid rgba(6,214,160,0.25); border-left:3px solid var(--teal);
    border-radius:10px; padding:0.85rem 1.1rem; margin:0.45rem 0; }
.tip-box strong { color:var(--teal); }

.badge { display:inline-block; background:rgba(244,162,97,0.12); border:1px solid rgba(244,162,97,0.3);
    color:var(--accent); border-radius:999px; padding:0.16rem 0.7rem;
    font-size:0.73rem; font-weight:500; margin:0.18rem; letter-spacing:0.05em; }

.divider { height:1px; background:linear-gradient(90deg,transparent,var(--accent),transparent); margin:1.8rem 0; border:none; }

.about-card { background:var(--card); border:1px solid var(--border); border-radius:14px; padding:1.5rem 1.7rem; margin-bottom:1rem; }
.about-card h3 { font-family:'Playfair Display',serif; color:var(--gold); margin-bottom:0.4rem; font-size:1.15rem; }
.about-card p { color:var(--muted); line-height:1.75; margin:0; }

div[data-testid="stMetric"] { background:var(--card); border:1px solid var(--border); border-radius:11px; padding:0.75rem 1rem; }
div[data-testid="stMetric"] label { color:var(--muted) !important; font-size:0.8rem !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:var(--gold) !important; font-family:'Playfair Display',serif; font-size:1.7rem !important; }

.stButton > button { background:linear-gradient(135deg,var(--accent),var(--accent2)); color:#0f0e17;
    border:none; border-radius:9px; font-weight:600; padding:0.5rem 1.2rem;
    transition:transform 0.15s,box-shadow 0.15s; width:100%; }
.stButton > button:hover { transform:translateY(-2px); box-shadow:0 6px 18px rgba(244,162,97,0.3); }

button[data-baseweb="tab"] { color:var(--muted) !important; font-weight:500; border-bottom:2px solid transparent; }
button[data-baseweb="tab"][aria-selected="true"] { color:var(--accent) !important; border-bottom:2px solid var(--accent) !important; background:transparent !important; }

details { background:var(--card); border:1px solid var(--border) !important; border-radius:10px; padding:0.3rem 0.7rem; }
.stProgress > div > div > div { background:linear-gradient(90deg,var(--accent),var(--gold)); border-radius:999px; }

.stSelectbox > div > div, .stTextInput > div > div > input,
.stTextArea textarea, .stNumberInput input {
    background:var(--surface) !important; border:1px solid var(--border) !important;
    border-radius:7px !important; color:var(--text) !important; }
[data-testid="stDataFrame"] { border:1px solid var(--border); border-radius:11px; overflow:hidden; }
.stRadio label, .stCheckbox label { color:var(--text) !important; }
[data-baseweb="tag"] { background:rgba(244,162,97,0.18) !important; border:1px solid rgba(244,162,97,0.38) !important; }
</style>
""", unsafe_allow_html=True)

# ── Session State & Helpers ───────────────────────────────────────────────────
for k, v in [("records",[]),("streak",7),("total_hours",42.5),("xp",1340)]:
    if k not in st.session_state: st.session_state[k] = v

def divider(): st.markdown('<hr class="divider">', unsafe_allow_html=True)
def section(t): st.markdown(f'<div class="section-title">{t}</div>', unsafe_allow_html=True)
def hero(t, s):
    st.markdown(f'<div class="hero-title">{t}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-sub">{s}</div>', unsafe_allow_html=True)

TIPS = [
    "Use the Pomodoro technique: 25 min focus, 5 min break.",
    "Review your notes within 24 hours to boost retention by 60%.",
    "Sleep is your brain's save button — do not skip it.",
    "Study in varied locations to improve memory encoding.",
    "Teach what you learned — the Feynman Technique works.",
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.1rem 0 0.6rem'>
        <div style='font-family:"Playfair Display",serif;font-size:1.5rem;color:#f4a261;font-weight:700;letter-spacing:0.02em'>StudyPulse</div>
        <div style='font-size:0.65rem;color:#a7a9be;letter-spacing:0.18em;text-transform:uppercase;margin-top:0.15rem'>Productivity Tracker</div>
    </div>
    <hr style='border-color:rgba(244,162,97,0.18);margin:0.6rem 0 1rem'>
    """, unsafe_allow_html=True)

    page = st.selectbox("Page", ["Home","Study Tracker","Dashboard","Achievements","About"], label_visibility="collapsed")

    st.markdown("<hr style='border-color:rgba(244,162,97,0.12);margin:1rem 0 0.8rem'>", unsafe_allow_html=True)
    st.markdown("**Quick Stats**")
    st.metric("Study Streak", f"{st.session_state.streak} days", "+1")
    st.metric("Total XP", f"{st.session_state.xp:,}", "+80")

    st.markdown("<hr style='border-color:rgba(244,162,97,0.12);margin:1rem 0 0.8rem'>", unsafe_allow_html=True)
    st.markdown("**Preferences**")
    show_tips    = st.toggle("Show Study Tips", value=True)
    compact_view = st.toggle("Compact Dashboard", value=False)
    st.caption("StudyPulse v2.0  ·  2025")


# =============================================================================
#  HOME
# =============================================================================
if page == "Home":
    hero("Study Smarter.<br>Track Better.", "Your personal academic companion — log sessions, visualize progress, level up.")

    for col, (num, label, delta) in zip(st.columns(4), [
        (st.session_state.streak, "Day Streak", "Keep it up"),
        (st.session_state.total_hours, "Total Hours", "+3.5 this week"),
        (f"{st.session_state.xp:,}", "Study XP", "Level 12"),
        (len(st.session_state.records), "Sessions Logged", "This run"),
    ]):
        col.markdown(f'<div class="stat-card"><div class="stat-number">{num}</div>'
                     f'<div class="stat-label">{label}</div><div class="stat-delta">{delta}</div></div>',
                     unsafe_allow_html=True)

    divider()
    col_l, col_r = st.columns([2, 1])

    with col_l:
        section("Level Progress")
        xp_lvl = st.session_state.xp % 200
        st.markdown(f"**Level 12** &nbsp;·&nbsp; {xp_lvl} / 200 XP to Level 13")
        st.progress(xp_lvl / 200)

        section("Daily Study Goal")
        goal = st.slider("Daily goal (hours)", 1, 12, 4)
        done = st.number_input("Hours completed today", 0.0, float(goal), 2.5, 0.5)
        pct  = min(done / goal, 1.0)
        st.progress(pct)
        st.caption(f"{done:.1f} / {goal} hrs  ·  {int(pct * 100)}% of goal reached")

    with col_r:
        if show_tips:
            section("Tip of the Day")
            st.markdown(f'<div class="tip-box">{random.choice(TIPS)}</div>', unsafe_allow_html=True)

        section("Subjects")
        tags = ["Mathematics","Programming","Science","English","History","AI","Networking","Web Dev"]
        st.markdown("".join(f'<span class="badge">{t}</span>' for t in tags), unsafe_allow_html=True)

    divider()
    c1, c2, c3 = st.columns(3)
    if c1.button("Start a Study Session"):
        st.balloons(); st.success("Head to Study Tracker to log your session.")
    if c2.button("View Dashboard"):
        st.info("Navigate to Dashboard from the sidebar.")
    if c3.button("Random Study Tip"):
        st.toast(random.choice(TIPS))


# =============================================================================
#  STUDY TRACKER
# =============================================================================
elif page == "Study Tracker":
    hero("Study Tracker", "Log your session, rate your focus, and earn XP.")
    tab1, tab2, tab3, tab4 = st.tabs(["Student Info", "Session Details", "Self-Assessment", "Submit"])

    with tab1:
        section("Student Information")
        c1, c2 = st.columns(2)
        with c1:
            name       = st.text_input("Full Name", placeholder="e.g. Maria Santos")
            age        = st.number_input("Age", 10, 40, 18)
            study_date = st.date_input("Study Date", datetime.date.today())
        with c2:
            school     = st.text_input("School / University", placeholder="e.g. DLSU")
            year_level = st.selectbox("Year Level", ["Grade 7-10","Grade 11-12","1st Year","2nd Year","3rd Year","4th Year","Graduate"])
            mood       = st.select_slider("Mood", ["Very Bad","Bad","Okay","Good","Excellent"])
        st.info("Your details are stored within this session only and are never sent externally.")

    with tab2:
        section("Session Details")
        c1, c2 = st.columns(2)
        with c1:
            subject        = st.selectbox("Main Subject", ["Mathematics","Science","Programming","English","History","Filipino","MAPEH"])
            other_subjects = st.multiselect("Additional Subjects", ["AI & Machine Learning","Cybersecurity","Networking","Web Development","Data Science"])
            study_method   = st.radio("Study Method", ["Solo","Group","Online Lecture","Tutoring"])
        with c2:
            hours    = st.slider("Hours Studied", 0, 12, 2)
            breaks   = st.number_input("Break Time (minutes)", 0, 120, 10)
            location = st.selectbox("Location", ["Home","Library","Cafe","School","Online","Other"])

        section("Environment")
        c3, c4 = st.columns(2)
        noise  = c3.select_slider("Noise Level", ["Silent","Soft Music","Ambient","Noisy"])
        device = c4.multiselect("Devices Used", ["Laptop","Tablet","Phone","Desktop","Physical Books"], default=["Laptop"])

    with tab3:
        section("Self-Assessment")
        c1, c2 = st.columns(2)
        with c1:
            focus_level   = st.slider("Focus Level", 0, 100, 70)
            productivity  = st.slider("Productivity Level", 0, 100, 65)
            comprehension = st.slider("Comprehension Level", 0, 100, 75)
        with c2:
            stress_level = st.slider("Stress Level", 0, 100, 30)
            energy_level = st.select_slider("Energy Level", ["Exhausted","Tired","Neutral","Energized","High Energy"])
            goals_met    = st.radio("Goals met this session?", ["Yes, fully","Partially","Not really"])

        section("Notes and Upload")
        notes  = st.text_area("Session Notes", placeholder="What did you learn? Any challenges? Plans for next session.", height=110)
        upload = st.file_uploader("Upload Study Material", type=["pdf","png","jpg","docx","txt"])
        if upload:
            st.success(f"Uploaded: {upload.name} ({upload.size} bytes)")

    with tab4:
        section("Review and Submit")
        try:
            preview = {
                "Field": ["Name","Subject","Hours","Focus","Productivity","Comprehension","Mood","Method"],
                "Value": [name or "—", subject, f"{hours} hrs", f"{focus_level}%",
                          f"{productivity}%", f"{comprehension}%", mood, study_method],
            }
        except NameError:
            preview = {"Field": ["Status"], "Value": ["Complete tabs 1–3 first"]}
        st.dataframe(pd.DataFrame(preview), use_container_width=True, hide_index=True)

        agree  = st.checkbox("I confirm the information above is accurate")
        notify = st.checkbox("Remind me to study again tomorrow")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Submit Study Record"):
                if not agree:
                    st.warning("Please confirm your information first.")
                else:
                    try:
                        st.session_state.records.append({
                            "Name": name, "Subject": subject, "Hours": hours,
                            "Focus": focus_level, "Productivity": productivity, "Date": str(study_date),
                        })
                        st.session_state.total_hours += hours
                        st.session_state.xp += hours * 40 + focus_level // 5
                        with st.spinner("Saving your record..."):
                            time.sleep(0.8)
                        st.success("Session logged successfully.")
                        st.balloons()
                        if notify: st.toast("Reminder set for tomorrow.")
                    except NameError:
                        st.error("Please complete tabs 1–3 before submitting.")
        with c2:
            if st.button("Clear Form"):
                st.info("Refresh the page to reset the form.")


# =============================================================================
#  DASHBOARD
# =============================================================================
elif page == "Dashboard":
    hero("Dashboard", "Visualize your weekly performance and study trends.")

    for col, (label, val, delta) in zip(st.columns(4), [
        ("Weekly Hours","25 hrs","+3 hrs"), ("Avg Focus","74%","+6%"),
        ("Avg Productivity","68%","+2%"), ("Sessions This Week", max(len(st.session_state.records),5), "+2"),
    ]):
        col.metric(label, val, delta)

    divider()
    section("Date Range")
    st.date_input("Select range",
                  value=(datetime.date.today() - datetime.timedelta(6), datetime.date.today()),
                  label_visibility="collapsed")

    if not compact_view:
        c1, c2 = st.columns(2)
        with c1:
            section("Study Hours This Week")
            st.line_chart(pd.DataFrame(
                {"Hours":[3,4.5,2,5,6,3.5,2], "Target":[4,4,4,4,4,3,2]},
                index=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]),
                color=["#f4a261","#06d6a0"])
        with c2:
            section("Daily Productivity (%)")
            st.bar_chart(pd.DataFrame({"Productivity":[65,72,58,80,88,70,55]},
                index=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]), color="#ffd166")

    section("Subject Breakdown")
    st.dataframe(pd.DataFrame({
        "Subject":   ["Mathematics","Programming","Science","English","History"],
        "Hours":     [8.5, 7.0, 4.5, 3.0, 2.0],
        "Avg Focus": [80, 85, 70, 65, 60],
    }), use_container_width=True, hide_index=True)

    section("Focus Trend — Last 14 Days")
    st.area_chart(pd.DataFrame(np.random.randint(55,95,size=(14,3)),
                  columns=["Focus","Productivity","Comprehension"]),
                  color=["#f4a261","#ffd166","#06d6a0"])

    if st.session_state.records:
        section("Logged Sessions")
        st.dataframe(pd.DataFrame(st.session_state.records), use_container_width=True, hide_index=True)

    with st.expander("Study Tips and Strategies"):
        c1, c2 = st.columns(2)
        for col, items in zip([c1,c2],[
            [("Pomodoro","25 min focus, 5 min break, repeat"),
             ("Active Recall","Test yourself rather than re-reading notes"),
             ("Spaced Repetition","Review material at increasing intervals")],
            [("Feynman Technique","Explain the concept as if teaching a beginner"),
             ("Sleep","Memory consolidation occurs during sleep — prioritize it"),
             ("Exercise","A 20-minute walk measurably boosts focus and cognition")],
        ]):
            for title, desc in items:
                col.markdown(f'<div class="tip-box"><strong>{title}</strong><br>{desc}</div>', unsafe_allow_html=True)


# =============================================================================
#  ACHIEVEMENTS
# =============================================================================
elif page == "Achievements":
    hero("Achievements", "Earn badges and level up by building consistent study habits.")

    section("XP and Level")
    xp, level, xp_lvl = st.session_state.xp, st.session_state.xp // 200 + 1, st.session_state.xp % 200
    c1, c2 = st.columns([3,1])
    c1.markdown(f"**Level {level}** &nbsp;·&nbsp; {xp_lvl} / 200 XP")
    c1.progress(xp_lvl / 200)
    c2.metric("Total XP", f"{xp:,}")

    divider()
    section("Badges")
    badges = [
        ("7-Day Streak",  "Studied 7 days in a row",         True),
        ("Bookworm",      "Logged 10+ sessions",             len(st.session_state.records) >= 10),
        ("Speedrunner",   "Studied 6+ hours in one session", False),
        ("Sharpshooter",  "Achieved focus level 90%+",       False),
        ("Night Owl",     "Studied after 10 PM",             False),
        ("Century Club",  "100 total study hours",           st.session_state.total_hours >= 100),
        ("Scholar",       "Logged all 5 subjects",           False),
        ("Overachiever",  "Exceeded daily goal 5x in a row", False),
    ]
    b_cols = st.columns(4)
    for i, (title, desc, earned) in enumerate(badges):
        border = "#ffd166" if earned else "rgba(244,162,97,0.13)"
        color  = "#06d6a0" if earned else "#a7a9be"
        b_cols[i % 4].markdown(f"""
        <div style="background:var(--card);border:1px solid {border};border-radius:12px;
                    padding:1.1rem;text-align:center;margin-bottom:0.75rem;opacity:{'1' if earned else '0.42'}">
            <div style="font-family:'Playfair Display',serif;color:#ffd166;font-weight:700;
                        font-size:0.92rem;margin-bottom:0.25rem">{title}</div>
            <div style="font-size:0.7rem;color:#a7a9be;line-height:1.4">{desc}</div>
            <div style="margin-top:0.45rem;font-size:0.7rem;color:{color};font-weight:500">
                {'Earned' if earned else 'Locked'}</div>
        </div>""", unsafe_allow_html=True)

    divider()
    section("Class Leaderboard")
    leaders = pd.DataFrame({
        "Rank":          ["1","2","3","4","5"],
        "Student":       ["Maria S.","Juan D.","Ana R.","Carlos L.","You"],
        "XP":            [2100,1890,1650,1500,xp],
        "Streak (days)": [14,10,8,6,st.session_state.streak],
        "Sessions":      [18,14,12,10,len(st.session_state.records)],
    })
    st.dataframe(leaders.sort_values("XP",ascending=False).reset_index(drop=True),
                 use_container_width=True, hide_index=True)

    divider()
    section("Profile Color")
    fav_color = st.color_picker("Choose your color", "#f4a261")
    st.markdown(f'<div style="display:inline-block;background:{fav_color};color:#0f0e17;'
                f'border-radius:999px;padding:0.28rem 1.1rem;font-weight:700;font-size:0.88rem;margin-top:0.4rem">'
                f'Selected: {fav_color}</div>', unsafe_allow_html=True)


# =============================================================================
#  ABOUT
# =============================================================================
elif page == "About":
    hero("About StudyPulse", "A brief overview of this application — what it does, who it's for, and how it works.")

    st.markdown("""
    <div class="about-card">
        <h3>What the App Does</h3>
        <p><strong style="color:#fffffe">StudyPulse</strong> is a personal academic productivity tracker
        that helps students build stronger, more consistent study habits. You can log study sessions
        in detail, rate your focus and comprehension, track your progress through interactive charts,
        and earn XP and achievement badges as you reach milestones.</p>
    </div>
    <div class="about-card">
        <h3>Target Users</h3>
        <p>Designed for <strong style="color:#fffffe">high school and college students</strong> (ages 13–25)
        who want to take ownership of their academic performance — whether preparing for exams,
        juggling multiple subjects, or simply trying to build a more disciplined study routine.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="about-card"><h3>Inputs and Outputs</h3></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Inputs Collected**")
        st.dataframe(pd.DataFrame({
            "Input":   ["Full Name & Age","School & Year Level","Study Date",
                        "Main & Additional Subjects","Study Hours & Break Time",
                        "Focus / Productivity / Comprehension",
                        "Mood & Energy Level","Study Method & Location",
                        "Session Notes","File Upload"],
            "Section": ["Student Info","Student Info","Student Info",
                        "Session Details","Session Details","Self-Assessment",
                        "Self-Assessment","Session Details","Submit","Submit"],
        }), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("**Outputs Shown**")
        st.dataframe(pd.DataFrame({
            "Output": ["XP & Level progress","Study streak counter",
                       "Weekly hours line chart","Daily productivity bar chart",
                       "14-day focus area chart","Subject breakdown table",
                       "Logged session history","Achievement badges",
                       "Class leaderboard","Tip of the Day"],
            "Page":   ["Home / Achievements","Home / Sidebar",
                       "Dashboard","Dashboard","Dashboard","Dashboard",
                       "Dashboard","Achievements","Achievements","Home"],
        }), use_container_width=True, hide_index=True)

    divider()
    st.markdown('<div style="text-align:center;color:#a7a9be;font-size:0.8rem;padding:0.5rem 0">'
                'StudyPulse v2.0  · 2026</div>', unsafe_allow_html=True)
