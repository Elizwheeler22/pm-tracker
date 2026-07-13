import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Project Health & Velocity Tracker",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Palette ──
SAGE        = "#6b8f71"
SAGE_DARK   = "#4a6b50"
SAGE_LIGHT  = "#9ab89f"
BLUSH       = "#c9918e"
EARTH       = "#7c5c4a"
CREAM       = "#faf7f2"
WARM_WHITE  = "#f5f0ea"
TEXT        = "#2c2416"
TEXT_MID    = "#5c4a38"
AMBER       = "#e8a87c"
GOLD        = "#d4b483"
BORDER      = "#ddd5cb"

st.markdown(f"""
<style>
    .block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; background: {CREAM}; }}
    section[data-testid="stSidebar"] {{ background: {WARM_WHITE}; border-right: 1px solid {BORDER}; }}
    div[data-testid="metric-container"] {{
        background: {WARM_WHITE}; border: 1px solid {BORDER};
        border-radius: 10px; padding: 1rem;
    }}
    .stDataFrame {{ border: 1px solid {BORDER}; border-radius: 8px; }}
    h1 {{ color: {TEXT} !important; font-size: 1.8rem !important; }}
    h2, h3 {{ color: {SAGE_DARK} !important; }}
</style>
""", unsafe_allow_html=True)


