import streamlit as st
import math

# --- [A] 우주 절대 상수 (Axioms) ---
PI_SQ = math.pi ** 2
C_SI = 299792458
G_STANDARD = 9.80665

# S_earth (지구 표면 거시 왜곡 지수)
S_EARTH = PI_SQ / G_STANDARD 

st.set_page_config(page_title="K-PROTOCOL Unification", layout="wide")
st.title("🛡️ KR K-PROTOCOL: System E vs System U 분리 엔진")
st.markdown("삐뚠 자(SI)로 측정한 고도와 광속을 모두 **절대 스케일**로 일제히 변환 후 대조합니다.")
st.write("---")

with st.sidebar:
    st.header("📍 현장 실측 데이터 (삐뚠 자 측정치)")
    h_si = st.number_input("SI 고도차 (m)", value=456.3, format="%.1f")
    g_bot = st.number_input("지면 중력 (m/s²)", value=9.8081912, format="%.7f")
    g_top = st.number_input("전망대 중력 (m/s²)", value=9.8067885, format="%.7f")
    observed_val = st.number_input("도쿄대 관측치", value=4.9300e-14, format="%.4e")

g_avg = (g_bot + g_top) / 2
S_avg = PI_SQ / g_avg

# ==========================================================
# 🌌 [System E] 현대 물리학의 렌즈 (SI 단위계 계산)
# ==========================================================
# 삐뚠 고도와 삐뚠 광속을 그대로 사용함
delta_t_SI = (g_avg * h_si) / (C_SI ** 2)


# ==========================================================
# 🌌 [System U] K-PROTOCOL의 렌즈 (절대 기하학 계산)
# ==========================================================
# 1. 삐뚠 광속을 절대 광속(c_k)으로 텐서 변환 (Vol. 3)
C_K = C_SI / S_EARTH

# 2. 삐뚠 고도를 절대 고도(h_k)로 텐서 변환 (Vol. 3-2)
h_k = h_si / S_avg

# 3. 절대 스케일 변수들만 사용하여 시간 지연 계산
delta_t_K = (g_avg * h_k) / (C_K ** 2)

# ==========================================================
# --- 결과 출력 ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌎 System E (현대 물리학)")
    st.write("왜곡된 SI 단위(m, c)를 그대로 사용한 예측치")
    st.code(f"SI 광속 (c) : {C_SI} m/s\nSI 고도 (h) : {h_si:.2f} m\n\nSI 계산치 : {delta_t_SI:.15e}")

with col2:
    st.subheader("🪐 System U (K-PROTOCOL)")
    st.write("텐서를 적용하여 절대 기하학 스케일로 변환한 예측치")
    st.code(f"절대 광속(c_k): {C_K:.1f} m/s\n절대 고도(h_k): {h_k:.2f} m\n\nK 절대치 : {delta_t_K:.15e}")

st.write("---")
st.markdown("### 🔍 데이터 분석")
st.write(f"- **실제 관측치 (Reference)**: `{observed_val:.15e}`")
st.write(f"- 현대 물리학(SI)과 K-PROTOCOL의 이원화 분리를 통해, 관측값이 어느 시스템에 더 근접하는지, 그리고 단위 변환이 결과에 어떤 물리적 증폭을 일으키는지 명확히 확인할 수 있습니다.")
