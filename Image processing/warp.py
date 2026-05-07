import numpy as np

def warp_image(image: np.ndarray,
               angle_deg: float,
               scale_x: float,
               scale_y: float) -> np.ndarray:

    H, W, C = image.shape
    # 1. חישוב מרכז התמונה (לפי ההנחיה של מרכזי פיקסלים)
    cx, cy = (W / 2.0, H / 2.0)

    # 2. המרת זווית לרדיאנים
    theta = np.radians(angle_deg)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    # 3. בניית מטריצות בסיסיות (הומוגניות 3x3)
    # מטריצת הזזה למרכז
    T1 = np.array([[1, 0, -cx],
                   [0, 1, -cy],
                   [0, 0, 1]])

    # מטריצת סיבוב ומתיחה משולבת
    # שימי לב: המתיחה היא הפוכה (1/s) כי אנחנו עושים Backward Mapping
    # אבל כאן נבנה את המטריצה הישרה ואז נהפוך את כולה
    R = np.array([[cos_t, -sin_t, 0],
                  [sin_t,  cos_t, 0],
                  [0,      0,     1]])
    
    S = np.array([[scale_x, 0,       0],
                  [0,       scale_y, 0],
                  [0,       0,       1]])

    # מטריצת הזזה חזרה מהמרכז
    T2 = np.array([[1, 0, cx],
                   [0, 1, cy],
                   [0, 0, 1]])

    # 4. הרכבת המטריצה הכוללת: M = T2 @ R @ S @ T1
    M = T2 @ R @ S @ T1
    
    # 5. חישוב המטריצה ההפוכה למיפוי לאחור
    try:
        M_inv = np.linalg.inv(M)
    except np.linalg.LinAlgError:
        return np.zeros_like(image)

    # יצירת תמונת פלט ריקה
    output = np.zeros_like(image)

    # 6. לולאה על כל פיקסל בתמונת הפלט (מיפוי לאחור)
    for i in range(H):
        for j in range(W):
            # מרכז הפיקסל הנוכחי בתמונת הפלט
            x_out, y_out = j + 0.5, i + 0.5
            
            # הכפלה במטריצה ההפוכה למציאת המקור בתמונה המקורית
            pos_out = np.array([x_out, y_out, 1.0])
            pos_in = M_inv @ pos_out
            
            x_in, y_in = pos_in[0], pos_in[1]
            
            # 7. אינטרפולציית השכן הקרוב (Nearest Neighbor)
            # מחשבים את אינדקס הפיקסל המקורי (מורידים 0.5 ומעגלים)
            src_j = int(floor(x_in - 0.5 + 0.5)) # פשוט round
            src_i = int(floor(y_in - 0.5 + 0.5))
            
            # בדיקה אם הנקודה נמצאת בתוך גבולות התמונה המקורית
            if 0 <= src_i < H and 0 <= src_j < W:
                output[i, j] = image[src_i, src_j]

    return output

def floor(x):
    return int(np.floor(x))

import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

# 1. פונקציית Warp וקטורית עם Nearest Neighbor
def warp_vectorized_nn(image, matrix):
    h, w = image.shape[:2]
    
    # יצירת רשת קואורדינטות (Grid) לכל תמונת היעד
    y_coords, x_coords = np.indices((h, w))
    # הפיכה למערך של נקודות הומוגניות (x, y, 1)
    coords = np.stack([x_coords.ravel(), y_coords.ravel(), np.ones(h*w)])
    
    # חישוב הטרנספורמציה ההפוכה
    inv_matrix = np.linalg.inv(matrix)
    src_coords = inv_matrix @ coords
    
    # חזרה לקואורדינטות רגילות (חילוק ב-Z למקרה של פרספקטיבה, למרות שפה זה אפיני)
    src_x = (src_coords[0] / src_coords[2]).reshape(h, w)
    src_y = (src_coords[1] / src_coords[2]).reshape(h, w)
    
    # Nearest Neighbor - עיגול פשוט
    src_x_int = np.round(src_x).astype(int)
    src_y_int = np.round(src_y).astype(int)
    
    # מסיכה (Mask) - לוודא שאנחנו בתוך גבולות התמונה המקורית
    mask = (src_x_int >= 0) & (src_x_int < w) & (src_y_int >= 0) & (src_y_int < h)
    
    result = np.zeros_like(image)
    result[mask] = image[src_y_int[mask], src_x_int[mask]]
    return result

# 2. אינטרפולציה ביליניארית וקטורית (ללא לולאות)
def warp_vectorized_bilinear(image, matrix):
    h, w = image.shape[:2]
    y_coords, x_coords = np.indices((h, w))
    coords = np.stack([x_coords.ravel(), y_coords.ravel(), np.ones(h*w)])
    
    inv_matrix = np.linalg.inv(matrix)
    src_coords = inv_matrix @ coords
    
    src_x = (src_coords[0] / src_coords[2]).reshape(h, w)
    src_y = (src_coords[1] / src_coords[2]).reshape(h, w)
    
    # מציאת 4 השכנים
    x0 = np.floor(src_x).astype(int)
    x1 = x0 + 1
    y0 = np.floor(src_y).astype(int)
    y1 = y0 + 1
    
    # חישוב אלפא ובטא (המרחקים השבריים)
    alpha = src_x - x0
    beta = src_y - y0
    
    # הגבלת אינדקסים כדי לא לצאת מהתמונה
    x0 = np.clip(x0, 0, w-1)
    x1 = np.clip(x1, 0, w-1)
    y0 = np.clip(y0, 0, h-1)
    y1 = np.clip(y1, 0, h-1)
    
    # נוסחת האינטרפולציה הביליניארית
    # P = (1-a)(1-b)I00 + a(1-b)I01 + (1-a)bI10 + abI11
    wa = (1 - alpha) * (1 - beta)
    wb = alpha * (1 - beta)
    wc = (1 - alpha) * beta
    wd = alpha * beta
    
    # הוספת מימד לערוצי צבע אם צריך
    if len(image.shape) == 3:
        wa, wb, wc, wd = wa[..., None], wb[..., None], wc[..., None], wd[..., None]
        
    result = (wa * image[y0, x0] + wb * image[y0, x1] + 
              wc * image[y1, x0] + wd * image[y1, x1]).astype(np.uint8)
    return result

# ===== סעיף ג' - השוואת ביצועים =====

def measure_time(func, image, matrix, runs=5):
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        func(image, matrix)
        end = time.perf_counter()
        times.append(end - start)
    return np.mean(times)


angle = np.radians(30)
matrix = np.array([
    [np.cos(angle), -np.sin(angle), 0],
    [np.sin(angle),  np.cos(angle), 0],
    [0, 0, 1]
])

sizes = [(50, 50), (100, 100), (200, 200), (500, 500)]

print(f"{'רוחב':<8}{'גובה':<8}{'NumPy NN (שנ)':<20}{'NumPy Bilinear (שנ)'}")
print("-" * 55)

for h, w in sizes:
    image = np.random.randint(0, 255, (h, w, 3), dtype=np.uint8)
    t_nn  = measure_time(warp_vectorized_nn, image, matrix)
    t_bil = measure_time(warp_vectorized_bilinear, image, matrix)
    print(f"{w:<8}{h:<8}{t_nn:<20.4f}{t_bil:.4f}")