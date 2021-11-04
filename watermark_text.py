import tkinter
from import_module import *
from tkinter.colorchooser import askcolor
from tkinter import messagebox
from collections import namedtuple


class LabelWatermarkText:
    def __init__(self, parent):
        self.parent = parent
        self.window = Tk()
        self.window.attributes('-topmost', 2)
        self.window.update()
        self.window.geometry('350x250')
        self.window.title('watermark text')
        self.window['padx'] = 5
        self.window['pady'] = 20
        self._fonts = setFont.Font(family='Helvetica', size=10)
        self.window.resizable(False, False)
        self.window.grid()

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=1)
        self.window.rowconfigure(4, weight=1)
        self.window.rowconfigure(5, weight=1)
        self.window.rowconfigure(6, weight=10)
        self.window.rowconfigure(7, weight=1)
    
        self.set_data()

        # label
        Label(self.window, text='Enter text', font=self._fonts).grid(column=0, row=0)

        # Entry
        self.entry_text = StringVar(self.window)
        self.entry = Entry(self.window, textvariable=self.entry_text, bd=5, width=30)
        self.entry.grid(column=1, row=0)
        self.entry.focus()

        Button(self.window, text='Finish', command=self.finish, width=7, font=self._fonts)\
            .grid(column=0, row=6)
        Button(self.window, text='Cancel', command=self.exit, width=7, font=self._fonts)\
            .grid(column=1, row=6)
        Button(self.window, text='Select a Color', command=self.change_color)\
            .grid(column=1, row=5)
        Button(self.window, text='Select font', command=self.GetFont)\
            .grid(column=0, row=5)

        self.var_radio = 1  # bug something.
        self.var = IntVar(self.window)  # not work if not use self.window.
        R1 = Radiobutton(self.window, text='top-left', variable=self.var, value=1, justify='center', command=self.set_value_radio)
        R2 = Radiobutton(self.window, text='top-right', variable=self.var, value=2, justify='center', command=self.set_value_radio)
        R3 = Radiobutton(self.window, text='bottom-left', variable=self.var, value=3, command=self.set_value_radio)
        R4 = Radiobutton(self.window, text='bottom-right', variable=self.var, value=4, command=self.set_value_radio)
        R5 = Radiobutton(self.window, text='center',  variable=self.var, value=5, justify='center', command=self.set_value_radio)
        R1.select()
        R1.grid(column=0, row=1)
        R2.grid(column=0, row=2)
        R3.grid(column=1, row=1, sticky='w')
        R4.grid(column=1, row=2, sticky='w')
        R5.grid(column=0, row=3)

        Label(self.window, text='set position by yourself (x,y)').grid(column=1, row=3, sticky='w')
        
        self.var_of_entry_pos = StringVar()
        self.entry_pos = Entry(self.window, textvariable=self.var_of_entry_pos, width=10)
        self.entry_pos.grid(column=1, row=4, sticky='w')
        
        self.window.mainloop()

    def set_value_radio(self):
        self.var_radio = self.var.get()
    
    def get_entry_pos(self):
        return self.entry_pos.get()

    def my_font(self):
        reads= ''
        values = []

        Fonts = namedtuple('Fonts', 'name file_name')
        with open('fonts.txt') as f:
            reads = f.readlines()

        for item in reads:
            data = eval(item.strip('\n'))
            values.append(data)

        combined = [Fonts(name, file) for name, file in values]

        return combined

    def warning(self, title='warning', msg='warning'):
        return messagebox.showinfo(title, msg)

    def change_color(self):
        self.colors = askcolor(title="Tkinter Color Chooser")[0]

    def check_position(self, position, text, font, photo, *, margin=10):
        text_width, text_hight = font.getsize(text=text)

        x, y = photo.size

        # top-left
        if position == 1:
            return (0 + margin, 0 + margin)
        # top-right
        elif position == 2:
            return (x - margin - text_width, 0 + margin)
        # bottom-left
        elif position == 3:
            return (0 + margin, y - margin -  text_hight)
        # bottom-right
        elif position == 4:
            return (x - margin - text_width, y - margin - text_hight)
        # center
        elif position == 5:
            return (x / 2 - text_width / 2, y / 2 - text_hight / 2)

    def watermark_text(self, output_image_path, 
                text, pos, color, drawing, font, photo):
        
            drawing.text(pos, text, fill=color, font=font)
            photo.show()
            photo.save(output_image_path)

    def create_image(self):
        self.text = self.get_text()
        entries = os.listdir('image_edited')

        output_path = f'image_edited/watermark_text{str(len(entries) + 1)}.jpg'
        try:
            name, size = self.value_from_setfont
        except TypeError:
            self.warning(msg='Please select font')
        else:
            photo = Image.open('select_img.png')
            drawing = ImageDraw.Draw(photo)

            if self.colors is None:
                select_color = (3, 8, 12)
            else:
                select_color = self.colors

            font_file = ''
            for item in self.my_font():
                if name == item.name:
                    font_file = item.file_name
                    break

            font = ImageFont.truetype(font=f'All_font/{font_file}', size=int(size))
            try:
                if self.get_entry_pos() == '':
                    pos = self.check_position(self.var_radio, self.text, font, photo)

                else:
                    pos = eval(self.get_entry_pos())
            except SyntaxError:

                self.warning(title='Error', msg='position incorrect')

            else:    
                self.watermark_text(output_image_path=output_path,
                                    text=self.text, pos=pos,
                                    color=select_color,
                                    drawing=drawing,
                                    photo=photo,
                                    font=font)

    def finish(self):
        self.create_image()
        self.set_data()
        self.reset_data_fo_parent()
        self.exit()

    def get_text(self):
        return self.entry_text.get()

    def GetFont(self):
        self.text = self.get_text()
        SetFont(self)

    def reset_data_fo_parent(self):
        if self.parent.label1:
            self.parent.label1.destroy()

        self.parent.button_watermark_text.destroy()
        self.parent.button_watermark_image.destroy()

    def set_data(self):
        self.colors = None
        self.text = ''
        self.value_from_setfont = None

    def exit(self):
        self.window.destroy()


