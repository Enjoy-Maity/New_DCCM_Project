from tkinter import messagebox
# from MessageBox import messagebox


class CustomException(Exception):
    def __init__(self, title, message):
        self.title = title
        self.message = message
        super().__init__(self.title, self.message)
        messagebox.showerror(self.title, self.message)


class CustomWarning(Exception):
    def __init__(self, title, message):
        self.title = title
        self.message = message
        super().__init__(self.title, self.message)
        messagebox.showwarning(self.title, self.message)


class CustomException_without_warning(Exception):
    def __init__(self, title, message):
        self.title = title
        self.message = message
        super().__init__(self.title, self.message)