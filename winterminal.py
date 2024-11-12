from logger import version
import sys
from icon import icon_data_start
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import io

class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        if self.text_widget.winfo_exists():
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.insert(tk.END, message)
            self.text_widget.yview(tk.END)
            self.text_widget.config(state=tk.DISABLED)

    def flush(self):
        # Пустой метод, необходимый для совместимости с sys.stdout
        pass

def win_terminal():
    # Создание главного окна
    win_terminal = tk.Toplevel()
    win_terminal.title(version)

    win_terminal.geometry("980x512")
    win_terminal.minsize(width=730, height=360)

    # Создание текстового виджета для отображения вывода
    text_widget = tk.scrolledtext.ScrolledText(win_terminal, wrap=tk.WORD, height=512, width=980, bg="#0c0c0c", fg="white")
    text_widget.pack()

    start_icon_image = Image.open(io.BytesIO(icon_data_start))
    start_icon_image_tk = ImageTk.PhotoImage(start_icon_image)

    # Устанавливаем иконку для окна подтверждения
    win_terminal.start_icon_image = start_icon_image_tk
    win_terminal.iconphoto(False, start_icon_image_tk)

    # Перенаправление стандартного вывода
    sys.stdout = RedirectText(text_widget)

    # Запуск основного цикла Tkinter
    win_terminal.transient()