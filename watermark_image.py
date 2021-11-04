from tkinter import font
from import_module import *
from tkinter import messagebox

class LabelWatermarkImage:
    def __init__(self, parent):
        self.parent = parent
        self.wt_img = Tk()
        self.wt_img.resizable(False, False)
        self.wt_img.geometry('300x200')
        self.wt_img.title('watermark image')
        self.set_data()

        self.wt_img['padx'] = 5
        self.wt_img['pady'] = 10
        self._fonts = setFont.Font(family='Arial', size=12)
        self.wt_img.grid()

        self.wt_img.columnconfigure(0, weight=1)
        self.wt_img.columnconfigure(1, weight=1)
        self.wt_img.columnconfigure(2, weight=1)
        self.wt_img.rowconfigure(0, weight=1)
        self.wt_img.rowconfigure(1, weight=1)
        self.wt_img.rowconfigure(2, weight=1)
        self.wt_img.rowconfigure(3, weight=1)
        self.wt_img.rowconfigure(4, weight=1)
        self.wt_img.rowconfigure(5, weight=1)

        Button(self.wt_img, text='Previous', font=self._fonts, command=self.previous_img).grid(column=0, row=0)
        Button(self.wt_img, text='Next', font=self._fonts, command=self.next_img).grid(column=1, row=0)
        Button(self.wt_img, text='Select', font=self._fonts, command=self.set_select_img).grid(column=2, row=0)
        Button(self.wt_img, text='Exit', font=self._fonts, command=self.exit).grid(column=2, row=3)
        Button(self.wt_img, text='enter', font=self._fonts, command=self.enter_size, width=4).grid(column=2, row=1)
        Label(self.wt_img, text='size (x,y)', font=self._fonts).grid(column=0, row=1, sticky='e')

        self.var_radio = 1
        self.var_int = IntVar(self.wt_img)  # not work if not use self.window.
        R1 = Radiobutton(self.wt_img, text='top-left', variable=self.var_int, value=1, justify='center', command=self.set_value_radio)
        R2 = Radiobutton(self.wt_img, text='top-right', variable=self.var_int, value=2, justify='center', command=self.set_value_radio)
        R3 = Radiobutton(self.wt_img, text='bottom-left', variable=self.var_int, value=3, command=self.set_value_radio)
        R4 = Radiobutton(self.wt_img, text='bottom-right', variable=self.var_int, value=4, command=self.set_value_radio)
        R1.select()
        R1.grid(column=0, row=3)
        R2.grid(column=1, row=3)
        R3.grid(column=0, row=4)
        R4.grid(column=1, row=4)
        
        self.var_string = StringVar(self.wt_img)
        self.entry_resize = Entry(self.wt_img, textvariable=self.var_string, width=10)
        self.entry_resize.grid(column=1, row=1, sticky='w')

        self.root_image = Toplevel()
        self.root_image.resizable(False, False)
        self.show_image()

        self.root_image.mainloop()
        self.wt_img.mainloop()

    def set_value_radio(self):
        self.var_radio = self.var_int.get()

    @staticmethod
    def loadImages(path):
        imagesList = os.listdir(path)
        return [Image.open(path + image) for image in imagesList]
        
    def warning(self, title='warning', msg='warning'):
        return messagebox.showinfo(title, msg)

    def previous_img(self):
        idx_previous = self.pilImages.index(self.current_img) - 1
        self.current_img = self.pilImages[idx_previous]
        self.show_image()

    def next_img(self):
        idx_previous = self.pilImages.index(self.current_img) + 1

        if idx_previous == (len(self.pilImages)):
            idx_previous = 0
        self.current_img = self.pilImages[idx_previous]
        self.show_image()

    def enter_size(self):
        size = self.var_string.get()
        if size == '':
            self.warning(msg='incorrect.')
        else:
            try:
                size_tuple = eval(size)
                if not isinstance(size_tuple, tuple):
                    raise TypeError
            except (TypeError, SyntaxError, NameError):
                self.warning(msg='incorrect. Please use coordinate.')
            else:
                self.show_image(size_tuple)

    def show_image(self, real_size=None):
        size_label = (320,240)
        frame = Frame(self.root_image, width=size_label[0], height=size_label[1], background='white')
        frame.pack_propagate(0)    
        frame.grid(column=1, row=2)
        image = self.current_img
        width, height = image.size
        if real_size is None:
            real_size = (width, height)

        if self.label_show_image != '':
            self.label_show_image.destroy()

        self.label_show_image = Label(self.wt_img, text=f'size: ({width}, {height})')
        image.thumbnail(size=(real_size))
        # set new current image
        self.current_img = image

        self.label_show_image.grid(column=0, row=2)
        show_image = image.resize(size=size_label)
        img = ImageTk.PhotoImage(show_image, Image.BILINEAR)
        self.make_label(frame, img)
        
    def make_label(self, parent, img):
        if self.label:
            self.label.destroy()
        self.label = Label(parent, image=img)
        self.label.image = img
        self.label.pack()

    def set_select_img(self):
        if self.label_show_image:
            self.label_show_image.destroy()

        self.select_watermark = self.current_img
        self.create_new_image()
        self.set_data()
        self.reset_data_fo_parent()
        self.exit()

    def reset_data_fo_parent(self):
        if self.parent.label1:
            self.parent.label1.destroy()
        self.parent.button_watermark_text.destroy()
        self.parent.button_watermark_image.destroy()

    def set_data(self):
        self.label = ''
        self.pilImages = LabelWatermarkImage.loadImages('imgs/')
        self.current_img = self.pilImages[0]
        self.select_watermark = ''
        self.label_show_image = ''


    def check_position(self, position, watermark, base_image, *, margin=10):
        img_width, img_hight = watermark.size
        x, y = base_image.size
        # top-left
        if position == 1:
            return (0 + margin, 0 + margin)
        # top-right
        elif position == 2:
            return (x - margin - img_width, 0 + margin)
        # bottom-left
        elif position == 3:
            return (0 + margin, y - margin -  img_hight)
        # bottom-right
        elif position == 4:
            return (x - margin - img_width, y - margin - img_hight)
        # center
        elif position == 5:
            return (x / 2 - img_width / 2, y / 2 - img_hight / 2)

    def create_new_image(self):
        body = self.parent.select_imgs[0]
        watermark = self.select_watermark
        position = self.check_position(self.var_radio, watermark, body)
        entries = os.listdir('image_edited')
        output_path = f'image_edited/watermark_image{str(len(entries) + 1)}.jpg'

        # add watermark to image
        body.paste(watermark, position)
        body.show()
        body.save(output_path)
    
    def exit(self):
        self.root_image.destroy() 
        self.wt_img.destroy()
    

if __name__ == "__main__":

    LabelWatermarkImage(None)