# ── Data ──
@st.cache_data
def load_data():
    projects = pd.DataFrame([
        {"Project": "CRM Platform Migration",   "Owner": "Sarah Chen",    "Status": "On Track", "Health": 87, "Completion": 72, "Priority": "High",     "Team": 5, "Due": "2025-08-30"},
        {"Project": "Q3 Marketing Launch",       "Owner": "James Okafor",  "Status": "At Risk",  "Health": 62, "Completion": 45, "Priority": "High",     "Team": 4, "Due": "2025-07-15"},
        {"Project": "Engineering Ops Revamp",    "Owner": "Priya Patel",   "Status": "On Track", "Health": 91, "Completion": 88, "Priority": "Medium",   "Team": 6, "Due": "2025-07-31"},
        {"Project": "Partner Integration Suite", "Owner": "Marcus Webb",   "Status": "Blocked",  "Health": 34, "Completion": 31, "Priority": "Critical", "Team": 7, "Due": "2025-09-15"},
        {"Project": "Analytics Infrastructure",  "Owner": "Yuki Tanaka",   "Status": "On Track", "Health": 78, "Completion": 61, "Priority": "Medium",   "Team": 3, "Due": "2025-10-01"},
        {"Project": "Mobile App v2.0",           "Owner": "Chris Rivera",  "Status": "At Risk",  "Health": 55, "Completion": 38, "Priority": "High",     "Team": 8, "Due": "2025-11-30"},
    ])

    velocity_raw = {
        "CRM Platform Migration":   ([42,38,45,41,47,44,46,43], [40,35,48,44,45,46,48,45]),
        "Q3 Marketing Launch":       ([30,32,28,25,24,22,20,18], [32,30,30,28,26,24,22,20]),
        "Engineering Ops Revamp":    ([55,58,52,60,57,63,61,65], [50,56,54,58,58,60,62,64]),
        "Partner Integration Suite": ([40,35,28,20,15,12,18,14], [42,40,38,38,36,34,30,28]),
        "Analytics Infrastructure":  ([28,31,30,34,32,35,33,36], [28,30,32,32,33,34,34,36]),
        "Mobile App v2.0":           ([50,44,48,40,35,30,28,25], [52,50,48,46,44,40,38,36]),
    }
    velocity_rows = []
    for proj, (completed, planned) in velocity_raw.items():
        for i, (c, p) in enumerate(zip(completed, planned)):
            velocity_rows.append({"Project": proj, "Sprint": f"S{i+1}", "Sprint_Num": i+1,
                                   "Completed": c, "Planned": p})
    velocity_df = pd.DataFrame(velocity_rows)

    milestones = pd.DataFrame([
        {"Project": "CRM Platform Migration",   "Milestone": "Data model finalized",       "Due": "2025-03-15", "Done": True},
        {"Project": "CRM Platform Migration",   "Milestone": "Migration scripts tested",    "Due": "2025-05-30", "Done": True},
        {"Project": "CRM Platform Migration",   "Milestone": "UAT complete",                "Due": "2025-07-25", "Done": False},
        {"Project": "CRM Platform Migration",   "Milestone": "Go-live",                     "Due": "2025-08-30", "Done": False},
        {"Project": "Q3 Marketing Launch",       "Milestone": "Creative brief approved",    "Due": "2025-04-01", "Done": True},
        {"Project": "Q3 Marketing Launch",       "Milestone": "Campaign assets complete",   "Due": "2025-06-15", "Done": False},
        {"Project": "Q3 Marketing Launch",       "Milestone": "Launch",                     "Due": "2025-07-15", "Done": False},
        {"Project": "Engineering Ops Revamp",    "Milestone": "Process audit complete",     "Due": "2025-01-31", "Done": True},
        {"Project": "Engineering Ops Revamp",    "Milestone": "Workflows documented",       "Due": "2025-04-30", "Done": True},
        {"Project": "Engineering Ops Revamp",    "Milestone": "Tooling rollout",            "Due": "2025-06-30", "Done": True},
        {"Project": "Engineering Ops Revamp",    "Milestone": "Team training complete",     "Due": "2025-07-31", "Done": False},
        {"Project": "Partner Integration Suite", "Milestone": "API contracts signed",       "Due": "2025-03-01", "Done": True},
        {"Project": "Partner Integration Suite", "Milestone": "Dev environment ready",      "Due": "2025-04-15", "Done": False},
        {"Project": "Partner Integration Suite", "Milestone": "Integration testing",        "Due": "2025-07-01", "Done": False},
        {"Project": "Analytics Infrastructure",  "Milestone": "Data warehouse provisioned", "Due": "2025-03-15", "Done": True},
        {"Project": "Analytics Infrastructure",  "Milestone": "ETL pipelines live",         "Due": "2025-06-01", "Done": True},
        {"Project": "Analytics Infrastructure",  "Milestone": "Dashboard suite delivered",  "Due": "2025-09-01", "Done": False},
        {"Project": "Mobile App v2.0",           "Milestone": "UX designs approved",        "Due": "2025-03-30", "Done": True},
        {"Project": "Mobile App v2.0",           "Milestone": "Core features in beta",      "Due": "2025-07-01", "Done": False},
        {"Project": "Mobile App v2.0",           "Milestone": "App store submission",       "Due": "2025-10-01", "Done": False},
        {"Project": "Mobile App v2.0",           "Milestone": "v2.0 launch",                "Due": "2025-11-30", "Done": False},
    ])

    workload = pd.DataFrame([
        {"Member": "Sarah Chen",    "Active": 12, "Blocked": 1, "Overdue": 0, "Project": "CRM Platform Migration"},
        {"Member": "Marcus Webb",   "Active": 18, "Blocked": 6, "Overdue": 4, "Project": "Partner Integration Suite"},
        {"Member": "Priya Patel",   "Active":  9, "Blocked": 0, "Overdue": 0, "Project": "Engineering Ops Revamp"},
        {"Member": "James Okafor",  "Active": 15, "Blocked": 3, "Overdue": 2, "Project": "Q3 Marketing Launch"},
        {"Member": "Yuki Tanaka",   "Active":  8, "Blocked": 0, "Overdue": 0, "Project": "Analytics Infrastructure"},
        {"Member": "Chris Rivera",  "Active": 20, "Blocked": 4, "Overdue": 3, "Project": "Mobile App v2.0"},
        {"Member": "Anika Singh",   "Active": 11, "Blocked": 2, "Overdue": 1, "Project": "CRM Platform Migration"},
        {"Member": "Dev Kapoor",    "Active":  7, "Blocked": 0, "Overdue": 0, "Project": "Engineering Ops Revamp"},
        {"Member": "Lena Kovacs",   "Active": 14, "Blocked": 5, "Overdue": 2, "Project": "Partner Integration Suite"},
        {"Member": "Tom Briggs",    "Active": 16, "Blocked": 3, "Overdue": 1, "Project": "Mobile App v2.0"},
    ])

    risks = pd.DataFrame([
        {"Project": "Partner Integration Suite", "Risk": "Third-party API changes",    "Level": "Critical", "Owner": "Marcus Webb",  "Mitigation": "Escalated to vendor; fallback being scoped"},
        {"Project": "Q3 Marketing Launch",       "Risk": "Creative vendor delay",       "Level": "High",     "Owner": "James Okafor", "Mitigation": "Secondary vendor identified"},
        {"Project": "Mobile App v2.0",           "Risk": "App store review timeline",   "Level": "High",     "Owner": "Chris Rivera", "Mitigation": "Submission date moved up 3 weeks"},
        {"Project": "CRM Platform Migration",    "Risk": "Data volume underestimated",  "Level": "Medium",   "Owner": "Sarah Chen",   "Mitigation": "Additional ETL capacity provisioned"},
        {"Project": "Analytics Infrastructure",  "Risk": "Q3 headcount gap",           "Level": "Medium",   "Owner": "Yuki Tanaka",  "Mitigation": "Contract resource request submitted"},
        {"Project": "Engineering Ops Revamp",    "Risk": "Adoption lag post-rollout",   "Level": "Low",      "Owner": "Priya Patel",  "Mitigation": "Champions program launched"},
    ])

    return projects, velocity_df, milestones, workload, risks

