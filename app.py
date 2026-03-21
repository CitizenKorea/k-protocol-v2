import streamlit as st
import pandas as pd
import plotly.express as px

# K-PROTOCOL 2 핵심 상수
G_STANDARD = 6.67430e-11 
g_STANDARD = 9.80665

# 실험실 데이터 (Table 1 기반)
lab_pairs = {
    "BIPM (France) vs. HUST (China)": {"G_err": 145, "g_req": 47},
    "NIST (USA) vs. BIPM (France)": {"G_err": 87, "g_req": 29},
    "JILA (USA) vs. UZH (Swiss)": {"G_err": 45, "g_req": 15}
}

st.title("🛰️ K-PROTOCOL 2: Big G Resolver")
st.markdown("### Resolving Global G Discrepancies via Volumetric Distortion ($S_{loc}^3$)")

selection = st.selectbox("분석할 연구소 쌍을 선택하세요:", list(lab_pairs.keys()))
data = lab_pairs[selection]

col1, col2 = st.columns(2)
with col1:
    st.metric("관측된 G 불일치", f"{data['G_err']} ppm")
with col2:
    # 수식 적용: Δg/g ≈ 1/3 * ΔG/G
    predicted_dg = (data['G_err'] / 1e6 / 3) * g_STANDARD * 1000 
    st.metric("예측된 국소 중력 이상 (Δg)", f"{predicted_dg:.2f} mGal")

st.info("실제 지질학적 중력 이상 데이터와 일치 여부를 검증하십시오.")

# 시각화
st.subheader("📊 차원별 메트릭 왜곡 증폭 (L³ Amplification)")
distortion = pd.DataFrame({
    'Dimension': ['Length (L¹)', 'Area (L²)', 'Volume (L³: G-Constant)'],
    'Effect (%)': [data['G_err']/3, (data['G_err']/3)*2, data['G_err']]
})
fig = px.bar(distortion, x='Dimension', y='Effect (%)', color='Dimension')
st.plotly_chart(fig)
