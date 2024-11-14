from icon import icon_data_start
from logger import logger_vcc
import tkinter as tk
from PIL import Image, ImageTk
import io

def init_win_settings():
    try:
        settings_window = tk.Toplevel()
        settings_window.geometry("400x550")
        settings_window.minsize(width=400, height=560)
        settings_window.maxsize(width=400, height=550)
        settings_window.title("Настройки")

        # Загружаем иконку для окна
        start_icon_image = Image.open(io.BytesIO(icon_data_start))
        start_icon_image_tk = ImageTk.PhotoImage(start_icon_image)

        # Устанавливаем иконку для окна подтверждения
        settings_window.start_icon_image = start_icon_image_tk
        settings_window.iconphoto(False, start_icon_image_tk)

        settings_window.transient()  # Устанавливает окно дочерним для основного
        settings_window.grab_set()
    except Exception:
        logger_vcc.error(f"Не удалось инициализировать окно настроек.", exc_info=True)
