import sys
import numpy as np
import cv2
import math
import matplotlib.pyplot as plt

# תרגיל 1
# סעיף א

def degrees_to_radians(degrees):
    return degrees * (math.pi / 180)
#סעיף ב
# רשימת הערכים במעלות
angles_deg = [0, 90, 180, 45, 30, 10, 5, 1]

# הדפסת כותרת ה-CSV
print("degrees,radians,sin,cos")

for deg in angles_deg:
    rad = degrees_to_radians(deg)
    s = math.sin(rad)
    c = math.cos(rad)
 #סעיף ג   
    # הדפסה בפורמט CSV 
    print(f"{deg},{rad:.4f},{s:.4f},{c:.4f}")


   
#  תרגיל 3

# סעיף א
theta = np.radians(30)  # המרה ממעלות לרדיאנים
r_30 = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)]
])
print("r_30 (Rotation Matrix):\n", r_30)


# סעיף ב
sx_2 = np.array([
    [2, 0],
    [0, 1]
])
print("\nsx_2 (Scaling Matrix):\n", sx_2)


# סעיף ג
rs = r_30 @ sx_2


# סעיף ד
sr = sx_2 @ r_30


# סעיף ה
# ה. הגדרת המלבן המקורי (רוחב 2, גובה 1, מרכז בראשית)
# הנקודות מייצגות את ארבעת הקודקודים + חזרה לנקודת ההתחלה כדי לסגור את הצורה
rectangle = np.array([
    [-1, -0.5],
    [ 1, -0.5],
    [ 1,  0.5],
    [-1,  0.5],
    [-1, -0.5]
]).T  # Transpose כדי שכל עמודה תהיה וקטור (נקודה)

# פונקציה עזר להחלת טרנספורמציה על נקודות המלבן
def transform(matrix, points):
    return matrix @ points

# חישוב המלבנים המותמרים
rect_rotated = transform(r_30, rectangle)  # ו
rect_scaled = transform(sx_2, rectangle)   # ז
rect_rs = transform(rs, rectangle)         # ח (RS)
rect_sr = transform(sr, rectangle)         # ח (SR)

# ט. הצגת התוצאות ב-Matplotlib
plt.figure(figsize=(10, 8))

# ציור המלבנים
plt.plot(rectangle[0, :], rectangle[1, :], label='Original', linewidth=2, color='black')
plt.plot(rect_rotated[0, :], rect_rotated[1, :], label='Rotated 30°', linestyle='--')
plt.plot(rect_scaled[0, :], rect_scaled[1, :], label='Scaled x2', linestyle='--')
plt.plot(rect_rs[0, :], rect_rs[1, :], label='RS (Scale then Rotate)', linewidth=2)
plt.plot(rect_sr[0, :], rect_sr[1, :], label='SR (Rotate then Scale)', linewidth=2)

# הגדרות גרף
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()
plt.axis('equal')  # חשוב כדי שהפרופורציות לא יתעוותו
plt.title('2D Transformations on a Rectangle')
plt.show()

