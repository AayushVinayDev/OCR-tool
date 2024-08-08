import pyautogui
import pytesseract
from PIL import Image, ImageGrab
import tkinter as tk

class ScreenshotTool:
    def __init__(self, master):
        self.master = master
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None

        # Create a transparent window
        self.master.attributes('-alpha', 0.3)
        self.master.geometry('{}x{}'.format(
            self.master.winfo_screenwidth(),
            self.master.winfo_screenheight()))

        self.master.bind('<ButtonPress-1>', self.on_button_press)
        self.master.bind('<B1-Motion>', self.on_move_press)
        self.master.bind('<ButtonRelease-1>', self.on_button_release)

        self.rect = None

        self.canvas = tk.Canvas(self.master, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        if not self.rect:
            self.rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_move_press(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y,
                           self.current_x, self.current_y)

    def on_button_release(self, event):
        self.master.destroy()

def capture_screenshot():
    root = tk.Tk()
    app = ScreenshotTool(root)
    root.mainloop()

    # Get the coordinates of the selection
    left = min(app.start_x, app.current_x)
    top = min(app.start_y, app.current_y)
    right = max(app.start_x, app.current_x)
    bottom = max(app.start_y, app.current_y)

    # Capture the selected area
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    return screenshot

def perform_ocr(image):
    # Perform OCR on the image
    text = pytesseract.image_to_string(image)
    return text

def save_text(text, filename):
    # Save the text to a file
    with open(filename, 'w') as f:
        f.write(text)

def main():
    # Capture screenshot
    screenshot = capture_screenshot()
    
    # Perform OCR
    text = perform_ocr(screenshot)
    
    # Save text
    save_text(text, 'output.txt')
    print("Text saved to output.txt")

if __name__ == "__main__":
    main()