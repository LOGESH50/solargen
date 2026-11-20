import streamlit as st
import math
import streamlit . components . v1 as components

st.set_page_config(
    page_title="SolarGen Dashboard",
    page_icon="☀️",
    layout="wide"
)

# ---------------- DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #10121d;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3, p, label {
    color: white !important;
}
[data-testid="stMetric"] {
    background: #202333;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #34384c;
}
[data-testid="stMetricLabel"] {
    color: #b8bfd0 !important;
}
[data-testid="stMetricValue"] {
    color: #ffbd38 !important;
}
.dashboard-card {
    background: #202333;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #34384c;
    margin-bottom: 15px;
}
.bar-chart {
    display: flex;
    align-items: end;
    justify-content: space-around;
    height: 240px;
    padding: 15px 5px 0;
    border-bottom: 1px solid #62677a;
    background: repeating-linear-gradient(
        to bottom,
        transparent 0px,
        transparent 58px,
        #383c4c 59px,
        transparent 60px
    );
}
.bar-wrap {
    height: 100%;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: end;
    align-items: center;
    gap: 7px;
    min-width: 0;
}
.bar {
    width: 55%;
    max-width: 35px;
    background: linear-gradient(#ffcf47, #f18b18);
    border-radius: 5px 5px 0 0;
    min-height: 3px;
}
.bar-label {
    font-size: 11px;
    color: #c2c6d3;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("☀️ SolarGen")
st.caption("SOLAR ENERGY MONITORING & ANALYSIS SYSTEM")

st.divider()

# ---------------- INPUTS ----------------

st.sidebar.title("⚙️ Solar Configuration")

panels = st.sidebar.number_input(
    "Number of solar panels", 1, 1000, 6
)

watt = st.sidebar.number_input(
    "Panel capacity (Watts)", 100, 1000, 550
)

sun_hours = st.sidebar.slider(
    "Peak sunlight hours", 1.0, 10.0, 5.0
)

efficiency = st.sidebar.slider(
    "System efficiency (%)", 50, 100, 80
)

sunlight_level = st.sidebar.slider(
    "Current sunlight level (%)", 0, 100, 65
)

days = st.sidebar.number_input(
    "Days since installation", 1, 10000, 30
)

# ---------------- CALCULATIONS ----------------

capacity = panels * watt / 1000

daily_energy = capacity * sun_hours * efficiency / 100

monthly_energy = daily_energy * 30

yearly_energy = daily_energy * 365

lifetime_energy = daily_energy * days

current_output = capacity * efficiency / 100 * sunlight_level / 100

peak_output = capacity * efficiency / 100

# ---------------- PERFORMANCE DASHBOARD ----------------

st.header("📊 Performance Dashboard")

c1, c2, c3 = st.columns(3)

c1.metric("System Capacity", f"{capacity:.2f} kW")
c2.metric("Daily Energy", f"{daily_energy:.2f} kWh")
c3.metric("Monthly Energy", f"{monthly_energy:.2f} kWh")

c4, c5, c6 = st.columns(3)

c4.metric("Estimated Current Output", f"{current_output:.2f} kW")
c5.metric("Estimated Peak Output", f"{peak_output:.2f} kW")
c6.metric("Lifetime Energy", f"{lifetime_energy:.2f} kWh")

st.divider()

# ---------------- ENERGY PRODUCTION GRAPH ----------------

st.header("📈 Energy Production Analysis")

period = st.selectbox(
    "Select graph period",
    ["Hourly", "Daily", "Monthly"]
)

if period == "Hourly":
    labels = [
        "6AM", "7AM", "8AM", "9AM",
        "10AM", "11AM", "12PM", "1PM",
        "2PM", "3PM", "4PM", "5PM"
    ]

    weights = [
        0.05, 0.15, 0.30, 0.50,
        0.70, 0.85, 1.00, 0.95,
        0.80, 0.65, 0.45, 0.25
    ]

    values = [
        daily_energy * w / sum(weights)
        for w in weights
    ]

elif period == "Daily":
    labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    weights = [0.8, 0.9, 1.0, 0.85, 0.95, 0.75, 0.9]

    values = [
        daily_energy * w for w in weights
    ]

else:
    labels = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    weights = [
        0.85, 0.90, 1.0, 1.05, 1.1, 0.85,
        0.65, 0.70, 0.75, 0.85, 0.90, 0.85
    ]

    values = [
        daily_energy * 30 * w for w in weights
    ]

maximum = max(values) if max(values) > 0 else 1

bars = ""

for label, value in zip(labels, values):
    height = max(2, value / maximum * 100)

    bars += f"""
    <div class="bar-wrap">
        <div class="bar" style="height:{height:.1f}%"></div>
        <span class="bar-label">{label}</span>
    </div>
    """

components.html(f"""
<style>
body {{
    background-color: #202333;
    color: white;
    font-family: Arial;
}}
.chart {{
    display: flex;
    align-items: end;
    justify-content: space-around;
    height: 230px;
    border-bottom: 1px solid #777;
    gap: 8px;
}}
.item {{
    flex: 1;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: end;
    align-items: center;
}}
.bar {{
    width: 65%;
    background: linear-gradient(#ffcf47, #f18b18);
    border-radius: 5px 5px 0 0;
}}
small {{ color: white; font-size: 11px; }}
</style>

<h3>Energy Generation - {period}</h3>
<div class="chart">
{''.join(
    f'<div class="item"><div class="bar" style="height:{max(2, v/maximum*100):.1f}%"></div><small>{label}</small></div>'
    for label, v in zip(labels, values)
)}
</div>
""", height=310)

# ---------------- PRODUCTION SUMMARY ----------------

st.header("⚡ Production Summary")

if period == "Hourly":
    total = sum(values)
elif period == "Daily":
    total = sum(values)
else:
    total = sum(values)

st.metric(
    f"Total Estimated Production ({period})",
    f"{total:.2f} kWh"
)

st.divider()

st.info(
    "SolarGen currently displays calculated estimates, "
    "not live inverter or sensor readings. Actual generation "
    "depends on weather, shading, location and panel orientation."
)

st.success("SolarGen Dashboard is running successfully! ☀️")