projects_df, velocity_df, milestones_df, workload_df, risks_df = load_data()

# ── Sidebar ──
st.sidebar.image(
    "https://images.unsplash.com/photo-1708697458415-cc9a4cbd8510?w=300&auto=format&fit=crop&q=80",
    use_column_width=True
)
st.sidebar.markdown("### 🌿 PM Tracker")
st.sidebar.markdown("---")

selected_projects = st.sidebar.multiselect(
    "Projects",
    options=projects_df["Project"].tolist(),
    default=projects_df["Project"].tolist()
)
status_filter = st.sidebar.multiselect(
    "Status",
    options=["On Track", "At Risk", "Blocked"],
    default=["On Track", "At Risk", "Blocked"]
)
st.sidebar.markdown("---")
st.sidebar.caption("Built by Elizabeth Post")
st.sidebar.caption("elizabethpost.netlify.app")

# Apply filters
fp = projects_df[
    projects_df["Project"].isin(selected_projects) &
    projects_df["Status"].isin(status_filter)
].copy()

# ── Header ──
st.title("Project Health & Velocity Tracker")
today_str = datetime.now().strftime("%B %d, %Y")
st.markdown(f"*{len(fp)} active projects · {today_str}*")
st.markdown("---")

# ── KPIs ──
k1, k2, k3, k4, k5 = st.columns(5)
avg_h = round(fp["Health"].mean()) if len(fp) else 0
avg_c = round(fp["Completion"].mean()) if len(fp) else 0
k1.metric("Total Projects", len(fp))
k2.metric("On Track",       len(fp[fp["Status"] == "On Track"]))
k3.metric("At Risk",        len(fp[fp["Status"] == "At Risk"]))
k4.metric("Blocked",        len(fp[fp["Status"] == "Blocked"]))
k5.metric("Avg Health",     f"{avg_h}%")

st.markdown("---")

# ── Project Health Cards ──
st.subheader("Project Health Overview")

STATUS_COLOR = {"On Track": SAGE, "At Risk": AMBER, "Blocked": BLUSH}
STATUS_ICON  = {"On Track": "🟢", "At Risk": "🟡", "Blocked": "🔴"}

