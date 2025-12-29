import sys
import PIL.Image

import sys
import PIL.Image

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} image-filename")
        exit(-1)

    file_name = sys.argv[1]
    try:
        img = PIL.Image.open(file_name)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return

    r, g, b = img.split()

    blank = PIL.Image.new('L', img.size, 0)

    red_display = PIL.Image.merge("RGB", (r, blank, blank))
    green_display = PIL.Image.merge("RGB", (blank, g, blank))
    blue_display = PIL.Image.merge("RGB", (blank, blank, b))

    # השורות האלו חייבות להיות בתוך ה-main (עם רווח)
    red_display.show(title="Red Channel Only")
    green_display.show(title="Green Channel Only")
    blue_display.show(title="Blue Channel Only")

if __name__ == "__main__":
    main()