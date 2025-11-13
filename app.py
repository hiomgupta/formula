import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------------------
#  Page Config
# ------------------------------------------------------------
st.set_page_config(
    page_title="Sustainable Formulation Optimizer",
    page_icon="🌿",
    layout="centered"
)

# ------------------------------------------------------------
#  Title & Header
# ------------------------------------------------------------
st.title("🌿 Sustainable Moisturizer Formulation Optimizer")

st.write("""
This app is an **interactive companion tool** to the report 
*“Sustainable Reformulation of CeraVe Moisturizing Cream.”*

It demonstrates computational formulation principles:
- Ingredient ratio adjustments  
- Sensory & stability predictions  
- Sustainability impact  
- Cost implications  
- ML-inspired optimisation loop  

(All predictions follow the logic described in the report.)
""")

st.divider()

# ------------------------------------------------------------
# Sidebar Inputs
# ------------------------------------------------------------
st.sidebar.header("Adjust Sustainable Ingredient Ratios (%)")

shea = st.sidebar.slider("Shea Butter (occlusive)", 0.0, 25.0, 10.0)
squalane = st.sidebar.slider("Squalane (emollient)", 0.0, 15.0, 4.0)
lc = st.sidebar.slider("Liquid Crystal Emulsifier", 0.0, 10.0, 3.0)
gum = st.sidebar.slider("Gum Blend (Xanthan/Sclerotium)", 0.0, 2.0, 0.6)
glda = st.sidebar.slider("GLDA (chelating agent)", 0.0, 1.0, 0.3)
pres = st.sidebar.slider("Natural Preservative System", 0.0, 2.0, 1.0)

total = shea + squalane + lc + gum + glda + pres
st.sidebar.markdown(f"### Total: **{total:.1f}%**")

# ------------------------------------------------------------
# Prediction Logic
# ------------------------------------------------------------
def clamp(x): 
    return max(0, min(10, x))

sensory = clamp(0.5*squalane + 0.2*lc - 0.3*gum)
sustainability = clamp(0.3*lc + 0.3*glda + 0.3*pres - 0.1*shea)
stability = clamp(0.5*lc + 0.4*gum - 0.1*shea)
cost = clamp(0.4*squalane + 0.3*lc + 0.2*gum)

# Traffic Light Indicators
def indicator(score):
    if score >= 7: return "🟢"
    if score >= 4: return "🟡"
    return "🔴"

# ------------------------------------------------------------
# Ingredient Breakdown (Pie Chart)
# ------------------------------------------------------------
df = pd.DataFrame({
    "Ingredient": ["Shea Butter", "Squalane", "LC Emulsifier", "Gum Blend", "GLDA", "Preservatives"],
    "Percentage": [shea, squalane, lc, gum, glda, pres]
})

fig_pie = px.pie(df, names="Ingredient", values="Percentage",
                 title="🧴 Ingredient Composition", hole=0.4)

st.subheader("🧴 Ingredient Breakdown")
st.plotly_chart(fig_pie, use_container_width=True)

# ------------------------------------------------------------
# Radar Chart (Performance)
# ------------------------------------------------------------
categories = ['Sensory Slip', 'Stability', 'Sustainability', 'Cost Impact']
values = [sensory, stability, sustainability, cost]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=values + [values[0]],
    theta=categories + [categories[0]],
    fill='toself'
))

fig_radar.update_layout(
    title="📈 Formulation Performance Radar Chart",
    polar=dict(radialaxis=dict(visible=True, range=[0,10])),
    showlegend=False
)

st.plotly_chart(fig_radar, use_container_width=True)

# ------------------------------------------------------------
# Numerical Performance Metrics
# ------------------------------------------------------------
st.header("📊 Performance Metrics")

col1, col2 = st.columns(2)

with col1:
    st.metric("✨ Sensory Slip", f"{sensory:.1f}/10")
    st.write(f"Status: {indicator(sensory)}")

with col2:
    st.metric("🧪 Stability", f"{stability:.1f}/10")
    st.write(f"Status: {indicator(stability)}")

col3, col4 = st.columns(2)

with col3:
    st.metric("🌱 Sustainability", f"{sustainability:.1f}/10")
    st.write(f"Status: {indicator(sustainability)}")

with col4:
    st.metric("💰 Cost Impact", f"{cost:.1f}/10")
    st.write(f"Status: {indicator(cost)}")

st.divider()

# ------------------------------------------------------------
# Explanation Section
# ------------------------------------------------------------
st.header("📘 Interpretation")

st.markdown("""
### 🌱 Sustainability  
PEG-free LC emulsifiers and GLDA improve environmental performance.

### ✨ Sensory Slip  
Squalane enhances slip; gums increase tack.

### 🧪 Stability  
Lamellar LC structures + gums increase stability; excess shea reduces it.

### 💰 Cost  
Squalane and LC emulsifiers contribute the most to cost.
""")

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.info("""
This app demonstrates the ML-inspired optimisation loop:
1. Adjust ingredients  
2. Predict outcomes  
3. Iterate  
4. Move toward an optimized sustainable formula  
""")

