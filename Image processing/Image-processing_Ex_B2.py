import numpy as np
import matplotlib.pyplot as plt

# ================================================
# תרגיל 2 סעיף ב: פונקציית הזזה
# ================================================
def translation_matrix(a, b):
    return np.array([
        [1, 0, a],
        [0, 1, b],
        [0, 0, 1]
    ], dtype=float)

# ================================================
# תרגיל 2 סעיף ג: פונקציית סיבוב
# ================================================
def rotation_matrix(theta_deg):
    theta_rad = np.radians(theta_deg)
    c, s = np.cos(theta_rad), np.sin(theta_rad)
    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ], dtype=float)

# ================================================
# תרגיל 2 סעיף ד: פונקציית קנה מידה
# ================================================
def scale_matrix(sx, sy=None):
    if sy is None:
        sy = sx
    return np.array([
        [sx, 0,  0],
        [0,  sy, 0],
        [0,  0,  1]
    ], dtype=float)

# ================================================
# תרגיל 2 סעיף ה: סיבוב סביב הנקודה (100, 200)
# ================================================
T_to_origin = translation_matrix(-100, -200)
R_30        = rotation_matrix(30)
T_back      = translation_matrix(100, 200)

final_matrix = T_back @ R_30 @ T_to_origin

print("Matrix for rotation around the point")
print(final_matrix)

# ================================================
# תרגיל 2 שאלה 2: יצירת מלבן בקואורדינטות הומוגניות
# ================================================
rect = np.array([
    [-1,  1,  1, -1, -1],
    [-0.5, -0.5, 0.5, 0.5, -0.5],
    [ 1,  1,  1,  1,  1]
])

# סעיף ב: סיבוב 30 מעלות
rect_rot_30 = rotation_matrix(30) @ rect

# סעיף ג: סיבוב 45 ואז מתיחה פי 2 בציר x
rect_rot_then_scale = scale_matrix(2, 1) @ rotation_matrix(45) @ rect

# סעיף ד: מתיחה פי 2 בציר x ואז סיבוב 45
rect_scale_then_rot = rotation_matrix(45) @ scale_matrix(2, 1) @ rect

# ================================================
# ציור
# ================================================
plt.figure(figsize=(10, 8))
plt.plot(rect[0, :],               rect[1, :],               'b-',  label='Original')
plt.plot(rect_rot_30[0, :],        rect_rot_30[1, :],        'r--', label='Rotate 30')
plt.plot(rect_rot_then_scale[0,:], rect_rot_then_scale[1,:], 'g-.', label='Rot 45 → Scale X')
plt.plot(rect_scale_then_rot[0,:], rect_scale_then_rot[1,:], 'm:',  label='Scale X → Rot 45')

plt.axhline(0, color='black', lw=1)
plt.axvline(0, color='black', lw=1)
plt.legend()
plt.axis('equal')
plt.title('Rectangle Transformations - Exercise 2')
plt.grid(True)
plt.show()

# ================================================
# תרגיל 2 שאלה 3: אינטרפולציה
# ================================================
def nearest_neighbor(alpha, beta, I00, I01, I10, I11):
    if alpha < 0.5:
        return I00 if beta < 0.5 else I10
    else:
        return I01 if beta < 0.5 else I11

def bilinear_interpolation(alpha, beta, I00, I01, I10, I11):
    top    = (1 - alpha) * I00 + alpha * I01
    bottom = (1 - alpha) * I10 + alpha * I11
    result = (1 - beta)  * top + beta  * bottom
    return result