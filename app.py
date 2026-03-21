import streamlit as st
import math

# ==========================================
# [A] 우주 절대 상수 및 시스템 세팅
# ==========================================
PI_SQ = 9.869604401089358  # math.pi ** 2
C_SI = 299792458           # 1983년 고정된 SI 광속
G_STANDARD = 9.80665       # 지구 표준 중력

# 지구 거시 왜곡 지수 (S_earth)
S_EARTH = PI_SQ / G_STANDARD 
# 절대 광속 확정 (c_k)
C_K = C_SI / S_EARTH

st.set_page_config(page_title="K-PROTOCOL 3-Layer Engine", layout="wide")

# ==========================================
# [B] 언어 선택 (사이드바 최상단)
# ==========================================
lang = st.sidebar.radio("🌐 Language / 언어", ["한국어", "English"])
st.sidebar.write("---")

# 언어별 타이틀 및 설명 세팅
if lang == "한국어":
    st.title("🛡️ K-PROTOCOL: 3-Layer 통합 증명 엔진")
    st.markdown("현대 물리학의 **국소적 착시(System E)**를 벗겨내고, **우주 절대 기하학(System U)**으로 변환한 뒤, 이를 다시 **관측자의 시계(Observation)**로 투영하는 3단계 증명 시스템입니다.")
else:
    st.title("🛡️ K-PROTOCOL: 3-Layer Unification Engine")
    st.markdown("A 3-step proof system that strips away the **local illusion of modern physics (System E)**, converts to **Absolute Cosmic Geometry (System U)**, and projects it back to the **Observer's Clock**.")
st.write("---")

# ==========================================
# [C] 현장 실측 데이터 입력
# ==========================================
with st.sidebar:
    if lang == "한국어":
        st.header("📍 현장 실측 데이터 (Ground Truth)")
        h_si = st.number_input("SI 고도차 (m)", value=456.3, format="%.1f")
        g_bot = st.number_input("지면 중력 (m/s²)", value=9.8081912, format="%.7f")
        g_top = st.number_input("전망대 중력 (m/s²)", value=9.8067885, format="%.7f")
        observed_val = st.number_input("도쿄대 관측치", value=4.9300e-14, format="%.4e")
    else:
        st.header("📍 Ground Truth Data")
        h_si = st.number_input("SI Altitude Diff (m)", value=456.3, format="%.1f")
        g_bot = st.number_input("Bottom Gravity (m/s²)", value=9.8081912, format="%.7f")
        g_top = st.number_input("Top Gravity (m/s²)", value=9.8067885, format="%.7f")
        observed_val = st.number_input("Observation (Ref)", value=4.9300e-14, format="%.4e")

g_avg = (g_bot + g_top) / 2
S_avg = PI_SQ / g_avg

# 공통 계산 로직
delta_t_SI = (g_avg * h_si) / (C_SI ** 2)
h_k = h_si / S_avg
delta_t_K = (g_avg * h_k) / (C_K ** 2)
k_projected = delta_t_K / (S_avg ** 2)
residual_pct = (abs(k_projected - observed_val) / observed_val) * 100

# ==========================================
# [D] 3-Layer 수학적 엔진 및 UI 렌더링
# ==========================================

# --------------------------------------------------
# Layer 1: System E
# --------------------------------------------------
if lang == "한국어":
    st.header("Layer 1: System E (현대 물리학의 착시)")
    st.error("**문제점**: 현대 물리학은 지구 중력에 의해 '수축된 고도($h$)'와 '왜곡된 광속($c$)'을 고정 상수로 사용하는 순환 오류에 빠져 있습니다.")
else:
    st.header("Layer 1: System E (The Distorted Local Lens)")
    st.error("**Problem**: Modern physics falls into a circular error by fixing 'contracted altitude ($h$)' and 'distorted light speed ($c$)' as absolute constants under Earth's gravity.")

col1_1, col1_2 = st.columns([1, 1])
with col1_1:
    st.markdown("**[SI Standard Formula]**")
    st.latex(r"\Delta t_{SI} = \frac{g_{avg} \cdot h_{SI}}{c_{SI}^2}")
    if lang == "한국어":
        st.write(f"- $c_{{SI}}$: 299,792,458 m/s (고정됨)")
        st.write(f"- $h_{{SI}}$: {h_si} m (수축된 척도)")
    else:
        st.write(f"- $c_{{SI}}$: 299,792,458 m/s (Fixed)")
        st.write(f"- $h_{{SI}}$: {h_si} m (Contracted Scale)")
with col1_2:
    if lang == "한국어":
        st.metric("SI 예측치 (가짜 척도)", f"{delta_t_SI:.15e}")
    else:
        st.metric("SI Prediction (False Scale)", f"{delta_t_SI:.15e}")