cols = st.columns(3)
for i, (_, row) in enumerate(fp.iterrows()):
    c = STATUS_COLOR.get(row["Status"], SAGE)
    with cols[i % 3]:
        st.markdown(f"""
        <div style="background:{WARM_WHITE};border:1px solid {BORDER};border-top:4px solid {c};
                    border-radius:10px;padding:18px;margin-bottom:16px;">
          <div style="font-size:11px;color:{TEXT_MID};text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:6px;">{row['Priority']} Priority</div>
          <div style="font-size:15px;font-weight:700;color:{TEXT};margin-bottom:2px;">{row['Project']}</div>
          <div style="font-size:12px;color:{TEXT_MID};margin-bottom:12px;">Owner: {row['Owner']} &nbsp;·&nbsp; {row['Team']} members</div>
          <div style="font-size:11px;color:{TEXT_MID};display:flex;justify-content:space-between;margin-bottom:4px;">
            <span>Completion</span><span>{row['Completion']}%</span>
          </div>
          <div style="background:#e8e0d8;border-radius:4px;height:6px;margin-bottom:14px;">
            <div style="background:{c};width:{row['Completion']}%;height:6px;border-radius:4px;"></div>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:26px;font-weight:700;color:{c};">{row['Health']}%</span>
            <span style="font-size:13px;color:{c};font-weight:600;">{STATUS_ICON.get(row['Status'],'')} {row['Status']}</span>
          </div>
          <div style="font-size:11px;color:#9a8878;margin-top:8px;">Due: {row['Due']}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Sprint Velocity ──
st.markdown("---")
st.subheader("Sprint Velocity")

v_left, v_right = st.columns([3, 1])

with v_left:
    proj_options = [p for p in selected_projects if p in velocity_df["Project"].unique()]
    if proj_options:
        chosen = st.selectbox("Select project", proj_options, key="vel_proj")
        pv = velocity_df[velocity_df["Project"] == chosen]

        fig_v = go.Figure()
        fig_v.add_bar(x=pv["Sprint"], y=pv["Planned"],   name="Planned",   marker_color=BORDER, opacity=0.8)
        fig_v.add_bar(x=pv["Sprint"], y=pv["Completed"], name="Completed", marker_color=SAGE)
        fig_v.add_scatter(x=pv["Sprint"], y=pv["Completed"], mode="lines+markers",
                          name="Trend", line=dict(color=EARTH, width=2, dash="dot"),
                          marker=dict(color=EARTH, size=7))
        fig_v.update_layout(
            barmode="overlay", paper_bgcolor=CREAM, plot_bgcolor=CREAM,
            font=dict(color=TEXT_MID, size=12), height=300,
            legend=dict(orientation="h", y=-0.2),
            margin=dict(l=0, r=0, t=10, b=0),
            yaxis=dict(title="Story Points", gridcolor="#ece6de"),
            xaxis=dict(title="Sprint")
        )
        st.plotly_chart(fig_v, use_container_width=True)

with v_right:
    if proj_options:
        avg_plan  = pv["Planned"].mean()
        avg_comp  = pv["Completed"].mean()
        variance  = (avg_comp - avg_plan) / avg_plan * 100
        last_eff  = pv.iloc[-1]["Completed"] / pv.iloc[-1]["Planned"] * 100
        st.metric("Avg Planned",          f"{avg_plan:.0f} pts")
        st.metric("Avg Completed",        f"{avg_comp:.0f} pts", delta=f"{variance:+.1f}% vs plan")
        st.metric("Last Sprint Efficiency", f"{last_eff:.0f}%")

# ── Milestones ──
st.markdown("---")
st.subheader("Milestone Tracker")

TODAY = pd.Timestamp("2025-07-10")
m = milestones_df[milestones_df["Project"].isin(selected_projects)].copy()
m["Due_dt"] = pd.to_datetime(m["Due"])
m["Overdue"] = (~m["Done"]) & (m["Due_dt"] < TODAY)
m["Status"]  = m.apply(lambda r: "✅ Done" if r["Done"] else ("🔴 Overdue" if r["Overdue"] else "⏳ Pending"), axis=1)
m["Due"]     = m["Due_dt"].dt.strftime("%b %d, %Y")

pct_done = round(m["Done"].mean() * 100) if len(m) else 0
overdue_ct = m["Overdue"].sum()

mc1, mc2, mc3 = st.columns(3)
mc1.metric("Total Milestones", len(m))
mc2.metric("Complete",         m["Done"].sum(),  delta=f"{pct_done}%")
mc3.metric("Overdue",          int(overdue_ct),  delta=None if overdue_ct == 0 else "needs attention")

st.dataframe(
    m[["Project", "Milestone", "Due", "Status"]],
    use_container_width=True,
    height=280,
    hide_index=True
)

# ── Risk Register ──
st.markdown("---")
st.subheader("Risk Register")

RISK_COLOR = {"Critical": BLUSH, "High": AMBER, "Medium": GOLD, "Low": SAGE_LIGHT}

r_left, r_right = st.columns([3, 1])
r_filtered = risks_df[risks_df["Project"].isin(selected_projects)]

with r_left:
    for _, row in r_filtered.iterrows():
        c = RISK_COLOR.get(row["Level"], SAGE)
        st.markdown(f"""
        <div style="background:{WARM_WHITE};border:1px solid {BORDER};border-left:4px solid {c};
                    border-radius:8px;padding:12px 16px;margin-bottom:10px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <span style="background:{c};color:#fff;font-size:11px;font-weight:700;
                         padding:2px 9px;border-radius:20px;">{row['Level']}</span>
            <span style="font-size:14px;font-weight:700;color:{TEXT};">{row['Risk']}</span>
          </div>
          <div style="font-size:12px;color:{TEXT_MID};">{row['Project']} · Owner: {row['Owner']}</div>
          <div style="font-size:12px;color:{TEXT_MID};margin-top:4px;">
            <em>Mitigation:</em> {row['Mitigation']}
          </div>
        </div>
        """, unsafe_allow_html=True)

with r_right:
    rc = r_filtered["Level"].value_counts().reindex(["Critical","High","Medium","Low"], fill_value=0).reset_index()
    rc.columns = ["Level", "Count"]
    risk_color_map = {"Critical": BLUSH, "High": AMBER, "Medium": GOLD, "Low": SAGE_LIGHT}
    fig_r = go.Figure()
    for _, row in rc.iterrows():
        fig_r.add_trace(go.Bar(
            x=[row["Count"]], y=[row["Level"]], orientation="h",
            name=row["Level"], marker_color=risk_color_map.get(row["Level"], SAGE),
            showlegend=False
        ))
    fig_r.update_layout(paper_bgcolor=CREAM, plot_bgcolor=CREAM,
                        font=dict(color=TEXT_MID), margin=dict(l=0,r=0,t=10,b=0),
                        height=240, xaxis_title="Count", yaxis_title="")
    st.plotly_chart(fig_r, use_container_width=True)

# ── Workload Balance ──
st.markdown("---")
st.subheader("Team Workload Balance")

w = workload_df[workload_df["Project"].isin(selected_projects)]

fig_w = go.Figure()
fig_w.add_bar(x=w["Member"], y=w["Active"],  name="Active",  marker_color=SAGE)
fig_w.add_bar(x=w["Member"], y=w["Blocked"], name="Blocked", marker_color=BLUSH)
fig_w.add_bar(x=w["Member"], y=w["Overdue"], name="Overdue", marker_color=EARTH)
fig_w.update_layout(
    barmode="stack", paper_bgcolor=CREAM, plot_bgcolor=CREAM,
    font=dict(color=TEXT_MID, size=12), height=320,
    legend=dict(orientation="h", y=-0.22),
    margin=dict(l=0, r=0, t=10, b=0),
    yaxis=dict(title="Tasks", gridcolor="#ece6de"),
    xaxis=dict(title="")
)
st.plotly_chart(fig_w, use_container_width=True)

overloaded = w[w["Active"] > 15]["Member"].tolist()
if overloaded:
    st.warning(f"Capacity alert: {', '.join(overloaded)} each have 15+ active tasks. Consider rebalancing.")

# ── Footer ──
st.markdown("---")
st.caption("Elizabeth Post · PM Operations Dashboard · elizabethpost.netlify.app")
