from PySide6.QtWidgets import QMessageBox, QApplication


class Messagebox:
    def __init__(self):
        self.title = None
        self.message = None

    def message_setter(self, title, message):
        self.title = title
        self.message = message

    def showinfo(self, title, message):
        self.message_setter(title, message)
        msg_box = QMessageBox(QApplication.activeWindow())
        msg_box.setWindowTitle(self.title)
        msg_box.setText(self.message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

    def showwarning(self, title, message):
        self.message_setter(title, message)
        msg_box = QMessageBox(QApplication.activeWindow())
        msg_box.setWindowTitle(self.title)
        msg_box.setText(self.message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.exec_()

    def showerror(self, title, message):
        self.message_setter(title, message)
        msg_box = QMessageBox(QApplication.activeWindow())
        msg_box.setWindowTitle(self.title)
        msg_box.setText(self.message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.exec_()

    def showcritical(self, title, message):
        self.message_setter(title, message)
        msg_box = QMessageBox(QApplication.activeWindow())
        msg_box.setWindowTitle(self.title)
        msg_box.setText(self.message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.exec_()

    def askyesno(self, title, message) -> bool:
        self.message_setter(title, message)
        msg_box = QMessageBox(QApplication.activeWindow())
        msg_box.setWindowTitle(self.title)
        msg_box.setText(self.message)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg_box.exec_() == QMessageBox.Yes

    def askokcancel(self, title, message) -> bool:
        self.message_setter(title, message)
        msg_box = QMessageBox(QApplication.activeWindow())
        msg_box.setWindowTitle(self.title)
        msg_box.setText(self.message)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return msg_box.exec_() == QMessageBox.Ok

    def askyesnocancel(self, title, message) -> bool:
        self.message_setter(title, message)
        msg_box = QMessageBox(QApplication.activeWindow())
        msg_box.setWindowTitle(self.title)
        msg_box.setText(self.message)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        return msg_box.exec_() == QMessageBox.Yes

    def askretrycancel(self, title, message) -> bool:
        self.message_setter(title, message)
        msg_box = QMessageBox(QApplication.activeWindow())
        msg_box.setWindowTitle(self.title)
        msg_box.setText(self.message)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
        return msg_box.exec_() == QMessageBox.Retry