st.write("---")

# --------------------------------------------------
# Layer 2: System U
# --------------------------------------------------
if lang == "한국어":
    st.header("Layer 2: System U (K-PROTOCOL 절대 우주)")
    st.success("**해결책**: K-PROTOCOL은 삐뚠 광속과 삐뚠 고도를 텐서($S_{loc}$)로 일제히 펴서, 왜곡 0%의 '우주 절대 기하학' 스케일로 동기화합니다.")
else:
    st.header("Layer 2: System U (The Absolute Geometric Universe)")
    st.success("**Solution**: K-PROTOCOL uses the tensor ($S_{loc}$) to unbend the distorted light speed and altitude simultaneously, synchronizing them to the Absolute Cosmic Geometry with 0% distortion.")

col2_1, col2_2 = st.columns([1, 1])
with col2_1:
    st.markdown("**[K-Absolute Formula]**")
    st.latex(r"c_k = \frac{c_{SI}}{S_{earth}} \quad , \quad h_k = \frac{h_{SI}}{S_{avg}}")
    st.latex(r"\Delta t_{K} = \frac{g_{avg} \cdot h_k}{c_k^2}")
    if lang == "한국어":
        st.write(f"- 절대 광속 ($c_k$): {C_K:.2f} m/s")
        st.write(f"- 절대 고도 ($h_k$): {h_k:.3f} m")
    else:
        st.write(f"- Absolute Light Speed ($c_k$): {C_K:.2f} m/s")
        st.write(f"- Absolute Altitude ($h_k$): {h_k:.3f} m")
with col2_2:
    if lang == "한국어":
        st.metric("K-PROTOCOL 절대치 (우주 참값)", f"{delta_t_K:.15e}")
    else:
        st.metric("K-PROTOCOL Absolute (Cosmic Truth)", f"{delta_t_K:.15e}")
st.write("---")

# --------------------------------------------------
# Layer 3: K-Projection
# --------------------------------------------------
if lang == "한국어":
    st.header("Layer 3: K-Projection (인간의 시계로 투영)")
    st.info("**증명**: 우주의 절대 시간을 다시 인간의 '왜곡된 원자시계 렌즈($S_{avg}^2$)'로 투영하면, 기하학적 굴절을 거쳐 관측치 근방으로 정확히 수렴합니다.")
else:
    st.header("Layer 3: K-Projection (Observation via Distorted Clock)")
    st.info("**Proof**: Projecting the Absolute Cosmic Time back through the human's 'distorted atomic clock lens ($S_{avg}^2$)' geometrically refracts it to converge perfectly near the observation value.")

col3_1, col3_2 = st.columns([1, 1])
with col3_1:
    st.markdown("**[Observation Projection Formula]**")
    st.latex(r"\Delta t_{obs} = \frac{\Delta t_{K}}{S_{avg}^2}")
    if lang == "한국어":
        st.write(f"- 투영 텐서 ($S_{{avg}}^2$): {S_avg**2:.7f}")
    else:
        st.write(f"- Projection Tensor ($S_{{avg}}^2$): {S_avg**2:.7f}")
with col3_2:
    if lang == "한국어":
        st.metric("K-투영치 (관측자 시계 눈금)", f"{k_projected:.15e}")
        st.metric("도쿄대 실제 관측치 (Reference)", f"{observed_val:.15e}", delta=f"잔차: {residual_pct:.4f}%", delta_color="inverse")
    else:
        st.metric("K-Projected (Observer's Clock)", f"{k_projected:.15e}")
        st.metric("Real Observation (Reference)", f"{observed_val:.15e}", delta=f"Residual: {residual_pct:.4f}%", delta_color="inverse")

st.write("---")
if lang == "한국어":
    st.markdown(f"""
    ### 🔬 결론 (Scientific Conclusion)
    현대 물리학이 측정한 `4.930`은 우주의 절대 시간이 아닙니다. 우주의 진짜 시간 지연은 **Layer 2의 `{delta_t_K:.3e}`**이며, 우리가 지구라는 찌그러진 공간($S_{{avg}}^2$) 안에서 시계를 보기 때문에 빛이 굴절되어 **Layer 3의 `{k_projected:.3e}`**로 보이는 것뿐입니다. (남은 잔차는 조석력 등 순수 환경 변수입니다.)
    """)
else:
    st.markdown(f"""
    ### 🔬 Scientific Conclusion
    The `4.930` measured by modern physics is not the absolute time of the universe. The true time dilation of the cosmos is **`{delta_t_K:.3e}` in Layer 2**. Because we observe the clock from within Earth's distorted space ($S_{{avg}}^2$), the light refracts and appears as **`{k_projected:.3e}` in Layer 3**. (The remaining residual is due to pure environmental variables like tidal forces.)
    """)
