import math

# [1] K-PROTOCOL AXIOMS (Vol.3_v3)
PI_SQ = math.pi ** 2
C_SI = 299792458
R_EARTH = 6371000

# [2] TOKYO SKYTREE REAL DATA (Ground Truth)
H_DIFF = 456.3
BGI_ANOMALY_MGAL = 154.12
OBSERVED_VAL = 4.9300e-14

# [3] DETERMINISTIC CALCULATION (K-PROTOCOL ENGINE)
# A. Local Gravity at Bottom (Real Data)
g_bottom = 9.80665 + (BGI_ANOMALY_MGAL / 100000.0)

# B. Local Gravity at Top (Deterministic Gradient)
g_top = g_bottom * ((R_EARTH / (R_EARTH + H_DIFF)) ** 2)

# C. Geometric Distortion Factor (S_loc)
S_bot = PI_SQ / g_bottom
S_top = PI_SQ / g_top
S_avg = (S_bot + S_top) / 2

# D. Master Formula: Geometric Illusion (S²-1) Elimination
# Vol.3 Section 3.4: k_val = SI_pred * (2 - S_avg²)
g_avg = (g_bottom + g_top) / 2
si_standard_calc = (g_avg * H_DIFF) / (C_SI ** 2)
k_absolute_val = si_standard_calc * (2 - (S_avg ** 2))

# [4] FINAL OUTPUT
accuracy = (1 - abs(k_absolute_val - OBSERVED_VAL) / OBSERVED_VAL) * 100

print(f"--- K-PROTOCOL DETERMINISTIC PROOF ---")
print(f"K-Standard Absolute Value : {k_absolute_val:.10e}")
print(f"Tokyo Real Observed Value : {OBSERVED_VAL:.10e}")
print(f"Deterministic Accuracy    : {accuracy:.10f} %")
print(f"---------------------------------------")
