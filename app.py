import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Page Config
# ------------------------------------------------------------
st.set_page_config(
    page_title="Sustainable Formulation Optimizer",
    page_icon="🌿",
    layout="centered"
)

# ------------------------------------------------------------
# Title & Header
# ------------------------------------------------------------
st.title("🌿 Sustainable Moisturizer Formulation Optimizer")

st.write("""
This app is an **interactive companion tool** to the report 
*“Sustainable Reformulation of CeraVe Moisturizing Cream.”*

It demonstrates:
- Ingredient ratio adjustments  
- Sensory & stability predictions  
- Sustainability vs. cost trade-offs  
- ML-inspired optimisation loop  
""")

st.divider()

# ------------------------------------------------------------
# Sidebar Inputs
# ------------------------------------------------------------
st.sidebar.header("Adjust Sustainable Ingredient Ratios (%)")

shea = st.sidebar.slider("Shea Butter (occlusive)", 0.0, 25.0, 10.0)
squalane = st.sidebar.slider("Squalane (emollient)", 0.0, 15.0, 4.0)
lc = st.sidebar.slider("Liquid Crystal Emulsifier", 0.0, 10.0, 3.0)
gum = st.sidebar.slider("Gum Blend", 0.0, 2.0, 0.6)
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

def indicator(score):
    if score >= 7: return "🟢"
    if score >= 4: return "🟡"
    return "🔴"

# ------------------------------------------------------------
# Ingredient Breakdown (Pie Chart with Matplotlib)
# ------------------------------------------------------------
labels = ["Shea Butter", "Squalane", "LC Emulsifier", "Gum Blend", "GLDA", "Preservatives"]
values = [shea, squalane, lc, gum, glda, pres]

fig1, ax1 = plt.subplots()
ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')

st.subheader("🧴 Ingredient Composition")
st.pyplot(fig1)

# ------------------------------------------------------------
# Radar Chart (Performance)
# ------------------------------------------------------------
metrics = ["Sensory", "Stability", "Sustainability", "Cost"]
scores = [sensory, stability, sustainability, cost]

# Repeat first value to close radar chart loop
scores_radar = scores + scores[:1]
angles = np.linspace(0, 2*np.pi, len(scores_radar))

fig2, ax2 = plt.subplots(subplot_kw={'projection': 'polar'})
ax2.plot(angles, scores_radar, marker='o')
ax2.fill(angles, scores_radar, alpha=0.25)
ax2.set_xticks(angles[:-1])
ax2.set_xticklabels(metrics)
ax2.set_ylim(0, 10)

st.subheader("📈 Formulation Performance Radar Chart")
st.pyplot(fig2)

# ------------------------------------------------------------
# Numeric Metrics
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
# Interpretation
# ------------------------------------------------------------
st.header("📘 Interpretation")

st.markdown("""
### 🌱 Sustainability  
PEG-free LC emulsifiers and GLDA improve environmental performance.

### ✨ Sensory Slip  
Squalane enhances glide; gums increase tack.

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
