import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------------------
#  Title & Header
# ------------------------------------------------------------
st.set_page_config(page_title="Sustainable Formulation Optimizer", page_icon="🌿")

st.title("🌿 Sustainable Moisturizer Formulation Optimizer")
st.write("""
This Streamlit app is an **interactive companion tool** to the report 
*“Sustainable Reformulation of CeraVe Moisturizing Cream.”*

It demonstrates the computational formulation workflow, including:

- Ingredient ratio adjustments  
- Sensory & stability predictions  
- Sustainability impact  
- Cost implications  
- The ML-inspired optimisation loop (Figure 4)

All predictions are modelled based on the scientific logic in the report.
""")

st.divider()

# ------------------------------------------------------------
# Sidebar: Ingredient Sliders
# ------------------------------------------------------------
st.sidebar.header("Adjust Sustainable Ingredient Ratios (%)")

shea = st.sidebar.slider("Shea Butter (occlusive)", 0.0, 25.0, 10.0)
squalane = st.sidebar.slider("Squalane (emollient)", 0.0, 15.0, 4.0)
lc = st.sidebar.slider("Liquid Crystal Emulsifier (Olivem-type)", 0.0, 10.0, 3.0)
gum = st.sidebar.slider("Xanthan + Sclerotium Gum Blend", 0.0, 2.0, 0.6)
glda = st.sidebar.slider("GLDA (biodegradable chelator)", 0.0, 1.0, 0.3)
pres = st.sidebar.slider("Natural Preservative System", 0.0, 2.0, 1.0)

total = shea + squalane + lc + gum + glda + pres
st.sidebar.write(f"### Total Active Chassis: **{total:.1f}%**")

# ------------------------------------------------------------
# Model Calculations
# ------------------------------------------------------------
def clamp(x): 
    return max(0, min(10, x))

# Sensory Slip Prediction
sensory_raw = (0.5 * squalane + 0.2 * lc - 0.3 * gum)

# Sustainability Score
sustain_raw = (0.3 * lc + 0.3 * glda + 0.3 * pres - 0.1 * shea)

# Stability Score
stability_raw = (0.5 * lc + 0.4 * gum - 0.1 * shea)

# Cost Score
cost_raw = (0.4 * squalane + 0.3 * lc + 0.2 * gum)

# Clamp values
sensory = clamp(sensory_raw)
sustainability = clamp(sustain_raw)
stability = clamp(stability_raw)
cost = clamp(cost_raw)

# ------------------------------------------------------------
# Traffic-light indicators
# ------------------------------------------------------------
def indicator(score):
    if score >= 7:
        return "🟢"
    elif score >= 4:
        return "🟡"
    else:
        return "🔴"

st.write(f"**Sensory Profile:** {indicator(sensory)}")
st.write(f"**Stability:** {indicator(stability)}")
st.write(f"**Sustainability:** {indicator(sustainability)}")
st.write(f"**Cost Impact:** {indicator(cost)}")

# ------------------------------------------------------------
# Pie Chart (Ingredient Breakdown)
# ------------------------------------------------------------
data = {
    "Ingredient": ["Shea Butter", "Squalane", "LC Emulsifier", "Gum Blend", "GLDA", "Preservatives"],
    "Percentage": [shea, squalane, lc, gum, glda, pres]
}
df = pd.DataFrame(data)

fig_pie = px.pie(df, names="Ingredient", values="Percentage",
                 title="🧴 Ingredient Composition", hole=0.4)

st.subheader("🧴 Ingredient Breakdown")
st.plotly_chart(fig_pie, use_container_width=True)

# ------------------------------------------------------------
# Radar Chart (Performance Profile)
# ------------------------------------------------------------
categories = ['Sensory Slip', 'Stability', 'Sustainability', 'Cost Impact']
values = [sensory, stability, sustainability, cost]

fig = go.Figure(data=go.Scatterpolar(
    r=values + [values[0]],
    theta=categories + [categories[0]],
    fill='toself',
    name='Formulation Profile'
))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0,10])),
    showlegend=False
)

st.subheader("📈 Formulation Performance Radar Chart")
st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# Explanation Section
# ------------------------------------------------------------
st.divider()
st.header("📘 Interpretation of Scores")

st.markdown("""
### 🌱 Sustainability  
- PEG-free LC emulsifiers increase sustainability  
- GLDA reduces ecological persistence  
- Natural preservatives are environmentally safer  

### ✨ Sensory Slip  
- Squalane improves slip  
- Gums increase drag/tack  
- Balances richness and glide  

### 🧪 Stability  
- LC emulsifiers + gums create lamellar phases  
- High shea levels disrupt stability  
- Matches the MVE vs LC discussion  

### 💰 Cost  
- Squalane and LC emulsifiers contribute most to cost  
- Gums and GLDA are moderately priced  
""")

# ------------------------------------------------------------
# Custom Background Color
# ------------------------------------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f7f7f7;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.info("""
This tool demonstrates the **ML prediction loop** described in the report:

1. Adjust formulation inputs  
2. Predict performance  
3. Iterate the design  
4. Move toward an optimized sustainable formula  

A practical example of computational formulation science.
""")
