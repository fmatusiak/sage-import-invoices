import tkinter as tk
from tkinter import filedialog


class FileOpener:

    def open(self):
        root = tk.Tk()
        root.withdraw()

        filePath = filedialog.askopenfilename()

        if not filePath:
            raise IOError('Invalid file path')

        return filePath
