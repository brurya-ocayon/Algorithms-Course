import sys
import numpy as np
import cv2

# קבלת קלט
R, G, B = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rgb_uint8 = np.array([[[B, G, R]]], dtype=np.uint8)

def manual_conversions(R, G, B):
    r, g, b = R/255.0, G/255.0, B/255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    # --- Hue ---
    if delta == 0:
        H = 0
    elif cmax == r:
        H = 60 * (((g - b) / delta) % 6)
    elif cmax == g:
        H = 60 * (((b - r) / delta) + 2)
    else:
        H = 60 * (((r - g) / delta) + 4)

    # --- HSV ---
    S_hsv = 0 if cmax == 0 else delta / cmax
    V = cmax

    # --- HSL ---
    L = (cmax + cmin) / 2
    S_hsl = 0 if delta == 0 else delta / (1 - abs(2 * L - 1))

    # --- YCrCb ---
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    Cr = (R - Y) * 0.713 + 128
    Cb = (B - Y) * 0.564 + 128

    return (H, S_hsv, V), (H, S_hsl, L), (Y, Cr, Cb)

# חישובים
manual_hsv, manual_hsl, manual_ycc = manual_conversions(R, G, B)

hsv_cv = cv2.cvtColor(rgb_uint8, cv2.COLOR_BGR2HSV)[0][0]
hls_cv = cv2.cvtColor(rgb_uint8, cv2.COLOR_BGR2HLS)[0][0]
ycc_cv = cv2.cvtColor(rgb_uint8, cv2.COLOR_BGR2YCrCb)[0][0]

# נרמול OpenCV להשוואה אמיתית
hsv_cv_norm = (
    hsv_cv[0] * 2,             # H מומר מ-0–179 ל-0–360
    hsv_cv[1] / 255.0,         # S מומר מ-0–255 ל-0–1
    hsv_cv[2] / 255.0
)

hls_cv_norm = (
    hls_cv[0] * 2,
    hls_cv[2] / 255.0,         # OpenCV שומר כ-HLS (H,L,S)
    hls_cv[1] / 255.0
)

print("\n===== HSV =====")
print("Manual:", manual_hsv)
print("OpenCV (normalized):", hsv_cv_norm)
print("Difference:",
      np.array(manual_hsv) - np.array(hsv_cv_norm))

print("\n===== HSL =====")
print("Manual:", manual_hsl)
print("OpenCV (normalized):", hls_cv_norm)
print("Difference:",
      np.array(manual_hsl) - np.array(hls_cv_norm))

print("\n===== YCrCb =====")
print("Manual:", manual_ycc)
print("OpenCV:", ycc_cv)
print("Difference:",
      np.array(manual_ycc) - np.array(ycc_cv))