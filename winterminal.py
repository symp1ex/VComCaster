from logger import logger_vcc
import about
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

class WinTerminalUi(object):
    def __init__(self):
        self.win_terminal = None

    def on_close(self, win_terminal):
        self.win_terminal = None
        win_terminal.destroy()

    def create_terminal_window(self):
        try:
            self.win_terminal = tk.Toplevel()
            self.win_terminal.protocol("WM_DELETE_WINDOW", lambda: self.on_close(self.win_terminal))
            # Создание главного окна
            self.win_terminal.title(about.version)

            self.win_terminal.geometry("980x512")
            self.win_terminal.minsize(width=730, height=360)

            # Создание текстового виджета для отображения вывода
            text_widget = tk.scrolledtext.ScrolledText(self.win_terminal, wrap=tk.WORD, height=512, width=980, bg="#0c0c0c", fg="white")
            text_widget.pack()

            start_icon_image = Image.open(io.BytesIO(icon_data_start))
            start_icon_image_tk = ImageTk.PhotoImage(start_icon_image)

            # Устанавливаем иконку для окна подтверждения
            self.win_terminal.start_icon_image = start_icon_image_tk
            self.win_terminal.iconphoto(False, start_icon_image_tk)

            # Перенаправление стандартного вывода
            sys.stdout = RedirectText(text_widget)

            # Запуск основного цикла Tkinter
            self.win_terminal.transient()
        except Exception:
            logger_vcc.error(f"Не удалось инициализировать окно терминала.", exc_info=True)

    def init_win_terminal(self):
        if not self.win_terminal:
            self.create_terminal_window()
        else:
            self.win_terminal.destroy()
            self.win_terminal = None
