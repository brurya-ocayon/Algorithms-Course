import cv2
import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# Question 1 – Gradient Image
# =========================================================
def create_gradient_image(height, width):
    img = np.zeros((height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            value = ((x + y) / (width + height - 2)) * 255
            img[y, x] = int(value)

    return img


print("Question 1")
grad_img = create_gradient_image(255, 255)
plt.imshow(grad_img, cmap='gray')
plt.title("Gradient Image")
plt.show()


# =========================================================
# Question 2 – Brighten Function
# =========================================================
def brighten(img, b, func):

    if func == "np":
        return np.add(img, b)  # NumPy addition (Modulo 256)

    elif func == "cv2":
        return cv2.add(img, b)  # OpenCV addition (Saturation)

    return img


# =========================================================
# Question 3 – Comparison
# =========================================================
print("Question 2+3")

res_np = brighten(grad_img, 100, "np")
res_cv2 = brighten(grad_img, 100, "cv2")

plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.imshow(res_np, cmap='gray')
plt.title("NumPy add (Modulo)")

plt.subplot(1,2,2)
plt.imshow(res_cv2, cmap='gray')
plt.title("OpenCV add (Saturation)")

plt.show()


# =========================================================
# Question 4 – Low Contrast Image
# =========================================================
def create_low_contrast(bg, fg):

    img = np.full((300, 300), bg, dtype=np.uint8)
    cv2.circle(img, (150, 150), 60, fg, -1)

    return img


print("Question 4")
low_contrast_img = create_low_contrast(100, 105)

plt.imshow(low_contrast_img, cmap='gray', vmin=0, vmax=255)
plt.title("Low Contrast Image")
plt.show()


# =========================================================
# Question 5 – Normalization
# =========================================================
def normalize_manual(img):

    min_val, max_val, _, _ = cv2.minMaxLoc(img)
    mean_val = np.mean(img)

    print("Normalization Info:")
    print(f"Min: {min_val}")
    print(f"Max: {max_val}")
    print(f"Mean: {mean_val:.2f}")

    if max_val > min_val:
        factor = 255 / (max_val - min_val)
        print(f"Stretching Factor: {factor:.2f}")

        src_float = img.astype(np.float32)
        dst_float = (src_float - min_val) * factor
        dst = np.clip(dst_float, 0, 255).astype(np.uint8)

        return dst

    return img


print("Question 5")
normalized_img = normalize_manual(low_contrast_img)

plt.imshow(normalized_img, cmap='gray')
plt.title("After Normalization")
plt.show()


# =========================================================
# Question 6 – Effect of Extreme Pixels
# =========================================================
print("Question 6")

modified_img = low_contrast_img.copy()

# שינוי שני פיקסלים
modified_img[0,0] = 0
modified_img[0,1] = 255

normalized_modified = normalize_manual(modified_img)

plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.imshow(modified_img, cmap='gray')
plt.title("After Adding 0 and 255 Pixels")

plt.subplot(1,2,2)
plt.imshow(normalized_modified, cmap='gray')
plt.title("Normalization After Modification")

plt.show()


# =========================================================
# Question 7 – Manual Histogram
# =========================================================
def manual_histogram(img):

    hist = [0] * 256

    for row in img:
        for pixel in row:
            hist[pixel] += 1

    return hist


print("Question 7")

hist_data = manual_histogram(grad_img)

plt.bar(range(256), hist_data)
plt.title("Manual Histogram")
plt.show()