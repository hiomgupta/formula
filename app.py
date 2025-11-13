import streamlit as st

# ------------------------------------------------------------
#  Title & Header
# ------------------------------------------------------------
st.set_page_config(page_title="Sustainable Formulation Optimizer", page_icon="🌿")

st.title("🌿 Sustainable Moisturizer Formulation Optimizer")
st.write("""
This Streamlit app is an **interactive companion tool** to the report 
*“Sustainable Reformulation of CeraVe Moisturizing Cream.”*

It demonstrates the **computational formulation workflow** discussed in the report, 
including:

- Ingredient ratio adjustments  
- Sensory & stability predictions  
- Sustainability impact  
- Cost implications  
- The ML-inspired optimisation loop (Figure 4)

All predictions are **modelled based on the scientific logic in the report**.
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
# Model Calculations (Designed to Match Your Report)
# ------------------------------------------------------------

# Sensory Slip Prediction (based on emollients)
sensory = (
    0.5 * squalane +   # Squalane improves slip
    0.2 * lc -         # LC adds some creaminess
    0.3 * gum          # gums increase tackiness
)

# Sustainability Score
sustainability = (
    0.3 * lc +        # LC are PEG-free & sustainable
    0.3 * glda +      # biodegradable chelator
    0.3 * pres -      # mild preservatives are good
    0.1 * shea        # shea has moderate sustainability impact
)

# Stability Score (LC + gum build structure)
stability = (
    0.5 * lc +
    0.4 * gum -
    0.1 * shea        # heavy oils destabilize LC systems
)

# Cost Score (Squalane & LC are expensive)
cost = (
    0.4 * squalane +
    0.3 * lc +
    0.2 * gum
)

# Clamp all scores between 0 and 10
def clamp(x): return max(0, min(10, x))
sensory = clamp(sensory)
sustainability = clamp(sustainability)
stability = clamp(stability)
cost = clamp(cost)

# ------------------------------------------------------------
# Results Display
# ------------------------------------------------------------
st.header("📊 Predicted Formulation Performance")

col1, col2 = st.columns(2)

with col1:
    st.metric("✨ Sensory Slip Score", f"{sensory:.1f} / 10")
    st.metric("🧪 Predicted Stability", f"{stability:.1f} / 10")

with col2:
    st.metric("🌱 Sustainability Score", f"{sustainability:.1f} / 10")
    st.metric("💰 Cost Impact", f"{cost:.1f} / 10")

st.divider()

# ------------------------------------------------------------
# Explanation Section (Links to Your Report)
# ------------------------------------------------------------
st.header("📘 How These Predictions Relate to the Report")

st.markdown("""
### 🌱 Sustainability  
- Driven by **PEG-free** LC emulsifiers  
- **GLDA** improves biodegradability  
- Natural preservatives reduce environmental persistence  

### ✨ Sensory Slip  
- Squalane contributes strong slip  
- Gums reduce slip (tackiness)  
- Matches the sensory discussion in the “Trade-offs” section  

### 🧪 Stability  
- LC emulsifiers + gums provide lamellar structure  
- Shea butter destabilizes at high concentrations  
- Directly connected to the **MVE vs LC** discussion  

### 💰 Cost  
- Squalane and LC emulsifiers are high-cost ingredients  
- Gum blends moderately increase cost  
- Reflects cost considerations in the “Scale-Up” section  
""")

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.info("""
This tool demonstrates the **ML prediction loop** described in the report:
1. Adjust ingredients  
2. Predict outcomes  
3. Iterate  
4. Converge toward an optimized sustainable formula  

It shows how computational thinking can support **green formulation science**.
""")
