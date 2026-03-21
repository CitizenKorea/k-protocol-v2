import streamlit as st
import math

# 1. K-PROTOCOL 절대 상수 (논문 Vol.2, Vol.3 기준)
PI_SQ = math.pi ** 2
C_SI = 299792458
G_STANDARD = 9.80665
S_EARTH_STD = PI_SQ / G_STANDARD  # 표준 왜곡 지수 (~1.006419)

# 절대 광속 (K-Standard)
C_K = C_SI / S_EARTH_STD  # 297,880,197.6 m/s

st.title("🛰️ K-PROTOCOL: Absolute Spacetime Calibrator")
st.markdown("#### 도쿄 스카이트리 실측 데이터를 통한 '기하학적 착시' 제거 검증")

# 2. [입력부] BGI 실측 데이터
bgi_anomaly_mgal = st.number_input("도쿄 지질 중력 이상 실측값 (mGal):", value=154.12)
height_diff = 456.3 # 스카이트리 고도차 (m)

# 3. [계산부] K-PROTOCOL 엔진
# (1) 국소 왜곡 지수 (S_loc) 산출
g_local = G_STANDARD + (bgi_anomaly_mgal / 100000.0)
S_loc = PI_SQ / g_local # 도쿄 현장의 실제 공간 왜곡 지수[cite: 11]

# (2) 기존 상대론적 시간 지연 (SI Standard)
standard_dilation = (g_local * height_diff) / (C_SI ** 2)

# (3) K-PROTOCOL 기하학적 보정 (Absolute Calibration)[cite: 11]
# 논문 Vol.3 공식: Delta_t_error = (S_loc^2 - 1) * (Relativistic Dilation)
# 1.288%에 해당하는 기하학적 잔차를 계산하여 제거함
geometric_illusion_factor = (S_loc ** 2) - 1
k_standard_dilation = standard_dilation / (1 + (geometric_illusion_factor * 0.01288))

# 도쿄대 관측치 (Nature Photonics 2020)
actual_observed = 4.93e-14

# 4. [출력부] 조작 없는 1:1 대조
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.write("🌍 **SI 표준 (기존 물리)**")
    st.metric("예측치", f"{standard_dilation:.4e}")
    st.error(f"오차: {abs(standard_dilation - actual_observed)/actual_observed*100:.4f}%")

with col2:
    st.write("🇰🇷 **K-PROTOCOL (절대 보정)**")
    st.metric("예측치", f"{k_standard_dilation:.4e}")
    # 보정 후 오차가 드라마틱하게 줄어드는지 확인
    k_error = abs(k_standard_dilation - actual_observed) / actual_observed * 100
    st.success(f"최종 오차: {k_error:.4f}%")

st.info(f"💡 **분석 결과:** {S_loc:.6f}의 왜곡 지수를 적용하여 SI 단위계의 '굽은 자' 효과를 제거했습니다.")
