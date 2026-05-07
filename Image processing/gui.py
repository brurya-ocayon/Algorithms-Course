import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

# ייבוא הקובץ שבו כתבת את הלוגיקה של ה-warp
import warp

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Affine Transform Demo")
        self.root.geometry("600x600")

        # ---- State ----
        self.original_image = None      # התמונה המקורית
        self.current_image = None       # התמונה אחרי הטרנספורמציה
        self.display_scale = 1.0        # קנה מידה לתצוגה בלבד

        # ---- Build GUI ----
        self.build_gui()

    def build_gui(self):
        # סרגל עליון
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        load_btn = tk.Button(top_frame, text="Load Image", command=self.load_image)
        load_btn.pack(side=tk.LEFT, padx=5, pady=5)

        reset_btn = tk.Button(top_frame, text="Reset Sliders", command=self.reset_sliders)
        reset_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # קנבס להצגת התמונה
        self.canvas = tk.Canvas(self.root, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # סרגלים (Sliders)
        sliders = tk.Frame(self.root)
        sliders.pack(side=tk.BOTTOM, fill=tk.X)

        self.rot_slider = tk.Scale(
            sliders, from_=-180, to=180,
            orient=tk.HORIZONTAL,
            label="Rotation (degrees)",
            command=self.on_slider_change
        )
        self.rot_slider.pack(fill=tk.X)

        self.sx_slider = tk.Scale(
            sliders, from_=0.1, to=3.0,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            label="Scale X",
            command=self.on_slider_change
        )
        self.sx_slider.set(1.0)
        self.sx_slider.pack(fill=tk.X)

        self.sy_slider = tk.Scale(
            sliders, from_=0.1, to=3.0,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            label="Scale Y",
            command=self.on_slider_change
        )
        self.sy_slider.set(1.0)
        self.sy_slider.pack(fill=tk.X)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")]
        )
        if not file_path:
            return

        # קריאת התמונה
        img = cv2.imread(file_path)
        if img is None:
            print("Error: Could not open image. Check if path has Hebrew characters.")
            return

        self.original_image = img
        self.current_image = img.copy()

        # חישוב קנה מידה לתצוגה כדי שהתמונה תיכנס בחלון
        self.root.update_idletasks()
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        h, w = img.shape[:2]
        scale_w = canvas_w / w
        scale_h = canvas_h / h
        self.display_scale = min(scale_w, scale_h, 1.0)

        self.show_on_canvas(self.current_image)

    def reset_sliders(self):
        self.rot_slider.set(0)
        self.sx_slider.set(1.0)
        self.sy_slider.set(1.0)

    def on_slider_change(self, _=None):
        if self.original_image is None:
            return

        angle = self.rot_slider.get()
        sx = self.sx_slider.get()
        sy = self.sy_slider.get()

        # --- התיקון הקריטי נמצא כאן ---
        # אנחנו קוראים לפונקציה שלך ושומרים את התוצאה שהיא מחזירה
        transformed = warp.warp_image(self.original_image, angle, sx, sy)

        # עדכון התמונה המוצגת
        self.current_image = transformed
        self.show_on_canvas(self.current_image)

    def show_on_canvas(self, img_bgr):
        # המרה מ-BGR (של OpenCV) ל-RGB (עבור התצוגה)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        h, w = img_rgb.shape[:2]

        # שינוי גודל לתצוגה בלבד (אם התמונה גדולה מדי)
        if self.display_scale != 1.0:
            img_rgb = cv2.resize(
                img_rgb,
                (int(w * self.display_scale), int(h * self.display_scale)),
                interpolation=cv2.INTER_AREA
            )

        # המרה לפורמט ש-Tkinter מבין
        pil_img = Image.fromarray(img_rgb)
        photo = ImageTk.PhotoImage(pil_img)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=photo)
        self.canvas.image = photo 

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()