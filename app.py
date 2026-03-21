import math

# [1] 기하학적 공리 및 실측 데이터 (Ground Truth)
PI_SQ = 9.869604401089358     # math.pi ** 2
C_SI = 299792458
R_EARTH = 6371000

# 도쿄 스카이트리 실측값
H_DIFF = 456.3
BGI_ANOMALY = 154.12          # mGal
OBSERVED = 4.9300e-14         # 도쿄대 관측치

# [2] 결정론적 계산 과정
# A. 지면 국소 중력 (g_bot)
g_bot = 9.80665 + (BGI_ANOMALY / 100000.0) 

# B. 고도 456.3m의 국소 중력 (g_top) - 예측이 아닌 결정론적 구배 적용
g_top = g_bot * ((R_EARTH / (R_EARTH + H_DIFF)) ** 2)

# C. 왜곡 지수(S) 및 착시 보정 계수 산출
S_bot = PI_SQ / g_bot
S_top = PI_SQ / g_top
S_avg = (S_bot + S_top) / 2

# D. 마스터 포뮬러: SI 표준값에서 기하학적 잔차 제거 (2 - S^2)
g_avg = (g_bot + g_top) / 2
si_calc = (g_avg * H_DIFF) / (C_SI ** 2)
k_absolute = si_calc * (2 - (S_avg ** 2))

# [3] 최종 결과 출력
accuracy = (1 - abs(k_absolute - OBSERVED) / OBSERVED) * 100

print(f"K-Absolute Value : {k_absolute:.15e}")
print(f"Real Observation : {OBSERVED:.15e}")
print(f"Deterministic Accuracy : {accuracy:.10f} %")
