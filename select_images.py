from import_module import *
from watermark_text import LabelWatermarkText
from watermark_image import LabelWatermarkImage


class SelectImages:
    def __init__(self, parent):
        self.parent = parent
        self.imges = Tk()
        self.imges.attributes('-topmost', 1)
        self.imges.update()
        self._fonts = setFont.Font(family='Helvetica', size=12)
        self.pilImages = SelectImages.loadImages('imgs/')
        self.current_img = self.pilImages[0]
        self.label1 = ''
        self.reset_data()
        self.set_window()
        self.create_button()
        self.show_image()
        self.imges.resizable(False, False)

        self.imges.mainloop()


    def set_window(self):
        self.imges.geometry('400x250')
        self.imges.title('Setting')
        self.imges['padx'] = 30
        self.imges['pady'] = 10
        self.imges.grid()

        # Configure grid
        self.imges.columnconfigure(0, weight=5)
        self.imges.columnconfigure(1, weight=1)
        self.imges.rowconfigure(0, weight=1)
        self.imges.rowconfigure(1, weight=1)
        self.imges.rowconfigure(2, weight=1)
        self.imges.rowconfigure(3, weight=5)
        self.imges.rowconfigure(4, weight=1)


    def previous_img(self):
        idx_previous = self.pilImages.index(self.current_img) - 1
        self.current_img = self.pilImages[idx_previous]
        self.show_image(rotate_img=False)

    def next_img(self):
        idx_previous = self.pilImages.index(self.current_img) + 1

        if idx_previous == (len(self.pilImages)):
            idx_previous = 0
        self.current_img = self.pilImages[idx_previous]
        self.show_image(rotate_img=False)

    def add_img(self):
        name_image = 'select_img.png'
        self.img_rotate.save(name_image)
        if self.img_rotate:
            self.select_imgs.append(Image.open(name_image))

        self.set_button()
        self.exit()

    def decor_rotate_img(fn):
        count = 0
        @wraps(fn)
        def inner(*args, **kwargs):
            nonlocal count
            if kwargs:
                count += 90
                kwargs['anchor'] = count
                if not kwargs['rotate_img'] or count == 360:
                    count = 0
            return fn(*args, **kwargs)
        return inner

    @decor_rotate_img
    def show_image(self, rotate_img=False, anchor=0):
        self.img_rotate = self.current_img

        if rotate_img and self.label1:
            self.img_rotate = self.current_img.rotate(anchor)

        img = self.img_rotate.resize((500, 400))        
        img = ImageTk.PhotoImage(img)
        if self.label1:
            self.label1.destroy()
        self.label1 = Label(image=img, bg='white')
        self.label1.image = img
        self.label1.grid(column=0, row=0, rowspan=4)


    def create_button(self):
        Button(self.imges, text='Previous', font=self._fonts, command=lambda: self.previous_img()).grid(row=0, column=0, sticky='n', pady=5)
        Button(self.imges, text='Next', font=self._fonts, command=lambda: self.next_img()).grid(row=0, column=1, sticky='n', pady=5)
        Button(self.imges, text='Select', font=self._fonts, command=lambda: self.add_img()).grid(row=4, column=0, sticky='n', pady=5)
        Button(self.imges, text='rotate', font=self._fonts, command=lambda: self.show_image(rotate_img=True)).grid(row=1, column=0, sticky='n', pady=5)
        Button(self.imges, text='exit', font=self._fonts, command=lambda: self.exit(), width=7).grid(column=1, row=4)

    @staticmethod
    def loadImages(path):
        imagesList = os.listdir(path)
        return [Image.open(path + image) for image in imagesList]

    def watermark_text(self):
        LabelWatermarkText(self)

    def watermark_image(self):
        LabelWatermarkImage(self)

    def set_button(self):
        self.button_watermark_text = Button(self.parent, text='watermark text', font=self._fonts, command=lambda: self.watermark_text())
        self.button_watermark_text.grid(row=0, column=2, sticky='w')
        self.button_watermark_image = Button(self.parent, text='watermark image', font=self._fonts, command=lambda: self.watermark_image())
        self.button_watermark_image.grid(row=1, column=2, sticky='nw')

    def reset_data(self):
        self.button_watermark_text = ''
        self.button_watermark_image = ''
        self.img_rotate = ''
        self.select_imgs = deque()
    
    def exit(self):
        self.imges.destroy()


if __name__ == "__main__":
    SelectImages()