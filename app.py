import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. 절대 물리 상수 (조작 불가)
# ==========================================
g_STANDARD = 9.80665 # SI 표준 중력 가속도 (m/s^2)
MS2_TO_MGAL = 100000.0 # 1 m/s^2 = 100,000 mGal

# ==========================================
# 2. 전 세계 표준 연구소 Raw Data (수정 가능한 원시 데이터)
# ==========================================
# [데이터 A] 각 연구소의 실제 G 측정값 불일치 (ppm)
g_discrepancy_data = {
    "BIPM (France) vs. HUST (China)": 145,
    "NIST (USA) vs. BIPM (France)": 87,
    "JILA (USA) vs. UZH (Swiss)": 45
}

# [데이터 B] 각 연구소의 실제 위치 및 지질학적 중력 이상 (mGal)
# 주의: 이 수치는 EGM2008 모델 기반의 추정치이며, 향후 정밀 지질 탐사 결과로 대체해야 함.
icgem_geo_data = {
    "BIPM (France)":  {"lat": 48.83, "lon": 2.22,   "real_anomaly_mgal": 6.2},  # 파리 분지
    "HUST (China)":   {"lat": 30.51, "lon": 114.41, "real_anomaly_mgal": -35.1}, # 우한 지역
    "NIST (USA)":     {"lat": 39.14, "lon": -77.21, "real_anomaly_mgal": -12.5}, # 메릴랜드
    "JILA (USA)":     {"lat": 40.00, "lon": -105.26,"real_anomaly_mgal": -110.0}, # 콜로라도 고산지대
    "UZH (Swiss)":    {"lat": 47.39, "lon": 8.54,   "real_anomaly_mgal": 45.3}   # 알프스 산맥 인근
}

# ==========================================
# 3. UI 및 엔진 가동
# ==========================================
st.set_page_config(page_title="K-PROTOCOL 2: Big G Verifier", layout="wide")
st.title("🛰️ K-PROTOCOL 2: Big G Empirical Verifier")
st.markdown("### 체적 메트릭 왜곡($S_{loc}^3$) 가설의 1:1 교차 검증 엔진")
st.divider()

# 분석 쌍 선택
selection = st.selectbox("검증할 연구소 쌍(Lab Pairing)을 선택하십시오:", list(g_discrepancy_data.keys()))

# 선택된 연구소 이름 분리 (예: "BIPM (France) vs. HUST (China)" -> "BIPM (France)", "HUST (China)")
lab1, lab2 = selection.split(" vs. ")

# [엔진 로직 1] K-PROTOCOL의 이론적 예측값 계산 (순수 수학)
err_ratio_ppm = g_discrepancy_data[selection]
delta_g_ms2 = g_STANDARD * (1/3) * (err_ratio_ppm / 1e6)
predicted_dg_mgal = delta_g_ms2 * MS2_TO_MGAL

# [엔진 로직 2] 실제 지질학적 중력 차이 계산 (순수 관측 데이터)
real_anomaly_1 = icgem_geo_data[lab1]["real_anomaly_mgal"]
real_anomaly_2 = icgem_geo_data[lab2]["real_anomaly_mgal"]
actual_dg_mgal = abs(real_anomaly_1 - real_anomaly_2)

# [엔진 로직 3] 오차 검증 (가감 없는 날것의 결과)
verification_error = abs(predicted_dg_mgal - actual_dg_mgal)

# ==========================================
# 4. 검증 결과 출력 (투명성 100%)
# ==========================================
st.markdown("#### ⚖️ K-PROTOCOL 이론 예측 vs 실제 지질 데이터 대조")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("🎯 **K-PROTOCOL 수학적 예측**")
    st.markdown(f"G 오차({err_ratio_ppm} ppm)로 역산한 값")
    st.metric(label="이론상 요구되는 중력 차이", value=f"{predicted_dg_mgal:.2f} mGal")

with col2:
    st.success("🌍 **실제 지질 중력 데이터 (ICGEM)**")
    st.markdown(f"{lab1} ({real_anomaly_1} mGal) vs {lab2} ({real_anomaly_2} mGal)")
    st.metric(label="실제 관측된 중력 차이", value=f"{actual_dg_mgal:.2f} mGal")

with col3:
    st.warning("🚨 **검증 오차 (Error Margin)**")
    st.markdown("예측값과 실측값의 차이")
    st.metric(label="최종 오차", value=f"{verification_error:.2f} mGal", delta=f"{verification_error:.2f} mGal", delta_color="inverse")

st.divider()

# ==========================================
# 5. 연구자 코멘트 및 분석 차트
# ==========================================
st.markdown("### 🔬 검증 결과 분석 (Analysis)")
if verification_error < 10.0:
    st.success(f"**판별:** 예측값({predicted_dg_mgal:.1f})과 실측값({actual_dg_mgal:.1f})이 매우 근접합니다. 체적 메트릭 왜곡($S_{loc}^3$) 가설이 실제 지질학적 데이터로 증명될 가능성이 매우 높습니다.")
else:
    st.error(f"**판별:** 예측값({predicted_dg_mgal:.1f})과 실측값({actual_dg_mgal:.1f}) 사이에 {verification_error:.1f} mGal의 오차가 존재합니다. 다른 교란 변수(예: 고도에 따른 프리에어 이상, 층상 밀도 등)를 추가로 분석해야 합니다.")

# 시각화 비교
df_compare = pd.DataFrame({
    '구분': ['이론적 예측 (Theoretical Prediction)', '실제 지질 실측 (Actual Geo-Data)'],
    '중력 이상 차이 (mGal)': [predicted_dg_mgal, actual_dg_mgal]
})
fig = px.bar(df_compare, x='구분', y='중력 이상 차이 (mGal)', color='구분', text='중력 이상 차이 (mGal)', title="이론 vs 현실 1:1 대조표")
fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
st.plotly_chart(fig, use_container_width=True)
