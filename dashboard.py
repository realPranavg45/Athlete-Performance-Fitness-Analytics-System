import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# ── Config ──────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Athlete Performance Dashboard", page_icon="🏆", layout="wide")

st.markdown("""
<style>
    /* ── Global ── */
    .main { background-color: #f8fafc; }
    .block-container { padding-top: 2.5rem; padding-bottom: 2rem; max-width: 1200px; }

    /* ── KPI Cards ── */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 18px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        text-align: center;
    }
    [data-testid="stMetricValue"] {
        font-size: 26px; font-weight: 800; color: #1e3a8a;
    }
    [data-testid="stMetricLabel"] {
        font-size: 11px; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px;
    }

    /* ── Section Dividers ── */
    .section-label {
        font-size: 13px; font-weight: 700; color: #3b82f6;
        text-transform: uppercase; letter-spacing: 2px;
        margin-bottom: 4px;
    }
    .section-title {
        font-size: 22px; font-weight: 700; color: #0f172a;
        margin-bottom: 4px; line-height: 1.3;
    }
    .section-desc {
        font-size: 14px; color: #64748b; margin-bottom: 24px; line-height: 1.5;
    }
    .spacer { margin-top: 48px; }
    .spacer-sm { margin-top: 28px; }

    /* ── Insight Cards ── */
    .insight-card {
        background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 16px 20px;
        margin-top: 12px;
        margin-bottom: 8px;
    }
    .insight-card .insight-icon { font-size: 16px; margin-right: 6px; }
    .insight-card .insight-title {
        font-size: 13px; font-weight: 700; color: #1e40af;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;
    }
    .insight-card .insight-body {
        font-size: 14px; color: #334155; line-height: 1.6;
    }
    .rec-card {
        background: linear-gradient(135deg, #fefce8 0%, #fff7ed 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 16px 20px;
        margin-top: 8px;
        margin-bottom: 8px;
    }
    .rec-card .insight-title { color: #92400e; }
    .rec-card .insight-body { color: #451a03; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 2px solid #e2e8f0; }
    .stTabs [data-baseweb="tab"] {
        height: 42px; background: transparent; border-radius: 6px 6px 0 0;
        font-size: 14px; font-weight: 500; color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        color: #1e40af; border-bottom: 3px solid #3b82f6; font-weight: 700;
    }

    /* ── Sidebar Styling (Light, Harmonious) ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #eef2f7 0%, #f8fafc 100%);
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] * {
        color: #334155 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #0f172a !important;
    }
    [data-testid="stSidebar"] .sidebar-brand {
        text-align: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid #cbd5e1;
        margin-bottom: 20px;
    }
    [data-testid="stSidebar"] .sidebar-brand h2 {
        font-size: 20px; font-weight: 800; letter-spacing: 1px;
        color: #1e3a8a !important; margin: 0;
    }
    [data-testid="stSidebar"] .sidebar-brand p {
        font-size: 11px; color: #64748b !important;
        text-transform: uppercase; letter-spacing: 2px; margin: 4px 0 0 0;
    }
    [data-testid="stSidebar"] .filter-group-label {
        font-size: 11px; font-weight: 700; color: #2563eb !important;
        text-transform: uppercase; letter-spacing: 1.5px;
        margin-top: 16px; margin-bottom: 6px;
    }
    [data-testid="stSidebar"] .sidebar-stat-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 16px;
        margin-top: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    [data-testid="stSidebar"] .sidebar-stat-box .stat-label {
        font-size: 10px; text-transform: uppercase; letter-spacing: 1px;
        color: #94a3b8 !important; margin-bottom: 2px;
    }
    [data-testid="stSidebar"] .sidebar-stat-box .stat-value {
        font-size: 18px; font-weight: 700; color: #1e40af !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #cbd5e1 !important;
    }
    [data-testid="stSidebar"] .stCaption {
        color: #94a3b8 !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Helpers ─────────────────────────────────────────────────────────────────────
def insight(title, body):
    st.markdown(f"""<div class='insight-card'>
        <div class='insight-title'>💡 {title}</div>
        <div class='insight-body'>{body}</div>
    </div>""", unsafe_allow_html=True)

def recommendation(title, body):
    st.markdown(f"""<div class='rec-card'>
        <div class='insight-title'>🎯 {title}</div>
        <div class='insight-body'>{body}</div>
    </div>""", unsafe_allow_html=True)


# ── Database ────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_engine():
    return create_engine('postgresql://postgres:Pranav2004@localhost:5522/Athlete')

engine = get_engine()

@st.cache_data
def q(query):
    with engine.connect() as conn:
        return pd.read_sql(query, conn)


# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand Header
    st.markdown("""
        <div class='sidebar-brand'>
            <h2>🏆 Athlete Analytics</h2>
            <p>Performance Dashboard</p>
        </div>
    """, unsafe_allow_html=True)

    # Filter Section: Activity
    st.markdown("<p class='filter-group-label'>Activity Filter</p>", unsafe_allow_html=True)
    all_workouts = q("SELECT DISTINCT workout_type FROM athlete_training")['workout_type'].tolist()
    selected_workouts = st.multiselect("Select Activities", all_workouts, default=all_workouts, label_visibility="collapsed")

    # Filter Section: Demographics
    st.markdown("<p class='filter-group-label'>Demographic Filters</p>", unsafe_allow_html=True)
    selected_gender = st.selectbox("Gender", ["All", "Male", "Female"], label_visibility="collapsed")
    all_ages = sorted(q("SELECT DISTINCT age_group FROM athlete_training")['age_group'].tolist())
    selected_age = st.multiselect("Age Cohort", all_ages, default=all_ages, label_visibility="collapsed")

    # Live Summary
    st.markdown("---")
    st.markdown("<p class='filter-group-label'>Current Selection</p>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class='sidebar-stat-box'>
            <div class='stat-label'>Activities</div>
            <div class='stat-value'>{len(selected_workouts)} of {len(all_workouts)}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div class='sidebar-stat-box'>
            <div class='stat-label'>Gender</div>
            <div class='stat-value'>{selected_gender}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div class='sidebar-stat-box'>
            <div class='stat-label'>Age Cohorts</div>
            <div class='stat-value'>{len(selected_age)} of {len(all_ages)}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("⚡ Connected to PostgreSQL")
    st.caption("Database: Athlete · Port: 5522")


# ── Filter Logic ────────────────────────────────────────────────────────────────
def quote_list(items):
    return ','.join("'" + str(i) + "'" for i in items)

wc = "WHERE workout_type IN (" + quote_list(selected_workouts) + ")"
wc += " AND age_group IN (" + quote_list(selected_age) + ")"
if selected_gender != "All":
    wc += " AND gender = '" + selected_gender + "'"


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL 0 — TITLE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("## 🏃‍♂️ Athlete Performance & Wellness Dashboard")
st.markdown("<p class='section-desc'>Real-time analytical reporting on training outcomes, physiological health, and population-level fitness trends.</p>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL 1 — KPI SCORECARD
# ═══════════════════════════════════════════════════════════════════════════════
kpis = q(f"""
    SELECT COUNT(*) as n, AVG(calories_burned) as cal, AVG(bmi) as bmi,
           AVG(workout_intensity) as wi, AVG(max_bpm) as bpm, AVG(fat_percentage) as fat
    FROM athlete_training {wc}
""")

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Participants", f"{kpis['n'][0]:,}")
k2.metric("Avg Calorie Burn", f"{kpis['cal'][0]:.0f} kcal")
k3.metric("Body Mass Index", f"{kpis['bmi'][0]:.1f}")
k4.metric("Training Intensity", f"{kpis['wi'][0]:.0%}")
k5.metric("Peak Heart Rate", f"{kpis['bpm'][0]:.0f} bpm")
k6.metric("Body Fat Ratio", f"{kpis['fat'][0]:.1f}%")

# ── KPI Insight ──
bmi_val = kpis['bmi'][0]
bmi_status = "within the healthy range (18.5–24.9)" if 18.5 <= bmi_val <= 24.9 else "outside the healthy range — worth flagging for targeted programs"
insight(
    "Executive Health Snapshot",
    f"Across <b>{kpis['n'][0]:,}</b> participants, the mean BMI of <b>{bmi_val:.1f}</b> is {bmi_status}. "
    f"On average, each training session burns <b>{kpis['cal'][0]:.0f} kcal</b> at a training intensity of <b>{kpis['wi'][0]:.0%}</b>."
)


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL 2 — THE BIG PICTURE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
st.markdown("<p class='section-label'>Training Intensity Overview</p>", unsafe_allow_html=True)
st.markdown("<p class='section-title'>Where are the highest-performing training segments?</p>", unsafe_allow_html=True)
st.markdown("<p class='section-desc'>This matrix maps average training intensity across activity categories and age cohorts, highlighting engagement hotspots and underperforming segments.</p>", unsafe_allow_html=True)

df_heat = q(f"SELECT age_group, workout_type, AVG(workout_intensity) as intensity FROM athlete_training {wc} GROUP BY 1, 2")
fig_heat = px.density_heatmap(
    df_heat, x='age_group', y='workout_type', z='intensity', histfunc="avg",
    color_continuous_scale='Viridis', text_auto='.2f',
    category_orders={"age_group": ["18-24", "25-34", "35-44", "45+"]}
)
fig_heat.update_layout(
    height=380, margin=dict(t=10, b=10, l=0, r=0),
    xaxis_title="Age Cohort", yaxis_title="Activity Category",
    coloraxis_colorbar=dict(title="Avg Intensity")
)
st.plotly_chart(fig_heat, use_container_width=True)

# ── Heatmap Insights ──
if not df_heat.empty:
    top_seg = df_heat.loc[df_heat['intensity'].idxmax()]
    low_seg = df_heat.loc[df_heat['intensity'].idxmin()]
    insight(
        "Highest & Lowest Engagement Segments",
        f"The highest average intensity (<b>{top_seg['intensity']:.2f}</b>) is found in "
        f"<b>{top_seg['workout_type']}</b> within the <b>{top_seg['age_group']}</b> age group. "
        f"Conversely, the lowest intensity (<b>{low_seg['intensity']:.2f}</b>) is in "
        f"<b>{low_seg['workout_type']}</b> for <b>{low_seg['age_group']}</b>."
    )
    recommendation(
        "Actionable Training Strategy",
        f"Consider designing progressive overload programs for the <b>{low_seg['age_group']}</b> "
        f"cohort doing <b>{low_seg['workout_type']}</b> to raise their engagement levels. "
        f"The <b>{top_seg['age_group']}</b> cohort may benefit from recovery-focused protocols to prevent overtraining."
    )


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL 3 — POPULATION CONTEXT
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
st.markdown("<p class='section-label'>Population Segmentation</p>", unsafe_allow_html=True)
st.markdown("<p class='section-title'>What does the athlete population look like?</p>", unsafe_allow_html=True)
st.markdown("<p class='section-desc'>Breakdown of training preferences, health-risk categories, and cardiovascular stress profiles across the filtered population.</p>", unsafe_allow_html=True)

p1, p2, p3 = st.columns([1, 1, 1], gap="large")

with p1:
    df_pop = q(f"SELECT workout_type, COUNT(*) as n FROM athlete_training {wc} GROUP BY 1 ORDER BY n DESC")
    fig_pop = px.pie(df_pop, values='n', names='workout_type', hole=0.55)
    fig_pop.update_layout(
        title=dict(text="Training Activity Share", font=dict(size=15)),
        height=340, margin=dict(t=50, b=10, l=10, r=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(size=10))
    )
    st.plotly_chart(fig_pop, use_container_width=True)

with p2:
    df_sun = q(f"SELECT age_group, bmi_category, COUNT(*) as n FROM athlete_training {wc} GROUP BY 1, 2")
    fig_sun = px.sunburst(df_sun, path=['age_group', 'bmi_category'], values='n',
                          color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_sun.update_layout(
        title=dict(text="Health Risk by Age Cohort", font=dict(size=15)),
        height=340, margin=dict(t=50, b=10, l=10, r=10)
    )
    st.plotly_chart(fig_sun, use_container_width=True)

with p3:
    df_hr = q(f"SELECT workout_type, AVG(resting_bpm) as rest, AVG(avg_bpm) as train, AVG(max_bpm) as peak FROM athlete_training {wc} GROUP BY 1")
    df_hr_m = df_hr.melt(id_vars='workout_type', var_name='Zone', value_name='BPM')
    fig_radar = px.line_polar(df_hr_m, r='BPM', theta='workout_type', color='Zone', line_close=True)
    fig_radar.update_layout(
        title=dict(text="Cardiovascular Stress Profile", font=dict(size=15)),
        height=340, margin=dict(t=50, b=10, l=10, r=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5, font=dict(size=10))
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ── Population Insights ──
if not df_pop.empty:
    top_activity = df_pop.iloc[0]
    total_n = df_pop['n'].sum()
    top_pct = top_activity['n'] / total_n * 100

    insight(
        "Leading Training Category",
        f"<b>{top_activity['workout_type']}</b> is the most popular activity, accounting for "
        f"<b>{top_pct:.1f}%</b> of all sessions ({top_activity['n']} out of {total_n}). "
        f"This suggests strong engagement in this category — ideal for building community programs around it."
    )

if not df_hr.empty:
    max_gap_idx = (df_hr['peak'] - df_hr['rest']).idxmax()
    max_gap_row = df_hr.loc[max_gap_idx]
    gap = max_gap_row['peak'] - max_gap_row['rest']
    recommendation(
        "Cardiovascular Risk Advisory",
        f"<b>{max_gap_row['workout_type']}</b> shows the largest resting-to-peak HR gap of <b>{gap:.0f} BPM</b> "
        f"(rest: {max_gap_row['rest']:.0f} → peak: {max_gap_row['peak']:.0f}). "
        f"Athletes in this sport experience the most cardiovascular stress and may need structured cool-down routines."
    )


# ═══════════════════════════════════════════════════════════════════════════════
# LEVEL 4 — DEEP-DIVE TABS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
st.markdown("<p class='section-label'>Detailed Analysis</p>", unsafe_allow_html=True)
st.markdown("<p class='section-title'>Explore targeted performance and health questions</p>", unsafe_allow_html=True)

t_perf, t_body, t_raw = st.tabs(["Training Efficiency", "Body Composition & Vitals", "Raw Data Export"])

# ── Tab 1: Performance ──────────────────────────────────────────────────────────
with t_perf:
    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    left, right = st.columns(2, gap="large")

    with left:
        df_eff = q(f"SELECT workout_type, AVG(calories_burned / NULLIF(session_duration_hours, 0)) as eff FROM athlete_training {wc} GROUP BY 1 ORDER BY eff DESC")
        fig_eff = px.bar(df_eff, x='eff', y='workout_type', orientation='h',
                         color='eff', color_continuous_scale='Blues',
                         labels={'eff': 'Calories Burned per Hour', 'workout_type': 'Activity'})
        fig_eff.update_layout(
            title=dict(text="Calorie Burn Rate by Activity Type", font=dict(size=15)),
            height=380, margin=dict(t=50, b=20, l=0, r=20), showlegend=False
        )
        st.plotly_chart(fig_eff, use_container_width=True)

    with right:
        df_sc = q(f"SELECT workout_intensity, calories_burned, workout_type FROM athlete_training {wc}")
        fig_sc = px.scatter(df_sc, x='workout_intensity', y='calories_burned', color='workout_type',
                            labels={'workout_intensity': 'Training Intensity (Ratio)', 'calories_burned': 'Calories Burned (kcal)', 'workout_type': 'Activity'})
        fig_sc.update_layout(
            title=dict(text="Does Higher Intensity Yield More Calorie Burn?", font=dict(size=15)),
            height=380, margin=dict(t=50, b=20, l=0, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5, font=dict(size=10))
        )
        st.plotly_chart(fig_sc, use_container_width=True)

    # ── Performance Insights ──
    if not df_eff.empty:
        best = df_eff.iloc[0]
        worst = df_eff.iloc[-1]
        diff = best['eff'] - worst['eff']
        insight(
            "Training Efficiency Gap",
            f"<b>{best['workout_type']}</b> leads with <b>{best['eff']:.0f} kcal/hr</b>, while "
            f"<b>{worst['workout_type']}</b> burns only <b>{worst['eff']:.0f} kcal/hr</b> — "
            f"a gap of <b>{diff:.0f} kcal/hr</b>. For time-constrained athletes, "
            f"switching to {best['workout_type']} can yield significantly higher calorie output per session."
        )
        recommendation(
            "Suggested Program Optimization",
            f"Athletes doing <b>{worst['workout_type']}</b> may not be targeting calorie burn as their primary goal. "
            f"Consider pairing it with a high-burn activity like <b>{best['workout_type']}</b> in a hybrid weekly plan."
        )

# ── Tab 2: Body Metrics ─────────────────────────────────────────────────────────
with t_body:
    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    left2, right2 = st.columns(2, gap="large")

    with left2:
        df_bf = q(f"SELECT bmi, fat_percentage, gender FROM athlete_training {wc}")
        fig_bf = px.scatter(df_bf, x='bmi', y='fat_percentage', color='gender', trendline="ols",
                            color_discrete_map={'Male': '#3b82f6', 'Female': '#ec4899'},
                            labels={'bmi': 'Body Mass Index', 'fat_percentage': 'Body Fat Percentage (%)', 'gender': 'Gender'})
        fig_bf.update_layout(
            title=dict(text="Body Composition: BMI vs. Fat Percentage", font=dict(size=15)),
            height=380, margin=dict(t=50, b=20, l=0, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_bf, use_container_width=True)

    with right2:
        df_hrd = q(f"SELECT avg_bpm, max_bpm FROM athlete_training {wc}")
        fig_h = go.Figure()
        fig_h.add_trace(go.Histogram(x=df_hrd['avg_bpm'], name='Training Heart Rate', marker_color='#60a5fa', opacity=0.65))
        fig_h.add_trace(go.Histogram(x=df_hrd['max_bpm'], name='Peak Heart Rate', marker_color='#f87171', opacity=0.65))
        fig_h.update_layout(
            barmode='overlay',
            title=dict(text="Training vs. Peak Heart Rate Distribution", font=dict(size=15)),
            height=380, margin=dict(t=50, b=20, l=0, r=20),
            xaxis_title="Heart Rate (Beats per Minute)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_h, use_container_width=True)

    # ── Body Metrics Insights ──
    if not df_bf.empty:
        corr = df_bf['bmi'].corr(df_bf['fat_percentage'])
        strength = "strong" if abs(corr) > 0.7 else "moderate" if abs(corr) > 0.4 else "weak"
        insight(
            "Body Composition Correlation Strength",
            f"BMI and Fat Percentage show a <b>{strength} positive correlation</b> (r = <b>{corr:.2f}</b>). "
            f"This confirms that BMI is a {'reliable' if abs(corr) > 0.5 else 'limited'} proxy for body fat in this population. "
            f"For precise body-composition tracking, direct fat measurement remains essential."
        )

    if not df_hrd.empty:
        avg_spread = df_hrd['max_bpm'].mean() - df_hrd['avg_bpm'].mean()
        recommendation(
            "Cardiovascular Training Headroom",
            f"The average gap between training BPM and max BPM is <b>{avg_spread:.0f} BPM</b>. "
            f"{'Most athletes are training well below their max — room to push harder in HIIT sessions.' if avg_spread > 30 else 'Athletes are training close to their max — monitor for signs of overtraining.'}"
        )

# ── Tab 3: Data Explorer ────────────────────────────────────────────────────────
with t_raw:
    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    df_full = q(f"SELECT * FROM athlete_training {wc}")
    st.dataframe(df_full, use_container_width=True, height=420)

    st.markdown("")
    st.download_button("📥 Export Filtered Dataset", df_full.to_csv(index=False), "athlete_export.csv", "text/csv")


# ── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
st.markdown("---")
st.caption("Athlete Performance Dashboard v4.0 · PostgreSQL · Streamlit · Plotly")
