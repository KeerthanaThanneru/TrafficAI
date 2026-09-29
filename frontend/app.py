import streamlit as st
import pandas as pd
import random
import os
import joblib

st.set_page_config(page_title="TrafficAI Dashboard", layout="wide")
st.title("🚦 TrafficAI — Smart Traffic Control Dashboard")

junctions = [1, 2, 3, 4]  # matches Member 2's junction_id numbers

model_path = "models/congestion_model.pkl"
data_path = "data/traffic_data.csv"

using_real_model = os.path.exists(model_path) and os.path.exists(data_path)

if using_real_model:
    model = joblib.load(model_path)
    df = pd.read_csv(data_path)
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour  # extract hour from timestamp
    st.success("✅ Using real AI model")
else:
    st.warning("⚠️ Using dummy data — real model not found yet")
    vehicle_counts = [random.randint(10, 120) for _ in junctions]
    congestion_levels = [random.choice(["Low", "Medium", "High"]) for _ in junctions]

st.header("Live Traffic Status")
cols = st.columns(4)

for i, junction in enumerate(junctions):
    with cols[i]:
        if using_real_model:
            latest = df[df["junction_id"] == junction].iloc[-1]
            sample = latest[["vehicle_count", "avg_speed", "hour"]].values.reshape(1, -1)
            prediction = model.predict(sample)[0]
            st.metric(f"Junction {junction}", f'{latest["vehicle_count"]} vehicles')
            st.write(f"Congestion: **{prediction}**")
        else:
            st.metric(f"Junction {junction}", f"{vehicle_counts[i]} vehicles")
            st.write(f"Congestion: **{congestion_levels[i]}**")

st.header("Junction Statistics")
if using_real_model:
    st.line_chart(df.groupby("hour")["vehicle_count"].mean())
else:
    dummy_df = pd.DataFrame({"Junction": junctions, "Vehicle Count": vehicle_counts})
    st.bar_chart(dummy_df.set_index("Junction"))

st.header("🌱 Sustainability Metrics")
total_vehicles = df["vehicle_count"].sum() if using_real_model else sum(vehicle_counts)
fuel_saved = total_vehicles * 0.02
st.metric("Estimated Fuel Saved (liters/day)", round(fuel_saved, 2))