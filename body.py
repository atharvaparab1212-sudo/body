import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---- Page Config ----
st.set_page_config(page_title="Fitness App Growth Model", layout="wide")

# ---- Custom Styling ----
page_bg = """
<style>

/* ---- Main App Background (light gym look) ---- */
.stApp {
    background-image: 
        linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
        url("https://images.unsplash.com/photo-1554284126-aa88f22d8b74");
    background-size: cover;
    background-attachment: fixed;
}

/* ---- Sidebar Black ---- */
section[data-testid="stSidebar"] {
    background-color: black !important;
}

/* Sidebar text white */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ---- Main text dark ---- */
h1, h2, h3, h4, p, label, div {
    color: black !important;
}

</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ---- Title ----
st.title("🏋️ Fitness App User Growth Simulator")

# ---- Sidebar Controls ----
st.sidebar.header("⚙️ Model Parameters")

days = st.sidebar.slider("Simulation Days", 30, 365, 120)
initial_users = st.sidebar.number_input("Initial Users", value=1000)
growth_rate = st.sidebar.slider("Daily Growth Rate (%)", 0.0, 10.0, 2.0) / 100
retention_rate = st.sidebar.slider("Retention Rate (%)", 50.0, 100.0, 85.0) / 100
churn_rate = st.sidebar.slider("Churn Rate (%)", 0.0, 50.0, 10.0) / 100

# ---- Retention Strategy ----
st.sidebar.header("💡 Retention Strategies")

strategy = st.sidebar.selectbox(
    "Choose Strategy",
    ["None", "Gamification", "Personal Coaching", "Push Notifications"]
)

strategy_boost = {
    "None": 0.0,
    "Gamification": 0.05,
    "Personal Coaching": 0.08,
    "Push Notifications": 0.03
}

retention_rate += strategy_boost[strategy]

# ---- Simulation ----
users = []
new_users_list = []
active_users_list = []
dropouts_list = []

current_users = initial_users

for day in range(days):
    new_users = current_users * growth_rate
    retained_users = current_users * retention_rate
    dropouts = current_users * churn_rate

    current_users = retained_users + new_users - dropouts

    users.append(current_users)
    new_users_list.append(new_users)
    active_users_list.append(retained_users)
    dropouts_list.append(dropouts)

# ---- DataFrame ----
df = pd.DataFrame({
    "Day": np.arange(1, days + 1),
    "Total Users": users,
    "New Users": new_users_list,
    "Active Users": active_users_list,
    "Dropouts": dropouts_list
})

# ---- Plot ----
st.subheader("📊 User Growth Over Time")

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(df["Day"], df["Total Users"], label="Total Users", linewidth=3)
ax.plot(df["Day"], df["Active Users"], label="Active Users", linestyle="--")
ax.plot(df["Day"], df["New Users"], label="New Users", linestyle=":")
ax.plot(df["Day"], df["Dropouts"], label="Dropouts", linestyle="-.")

ax.set_xlabel("Days")
ax.set_ylabel("Users")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# ---- Insights ----
st.subheader("📈 Insights")

st.write(f"**Final User Count:** {int(users[-1])}")
st.write(f"**Retention Strategy Applied:** {strategy}")
st.write(f"**Effective Retention Rate:** {round(retention_rate*100,2)}%")

# ---- Table ----
st.subheader("📋 Data Preview")
st.dataframe(df.tail(10))
