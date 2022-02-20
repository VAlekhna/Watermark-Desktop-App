import copy
from tkinter import Tk, StringVar, Button, Entry, filedialog, Label, messagebox

from PIL import Image, ImageTk, ImageDraw, ImageFont

# ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
WATERMARK_FONT = ImageFont.truetype("arial.ttf", 25)
WM_FONT_SIZE = 25

# ---------------------------- WATERMARK MECHANISM ------------------------------- #


class Watermark(Tk):
    def __init__(self):
        super().__init__()
        self.w_mark = StringVar()
        self.title('Watermarking Desktop App')
        self.config(bg=GREEN)
        self.w = self.winfo_screenwidth() // 2
        self.h = self.winfo_screenheight() // 2
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.geometry(f'1200x600+{self.w - 600}+{self.h - 300}')

        open_image_button = Button(text='Open image', highlightthickness=0, command=self.open_image)
        open_image_button.place(width=120, relx=0.5, x=-260, rely=1, y=-25)

        watermark_text_input = Entry(textvariable=self.w_mark)
        watermark_text_input.insert(0, 'Python')
        watermark_text_input.place(width=120, relx=0.5, x=-125, rely=1, y=-22)

        preview_button = Button(text='Preview Watermark', highlightthickness=0, command=self.add_watermark)
        preview_button.place(width=120, relx=0.5, x=5, rely=1, y=-25)

        save_image_button = Button(text='Save Image', highlightthickness=0, command=self.save_image)
        save_image_button.place(width=120, relx=0.5, x=140, rely=1, y=-25)

    def open_image(self):
        try:
            self.picture_panel.destroy()
        except AttributeError:
            pass
        self.filename = filedialog.askopenfilename(initialdir='/', title='Select image',
                                                   filetype=(("jpeg", "*.jpg"), ("png", "*.png")))
        self.picture = Picture(Image.open(self.filename))
        preview_picture = ImageTk.PhotoImage(self.picture.picture_small)
        self.picture_panel = Label(image=preview_picture)
        self.picture_panel.image = preview_picture
        self.picture_panel.place(relwidth=1.0)

    def add_watermark(self):
        self.picture_panel.destroy()
        watermark = self.w_mark.get()
        preview_watermark_picture = copy.copy(self.picture.picture_small).convert('RGBA')
        text = Image.new('RGBA', preview_watermark_picture.size, (255, 255, 255, 0))
        watermark_font = WATERMARK_FONT
        drawing = ImageDraw.Draw(text)
        picture_width, picture_height = preview_watermark_picture.size
        drawing.text((picture_width - 10, picture_height - 10), watermark,
                     font=watermark_font, anchor='rs', fill=PINK)
        combined_picture = Image.alpha_composite(preview_watermark_picture, text)
        preview_picture = ImageTk.PhotoImage(combined_picture)
        self.picture_panel = Label(image=preview_picture)
        self.picture_panel.image = preview_picture
        self.picture_panel.place(relwidth=1.0)
        self.new_watermark = watermark

    def save_image(self):
        final_picture = self.picture.picture.convert('RGBA')
        text = Image.new('RGBA', final_picture.size, (255, 255, 255, 0))
        watermark_font = WATERMARK_FONT
        drawing = ImageDraw.Draw(text)
        picture_width, picture_height = self.picture.picture.size
        drawing.text((picture_width - int(10 / self.picture.picture_scale),
                      picture_height - int(10 / self.picture.picture_scale)), self.new_watermark,
                     font=watermark_font, anchor='rs', fill=PINK)
        combined_picture = Image.alpha_composite(final_picture, text)
        count = 1
        for symbol in reversed(self.filename):
            if symbol == '.':
                break
            count += 1
        filename = self.filename[:-count]
        extension = self.filename[-count:]
        new_filename = f"{filename}_wtm{extension}"
        combined_picture.convert('RGB').save(new_filename)
        count = 0
        for symbol in reversed(new_filename):
            if symbol == '/':
                break
            count += 1
        messagebox.showinfo("Watermark successfully added", f"Image saved as\n{new_filename[-count:]}")


class Picture:
    def __init__(self, picture):
        self.picture = picture
        self.width, self.height = picture.size
        self.picture_small = self.resize()

    def resize(self):
        picture_scale = self.scale()
        new_width = self.width * picture_scale
        new_height = self.height * picture_scale
        return self.picture.resize((int(new_width), int(new_height)),
                                   Image.ANTIALIAS)

    def scale(self):
        self.picture_scale = (WINDOW_WIDTH - 50) / self.width
        if self.picture_scale * self.height > WINDOW_HEIGHT - 30:
            self.picture_scale = (WINDOW_HEIGHT - 30) / self.height
        return self.picture_scale


window = Watermark()
window.mainloop()
