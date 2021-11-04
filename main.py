from import_module import *
from select_images import SelectImages


class Windows:
    def __init__(self):
        self.windows = Tk()
        self.windows.attributes('-topmost', 0)
        self._width = self.windows.winfo_screenwidth()
        self._height = self.windows.winfo_screenheight()
        self._fonts = setFont.Font(family='Arial', size=12)
        
        try:
            self.set_window()
            self.create_button()
        except Exception as err:
            print(f'Erorr at Class Windows is {err}')
        finally:
            self.windows.mainloop()
    
    def set_window(self):
        self.windows.geometry(f'{self._width}x{self._height}')
        self.windows.title('Photo Application')
        self.windows['padx'] = 50
        self.windows['pady'] = 10
        self.windows.grid()

        #Configure gird
        self.windows.columnconfigure(0, weight=10)
        self.windows.columnconfigure(1, weight=1)
        self.windows.columnconfigure(2, weight=3)
        self.windows.rowconfigure(0, weight=1)
        self.windows.rowconfigure(1, weight=1)
        self.windows.rowconfigure(2, weight=5)
        self.windows.rowconfigure(3, weight=1)
        self.windows.rowconfigure(4, weight=1)

    def create_button(self):
        # Button
        self.button_select_img = Button(self.windows, text='Select Images', font=self._fonts, command=lambda: self.select_img()).grid(row=0, column=2, sticky='e')
        self.button_exit = Button(self.windows, text='exit', font=self._fonts,  width=7,command=lambda: self.exit()).grid(row=3, column=2, sticky='e')
    
    def select_img(self):
        Img = SelectImages(self.windows)
        self.images = Img.select_imgs
        
    def exit(self):
        self.windows.destroy()


if __name__=='__main__':
    Windows()