class SetFont:
    DEFAULT_FONT = 16

    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.root.attributes('-topmost', 3)
        self.root.title('select font')
        self.root.geometry('500x250')
        self.root['padx'] = 5
        self.root['pady'] = 20
        self.root.grid()

        self.root.columnconfigure(0)
        self.root.columnconfigure(1, weight=2)
        self.root.columnconfigure(2)
        self.root.rowconfigure(0)
        self.root.rowconfigure(1)
        self.root.rowconfigure(2)
        self.root.rowconfigure(3)
        
        self.font_size = SetFont.DEFAULT_FONT
        self.select_font = ''

        self.lbFonts = Listbox(self.root)
        self.lbFonts.grid(column=0, row=0, rowspan=2)
        self.button_exit = Button(self.root, command=self.exit, text='Exit', width=7)\
            .grid(column=0, row=3, sticky='e')
        self.button_save = Button(self.root, command=self.save, text='Save', width=7)\
            .grid(column=0, row=3, sticky='w')

        Label(self.root, text='font size').grid(column=1, row=0, sticky='nw', padx=20)

        self.entry_font_size = Entry(self.root, width=5)
        self.entry_font_size.insert(0, str(SetFont.DEFAULT_FONT))
        self.entry_font_size.grid(column=1, row=0, sticky='n')
        self.entry_font_size.bind("<Return>", self.changeFont)

        self.available_fonts = self.parent.my_font()

        for f in self.available_fonts:
            self.lbFonts.insert(END, f.name)

        self.lbFonts.bind("<Double-Button-1>", self.changeFont)

        if self.parent.text:
            self.label = Label(self.root, text=self.parent.text)
        else:
            self.label = Label(self.root, text="Test Font")
        self.label.grid(column=1, row=0, sticky='s')

        self.root.mainloop()

    def exit(self):
        self.root.destroy()

    def get_font_size(self):
        return self.entry_font_size.get()

    def save(self):
        self.font_size = self.get_font_size()
        if not (str(self.font_size) and self.select_font):
            self.parent.warning(msg='please enter size or name of font.')
        else:
            self.parent.value_from_setfont = (self.select_font, self.font_size)
            self.exit()
        
    def changeFont(self, event):
        self.font_size = int(self.get_font_size())
        try:
            self.font_size %= 10
        except ValueError:
            self.font_size = 1
        try:
            self.select_font = self.lbFonts.get(self.lbFonts.curselection())
        except tkinter.TclError:
            self.parent.warning(msg='Please select font name.')
        else:
            self.label.config(font=(self.select_font, str(self.font_size)))

    def fine_font(self, font_name):
        for f in self.parent.my_font():
            if font_name == f.name:
                return f

    def get_values(self):
        return (self.font_size, self.select_font)


if __name__ == "__main__":
    LabelWatermarkText()
    # Font()
    # SetColor()
