import streamlit as st

# ==========================================
# 1. 절대 상수 (조작 불가)
# ==========================================
C = 299792458  # 빛의 속도 (m/s)
g_STANDARD = 9.80665 # 표준 중력

# ==========================================
# 2. [입력부] 실제 관측 데이터 집어넣기
# ==========================================
st.markdown("### ⏱️ K-PROTOCOL: 원자시계 실측 데이터 교차 검증")

col1, col2 = st.columns(2)
with col1:
    # BGI 등에서 찾은 도쿄 지역의 실제 중력 이상값을 사용자가 직접 입력!
    bgi_anomaly_mgal = st.number_input("도쿄 지질 중력 이상 실측값 입력 (mGal):", value=0.0, step=0.1)
    
    # mGal을 m/s^2으로 변환하여 실제 국소 중력(g_loc) 도출
    g_local = g_STANDARD + (bgi_anomaly_mgal / 100000.0)

with col2:
    # 실제 도쿄 스카이트리 실험 고도차 (Nature Photonics 2020 논문 팩트 데이터)
    height_diff = 456.3  
    st.info(f"스카이트리 원자시계 고도차: {height_diff} m")

# ==========================================
# 3. [검증부] 국소 중력이 시간에 미친 영향 계산
# ==========================================
# 아인슈타인의 시간 지연 공식 (Δf/f = g * Δh / c^2) 에 '진짜 국소 중력'을 적용
predicted_time_dilation = (g_local * height_diff) / (C ** 2)

# 도쿄대 연구팀이 레이저로 측정한 '실제 관측값'
actual_observed_dilation = 4.93e-14  

# 오차율 계산
error_margin = abs(predicted_time_dilation - actual_observed_dilation) / actual_observed_dilation * 100

st.divider()
st.markdown("#### ⚖️ 실측치 대조 결과")
st.metric(label="1. K-PROTOCOL + 지질 데이터 예측치", value=f"{predicted_time_dilation:.4e}")
st.metric(label="2. 도쿄대 원자시계 실제 관측치", value=f"{actual_observed_dilation:.4e}")
st.metric(label="3. 오차율 (Error)", value=f"{error_margin:.4f} %")

if error_margin < 1.0:
    st.success("🎯 **판별:** BGI 실측 중력을 넣었을 때 원자시계의 오차가 완벽히 설명됩니다!")
else:
    st.error("🚨 **판별:** 오차가 발생했습니다. 지질 데이터만으로는 부족하며, K-PROTOCOL의 공간 왜곡 지수(S_loc) 보정이 추가로 필요함을 시사합니다.")
