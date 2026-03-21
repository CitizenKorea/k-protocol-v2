import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. 절대 물리 상수 및 단위 변환 (조작 없음)
# ==========================================
# SI 표준 중력 가속도 (m/s^2)
g_STANDARD = 9.80665 

# 물리 단위 변환: 1 Gal = 0.01 m/s^2, 1 mGal = 10^-5 m/s^2
# 따라서 m/s^2 에 100,000 을 곱해야 순수한 mGal 값이 나옵니다.
MS2_TO_MGAL = 100000.0 

# ==========================================
# 2. 관측 데이터 (Raw Data)
# ==========================================
# 전 세계 표준 연구소들의 실제 G 측정 불일치 데이터 (단위: ppm)
# 논문 [Technical Report Vol. 2]의 Table 1 원본 수치
lab_pairs = {
    "BIPM (France) vs. HUST (China)": {"G_err_ppm": 145},
    "NIST (USA) vs. BIPM (France)": {"G_err_ppm": 87},
    "JILA (USA) vs. UZH (Swiss)": {"G_err_ppm": 45}
}

# ==========================================
# 3. UI 및 앱 구조 설정
# ==========================================
st.set_page_config(page_title="K-PROTOCOL 2: Big G Resolver", layout="wide")
st.title("🛰️ K-PROTOCOL 2: Big G Resolver")
st.markdown("### 체적 메트릭 왜곡($S_{loc}^3$)을 통한 중력 상수(G) 불일치 해석 (투명성 보고서)")
st.divider()

# --- Section A: 논문 요약 및 데이터 출처 ---
with st.expander("📚 1. 이론적 배경 및 데이터 출처 (Methodology & Sources)", expanded=True):
    st.markdown("""
    **[이론적 배경: Volumetric Metric Distortion]**
    본 엔진은 [Technical Report Vol. 2]에 명시된 바와 같이, 중력 상수 $G$의 차원 $[L^3/MT^2]$ 중 **체적($L^3$)**에 주목합니다. 
    미세한 국소 중력 이상($\Delta g_{loc}$)이 시공간을 기하학적으로 왜곡시킬 때($S_{loc}$), 이 왜곡은 $G$ 측정 시 체적 차원에서 **3배 증폭**되어 나타납니다.
    따라서 연구소 간의 측정 오차는 장비의 문제가 아니라 기하학적 필연입니다.
    
    * **적용 공식**: $\frac{\Delta G}{G} \\approx 3 \\times \frac{\Delta g_{loc}}{g_{loc}}$

    **[데이터 출처 (Data Sources)]**
    * **G 측정 불일치 데이터 (Observed $\Delta G$)**: 전 세계 주요 표준 연구소(BIPM, NIST, HUST 등)에서 과거 발표한 Torsion Balance 기반 고정밀 $G$ 측정 논문들의 상호 오차율(ppm).
    * **검증용 지질 중력 데이터 (Gravity Anomaly)**: 향후 ICGEM (International Centre for Global Earth Models)의 EGM2008 등 초정밀 전 지구 중력장 모델을 통해 해당 연구소 좌표의 실제 Bouguer/Free-air anomaly 수치를 수집하여 본 엔진의 예측값과 대조할 예정입니다.
    """)

# --- Section B: 순수 수학 엔진 (가공 없음) ---
st.markdown("### ⚙️ 기하학적 중력 이상 예측 엔진 (Raw Calculation)")
selection = st.selectbox("분석할 연구소 쌍(Lab Pairing)을 선택하십시오:", list(lab_pairs.keys()))
data = lab_pairs[selection]

# 엄밀한 물리 계산 (가공/보정 일절 없음)
err_ratio = data['G_err_ppm'] / 1e6 # ppm을 실수 비율로 변환
delta_g_ms2 = g_STANDARD * (1/3) * err_ratio # 순수 공식 적용 (단위: m/s^2)
predicted_dg_mgal = delta_g_ms2 * MS2_TO_MGAL # 단위 변환 (m/s^2 -> mGal)

col1, col2 = st.columns(2)
with col1:
    st.info("📊 **실제 관측된 G 측정 불일치 (Input)**")
    st.metric(label="Observed G Discrepancy", value=f"{data['G_err_ppm']} ppm")
with col2:
    st.success("🎯 **도출된 필요 국소 중력 이상 (Pure Output)**")
    st.metric(label="Predicted Local Gravity Anomaly (Δg)", value=f"{predicted_dg_mgal:.4f} mGal")

st.caption("위 도출값은 어떠한 인위적 곡선 맞춤(Curve-fitting)이나 조작이 포함되지 않은, 순수 물리 공식과 SI 단위 변환에 의한 100% 원시 계산값(Raw Calculated Value)입니다.")
st.divider()

# --- Section C: 결과 시각화 ---
st.markdown("### 📈 차원별 왜곡 증폭률 시각화")
distortion = pd.DataFrame({
    '차원 (Dimension)': ['길이 Length (L¹)', '면적 Area (L²)', '체적 Volume (L³: G 상수)'],
    '왜곡 증폭률 (ppm)': [data['G_err_ppm']/3, (data['G_err_ppm']/3)*2, data['G_err_ppm']]
})
fig = px.bar(distortion, x='차원 (Dimension)', y='왜곡 증폭률 (ppm)', color='차원 (Dimension)',
             title=f"국소 중력 왜곡이 {selection} 간의 G 측정에 미친 체적 증폭 효과")
st.plotly_chart(fig, use_container_width=True)
